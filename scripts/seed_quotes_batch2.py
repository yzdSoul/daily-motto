"""Batch 2: Fill up existing categories to reach ~120 total"""
from pymongo import MongoClient
import certifi

uri = "mongodb+srv://crawleryzd:crawleryzd123@mycluster.lyqtjvs.mongodb.net/"
client = MongoClient(uri, tlsCAFile=certifi.where())
db = client["daily_motto"]

quotes = [
    # ===== 哲理智慧 (add 7) =====
    {"cn": "上善若水，水善利万物而不争。", "en": "The highest good is like water; it benefits all things without contention.", "author": "老子", "category": "哲理智慧", "source": "curated"},
    {"cn": "塞翁失马，焉知非福。", "en": "The old man lost his horse — who knows if it's a blessing in disguise?", "author": "《淮南子》", "category": "哲理智慧", "source": "curated"},
    {"cn": "存在即合理。", "en": "What is real is rational.", "author": "Hegel", "category": "哲理智慧", "source": "curated"},
    {"cn": "认识你自己。", "en": "Know thyself.", "author": "Socrates", "category": "哲理智慧", "source": "curated"},
    {"cn": "人不能两次踏进同一条河流。", "en": "One cannot step into the same river twice.", "author": "Heraclitus", "category": "哲理智慧", "source": "curated"},
    {"cn": "我思故我在。", "en": "I think, therefore I am.", "author": "Descartes", "category": "哲理智慧", "source": "curated"},
    {"cn": "无欲则刚。", "en": "Desirelessness makes one strong.", "author": "林则徐", "category": "哲理智慧", "source": "curated"},
    {"cn": "宇宙的真相是变化，生活的智慧是适应。", "en": "The truth of the universe is change; the wisdom of life is adaptation.", "author": "佚名", "category": "哲理智慧", "source": "curated"},

    # ===== 励志奋斗 (add 7) =====
    {"cn": "世上无难事，只怕有心人。", "en": "Nothing in the world is difficult for a determined mind.", "author": "佚名", "category": "励志奋斗", "source": "curated"},
    {"cn": "千磨万击还坚劲，任尔东西南北风。", "en": "Battered by a thousand blows, still I stand firm; let the winds blow from every direction.", "author": "郑燮", "category": "励志奋斗", "source": "curated"},
    {"cn": "没有比人更高的山，没有比脚更长的路。", "en": "No mountain is higher than man; no road is longer than the foot.", "author": "汪国真", "category": "励志奋斗", "source": "curated"},
    {"cn": "吃得苦中苦，方为人上人。", "en": "One who endures the bitterest hardship becomes the best of people.", "author": "佚名", "category": "励志奋斗", "source": "curated"},
    {"cn": "不经历风雨，怎么见彩虹。", "en": "No rainbow appears without a storm.", "author": "佚名", "category": "励志奋斗", "source": "curated"},
    {"cn": "坚持就是胜利。", "en": "Perseverance is victory.", "author": "佚名", "category": "励志奋斗", "source": "curated"},
    {"cn": "志当存高远。", "en": "Set your aspirations high.", "author": "诸葛亮", "category": "励志奋斗", "source": "curated"},

    # ===== 人生态度 (add 7) =====
    {"cn": "宠辱不惊，看庭前花开花落。", "en": "Stay calm in honor and disgrace, watching flowers bloom and fall in the courtyard.", "author": "《菜根谭》", "category": "人生态度", "source": "curated"},
    {"cn": "一切都是最好的安排。", "en": "Everything happens for the best.", "author": "佚名", "category": "人生态度", "source": "curated"},
    {"cn": "活在当下。", "en": "Live in the present moment.", "author": "佚名", "category": "人生态度", "source": "curated"},
    {"cn": "简单生活，快乐人生。", "en": "Live simply, live happily.", "author": "佚名", "category": "人生态度", "source": "curated"},
    {"cn": "笑对人生，人生也会对你微笑。", "en": "Smile at life, and life will smile back at you.", "author": "佚名", "category": "人生态度", "source": "curated"},
    {"cn": "人生如茶，苦后回甘。", "en": "Life is like tea — bitter at first, sweet in the aftertaste.", "author": "佚名", "category": "人生态度", "source": "curated"},
    {"cn": "尽人事，听天命。", "en": "Do your best and let fate do the rest.", "author": "佚名", "category": "人生态度", "source": "curated"},

    # ===== 读书学习 (add 10) =====
    {"cn": "学如逆水行舟，不进则退。", "en": "Learning is like rowing upstream; not to advance is to fall back.", "author": "佚名", "category": "读书学习", "source": "curated"},
    {"cn": "温故而知新，可以为师矣。", "en": "Reviewing the old and knowing the new makes a teacher.", "author": "孔子", "category": "读书学习", "source": "curated"},
    {"cn": "书山有路勤为径，学海无涯苦作舟。", "en": "Diligence is the path on the mountain of books; hard work is the boat on the endless sea of learning.", "author": "韩愈", "category": "读书学习", "source": "curated"},
    {"cn": "学而不厌，诲人不倦。", "en": "Learn without satiety; teach without fatigue.", "author": "孔子", "category": "读书学习", "source": "curated"},
    {"cn": "书籍是人类进步的阶梯。", "en": "Books are the ladder of human progress.", "author": "Gorky", "category": "读书学习", "source": "curated"},
    {"cn": "授人以鱼，不如授人以渔。", "en": "Give a man a fish and you feed him for a day; teach him to fish and you feed him for a lifetime.", "author": "佚名", "category": "读书学习", "source": "curated"},
    {"cn": "吾生也有涯，而知也无涯。", "en": "Life is finite, but knowledge is infinite.", "author": "庄子", "category": "读书学习", "source": "curated"},
    {"cn": "读万卷书，行万里路。", "en": "Read ten thousand books, travel ten thousand miles.", "author": "董其昌", "category": "读书学习", "source": "curated"},
    {"cn": "学而不思则罔，思而不学则殆。", "en": "Learning without thought is labor lost; thought without learning is perilous.", "author": "孔子", "category": "读书学习", "source": "curated"},
    {"cn": "知之者不如好之者，好之者不如乐之者。", "en": "Those who know are not as good as those who love; those who love are not as good as those who delight.", "author": "孔子", "category": "读书学习", "source": "curated"},

    # ===== 英文智慧 (add 5) =====
    {"cn": "行动胜于言语。", "en": "Actions speak louder than words.", "author": "佚名", "category": "英文智慧", "source": "curated"},
    {"cn": "每天都是一个新的开始。", "en": "Every day is a new beginning.", "author": "佚名", "category": "英文智慧", "source": "curated"},
    {"cn": "你最害怕的事情往往是你最需要去做的事情。", "en": "The thing you fear most is often the thing you most need to do.", "author": "佚名", "category": "英文智慧", "source": "curated"},
    {"cn": "简单是终极的复杂。", "en": "Simplicity is the ultimate sophistication.", "author": "Leonardo da Vinci", "category": "英文智慧", "source": "curated"},
    {"cn": "不要等待；时机永远不会完美。", "en": "Don't wait; the time will never be just right.", "author": "Napoleon Hill", "category": "英文智慧", "source": "curated"},
]

# Insert
count = 0
for q in quotes:
    try:
        if not db.quotes.find_one({"cn": q["cn"]}):
            db.quotes.insert_one(q)
            count += 1
    except Exception as e:
        print(f"  ⚠️  跳过: {q['cn'][:20]}... - {e}")

total = db.quotes.count_documents({})
distinct = db.quotes.distinct("category")
print(f"✅ 新增 {count} 条格言")
print(f"📊 总格言数: {total}")
print(f"\n📂 各分类:")
for cat in distinct:
    cnt = db.quotes.count_documents({"category": cat})
    print(f"   {cat}: {cnt} 条")

client.close()
