"""Initialize MongoDB collections for daily-motto"""
from pymongo import MongoClient
import certifi

uri = "mongodb+srv://crawleryzd:crawleryzd123@mycluster.lyqtjvs.mongodb.net/"
client = MongoClient(uri, tlsCAFile=certifi.where())
db = client["daily_motto"]

# Drop existing if re-running
cols = db.list_collection_names()

if "quotes" not in cols:
    db.create_collection("quotes")
    db.quotes.create_index("cn", unique=True)
    db.quotes.create_index("category")
    print("✅ created: quotes collection + indexes")
else:
    print("ℹ️  quotes collection already exists")

if "pending_quotes" not in cols:
    db.create_collection("pending_quotes")
    db.pending_quotes.create_index("status")
    print("✅ created: pending_quotes collection + indexes")
else:
    print("ℹ️  pending_quotes collection already exists")

print(f"\n📦 Databases: {client.list_database_names()}")
print(f"📂 daily_motto collections: {db.list_collection_names()}")
client.close()
