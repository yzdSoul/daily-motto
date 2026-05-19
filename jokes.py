"""
每日冷笑话数据模块 - MongoDB 版
提供冷笑话查询、随机、搜索功能
"""

import os
import random
from datetime import date
from pymongo import MongoClient
import certifi

# MongoDB 连接（复用格言的数据库）
MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://crawleryzd:crawleryzd123@mycluster.lyqtjvs.mongodb.net/")
_client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
_db = _client["daily_motto"]

# 集合引用
JOKES_COL = _db["jokes"]

# 笑话分类
JOKE_CATEGORIES = [
    "程序员笑话",
    "冷笑话",
    "谐音梗",
    "动物笑话",
    "生活段子",
    "校园笑话",
    "职场幽默",
    "奇葩问答",
]


# ===== 笑话查询 =====

def get_joke_count():
    """获取笑话总数"""
    return JOKES_COL.count_documents({})


def get_random_joke():
    """获取随机冷笑话"""
    count = get_joke_count()
    if count == 0:
        return None
    skip = random.randint(0, count - 1)
    return JOKES_COL.find_one({}, {"_id": False}, skip=skip)


def get_daily_joke():
    """根据日期获取每日冷笑话（每日固定同一条）"""
    count = get_joke_count()
    if count == 0:
        return None
    seed = date.today().toordinal()
    rng = random.Random(seed + 999)  # 用偏移量避免和格言撞车
    skip = rng.randint(0, count - 1)
    return JOKES_COL.find_one({}, {"_id": False}, skip=skip)


def search_jokes(keyword):
    """搜索冷笑话"""
    if not keyword:
        return []
    keyword = keyword.lower()
    regex = f".*{keyword}.*"
    cursor = JOKES_COL.find({
        "$or": [
            {"joke_cn": {"$regex": regex, "$options": "i"}},
            {"punchline_cn": {"$regex": regex, "$options": "i"}},
            {"joke_en": {"$regex": regex, "$options": "i"}},
            {"punchline_en": {"$regex": regex, "$options": "i"}},
            {"category": {"$regex": regex, "$options": "i"}},
        ]
    }, {"_id": False})
    return list(cursor)


def get_jokes_by_category(category):
    """按分类获取笑话"""
    return list(JOKES_COL.find({"category": category}, {"_id": False}))


def get_all_jokes():
    """获取全部笑话"""
    return list(JOKES_COL.find({}, {"_id": False}))


# ===== 管理功能 =====

def add_joke(joke_cn, punchline_cn, category,
             joke_en="", punchline_en="", source="curated"):
    """添加一条冷笑话"""
    doc = {
        "joke_cn": joke_cn,
        "punchline_cn": punchline_cn,
        "joke_en": joke_en,
        "punchline_en": punchline_en,
        "category": category,
        "source": source,
    }
    try:
        JOKES_COL.insert_one(doc)
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}


def add_jokes_batch(jokes_list):
    """批量添加冷笑话"""
    success = 0
    failed = 0
    for j in jokes_list:
        result = add_joke(
            j["joke_cn"], j["punchline_cn"], j["category"],
            j.get("joke_en", ""), j.get("punchline_en", ""),
            j.get("source", "curated"),
        )
        if result["success"]:
            success += 1
        else:
            failed += 1
    return {"success": success, "failed": failed}
