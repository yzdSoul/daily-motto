"""
每日格言 Web App
Flask 后端 + REST API
"""

import random
from datetime import date
from flask import Flask, render_template, jsonify, request

from quotes import QUOTES, CATEGORIES, get_random_quote, get_daily_quote, search_quotes, get_quotes_by_category

app = Flask(__name__)


@app.route("/")
def index():
    """首页 - 展示每日格言和随机格言"""
    daily = get_daily_quote()
    random_q = get_random_quote()
    return render_template("index.html",
                         daily=daily,
                         random=random_q,
                         today=date.today().isoformat(),
                         total=len(QUOTES),
                         categories=CATEGORIES)


@app.route("/all")
def all_quotes():
    """全部格言页面"""
    category = request.args.get("category", "")
    if category and category in CATEGORIES:
        quotes = get_quotes_by_category(category)
    else:
        quotes = QUOTES
        category = "全部"
    return render_template("all.html",
                         quotes=quotes,
                         current_category=category,
                         categories=CATEGORIES)


@app.route("/search")
def search():
    """搜索页面"""
    q = request.args.get("q", "").strip()
    results = search_quotes(q) if q else []
    return render_template("search.html",
                         results=results,
                         keyword=q,
                         categories=CATEGORIES)


# ========== REST API ==========

@app.route("/api/random")
def api_random():
    """API: 获取随机格言"""
    q = get_random_quote()
    return jsonify(q)


@app.route("/api/daily")
def api_daily():
    """API: 获取每日格言"""
    q = get_daily_quote()
    return jsonify({
        "date": date.today().isoformat(),
        "quote": q,
    })


@app.route("/api/all")
def api_all():
    """API: 获取全部格言"""
    category = request.args.get("category", "")
    if category and category in CATEGORIES:
        quotes = get_quotes_by_category(category)
    else:
        quotes = QUOTES
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
    """API: 获取所有分类"""
    counts = {cat: len(get_quotes_by_category(cat)) for cat in CATEGORIES}
    return jsonify({
        "categories": CATEGORIES,
        "counts": counts,
        "total": len(QUOTES),
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
