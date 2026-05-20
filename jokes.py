"""
每日冷笑话数据模块 - MongoDB 版
提供冷笑话查询、随机、搜索功能
"""

import os
import random
from datetime import date
from pymongo import MongoClient
import certifi

# MongoDB 连接（懒加载）
_client = None
_db = None
JOKES_COL = None
PENDING_JOKES_COL = None

def _ensure_collections():
    global _client, _db, JOKES_COL, PENDING_JOKES_COL
    if _client is None:
        MONGO_URI = os.environ.get("MONGO_URI") or os.environ.get("MONGODB_URI", "mongodb+srv://crawleryzd:crawleryzd123@mycluster.lyqtjvs.mongodb.net/")
        _client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
        _db = _client["daily_motto"]
        JOKES_COL = _db["jokes"]
        PENDING_JOKES_COL = _db["pending_jokes"]
    return JOKES_COL, PENDING_JOKES_COL

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
    JOKES_COL, _ = _ensure_collections()
    return JOKES_COL.count_documents({})


def get_random_joke():
    """获取随机冷笑话"""
    JOKES_COL, _ = _ensure_collections()
    count = get_joke_count()
    if count == 0:
        return None
    skip = random.randint(0, count - 1)
    return JOKES_COL.find_one({}, {"_id": False}, skip=skip)


def get_daily_joke():
    """根据日期获取每日冷笑话（每日固定同一条）"""
    JOKES_COL, _ = _ensure_collections()
    count = get_joke_count()
    if count == 0:
        return None
    seed = date.today().toordinal()
    rng = random.Random(seed + 999)  # 用偏移量避免和格言撞车
    skip = rng.randint(0, count - 1)
    return JOKES_COL.find_one({}, {"_id": False}, skip=skip)


def search_jokes(keyword):
    """搜索冷笑话"""
    JOKES_COL, _ = _ensure_collections()
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
    JOKES_COL, _ = _ensure_collections()
    return list(JOKES_COL.find({"category": category}, {"_id": False}))


def get_all_jokes():
    """获取全部笑话"""
    JOKES_COL, _ = _ensure_collections()
    return list(JOKES_COL.find({}, {"_id": False}))


def get_all_joke_categories_with_counts():
    """获取所有笑话分类及数量（1次聚合查询）"""
    JOKES_COL, _ = _ensure_collections()
    pipeline = [
        {"$group": {"_id": "$category", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}},
    ]
    results = list(JOKES_COL.aggregate(pipeline))
    counts = {r["_id"]: r["count"] for r in results}
    for cat in JOKES_CATEGORIES:
        if cat not in counts:
            counts[cat] = 0
    return counts


# ===== 管理功能 =====

def add_joke(joke_cn, punchline_cn, category,
             joke_en="", punchline_en="", source="curated"):
    """添加一条冷笑话"""
    JOKES_COL, _ = _ensure_collections()
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


# ===== 投稿相关 =====

def submit_joke(joke_cn, punchline_cn, category, joke_en="", punchline_en="", submitter=""):
    """用户提交冷笑话 -> pending_jokes"""
    JOKES_COL, PENDING_JOKES_COL = _ensure_collections()
    doc = {
        "joke_cn": joke_cn,
        "punchline_cn": punchline_cn,
        "joke_en": joke_en,
        "punchline_en": punchline_en,
        "category": category,
        "source": "user_submit",
        "status": "pending",
        "submitter": submitter or "",
        "review_notes": "",
        "submitted_at": date.today().isoformat(),
    }
    # 检查是否与已有笑话重复
    existing = JOKES_COL.find_one({"joke_cn": joke_cn})
    if existing:
        return {"success": False, "error": "这条笑话已存在"}
    pending = PENDING_JOKES_COL.find_one({"joke_cn": joke_cn, "status": "pending"})
    if pending:
        return {"success": False, "error": "这条笑话已有人提交，正在审核中"}

    PENDING_JOKES_COL.insert_one(doc)
    return {"success": True, "message": "提交成功，等待审核"}


def get_pending_jokes():
    """获取待审核的投稿"""
    _, PENDING_JOKES_COL = _ensure_collections()
    return list(PENDING_JOKES_COL.find({"status": "pending"}, {"_id": False}))


def approve_joke(joke_cn):
    """批准投稿 -> 移入 jokes"""
    JOKES_COL, PENDING_JOKES_COL = _ensure_collections()
    doc = PENDING_JOKES_COL.find_one_and_update(
        {"joke_cn": joke_cn, "status": "pending"},
        {"$set": {"status": "approved"}},
    )
    if doc:
        joke = {
            "joke_cn": doc["joke_cn"],
            "punchline_cn": doc["punchline_cn"],
            "joke_en": doc.get("joke_en", ""),
            "punchline_en": doc.get("punchline_en", ""),
            "category": doc["category"],
            "source": "user_submit",
        }
        try:
            JOKES_COL.insert_one(joke)
        except Exception:
            return {"success": False, "error": "入库失败（可能已存在）"}
        return {"success": True, "message": f"已批准: {doc['joke_cn'][:30]}..."}
    return {"success": False, "error": "未找到该投稿"}


def reject_joke(joke_cn, reason=""):
    """拒绝投稿"""
    _, PENDING_JOKES_COL = _ensure_collections()
    PENDING_JOKES_COL.find_one_and_update(
        {"joke_cn": joke_cn, "status": "pending"},
        {"$set": {"status": "rejected", "review_notes": reason}},
    )
    return {"success": True, "message": "已拒绝"}


def get_jokes_paginated(category=None, page=1, per_page=20):
    """分页获取冷笑话"""
    JOKES_COL, _ = _ensure_collections()
    skip = (page - 1) * per_page
    query = {"category": category} if category else {}
    cursor = JOKES_COL.find(query, {"_id": False}).skip(skip).limit(per_page)
    return list(cursor)


def get_jokes_count(category=None):
    """获取冷笑话总数（可指定分类）"""
    JOKES_COL, _ = _ensure_collections()
    query = {"category": category} if category else {}
    return JOKES_COL.count_documents(query)
