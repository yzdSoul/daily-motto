"""
每日格言数据模块
包含精选的中英文对照格言及分类
"""

QUOTES = [
    # 哲理智慧
    {
        "cn": "千里之行，始于足下。",
        "en": "A journey of a thousand miles begins with a single step.",
        "author": "老子",
        "category": "哲理智慧",
    },
    {
        "cn": "学而不思则罔，思而不学则殆。",
        "en": "Learning without thought is labor lost; thought without learning is perilous.",
        "author": "孔子",
        "category": "哲理智慧",
    },
    {
        "cn": "知之为知之，不知为不知，是知也。",
        "en": "To know what you know and what you do not know, that is true knowledge.",
        "author": "孔子",
        "category": "哲理智慧",
    },
    {
        "cn": "不积跬步，无以至千里。",
        "en": "Without small steps, one cannot travel a thousand miles.",
        "author": "荀子",
        "category": "哲理智慧",
    },
    # 励志奋斗
    {
        "cn": "宝剑锋从磨砺出，梅花香自苦寒来。",
        "en": "A sharp sword is honed from grinding; plum blossoms fragrance comes from bitter cold.",
        "author": "《警世贤文》",
        "category": "励志奋斗",
    },
    {
        "cn": "业精于勤，荒于嬉。",
        "en": "Mastery comes from diligence, and idleness leads to failure.",
        "author": "韩愈",
        "category": "励志奋斗",
    },
    {
        "cn": "长风破浪会有时，直挂云帆济沧海。",
        "en": "Riding the wind and breaking the waves, I will hoist my sail and cross the vast ocean.",
        "author": "李白",
        "category": "励志奋斗",
    },
    {
        "cn": "天生我材必有用。",
        "en": "Heaven has endowed me with talents for a purpose.",
        "author": "李白",
        "category": "励志奋斗",
    },
    # 人生态度
    {
        "cn": "路漫漫其修远兮，吾将上下而求索。",
        "en": "The road ahead is long and winding, I will search high and low.",
        "author": "屈原",
        "category": "人生态度",
    },
    {
        "cn": "人生自古谁无死，留取丹心照汗青。",
        "en": "Everyone dies; let me leave a loyal heart shining in history.",
        "author": "文天祥",
        "category": "人生态度",
    },
    {
        "cn": "欲穷千里目，更上一层楼。",
        "en": "To see a thousand miles further, climb one more story higher.",
        "author": "王之涣",
        "category": "人生态度",
    },
    # 读书学习
    {
        "cn": "读书破万卷，下笔如有神。",
        "en": "Having read ten thousand books, writing feels inspired.",
        "author": "杜甫",
        "category": "读书学习",
    },
    # English Wisdom
    {
        "cn": "走得慢没关系，只要不停下脚步。",
        "en": "It does not matter how slowly you go as long as you do not stop.",
        "author": "Confucius",
        "category": "英文智慧",
    },
    {
        "cn": "成就伟大事业的唯一方法，就是热爱你所做的事。",
        "en": "The only way to do great work is to love what you do.",
        "author": "Steve Jobs",
        "category": "英文智慧",
    },
    {
        "cn": "求知若饥，虚心若愚。",
        "en": "Stay hungry, stay foolish.",
        "author": "Steve Jobs",
        "category": "英文智慧",
    },
    {
        "cn": "种一棵树最好的时间是十年前，其次是现在。",
        "en": "The best time to plant a tree was 20 years ago. The second best time is now.",
        "author": "Chinese Proverb",
        "category": "英文智慧",
    },
    {
        "cn": "困难之中蕴藏着机会。",
        "en": "In the middle of difficulty lies opportunity.",
        "author": "Albert Einstein",
        "category": "英文智慧",
    },
    {
        "cn": "成功不是终点，失败也非末日，最重要的是继续前行的勇气。",
        "en": "Success is not final, failure is not fatal: it is the courage to continue that counts.",
        "author": "Winston Churchill",
        "category": "英文智慧",
    },
    # 新增格言
    {
        "cn": "己所不欲，勿施于人。",
        "en": "Do not do to others what you do not want done to yourself.",
        "author": "孔子",
        "category": "哲理智慧",
    },
    {
        "cn": "天行健，君子以自强不息。",
        "en": "As heaven's movement is ever vigorous, so must a gentleman ceaselessly strive.",
        "author": "《周易》",
        "category": "励志奋斗",
    },
    {
        "cn": "海纳百川，有容乃大。",
        "en": "The ocean admits all rivers, and its greatness lies in its capacity.",
        "author": "林则徐",
        "category": "人生态度",
    },
    {
        "cn": "三人行，必有我师焉。",
        "en": "When three walk together, there is always something I can learn.",
        "author": "孔子",
        "category": "读书学习",
    },
    {
        "cn": "The future belongs to those who believe in the beauty of their dreams.",
        "en": "未来属于那些相信梦想之美的人。",
        "author": "Eleanor Roosevelt",
        "category": "英文智慧",
    },
    {
        "cn": "人生如逆旅，我亦是行人。",
        "en": "Life is like a journey, and I am but a traveler.",
        "author": "苏轼",
        "category": "人生态度",
    },
]

CATEGORIES = sorted(set(q["category"] for q in QUOTES))


def get_quote_by_id(idx):
    """根据索引获取格言"""
    if 0 <= idx < len(QUOTES):
        return QUOTES[idx]
    return None


def get_random_quote():
    """获取随机格言"""
    import random
    return random.choice(QUOTES)


def get_daily_quote():
    """根据日期获取每日格言"""
    import random
    from datetime import date
    seed = date.today().toordinal()
    rng = random.Random(seed)
    return rng.choice(QUOTES)


def search_quotes(keyword):
    """搜索格言"""
    keyword = keyword.lower()
    results = []
    for q in QUOTES:
        if (keyword in q["cn"].lower() or
            keyword in q["en"].lower() or
            keyword in q["author"].lower() or
            keyword in q["category"].lower()):
            results.append(q)
    return results


def get_quotes_by_category(category):
    """按分类获取格言"""
    return [q for q in QUOTES if q["category"] == category]
