"""
种⼦脚本：插⼊初始冷笑话到 MongoDB
"""

import sys
import os

# 确保可以导⼊项⽬模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jokes import add_jokes_batch

JOKES = [
    # ===== 程序员笑话 =====
    {
        "joke_cn": "为什么程序员分不清万圣节和圣诞节？",
        "punchline_cn": "因为 Oct 31 == Dec 25",
        "joke_en": "Why do programmers confuse Halloween and Christmas?",
        "punchline_en": "Because Oct 31 == Dec 25",
        "category": "程序员笑话",
    },
    {
        "joke_cn": "程序员最怕什么？",
        "punchline_cn": "怕自己写的代码被别人review",
        "joke_en": "What are programmers most afraid of?",
        "punchline_en": "Having their own code reviewed by others",
        "category": "程序员笑话",
    },
    {
        "joke_cn": "为什么 Python 程序员不喜欢蚊子？",
        "punchline_cn": "因为蚊子会 bite (字节)",
        "category": "程序员笑话",
    },
    {
        "joke_cn": "程序员 A：我昨天写了 1000 ⾏代码。\n程序员 B：我也是，不过我修了 500 ⾏ bug。\n程序员 A：那你还剩 500 ⾏？\n程序员 B：不，原来有 1000 ⾏ bug。",
        "punchline_cn": "修不完的 bug，写不完的坑",
        "category": "程序员笑话",
    },
    {
        "joke_cn": "为什么程序员总是在冰箱⾥放很多饮料？",
        "punchline_cn": "因为他们需要频繁地 refresh",
        "joke_en": "Why do programmers keep lots of drinks in the fridge?",
        "punchline_en": "Because they need to refresh frequently",
        "category": "程序员笑话",
    },
    {
        "joke_cn": "怎么区分⼀个好的程序员和⼀个差的程序员？",
        "punchline_cn": "好的程序员说：这个功能我⼩时能写完。差的程序员说：这个功能我⼩时就能写完。",
        "category": "程序员笑话",
    },
    {
        "joke_cn": "为什么 Java 程序员必须戴眼镜？",
        "punchline_cn": "因为他们不戴眼镜就看不清 C#",
        "joke_en": "Why must Java programmers wear glasses?",
        "punchline_en": "Because they can't see C# without them",
        "category": "程序员笑话",
    },
    {
        "joke_cn": "Git 和女朋友有什么共同点？",
        "punchline_cn": "你永远不知道什么时候会冲突",
        "category": "程序员笑话",
    },
    {
        "joke_cn": "什么东西越洗越脏？",
        "punchline_cn": "代码。重构前还跑得好好的，重构完全炸了。",
        "category": "程序员笑话",
    },
    {
        "joke_cn": "为什么程序员在⽣死攸关的时候不会求救？",
        "punchline_cn": "因为他们满脑⼦都是：SOS... 哦不对，是 O(n!)",
        "category": "程序员笑话",
    },

    # ===== 冷笑话 =====
    {
        "joke_cn": "有⼀天，⾯包⾛在路上，突然觉得饿了。",
        "punchline_cn": "于是它把⾃⼰吃了。",
        "category": "冷笑话",
    },
    {
        "joke_cn": "有⼀个⾲菜⾖腐馅的包⼦⾛在路上，突然觉得⾃⼰不好吃。",
        "punchline_cn": "于是它变成了⾲菜馅⼉。",
        "category": "冷笑话",
    },
    {
        "joke_cn": "孙悟空为什么⽆法通过⼿机进⾏视频通话？",
        "punchline_cn": "因为他没有 72 change",
        "category": "冷笑话",
    },
    {
        "joke_cn": "鲨⻥吃了⼀块绿⾖糕。",
        "punchline_cn": "结果变成了绿⾖沙。",
        "category": "冷笑话",
    },
    {
        "joke_cn": "什么帽⼦不能戴？",
        "punchline_cn": "螺丝帽。",
        "category": "冷笑话",
    },
    {
        "joke_cn": "什么球不能踢？",
        "punchline_cn": "⾦⾥球（眼⾥的⾦⾥球）。",
        "category": "冷笑话",
    },
    {
        "joke_cn": "什么⽔不能喝？",
        "punchline_cn": "薪⽔。",
        "category": "冷笑话",
    },
    {
        "joke_cn": "小明的妈妈有三个儿子，⼤⼉⼦叫⼤⽑，⼆⼉⼦叫⼆⽑。",
        "punchline_cn": "三⼉⼦叫什么？答：叫⼩明。",
        "category": "冷笑话",
    },
    {
        "joke_cn": "有⼀个鸡蛋去茶馆喝茶，结果它变成了什么？",
        "punchline_cn": "茶⽐蛋。",
        "category": "冷笑话",
    },
    {
        "joke_cn": "什么东⻄你越给它⽔喝它越渴？",
        "punchline_cn": "⽕。",
        "category": "冷笑话",
    },

    # ===== 谐⾳梗 =====
    {
        "joke_cn": "什么⽔果⼿机最畅销？",
        "punchline_cn": "苹果（Apple）。",
        "category": "谐⾳梗",
    },
    {
        "joke_cn": "什么花最会照顾⾃⼰？",
        "punchline_cn": "茉莉花 —— 莫离花（别离开我）。",
        "category": "谐⾳梗",
    },
    {
        "joke_cn": "为什么数学书特别忧郁？",
        "punchline_cn": "因为它有太多问题（problems）。",
        "category": "谐⾳梗",
    },
    {
        "joke_cn": "哪个城市最懂⾳乐？",
        "punchline_cn": "宁波（宁 拨）。",
        "category": "谐⾳梗",
    },
    {
        "joke_cn": "什么糖果不甜？",
        "punchline_cn": "⽩糖（⽩躺）—— 躺平了当然不甜。",
        "category": "谐⾳梗",
    },
    {
        "joke_cn": "什么⻥最聪明？",
        "punchline_cn": "鲸⻥ —— 因为它有＂鲸＂（惊）⼈的智慧。",
        "category": "谐⾳梗",
    },
    {
        "joke_cn": "什么⻔永远关不上？",
        "punchline_cn": "⼤⻔（达⻔）—— 叶问⾥的⻔派关不上。",
        "category": "谐⾳梗",
    },
    {
        "joke_cn": "为什么⼿机不能睡觉？",
        "punchline_cn": "因为它有太多未接来电（未接，即未接觉）。",
        "category": "谐⾳梗",
    },

    # ===== 动物笑话 =====
    {
        "joke_cn": "为什么企鹅的肚⼦是⽩⾊的？",
        "punchline_cn": "因为如果它的⼿不够⻓，就洗不到⾃⼰的肚⼦。",
        "category": "动物笑话",
    },
    {
        "joke_cn": "⼀只猫从⼗层楼跳下来，然后呢？",
        "punchline_cn": "它到⼆⼗层了。",
        "category": "动物笑话",
    },
    {
        "joke_cn": "为什么袋⿏⽆法减肥？",
        "punchline_cn": "因为它每天都要把孩⼦装在⼝袋⾥跑来跑去，结果练出了袋⿏肌。",
        "category": "动物笑话",
    },
    {
        "joke_cn": "鱼为什么不能在陆地上⽣活？",
        "punchline_cn": "因为地上有猫。",
        "category": "动物笑话",
    },
    {
        "joke_cn": "什么动物最⽼实？",
        "punchline_cn": "⽜，因为⽜（扭）扭捏捏的反义词是⼤⽅，⽜不⼤⽅。",
        "category": "动物笑话",
    },

    # ===== ⽣活段⼦ =====
    {
        "joke_cn": "减肥最有效的⽅法是什 么？",
        "punchline_cn": "把⾃⼰的照⽚贴在冰箱上，然后每天看着它吃。",
        "category": "⽣活段⼦",
    },
    {
        "joke_cn": "为什么现在的年轻⼈不喜欢喝⽜奶？",
        "punchline_cn": "因为⼩时候喝太多，现在看到⽜就想逃（脱敏）。",
        "category": "⽣活段⼦",
    },
    {
        "joke_cn": "今天去银⾏取钱，柜员说：先⽣你要取多少？",
        "punchline_cn": "我说：全部。然后她看了我⼀眼，说：先⽣，你卡⾥只有 3 块 5。",
        "category": "⽣活段⼦",
    },
    {
        "joke_cn": "为什么现在的闹钟越来越不靠谱？",
        "punchline_cn": "因为闹钟响的时候，你总能把⾃⼰说服：再睡五分钟。",
        "category": "⽣活段⼦",
    },
    {
        "joke_cn": "我给我妈买了⼀个⼿机，告诉她字体可以调⼤。",
        "punchline_cn": "第⼆天她说：我把字体调到最⼤了，为什么还是看不到你的消息？原来她还没打开微信。",
        "category": "⽣活段⼦",
    },

    # ===== 校园笑话 =====
    {
        "joke_cn": "⽼师问：谁能说出＂⼀石⼆鸟＂这个成语的典故？",
        "punchline_cn": "⼩明说：古代有⼀个⼈拿⽯头砸了⼀下，结果两只⻦都死了。这个故事的教训是：不要乱扔⽯头。",
        "category": "校园笑话",
    },
    {
        "joke_cn": "数学考试时，⼩明在看⼩抄被抓住了。",
        "punchline_cn": "⽼师：你为什么要作弊？⼩明：因为这题太复杂了，我想看看答案是不是和我想的⼀样。",
        "category": "校园笑话",
    },
    {
        "joke_cn": "为什么学⽣上课总是很困？",
        "punchline_cn": "因为知识是⽆价的，所以⽼师给的都是免费的——免费的东西⼤家都不珍惜。",
        "category": "校园笑话",
    },
    {
        "joke_cn": "物理课上，⽼师问：为什么打雷时我们先看到闪电后听到雷声？",
        "punchline_cn": "⼩明答：因为眼睛在⽿朵前⾯。",
        "category": "校园笑话",
    },

    # ===== 职场幽默 =====
    {
        "joke_cn": "上班最幸福的三个字是什么？",
        "punchline_cn": "不是＂我爱你＂，是＂下班了＂。",
        "category": "职场幽默",
    },
    {
        "joke_cn": "⼀个同事请假说：⽼板，我明天要去医院看⼼脏。",
        "punchline_cn": "⽼板问：你⼼脏怎么了？同事说：因为我听到项⽬上线时间提前了。",
        "category": "职场幽默",
    },
    {
        "joke_cn": "为什么周⼀总是感觉最⻓？",
        "punchline_cn": "因为从周⼀到周五的距离是⼀个光年。",
        "category": "职场幽默",
    },
    {
        "joke_cn": "⾯试官：你⼯作五年的经验总结是什么？",
        "punchline_cn": "我：只要不尴尬，尴尬的就是别⼈。尤其是开会的时候。",
        "category": "职场幽默",
    },
]


def main():
    result = add_jokes_batch(JOKES)
    print(f"✅ 插⼊完成：成功 {result['success']} 条，失败 {result['failed']} 条")
    print(f"📊 当前笑话总数：{sum(1 for _ in JOKES)}")


if __name__ == "__main__":
    main()
