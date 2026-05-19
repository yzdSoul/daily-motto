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
from jokes import (JOKE_CATEGORIES, get_random_joke, get_daily_joke,
                    search_jokes, get_jokes_by_category, get_all_jokes,
                    get_joke_count)

app = Flask(__name__)


# ========== 首页 ==========

@app.route("/")
def index():
    """首页 - 展示每日格言、随机格言和每日冷笑话"""
    daily = get_daily_quote()
    random_q = get_random_quote()
    daily_joke = get_daily_joke()
    return render_template("index.html",
                         daily=daily,
                         random=random_q,
                         daily_joke=daily_joke,
                         today=date.today().isoformat(),
                         total=get_quote_count(),
                         joke_total=get_joke_count(),
                         categories=CATEGORIES,
                         joke_categories=JOKE_CATEGORIES)


# ========== 格言页面 ==========

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


# ========== 格言 API ==========

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


# ========== 冷笑话页面 ==========

@app.route("/jokes")
def jokes_list():
    """冷笑话列表页"""
    category = request.args.get("category", "")
    if category and category in JOKE_CATEGORIES:
        jokes = get_jokes_by_category(category)
    else:
        jokes = get_all_jokes()
        category = "全部"
    return render_template("jokes.html",
                         jokes=jokes,
                         current_category=category,
                         categories=JOKE_CATEGORIES)


# ========== 冷笑话 API ==========

@app.route("/api/joke/random")
def api_joke_random():
    """API: 获取随机冷笑话"""
    j = get_random_joke()
    return jsonify(j)


@app.route("/api/joke/daily")
def api_joke_daily():
    """API: 获取每日冷笑话"""
    j = get_daily_joke()
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
    """API: 获取冷笑话分类"""
    counts = {cat: len(get_jokes_by_category(cat)) for cat in JOKE_CATEGORIES}
    return jsonify({
        "categories": JOKE_CATEGORIES,
        "counts": counts,
        "total": get_joke_count(),
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
