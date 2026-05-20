"""
每日格言数据模块 - MongoDB 版
提供格言查询、搜索、投稿功能
"""
import os
import random
from datetime import date
from pymongo import MongoClient
import certifi

# MongoDB 连接
MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://crawleryzd:crawleryzd123@mycluster.lyqtjvs.mongodb.net/")
_client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
_db = _client["daily_motto"]

# 集合引用
QUOTES_COL = _db["quotes"]
PENDING_COL = _db["pending_quotes"]
VISITS_COL = _db["visit_logs"]  # 每日访问量统计

# 分类（硬编码，保持顺序稳定）
CATEGORIES = [
    "哲理智慧", "励志奋斗", "人生态度", "读书学习", "英文智慧",
    "爱情友谊", "时间光阴", "自然万物", "处世之道", "家国情怀",
    "小说名句", "电影名句", "动漫名句",
]


# ===== 格言查询 =====

def get_quote_count():
    """获取格言总数"""
    return QUOTES_COL.count_documents({})


def get_random_quote():
    """获取随机格言"""
    count = get_quote_count()
    if count == 0:
        return None
    skip = random.randint(0, count - 1)
    return QUOTES_COL.find_one({}, {"_id": False}, skip=skip)


def get_daily_quote():
    """根据日期获取每日格言"""
    count = get_quote_count()
    if count == 0:
        return None
    seed = date.today().toordinal()
    rng = random.Random(seed)
    skip = rng.randint(0, count - 1)
    return QUOTES_COL.find_one({}, {"_id": False}, skip=skip)


def search_quotes(keyword):
    """搜索格言（模糊匹配）"""
    if not keyword:
        return []
    keyword = keyword.lower()
    regex = f".*{keyword}.*"
    cursor = QUOTES_COL.find({
        "$or": [
            {"cn": {"$regex": regex, "$options": "i"}},
            {"en": {"$regex": regex, "$options": "i"}},
            {"author": {"$regex": regex, "$options": "i"}},
            {"category": {"$regex": regex, "$options": "i"}},
        ]
    }, {"_id": False})
    return list(cursor)


def get_quotes_by_category(category):
    """按分类获取格言"""
    return list(QUOTES_COL.find({"category": category}, {"_id": False}))


def get_all_quotes():
    """获取全部格言"""
    return list(QUOTES_COL.find({}, {"_id": False}))


def get_all_categories_with_counts():
    """获取所有分类及数量"""
    pipeline = [
        {"$group": {"_id": "$category", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}},
    ]
    results = list(QUOTES_COL.aggregate(pipeline))
    counts = {r["_id"]: r["count"] for r in results}
    # 保证所有定义过的分类都有（即使为 0）
    for cat in CATEGORIES:
        if cat not in counts:
            counts[cat] = 0
    return counts


# ===== 投稿相关 =====

def submit_quote(cn, author, category, en="", submitter=""):
    """用户提交格言 -> pending_quotes"""
    doc = {
        "cn": cn,
        "en": en,
        "author": author,
        "category": category,
        "source": "user_submit",
        "status": "pending",
        "submitter": submitter or "",
        "review_notes": "",
        "submitted_at": date.today().isoformat(),
    }
    # 检查是否与已有格言重复
    existing = QUOTES_COL.find_one({"cn": cn})
    if existing:
        return {"success": False, "error": "这条格言已存在"}
    pending = PENDING_COL.find_one({"cn": cn, "status": "pending"})
    if pending:
        return {"success": False, "error": "这条格言已有人提交，正在审核中"}

    PENDING_COL.insert_one(doc)
    return {"success": True, "message": "提交成功，等待审核"}


def get_pending_quotes():
    """获取待审核的投稿"""
    return list(PENDING_COL.find({"status": "pending"}, {"_id": False}))


def approve_quote(cn):
    """批准投稿 -> 移入 quotes"""
    doc = PENDING_COL.find_one_and_update(
        {"cn": cn, "status": "pending"},
        {"$set": {"status": "approved"}},
    )
    if doc:
        quote = {
            "cn": doc["cn"],
            "en": doc.get("en", ""),
            "author": doc["author"],
            "category": doc["category"],
            "source": "user_submit",
        }
        try:
            QUOTES_COL.insert_one(quote)
        except Exception:
            return {"success": False, "error": "入库失败（可能已存在）"}
        return {"success": True, "message": f"已批准: {doc['cn']}"}
    return {"success": False, "error": "未找到该投稿"}


def reject_quote(cn, reason=""):
    """拒绝投稿"""
    PENDING_COL.find_one_and_update(
        {"cn": cn, "status": "pending"},
        {"$set": {"status": "rejected", "review_notes": reason}},
    )
    return {"success": True, "message": "已拒绝"}


def add_quote(cn, en, author, category, source="curated"):
    """直接添加一条格言（AI 生成或手工精选）"""
    doc = {
        "cn": cn,
        "en": en,
        "author": author,
        "category": category,
        "source": source,
    }
    try:
        QUOTES_COL.insert_one(doc)
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}


def add_quotes_batch(quotes_list):
    """批量添加格言"""
    success = 0
    failed = 0
    for q in quotes_list:
        result = add_quote(q["cn"], q.get("en", ""), q["author"], q["category"], q.get("source", "ai_generated"))
        if result["success"]:
            success += 1
        else:
            failed += 1
    return {"success": success, "failed": failed}


# ===== 访问量统计 =====

def record_visit():
    """记录一次页面访问（PV）"""
    today = date.today().isoformat()
    VISITS_COL.update_one(
        {"date": today},
        {"$inc": {"count": 1}},
        upsert=True
    )


def get_today_visits():
    """获取今日访问量"""
    today = date.today().isoformat()
    doc = VISITS_COL.find_one({"date": today})
    return doc["count"] if doc else 0


def get_visit_history(days=7):
    """获取最近 N 天的访问历史"""
    from datetime import timedelta
    results = []
    for i in range(days - 1, -1, -1):
        d = (date.today() - timedelta(days=i)).isoformat()
        doc = VISITS_COL.find_one({"date": d})
        results.append({
            "date": d,
            "count": doc["count"] if doc else 0
        })
    return results
