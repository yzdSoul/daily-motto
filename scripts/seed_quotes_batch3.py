"""Batch 3: Final batch to reach 120"""
from pymongo import MongoClient
import certifi

uri = "mongodb+srv://crawleryzd:crawleryzd123@mycluster.lyqtjvs.mongodb.net/"
client = MongoClient(uri, tlsCAFile=certifi.where())
db = client["daily_motto"]

quotes = [
    {"cn": "滴水穿石，非一日之功。", "en": "Dripping water wears through stone — not by strength but by persistence.", "author": "佚名", "category": "励志奋斗", "source": "curated"},
    {"cn": "花有重开日，人无再少年。", "en": "Flowers may bloom again, but youth never returns.", "author": "关汉卿", "category": "时间光阴", "source": "curated"},
    {"cn": "家和万事兴。", "en": "A harmonious family brings prosperity in all things.", "author": "佚名", "category": "家国情怀", "source": "curated"},
    {"cn": "君子和而不同，小人同而不和。", "en": "Gentlemen harmonize despite differences; petty men are alike yet never in harmony.", "author": "孔子", "category": "处世之道", "source": "curated"},
    {"cn": "问渠那得清如许，为有源头活水来。", "en": "Why is the pond so clear? Because fresh water flows from its source.", "author": "朱熹", "category": "读书学习", "source": "curated"},
]

count = 0
for q in quotes:
    try:
        if not db.quotes.find_one({"cn": q["cn"]}):
            db.quotes.insert_one(q)
            count += 1
    except Exception as e:
        print(f"  ⚠️  {e}")

total = db.quotes.count_documents({})
print(f"✅ 新增 {count} 条")
print(f"📊 总格言数: {total}")
client.close()
