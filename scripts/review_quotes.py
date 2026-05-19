"""Review pending quotes - display pending submissions for AI + human review"""
import os
from pymongo import MongoClient
import certifi

uri = os.environ.get("MONGODB_URI", "mongodb+srv://crawleryzd:YOUR_PASSWORD@mycluster.lyqtjvs.mongodb.net/")
client = MongoClient(uri, tlsCAFile=certifi.where())
db = client["daily_motto"]

pending = list(db["pending_quotes"].find({"status": "pending"}))

if not pending:
    print("📭 没有待审核的投稿")
else:
    for i, q in enumerate(pending, 1):
        print(f"\n{'='*50}")
        print(f"  #{i}")
        print(f"  中文: {q['cn']}")
        print(f"  英文: {q.get('en', '(无)')}")
        print(f"  作者: {q['author']}")
        print(f"  分类: {q['category']}")
        print(f"  投稿人: {q.get('submitter', '匿名')}")
        print(f"  时间: {q.get('submitted_at', '未知')}")
    print(f"\n{'='*50}")
    print(f"📊 共 {len(pending)} 条待审核")

client.close()
