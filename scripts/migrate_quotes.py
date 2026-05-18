"""Migrate existing quotes from quotes.py to MongoDB"""
import sys, json
sys.path.insert(0, ".")
from quotes import QUOTES, CATEGORIES
from pymongo import MongoClient
import certifi

uri = "mongodb+srv://crawleryzd:crawleryzd123@mycluster.lyqtjvs.mongodb.net/"
client = MongoClient(uri, tlsCAFile=certifi.where())
db = client["daily_motto"]

existing = db.quotes.count_documents({})
print(f"📊 MongoDB 现有格言: {existing} 条")

docs = []
new_count = 0
skip_count = 0
for q in QUOTES:
    doc = {
        "cn": q["cn"],
        "en": q["en"],
        "author": q["author"],
        "category": q["category"],
        "source": "curated",
    }
    # Skip if already exists (by unique cn index)
    if not db.quotes.find_one({"cn": q["cn"]}):
        docs.append(doc)
        new_count += 1
    else:
        skip_count += 1

if docs:
    db.quotes.insert_many(docs, ordered=False)
    print(f"✅ 已迁移 {new_count} 条格言到 MongoDB")
else:
    print(f"ℹ️  无需迁移")

if skip_count:
    print(f"⏭️  跳过 {skip_count} 条（已存在）")

total = db.quotes.count_documents({})
print(f"\n📊 MongoDB 格言总数: {total}")
print(f"📂 分类: {db.quotes.distinct('category')}")
client.close()
