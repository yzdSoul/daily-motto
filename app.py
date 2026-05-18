"""
每日格言 Web App
Flask 后端 + REST API
"""

import random
from datetime import date
from flask import Flask, render_template, jsonify, request

from quotes import (CATEGORIES, get_random_quote, get_daily_quote,
                     search_quotes, get_quotes_by_category, get_all_quotes,
                     get_quote_count, submit_quote)

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
                         total=get_quote_count(),
                         categories=CATEGORIES)


@app.route("/all")
def all_quotes():
    """全部格言页面"""
    category = request.args.get("category", "")
    if category and category in CATEGORIES:
        quotes = get_quotes_by_category(category)
    else:
        quotes = get_all_quotes()
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
    """API: 获取所有分类"""
    counts = {cat: len(get_quotes_by_category(cat)) for cat in CATEGORIES}
    return jsonify({
        "categories": CATEGORIES,
        "counts": counts,
        "total": get_quote_count(),
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
        elif category not in CATEGORIES:
            errors["category"] = "分类无效"

        if not errors:
            result = submit_quote(cn, author, category, en, submitter)
            if result["success"]:
                return render_template("submit.html",
                                     success=True,
                                     categories=CATEGORIES)
            else:
                errors["cn"] = result.get("error", "提交失败，请重试")

        return render_template("submit.html",
                             errors=errors,
                             form_data=request.form,
                             categories=CATEGORIES)

    return render_template("submit.html",
                         categories=CATEGORIES,
                         form_data={},
                         errors={})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
