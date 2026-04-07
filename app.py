import sqlite3
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

load_dotenv()
def get_db_connection():
    conn = sqlite3.connect("properties.db")
    conn.row_factory = sqlite3.Row
    return conn

def load_properties():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM properties")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

properties = load_properties()

documents = []

for prop in properties:
    content = f"""
        Property ID: {prop['id']}
        Title: {prop['title']}
        Description: {prop['description']}
        City: {prop['city']}
        Price: {prop['price']}
        Bedrooms: {prop['bedrooms']}
        Type: {prop['type']}
        """
    doc = Document(
        page_content=content,
        metadata={
            "id": prop["id"],
            "city": prop["city"],
            "price": prop["price"],
            "bedrooms": prop["bedrooms"],
            "type": prop["type"]
        }
    )
    documents.append(doc)


embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma.from_documents(documents, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

def search_properties(query: str):
    results = retriever.invoke(query)

    if not results:
        return "No matching properties found."

    output = []
    for doc in results:
        output.append(
            f"ID: {doc.metadata['id']}\n"
            f"City: {doc.metadata['city']}\n"
            f"Price: {doc.metadata['price']}\n"
            f"Bedrooms: {doc.metadata['bedrooms']}\n"
            f"Type: {doc.metadata['type']}\n"
            f"Details:\n{doc.page_content.strip()}\n"
        )

    return "\n\n".join(output)

def list_all_properties(_input=""):
    props = load_properties()

    if not props:
        return "No properties available."

    output = []
    for prop in props:
        output.append(
            f"ID: {prop['id']} | {prop['title']} | City: {prop['city']} | Price: {prop['price']} | Bedrooms: {prop['bedrooms']} | Type: {prop['type']}"
        )

    return "\n".join(output)

def get_property_by_id(property_id: str):
    props = load_properties()

    for prop in props:
        if prop["id"].lower() == property_id.lower():
            return (
                f"ID: {prop['id']}\n"
                f"Title: {prop['title']}\n"
                f"Description: {prop['description']}\n"
                f"City: {prop['city']}\n"
                f"Price: {prop['price']}\n"
                f"Bedrooms: {prop['bedrooms']}\n"
                f"Type: {prop['type']}"
            )
    return "Property not found."

tools = {
    "search_properties": search_properties,
    "list_all_properties": list_all_properties,
    "get_property_by_id": get_property_by_id
}

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

system_prompt = """
You are a real estate AI assistant.

You help users find and understand property listings.

You have these tools:

1. search_properties
- Use this when the user describes the property they want
- Example: "I want a cheap apartment near the university"

2. list_all_properties
- Use this when the user asks to see all available properties
- Example: "Show all properties"

3. get_property_by_id
- Use this when the user asks about one property using its ID
- Example: "Show details for P001"

To use a tool, respond EXACTLY in this format:
THOUGHT: your reasoning
ACTION: tool_name
INPUT: input

When you are ready to answer, respond EXACTLY in this format:
THOUGHT: I now have enough information
FINAL ANSWER: your answer
"""

def run_agent(question: str):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question}
    ]

    for _ in range(5):
        llm_output = llm.invoke(messages).content
        messages.append({"role": "assistant", "content": llm_output})

        if "FINAL ANSWER:" in llm_output:
            return llm_output.split("FINAL ANSWER:")[-1].strip()

        if "ACTION:" in llm_output and "INPUT:" in llm_output:
            action = llm_output.split("ACTION:")[-1].split("\n")[0].strip()
            input_ = llm_output.split("INPUT:")[-1].split("\n")[0].strip()

            if action in tools:
                result = tools[action](input_)
            else:
                result = "Tool not found."

            messages.append({"role": "user", "content": f"Observation: {result}"})

    return "I could not find an answer."

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    question: str

@app.get("/")
def home():
    return {"message": "Real Estate AI API is running"}

@app.get("/properties")
def get_properties():
    return load_properties()

@app.get("/property/{property_id}")
def get_single_property(property_id: str):
    props = load_properties()
    for prop in props:
        if prop["id"].lower() == property_id.lower():
            return prop
    return {"error": "Property not found"}

@app.post("/chat")
def chat(req: ChatRequest):
    answer = run_agent(req.question)
    return {"answer": answer}