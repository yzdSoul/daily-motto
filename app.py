"""
每日格言 Web App
Flask 后端 + REST API
"""

import random
from datetime import date
from flask import Flask, render_template, jsonify, request

from quotes import (ALL_CATEGORIES, QUOTE_CATEGORIES, FAMOUS_CATEGORIES, get_random_quote, get_daily_quote,
                     search_quotes, get_quotes_by_category, get_all_quotes,
                     get_quote_count, get_all_categories_with_counts, submit_quote,
                     record_visit_safe, get_today_visits, get_today_pv, get_visit_history,
                     get_quotes_paginated, get_quotes_count)
from jokes import (JOKE_CATEGORIES, get_random_joke, get_daily_joke,
                    search_jokes, get_jokes_by_category, get_all_jokes,
                    get_joke_count, get_all_joke_categories_with_counts,
                    submit_joke, get_jokes_paginated, get_jokes_count)

app = Flask(__name__)

# ===== HTTP 缓存头 =====

@app.after_request
def add_caching_headers(response):
    # 静态资源：浏览器缓存 30 天（带版本号可长期缓存）
    if request.path.startswith('/static/'):
        response.headers['Cache-Control'] = 'public, max-age=2592000, immutable'
    # 每日 API：当天不变，缓存到明天
    elif request.path in ('/api/daily', '/api/joke/daily'):
        response.headers['Cache-Control'] = 'public, max-age=86400'
    # 分类 API：变化不频繁，缓存 5 分钟
    elif request.path in ('/api/categories', '/api/jokes/categories'):
        response.headers['Cache-Control'] = 'public, max-age=300'
    # 随机 API：不缓存
    elif request.path in ('/api/random', '/api/joke/random'):
        response.headers['Cache-Control'] = 'no-cache'
    return response


# 每日缓存（避免同一天重复查询 MongoDB）
_daily_cache = {}
_cache_date = None


def _get_or_refresh_cache(key, fetcher):
    """每日缓存：同一天只查一次 MongoDB"""
    global _cache_date
    today = date.today().isoformat()
    if _cache_date != today:
        _daily_cache.clear()
        _cache_date = today
    if key not in _daily_cache:
        _daily_cache[key] = fetcher()
    return _daily_cache[key]


# ========== 首页 ==========

@app.route("/")
def index():
    """首页 - 展示每日格言、随机格言和每日冷笑话"""
    # 记录访问（IP去重）
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ip:
        # X-Forwarded-For 可能包含多个IP，取第一个
        ip = ip.split(',')[0].strip()
    record_visit_safe(ip or 'unknown')
    
    # 总数每天只查一次
    total = _get_or_refresh_cache("quote_count", get_quote_count)
    joke_total = _get_or_refresh_cache("joke_count", get_joke_count)
    today_visits = _get_or_refresh_cache("today_visits", get_today_visits)
    today_pv = _get_or_refresh_cache("today_pv", get_today_pv)

    daily = _get_or_refresh_cache("daily_quote", get_daily_quote)
    daily_joke = _get_or_refresh_cache("daily_joke", get_daily_joke)
    random_q = get_random_quote()  # 随机每次不同，不缓存
    return render_template("index.html",
                         daily=daily,
                         random=random_q,
                         daily_joke=daily_joke,
                         today=date.today().isoformat(),
                         total=total,
                         joke_total=joke_total,
                         today_visits=today_visits,
                         today_pv=today_pv,
                         categories=QUOTE_CATEGORIES,
                         famous_categories=FAMOUS_CATEGORIES,
                         joke_categories=JOKE_CATEGORIES)


# ========== 格言页面 ==========

@app.route("/all")
def all_quotes():
    """全部格言页面（分页）"""
    category = request.args.get("category", "")
    page = request.args.get("page", 1, type=int)
    if page < 1:
        page = 1
    per_page = 20
    
    if category and category in QUOTE_CATEGORIES:
        quotes = get_quotes_paginated(category, page, per_page)
        total = get_quotes_count(category)
    else:
        # 只显示格言分类（不含名句）
        quotes = get_quotes_paginated(None, page, per_page)
        # 过滤掉名句分类
        quotes = [q for q in quotes if q.get("category") in QUOTE_CATEGORIES]
        total = get_quotes_count()
        category = "全部"
    
    total_pages = (total + per_page - 1) // per_page
    
    return render_template("all.html",
                         quotes=quotes,
                         current_category=category,
                         categories=QUOTE_CATEGORIES,
                         page=page,
                         total_pages=total_pages,
                         total=total)


@app.route("/quotes")
def famous_quotes():
    """经典名句页面（小说/电影/动漫）"""
    category = request.args.get("category", "")
    if category and category in FAMOUS_CATEGORIES:
        quotes = get_quotes_by_category(category)
    else:
        # 只显示名句分类
        all_q = get_all_quotes()
        quotes = [q for q in all_q if q.get("category") in FAMOUS_CATEGORIES]
        category = "全部"
    return render_template("quotes.html",
                         quotes=quotes,
                         current_category=category,
                         categories=FAMOUS_CATEGORIES,
                         total=len([q for q in get_all_quotes() if q.get("category") in FAMOUS_CATEGORIES]))


@app.route("/search")
def search():
    """搜索页面（同时搜索格言和冷笑话）"""
    q = request.args.get("q", "").strip()
    quote_results = search_quotes(q) if q else []
    joke_results = search_jokes(q) if q else []
    return render_template("search.html",
                         quote_results=quote_results,
                         joke_results=joke_results,
                         keyword=q,
                         categories=ALL_CATEGORIES)


# ========== 格言 API ==========

@app.route("/api/random")
def api_random():
    """API: 获取随机格言"""
    q = get_random_quote()
    return jsonify(q)


@app.route("/api/daily")
def api_daily():
    """API: 获取每日格言（每日缓存）"""
    q = _get_or_refresh_cache("daily_quote", get_daily_quote)
    return jsonify({
        "date": date.today().isoformat(),
        "quote": q,
    })


@app.route("/api/all")
def api_all():
    """API: 获取全部格言"""
    category = request.args.get("category", "")
    if category and category in ALL_CATEGORIES:
        quotes = get_quotes_by_category(category)
    else:
        quotes = get_all_quotes()
    return jsonify({
        "total": len(quotes),
        "quotes": quotes,
    })


@app.route("/api/search")
def api_search():
    """API: 搜索格言"""
    q = request.args.get("q", "").strip()
    results = search_quotes(q) if q else []
    return jsonify({
        "keyword": q,
        "total": len(results),
        "results": results,
    })


@app.route("/api/categories")
def api_categories():
    """API: 获取所有分类（每日缓存）"""
    counts = _get_or_refresh_cache("quote_category_counts", get_all_categories_with_counts)
    total = _get_or_refresh_cache("quote_count", get_quote_count)
    return jsonify({
        "categories": ALL_CATEGORIES,
        "counts": counts,
        "total": total,
    })


# ========== Widget ==========

@app.route("/widget")
def widget():
    """可嵌入 Widget - 每日格言卡片"""
    daily = get_daily_quote()
    return render_template("widget.html",
                         quote=daily,
                         today=date.today().isoformat())


# ========== 投稿 ==========

@app.route("/submit", methods=["GET", "POST"])
def submit():
    """用户投稿格言"""
    if request.method == "POST":
        cn = request.form.get("cn", "").strip()
        en = request.form.get("en", "").strip()
        author = request.form.get("author", "").strip()
        category = request.form.get("category", "").strip()
        submitter = request.form.get("submitter", "").strip()

        errors = {}
        if not cn:
            errors["cn"] = "请输入中文格言"
        if not author:
            errors["author"] = "请输入作者"
        if not category:
            errors["category"] = "请选择分类"
        elif category not in ALL_CATEGORIES:
            errors["category"] = "分类无效"

        if not errors:
            result = submit_quote(cn, author, category, en, submitter)
            if result["success"]:
                return render_template("submit.html",
                                     success=True,
                                     categories=ALL_CATEGORIES)
            else:
                errors["cn"] = result.get("error", "提交失败，请重试")

        return render_template("submit.html",
                             errors=errors,
                             form_data=request.form,
                             categories=ALL_CATEGORIES)

    return render_template("submit.html",
                         categories=ALL_CATEGORIES,
                         form_data={},
                         errors={})


# ========== 冷笑话投稿 ==========

@app.route("/submit/joke", methods=["GET", "POST"])
def submit_joke_route():
    """用户投稿冷笑话"""
    if request.method == "POST":
        joke_cn = request.form.get("joke_cn", "").strip()
        punchline_cn = request.form.get("punchline_cn", "").strip()
        joke_en = request.form.get("joke_en", "").strip()
        punchline_en = request.form.get("punchline_en", "").strip()
        category = request.form.get("category", "").strip()
        submitter = request.form.get("submitter", "").strip()

        errors = {}
        if not joke_cn:
            errors["joke_cn"] = "请输入冷笑话内容"
        if not punchline_cn:
            errors["punchline_cn"] = "请输入笑点/答案"
        if not category:
            errors["category"] = "请选择分类"
        elif category not in JOKE_CATEGORIES:
            errors["category"] = "分类无效"

        if not errors:
            result = submit_joke(joke_cn, punchline_cn, category, joke_en, punchline_en, submitter)
            if result["success"]:
                return render_template("submit_joke.html",
                                     success=True,
                                     form_data=request.form,
                                     categories=JOKE_CATEGORIES)
            else:
                errors["joke_cn"] = result.get("error", "提交失败，请重试")

        return render_template("submit_joke.html",
                             errors=errors,
                             form_data=request.form,
                             categories=JOKE_CATEGORIES)

    return render_template("submit_joke.html",
                         categories=JOKE_CATEGORIES,
                         form_data={},
                         errors={})


# ========== 冷笑话页面 ==========

@app.route("/jokes")
def jokes_list():
    """冷笑话列表页（分页）"""
    category = request.args.get("category", "")
    page = request.args.get("page", 1, type=int)
    if page < 1:
        page = 1
    per_page = 20
    
    if category and category in JOKE_CATEGORIES:
        jokes = get_jokes_paginated(category, page, per_page)
        total = get_jokes_count(category)
    else:
        jokes = get_jokes_paginated(None, page, per_page)
        total = get_jokes_count()
        category = "全部"
    
    total_pages = (total + per_page - 1) // per_page
    
    return render_template("jokes.html",
                         jokes=jokes,
                         current_category=category,
                         categories=JOKE_CATEGORIES,
                         page=page,
                         total_pages=total_pages,
                         total=total)


# ========== 冷笑话 API ==========

@app.route("/api/joke/random")
def api_joke_random():
    """API: 获取随机冷笑话"""
    j = get_random_joke()
    return jsonify(j)


@app.route("/api/joke/daily")
def api_joke_daily():
    """API: 获取每日冷笑话（每日缓存）"""
    j = _get_or_refresh_cache("daily_joke", get_daily_joke)
    return jsonify({
        "date": date.today().isoformat(),
        "joke": j,
    })


@app.route("/api/jokes/all")
def api_jokes_all():
    """API: 获取全部冷笑话"""
    category = request.args.get("category", "")
    if category and category in JOKE_CATEGORIES:
        jokes = get_jokes_by_category(category)
    else:
        jokes = get_all_jokes()
    return jsonify({
        "total": len(jokes),
        "jokes": jokes,
    })


@app.route("/api/jokes/search")
def api_jokes_search():
    """API: 搜索冷笑话"""
    q = request.args.get("q", "").strip()
    results = search_jokes(q) if q else []
    return jsonify({
        "keyword": q,
        "total": len(results),
        "results": results,
    })


@app.route("/api/jokes/categories")
def api_jokes_categories():
    """API: 获取冷笑话分类（每日缓存）"""
    counts = _get_or_refresh_cache("joke_category_counts", get_all_joke_categories_with_counts)
    total = _get_or_refresh_cache("joke_count", get_joke_count)
    return jsonify({
        "categories": JOKE_CATEGORIES,
        "counts": counts,
        "total": total,
    })


# ===== Debug: 查看请求IP和数据库状态 =====
@app.route("/api/debug/ip")
def debug_ip():
    db_status = "unknown"
    db_name = "unknown"
    try:
        from quotes import _ensure_collections
        _, _, _ = _ensure_collections()
        from quotes import _client, _db
        _client.admin.command('ping')
        db_status = "connected"
        db_name = _db.name
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return jsonify({
        "remote_addr": request.remote_addr,
        "x_forwarded_for": request.headers.get('X-Forwarded-For'),
        "x_real_ip": request.headers.get('X-Real-IP'),
        "mongo_uri_env": os.environ.get("MONGO_URI", "NOT_SET")[:30] + "...",
        "mongodb_uri_env": os.environ.get("MONGODB_URI", "NOT_SET")[:30] + "...",
        "db_status": db_status,
        "db_name": db_name
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
