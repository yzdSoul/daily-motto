#!/usr/bin/env python3
"""
批量添加80条格言到MongoDB
每个分类8条，共10个分类
"""
from quotes import add_quote, get_all_categories_with_counts, get_quote_count

# 80条新格言数据（每个分类8条）
new_quotes = [
    # ========== 哲理智慧 (8条) ==========
    {"cn": "未经审视的人生不值得过。", "en": "The unexamined life is not worth living.", "author": "苏格拉底", "category": "哲理智慧"},
    {"cn": "人生而自由，却无往不在枷锁之中。", "en": "Man is born free, and everywhere he is in chains.", "author": "卢梭", "category": "哲理智慧"},
    {"cn": "万物皆有裂痕，那是光照进来的地方。", "en": "There is a crack in everything, that's how the light gets in.", "author": "莱昂纳德·科恩", "category": "哲理智慧"},
    {"cn": "知人者智，自知者明。", "en": "Knowing others is wisdom; knowing yourself is enlightenment.", "author": "老子", "category": "哲理智慧"},
    {"cn": "我们听到的一切都是一个观点，不是事实；我们看见的一切都是一个视角，不是真相。", "en": "Everything we hear is an opinion, not a fact. Everything we see is a perspective, not the truth.", "author": "马可·奥勒留", "category": "哲理智慧"},
    {"cn": "存在先于本质。", "en": "Existence precedes essence.", "author": "萨特", "category": "哲理智慧"},
    {"cn": "道可道，非常道；名可名，非常名。", "en": "The Tao that can be told is not the eternal Tao. The name that can be named is not the eternal name.", "author": "老子", "category": "哲理智慧"},
    {"cn": "幸福是把灵魂安放在最适当的位置。", "en": "Happiness is the settling of the soul into its most appropriate place.", "author": "亚里士多德", "category": "哲理智慧"},

    # ========== 励志奋斗 (8条) ==========
    {"cn": "天才是百分之一的灵感加上百分之九十九的汗水。", "en": "Genius is one percent inspiration and ninety-nine percent perspiration.", "author": "爱迪生", "category": "励志奋斗"},
    {"cn": "冬天来了，春天还会远吗？", "en": "If winter comes, can spring be far behind?", "author": "雪莱", "category": "励志奋斗"},
    {"cn": "生活就像海洋，只有意志坚强的人，才能到达彼岸。", "en": "Life is like the ocean; only those with strong wills can reach the other shore.", "author": "马克思", "category": "励志奋斗"},
    {"cn": "即使跌倒一百次，也要一百零一次地站起来。", "en": "Even if you fall down a hundred times, you must rise a hundred and one times.", "author": "张海迪", "category": "励志奋斗"},
    {"cn": "不要问国家能为你做什么，而要问你能为国家做什么。", "en": "Ask not what your country can do for you; ask what you can do for your country.", "author": "肯尼迪", "category": "励志奋斗"},
    {"cn": "一个人的命运，当然要靠自我奋斗，但也要考虑历史的进程。", "en": "A person's destiny depends on both self-struggle and the course of history.", "author": "佚名", "category": "励志奋斗"},
    {"cn": "既然选择了远方，便只顾风雨兼程。", "en": "Having chosen the distant horizon, I will brave wind and rain all the way.", "author": "汪国真", "category": "励志奋斗"},
    {"cn": "世界上只有一种真正的英雄主义，那就是认清生活的真相后依然热爱生活。", "en": "There is only one true heroism in the world: to see the world as it is and to love it.", "author": "罗曼·罗兰", "category": "励志奋斗"},

    # ========== 人生态度 (8条) ==========
    {"cn": "不以物喜，不以己悲。", "en": "Not pleased by external gains, not saddened by personal losses.", "author": "范仲淹", "category": "人生态度"},
    {"cn": "人生如逆旅，我亦是行人。", "en": "Life is but a journey against the current; I too am but a traveler.", "author": "苏轼", "category": "人生态度"},
    {"cn": "宠辱不惊，看庭前花开花落；去留无意，望天上云卷云舒。", "en": "Unmoved by honor or disgrace, I watch flowers bloom and fall; unconcerned by staying or leaving, I watch clouds gather and scatter.", "author": "洪应明", "category": "人生态度"},
    {"cn": "我们终此一生，就是要摆脱他人的期待，找到真正的自己。", "en": "We spend our whole lives trying to escape the expectations of others, to find our true selves.", "author": "伍绮诗", "category": "人生态度"},
    {"cn": "你若爱，生活哪里都可爱；你若恨，生活哪里都可恨。", "en": "If you love, life is lovable everywhere; if you hate, life is hateful everywhere.", "author": "丰子恺", "category": "人生态度"},
    {"cn": "生命不是要活得长久，而是要活得精彩。", "en": "Life is not about living long, but about living brilliantly.", "author": "塞内卡", "category": "人生态度"},
    {"cn": "且将新火试新茶，诗酒趁年华。", "en": "Let's try new tea with fresh fire; enjoy poetry and wine while youth lasts.", "author": "苏轼", "category": "人生态度"},
    {"cn": "真正的平静，不是避开车马喧嚣，而是在心中修篱种菊。", "en": "True peace is not avoiding the noise of the world, but planting chrysanthemums in the garden of your heart.", "author": "林徽因", "category": "人生态度"},

    # ========== 读书学习 (8条) ==========
    {"cn": "博学之，审问之，慎思之，明辨之，笃行之。", "en": "Learn extensively, inquire accurately, think carefully, discriminate clearly, and practice devotedly.", "author": "《礼记》", "category": "读书学习"},
    {"cn": "我扑在书上，就像饥饿的人扑在面包上。", "en": "I throw myself upon books as a hungry man throws himself upon bread.", "author": "高尔基", "category": "读书学习"},
    {"cn": "书籍是人类进步的阶梯。", "en": "Books are the ladder of human progress.", "author": "高尔基", "category": "读书学习"},
    {"cn": "学而不思则罔，思而不学则殆。", "en": "Learning without thought is labor lost; thought without learning is perilous.", "author": "孔子", "category": "读书学习"},
    {"cn": "读书之法，在循序而渐进，熟读而精思。", "en": "The method of reading lies in proceeding step by step, reading thoroughly and thinking deeply.", "author": "朱熹", "category": "读书学习"},
    {"cn": "吾生也有涯，而知也无涯。", "en": "My life has its limits, but knowledge is boundless.", "author": "庄子", "category": "读书学习"},
    {"cn": "纸上得来终觉浅，绝知此事要躬行。", "en": "Knowledge from books is superficial after all; to truly understand, one must practice.", "author": "陆游", "category": "读书学习"},
    {"cn": "读书不是为了雄辩和驳斥，也不是为了轻信和盲从，而是为了思考和权衡。", "en": "Reading is not for argumentation and refutation, nor for blind belief, but for thinking and weighing.", "author": "培根", "category": "读书学习"},

    # ========== 英文智慧 (8条) ==========
    {"cn": "知识就是力量。", "en": "Knowledge is power.", "author": "培根", "category": "英文智慧"},
    {"cn": "生命诚可贵，爱情价更高；若为自由故，二者皆可抛。", "en": "Life is dear, love is dearer; both can be given up for freedom.", "author": "裴多菲", "category": "英文智慧"},
    {"cn": "生存还是毁灭，这是一个问题。", "en": "To be, or not to be, that is the question.", "author": "莎士比亚", "category": "英文智慧"},
    {"cn": "幸福的家庭都是相似的，不幸的家庭各有各的不幸。", "en": "Happy families are all alike; every unhappy family is unhappy in its own way.", "author": "列夫·托尔斯泰", "category": "英文智慧"},
    {"cn": "黑夜给了我黑色的眼睛，我却用它寻找光明。", "en": "The night gave me dark eyes, yet I use them to seek the light.", "author": "顾城", "category": "英文智慧"},
    {"cn": "人是一根有思想的芦苇。", "en": "Man is but a reed, the weakest in nature, but he is a thinking reed.", "author": "帕斯卡", "category": "英文智慧"},
    {"cn": "我不同意你的观点，但我誓死捍卫你说话的权利。", "en": "I disapprove of what you say, but I will defend to the death your right to say it.", "author": "伏尔泰", "category": "英文智慧"},
    {"cn": "给岁月以文明，而不是给文明以岁月。", "en": "Give time to civilization, not civilization to time.", "author": "刘慈欣", "category": "英文智慧"},

    # ========== 爱情友谊 (8条) ==========
    {"cn": "愿得一心人，白头不相离。", "en": "I wish to find one true heart, and never part until our hair turns white.", "author": "卓文君", "category": "爱情友谊"},
    {"cn": "曾经沧海难为水，除却巫山不是云。", "en": "Having seen the ocean, other waters seem bland; having seen the clouds of Wu, others are not clouds.", "author": "元稹", "category": "爱情友谊"},
    {"cn": "身无彩凤双飞翼，心有灵犀一点通。", "en": "Though we lack the wings of colorful phoenixes to fly side by side, our hearts are connected as if by a single thread.", "author": "李商隐", "category": "爱情友谊"},
    {"cn": "爱情不是占有，而是欣赏。", "en": "Love is not about possession; it is about appreciation.", "author": "泰戈尔", "category": "爱情友谊"},
    {"cn": "友谊是两颗心真诚相待，而不是一颗心对另一颗心的敲打。", "en": "Friendship is two hearts treating each other sincerely, not one heart beating upon another.", "author": "鲁迅", "category": "爱情友谊"},
    {"cn": "爱是恒久忍耐，又有恩慈。", "en": "Love is patient, love is kind.", "author": "《圣经》", "category": "爱情友谊"},
    {"cn": "人生得一知己足矣，斯世当以同怀视之。", "en": "To have one true friend in life is enough; in this world, treat him as a kindred spirit.", "author": "鲁迅", "category": "爱情友谊"},
    {"cn": "最好的爱情，是两个人一起变得更好。", "en": "The best love is when two people become better together.", "author": "佚名", "category": "爱情友谊"},

    # ========== 时间光阴 (8条) ==========
    {"cn": "少壮不努力，老大徒伤悲。", "en": "If one does not work hard in youth, one will regret it in old age.", "author": "《长歌行》", "category": "时间光阴"},
    {"cn": "逝者如斯夫，不舍昼夜。", "en": "Time passes like this river, flowing day and night without cease.", "author": "孔子", "category": "时间光阴"},
    {"cn": "一寸光阴一寸金，寸金难买寸光阴。", "en": "An inch of time is worth an inch of gold, yet an inch of gold cannot buy an inch of time.", "author": "《增广贤文》", "category": "时间光阴"},
    {"cn": "你热爱生命吗？那么别浪费时间，因为时间是组成生命的材料。", "en": "Do you love life? Then do not squander time, for that is the stuff life is made of.", "author": "富兰克林", "category": "时间光阴"},
    {"cn": "盛年不重来，一日难再晨。", "en": "Prime years do not return; a day does not have two dawns.", "author": "陶渊明", "category": "时间光阴"},
    {"cn": "时间就像海绵里的水，只要愿挤，总还是有的。", "en": "Time is like water in a sponge; if you are willing to squeeze, there is always some.", "author": "鲁迅", "category": "时间光阴"},
    {"cn": "明日复明日，明日何其多。我生待明日，万事成蹉跎。", "en": "Tomorrow after tomorrow, how many tomorrows there are. If I wait for tomorrow, all things will come to naught.", "author": "钱福", "category": "时间光阴"},
    {"cn": "岁月不居，时节如流。", "en": "Years do not stay; seasons flow like water.", "author": "孔融", "category": "时间光阴"},

    # ========== 自然万物 (8条) ==========
    {"cn": "天地有大美而不言。", "en": "Heaven and earth possess great beauty without speaking.", "author": "庄子", "category": "自然万物"},
    {"cn": "采菊东篱下，悠然见南山。", "en": "Picking chrysanthemums by the eastern fence, leisurely I see the southern mountain.", "author": "陶渊明", "category": "自然万物"},
    {"cn": "落霞与孤鹜齐飞，秋水共长天一色。", "en": "Rosy clouds and a lone wild duck fly together; autumn waters merge with the boundless sky in one hue.", "author": "王勃", "category": "自然万物"},
    {"cn": "大自然从不欺骗我们；欺骗我们的永远是我们自己。", "en": "Nature never deceives us; it is always we who deceive ourselves.", "author": "卢梭", "category": "自然万物"},
    {"cn": "一花一世界，一叶一菩提。", "en": "One flower is a world; one leaf is a bodhi.", "author": "佛经", "category": "自然万物"},
    {"cn": "明月松间照，清泉石上流。", "en": "Bright moonlight shines among the pines; clear spring water flows over the stones.", "author": "王维", "category": "自然万物"},
    {"cn": "山重水复疑无路，柳暗花明又一村。", "en": "Mountains multiply and streams double back, I doubt there's a road ahead; willows dark and flowers bright, another village appears.", "author": "陆游", "category": "自然万物"},
    {"cn": "大自然是善良的慈母，也是冷酷的屠夫。", "en": "Nature is a kind mother, but also a cruel butcher.", "author": "雨果", "category": "自然万物"},

    # ========== 处世之道 (8条) ==========
    {"cn": "己所不欲，勿施于人。", "en": "Do not do to others what you do not want done to yourself.", "author": "孔子", "category": "处世之道"},
    {"cn": "君子和而不同，小人同而不和。", "en": "The noble man is harmonious but not conforming; the petty man is conforming but not harmonious.", "author": "孔子", "category": "处世之道"},
    {"cn": "水至清则无鱼，人至察则无徒。", "en": "When water is too clear, there are no fish; when a man is too scrutinizing, he has no followers.", "author": "《汉书》", "category": "处世之道"},
    {"cn": "静坐常思己过，闲谈莫论人非。", "en": "In silence, often reflect on your own faults; in idle talk, do not discuss others' shortcomings.", "author": "《格言联璧》", "category": "处世之道"},
    {"cn": "良药苦口利于病，忠言逆耳利于行。", "en": "Good medicine tastes bitter but cures illness; faithful words offend the ear but benefit conduct.", "author": "《史记》", "category": "处世之道"},
    {"cn": "海纳百川，有容乃大；壁立千仞，无欲则刚。", "en": "The sea accepts all rivers, greatness lies in its capacity; a cliff stands a thousand feet high, strength lies in its lack of desire.", "author": "林则徐", "category": "处世之道"},
    {"cn": "勿以恶小而为之，勿以善小而不为。", "en": "Do not commit evil because it is small; do not neglect good because it is small.", "author": "刘备", "category": "处世之道"},
    {"cn": "大智若愚，大巧若拙。", "en": "Great wisdom appears foolish; great skill appears clumsy.", "author": "老子", "category": "处世之道"},

    # ========== 家国情怀 (8条) ==========
    {"cn": "苟利国家生死以，岂因祸福避趋之。", "en": "If it benefits the country, I will risk my life; how could I avoid it for personal fortune or misfortune?", "author": "林则徐", "category": "家国情怀"},
    {"cn": "人生自古谁无死，留取丹心照汗青。", "en": "Since ancient times, who has lived forever? Leave a loyal heart to illuminate the annals of history.", "author": "文天祥", "category": "家国情怀"},
    {"cn": "为中华之崛起而读书。", "en": "Study for the rise of China.", "author": "周恩来", "category": "家国情怀"},
    {"cn": "天下兴亡，匹夫有责。", "en": "The rise and fall of the nation is the responsibility of every common man.", "author": "顾炎武", "category": "家国情怀"},
    {"cn": "为什么我的眼里常含泪水？因为我对这土地爱得深沉。", "en": "Why are there always tears in my eyes? Because I love this land so deeply.", "author": "艾青", "category": "家国情怀"},
    {"cn": "位卑未敢忘忧国。", "en": "Though humble in position, I dare not forget to worry about the country.", "author": "陆游", "category": "家国情怀"},
    {"cn": "捐躯赴国难，视死忽如归。", "en": "Giving one's life for the country's crisis, treating death as if returning home.", "author": "曹植", "category": "家国情怀"},
    {"cn": "先天下之忧而忧，后天下之乐而乐。", "en": "Be the first to worry about the world's troubles, and the last to enjoy its pleasures.", "author": "范仲淹", "category": "家国情怀"},
]


def check_exists(cn):
    """检查中文内容是否已存在"""
    from quotes import QUOTES_COL
    return QUOTES_COL.find_one({"cn": cn}) is not None


def main():
    print("=" * 60)
    print("开始批量添加80条格言")
    print("=" * 60)

    # 先检查是否有重复
    existing_count = 0
    unique_quotes = []
    for q in new_quotes:
        if check_exists(q["cn"]):
            print(f"[跳过] 已存在: {q['cn'][:30]}...")
            existing_count += 1
        else:
            unique_quotes.append(q)

    print(f"\n待添加: {len(unique_quotes)} 条, 已存在跳过: {existing_count} 条")
    print("-" * 60)

    success = 0
    failed = 0
    failed_items = []

    for i, q in enumerate(unique_quotes, 1):
        result = add_quote(q["cn"], q["en"], q["author"], q["category"], source="curated")
        if result["success"]:
            success += 1
            print(f"[{i}/{len(unique_quotes)}] ✓ {q['category']} | {q['cn'][:30]}...")
        else:
            failed += 1
            failed_items.append((q, result.get("error", "未知错误")))
            print(f"[{i}/{len(unique_quotes)}] ✗ {q['category']} | {q['cn'][:30]}... | 错误: {result.get('error', '')}")

    print("\n" + "=" * 60)
    print("添加结果统计")
    print("=" * 60)
    print(f"成功: {success} 条")
    print(f"失败: {failed} 条")
    print(f"跳过(已存在): {existing_count} 条")

    if failed_items:
        print("\n失败明细:")
        for q, err in failed_items:
            print(f"  - {q['cn'][:40]}... | 错误: {err}")

    # 统计各分类数量
    print("\n" + "=" * 60)
    print("各分类最终数量")
    print("=" * 60)
    counts = get_all_categories_with_counts()
    total = 0
    for cat in ["哲理智慧", "励志奋斗", "人生态度", "读书学习", "英文智慧",
                "爱情友谊", "时间光阴", "自然万物", "处世之道", "家国情怀"]:
        count = counts.get(cat, 0)
        total += count
        print(f"  {cat}: {count} 条")
    print(f"\n总计: {total} 条")

    # 对比添加前后
    print("\n" + "=" * 60)
    print("添加前后对比")
    print("=" * 60)
    before = 120
    after = get_quote_count()
    print(f"添加前: {before} 条")
    print(f"添加后: {after} 条")
    print(f"净增加: {after - before} 条")


if __name__ == "__main__":
    main()
