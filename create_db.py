import sqlite3

conn = sqlite3.connect("properties.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS properties (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    city TEXT NOT NULL,
    price REAL NOT NULL,
    bedrooms INTEGER NOT NULL,
    type TEXT NOT NULL
)
""")

sample_data = [
    ("P001", "Apartment in Ramallah", "Modern apartment near university, 3 bedrooms, 2 bathrooms, 120 sqm.", "Ramallah", 95000, 3, "Apartment"),
    ("P002", "Luxury Apartment in Ramallah", "Luxury apartment with balcony and city view, 4 bedrooms, 3 bathrooms, 180 sqm.", "Ramallah", 150000, 4, "Apartment"),
    ("P003", "Small Apartment in Ramallah", "Affordable small apartment, 2 bedrooms, 1 bathroom, near services.", "Ramallah", 70000, 2, "Apartment"),
    ("P004", "Villa in Nablus", "Large villa with garden and parking, 5 bedrooms, 4 bathrooms, 300 sqm.", "Nablus", 250000, 5, "Villa"),
    ("P005", "Apartment in Nablus", "Nice apartment in city center, 3 bedrooms, 2 bathrooms.", "Nablus", 90000, 3, "Apartment"),
    ("P006", "Cheap Apartment in Nablus", "Budget apartment, 2 bedrooms, 1 bathroom, close to university.", "Nablus", 65000, 2, "Apartment"),
    ("P007", "Apartment in Jenin", "Modern apartment, 3 bedrooms, 2 bathrooms, 110 sqm.", "Jenin", 80000, 3, "Apartment"),
    ("P008", "Small Apartment in Jenin", "Affordable apartment, 2 bedrooms, 1 bathroom, near shops.", "Jenin", 60000, 2, "Apartment"),
    ("P009", "House in Jenin", "Family house with garden, 4 bedrooms, 3 bathrooms.", "Jenin", 130000, 4, "House"),
    ("P010", "House in Hebron", "Spacious house in quiet area, 4 bedrooms, 3 bathrooms, 200 sqm.", "Hebron", 140000, 4, "House"),
    ("P011", "Apartment in Hebron", "Modern apartment, 3 bedrooms, 2 bathrooms, close to schools.", "Hebron", 85000, 3, "Apartment"),
    ("P012", "Cheap Apartment in Hebron", "Affordable apartment, 2 bedrooms, 1 bathroom.", "Hebron", 55000, 2, "Apartment"),
    ("P013", "Apartment in Bethlehem", "Beautiful apartment near city center, 3 bedrooms, 2 bathrooms.", "Bethlehem", 90000, 3, "Apartment"),
    ("P014", "Luxury Villa in Bethlehem", "Luxury villa with garden and parking, 5 bedrooms, 4 bathrooms.", "Bethlehem", 270000, 5, "Villa"),
    ("P015", "Apartment in Tulkarm", "Cozy apartment, 2 bedrooms, 1 bathroom, near university.", "Tulkarm", 60000, 2, "Apartment"),
]
cursor.executemany("""
INSERT OR REPLACE INTO properties (id, title, description, city, price, bedrooms, type)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", sample_data)

conn.commit()
conn.close()