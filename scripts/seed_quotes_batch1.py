"""Batch 1: 5 new categories - 爱情友谊, 时间光阴, 自然万物, 处世之道, 家国情怀"""
from pymongo import MongoClient
import certifi

uri = "mongodb+srv://crawleryzd:crawleryzd123@mycluster.lyqtjvs.mongodb.net/"
client = MongoClient(uri, tlsCAFile=certifi.where())
db = client["daily_motto"]

quotes = [
    # ===== 爱情友谊 =====
    {"cn": "执子之手，与子偕老。", "en": "Hold your hand, grow old with you.", "author": "《诗经》", "category": "爱情友谊", "source": "curated"},
    {"cn": "两情若是久长时，又岂在朝朝暮暮。", "en": "If love between two hearts lasts long, why need they be together day and night?", "author": "秦观", "category": "爱情友谊", "source": "curated"},
    {"cn": "海内存知己，天涯若比邻。", "en": "A bosom friend afar brings a distant land near.", "author": "王勃", "category": "爱情友谊", "source": "curated"},
    {"cn": "真正的朋友是在你最黑暗的时候，依然陪在你身边的人。", "en": "A true friend is someone who stays by your side in your darkest moments.", "author": "佚名", "category": "爱情友谊", "source": "curated"},
    {"cn": "爱不是彼此凝视，而是一起朝同一个方向看。", "en": "Love is not gazing at each other, but looking together in the same direction.", "author": "Antoine de Saint-Exupéry", "category": "爱情友谊", "source": "curated"},
    {"cn": "友谊是灵魂的结合。", "en": "Friendship is the union of souls.", "author": "Voltaire", "category": "爱情友谊", "source": "curated"},
    {"cn": "相知无远近，万里尚为邻。", "en": "True understanding knows no distance; ten thousand miles are but a step.", "author": "张九龄", "category": "爱情友谊", "source": "curated"},
    {"cn": "世间最美好的东西，莫过于有几个头脑和心地都很正直的朋友。", "en": "The greatest gift in life is having a few friends with both intelligence and integrity.", "author": "爱因斯坦", "category": "爱情友谊", "source": "curated"},
    {"cn": "衣带渐宽终不悔，为伊消得人憔悴。", "en": "My belt grows loose, yet I regret not; for you I pine away, body and soul.", "author": "柳永", "category": "爱情友谊", "source": "curated"},
    {"cn": "爱情是生活的诗歌和太阳。", "en": "Love is the poetry and sunshine of life.", "author": "Belinsky", "category": "爱情友谊", "source": "curated"},
    {"cn": "君子之交淡如水。", "en": "The friendship of a gentleman is as pure as water.", "author": "庄子", "category": "爱情友谊", "source": "curated"},
    {"cn": "友谊使欢乐倍增，使痛苦减半。", "en": "Friendship doubles joy and halves grief.", "author": "Francis Bacon", "category": "爱情友谊", "source": "curated"},

    # ===== 时间光阴 =====
    {"cn": "逝者如斯夫，不舍昼夜。", "en": "Time flows away like the river, day and night without rest.", "author": "孔子", "category": "时间光阴", "source": "curated"},
    {"cn": "盛年不重来，一日难再晨。及时当勉励，岁月不待人。", "en": "Prime years never return; no morning comes twice. Seize the hour to strive; time waits for no one.", "author": "陶渊明", "category": "时间光阴", "source": "curated"},
    {"cn": "光阴似箭，日月如梭。", "en": "Time flies like an arrow, days and months like a shuttle.", "author": "佚名", "category": "时间光阴", "source": "curated"},
    {"cn": "时间就是生命。浪费别人的时间等于谋财害命。", "en": "Time is life. Wasting others' time is robbery.", "author": "鲁迅", "category": "时间光阴", "source": "curated"},
    {"cn": "莫等闲，白了少年头，空悲切。", "en": "Do not waste your youth; regret comes too late when your hair turns grey.", "author": "岳飞", "category": "时间光阴", "source": "curated"},
    {"cn": "时间是一去不复返的河流。", "en": "Time is a river that never returns.", "author": "Ovid", "category": "时间光阴", "source": "curated"},
    {"cn": "昨日之日不可留。", "en": "Yesterday cannot be retrieved.", "author": "佚名", "category": "时间光阴", "source": "curated"},
    {"cn": "时间是最公平的，给任何人都是二十四小时。", "en": "Time is the fairest judge — it gives everyone twenty-four hours.", "author": "佚名", "category": "时间光阴", "source": "curated"},
    {"cn": "少年易老学难成，一寸光阴不可轻。", "en": "Youth flies, learning takes time; never take a single inch of light lightly.", "author": "朱熹", "category": "时间光阴", "source": "curated"},
    {"cn": "时间检验一切真理。", "en": "Time is the test of all truth.", "author": "佚名", "category": "时间光阴", "source": "curated"},

    # ===== 自然万物 =====
    {"cn": "落霞与孤鹜齐飞，秋水共长天一色。", "en": "Sunset clouds fly with the solitary duck; autumn water shares the sky's one hue.", "author": "王勃", "category": "自然万物", "source": "curated"},
    {"cn": "采菊东篱下，悠然见南山。", "en": "Plucking chrysanthemums under the eastern fence, I gaze at the southern hills in peace.", "author": "陶渊明", "category": "自然万物", "source": "curated"},
    {"cn": "大漠孤烟直，长河落日圆。", "en": "Solitary smoke straight in the vast desert; the setting sun round over the long river.", "author": "王维", "category": "自然万物", "source": "curated"},
    {"cn": "明月几时有？把酒问青天。", "en": "When will the moon be bright? Raising my cup, I ask the blue sky.", "author": "苏轼", "category": "自然万物", "source": "curated"},
    {"cn": "大自然从未背叛一颗爱她的心。", "en": "Nature never betrays the heart that loves her.", "author": "William Wordsworth", "category": "自然万物", "source": "curated"},
    {"cn": "一花一世界，一叶一菩提。", "en": "In a flower lies a world; in a leaf, enlightenment.", "author": "佛家偈语", "category": "自然万物", "source": "curated"},
    {"cn": "春眠不觉晓，处处闻啼鸟。", "en": "Spring sleep knows no dawn; birds sing everywhere.", "author": "孟浩然", "category": "自然万物", "source": "curated"},
    {"cn": "会当凌绝顶，一览众山小。", "en": "I must ascend the mountain's crest; then all peaks appear small.", "author": "杜甫", "category": "自然万物", "source": "curated"},
    {"cn": "水是万物的本源。", "en": "Water is the source of all things.", "author": "Thales", "category": "自然万物", "source": "curated"},
    {"cn": "人法地，地法天，天法道，道法自然。", "en": "Man follows earth, earth follows heaven, heaven follows the Tao, the Tao follows nature.", "author": "老子", "category": "自然万物", "source": "curated"},
    {"cn": "望月思故乡。", "en": "Gazing at the moon, I long for home.", "author": "李白", "category": "自然万物", "source": "curated"},
    {"cn": "行到水穷处，坐看云起时。", "en": "Walk to where the water ends, sit and watch the clouds rise.", "author": "王维", "category": "自然万物", "source": "curated"},

    # ===== 处世之道 =====
    {"cn": "己所不欲，勿施于人。", "en": "Do not do to others what you do not want done to yourself.", "author": "孔子", "category": "处世之道", "source": "curated"},
    {"cn": "良言一句三冬暖，恶语伤人六月寒。", "en": "Kind words warm three winter months; harsh words chill a June day.", "author": "佚名", "category": "处世之道", "source": "curated"},
    {"cn": "退一步海阔天空。", "en": "Step back and the sea is wide, the sky is vast.", "author": "佚名", "category": "处世之道", "source": "curated"},
    {"cn": "满招损，谦受益。", "en": "Pride brings loss; humility brings gain.", "author": "《尚书》", "category": "处世之道", "source": "curated"},
    {"cn": "不以物喜，不以己悲。", "en": "Do not be elated by gain nor saddened by loss.", "author": "范仲淹", "category": "处世之道", "source": "curated"},
    {"cn": "静坐常思己过，闲谈莫论人非。", "en": "Sit quietly and reflect on your own faults; in idle talk, do not judge others.", "author": "佚名", "category": "处世之道", "source": "curated"},
    {"cn": "大智若愚，大巧若拙。", "en": "The greatest wisdom seems foolish; the greatest skill seems clumsy.", "author": "老子", "category": "处世之道", "source": "curated"},
    {"cn": "欲速则不达。", "en": "Haste makes waste.", "author": "孔子", "category": "处世之道", "source": "curated"},
    {"cn": "忍耐是苦涩的，但它的果实是甘甜的。", "en": "Patience is bitter, but its fruit is sweet.", "author": "Rousseau", "category": "处世之道", "source": "curated"},
    {"cn": "严于律己，宽以待人。", "en": "Be strict with yourself and lenient toward others.", "author": "孔子", "category": "处世之道", "source": "curated"},
    {"cn": "世上本无事，庸人自扰之。", "en": "There is no trouble in the world; only the foolish invite it.", "author": "佚名", "category": "处世之道", "source": "curated"},
    {"cn": "赠人玫瑰，手有余香。", "en": "When you give a rose, its fragrance lingers on your hand.", "author": "佚名", "category": "处世之道", "source": "curated"},

    # ===== 家国情怀 =====
    {"cn": "天下兴亡，匹夫有责。", "en": "The rise and fall of the nation is the responsibility of every citizen.", "author": "顾炎武", "category": "家国情怀", "source": "curated"},
    {"cn": "先天下之忧而忧，后天下之乐而乐。", "en": "Worry before the world worries; rejoice after the world rejoices.", "author": "范仲淹", "category": "家国情怀", "source": "curated"},
    {"cn": "位卑未敢忘忧国。", "en": "Though humble in rank, I never forget my country.", "author": "陆游", "category": "家国情怀", "source": "curated"},
    {"cn": "为中华之崛起而读书。", "en": "Study for the rise of China.", "author": "周恩来", "category": "家国情怀", "source": "curated"},
    {"cn": "人生自古谁无死，留取丹心照汗青。", "en": "Everyone dies; let me leave a loyal heart shining in history.", "author": "文天祥", "category": "家国情怀", "source": "curated"},
    {"cn": "捐躯赴国难，视死忽如归。", "en": "Facing national crisis, death is but a return home.", "author": "曹植", "category": "家国情怀", "source": "curated"},
    {"cn": "家是最小国，国是千万家。", "en": "The family is the smallest nation; the nation is millions of families.", "author": "佚名", "category": "家国情怀", "source": "curated"},
    {"cn": "横眉冷对千夫指，俯首甘为孺子牛。", "en": "Fierce-browed, I defy a thousand pointing fingers; head bowed, I serve like a willing ox.", "author": "鲁迅", "category": "家国情怀", "source": "curated"},
    {"cn": "国之不存，何以家为？", "en": "If the nation falls, what home remains?", "author": "左宗棠", "category": "家国情怀", "source": "curated"},
    {"cn": "没有国，哪有家。", "en": "Without a country, there can be no home.", "author": "佚名", "category": "家国情怀", "source": "curated"},
    {"cn": "为了一个更美好的世界而奋斗。", "en": "Strive for a better world.", "author": "孙中山", "category": "家国情怀", "source": "curated"},
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
counts = {}
for cat in distinct:
    counts[cat] = db.quotes.count_documents({"category": cat})

print(f"✅ 新增 {count} 条格言")
print(f"📊 总格言数: {total}")
print(f"📂 各分类:")
for cat, cnt in sorted(counts.items()):
    print(f"   {cat}: {cnt} 条")

client.close()
