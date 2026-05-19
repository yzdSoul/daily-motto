"""
批量补充冷笑话脚本
"""
import sys
sys.path.insert(0, '/home/ubuntu/projects/daily-motto-web')
from jokes import add_jokes_batch

NEW_JOKES = [
    # ===== 谐音梗 =====
    {'joke_cn': '什么布不能做衣服？', 'punchline_cn': '瀑布，因为是瀑布（布）。', 'category': '谐音梗'},
    {'joke_cn': '什么鬼最受欢迎？', 'punchline_cn': '酒鬼，因为大家都喜欢和他干杯。', 'category': '谐音梗'},
    {'joke_cn': '什么河不能游泳？', 'punchline_cn': '银河，游不动。', 'category': '谐音梗'},
    {'joke_cn': '什么书最香？', 'punchline_cn': '菜谱，因为书（蔬）香。', 'category': '谐音梗'},
    {'joke_cn': '什么剑最锋利？', 'punchline_cn': '保健（宝剑），健康最重要。', 'category': '谐音梗'},
    {'joke_cn': '什么蛋不能吃？', 'punchline_cn': '零蛋，考试得零分的那个。', 'category': '谐音梗'},

    # ===== 动物笑话 =====
    {'joke_cn': '小白兔和长颈鹿一起散步。长颈鹿说：你看前面的森林多美！小白兔说：你脖子那么长当然看得见，我看到的全是草！', 'punchline_cn': '这就是传说中的站得高看得远。', 'category': '动物笑话'},
    {'joke_cn': '蚂蚁迷路了，问大象：能帮我指路吗？', 'punchline_cn': '大象说：你踩到我脚了。蚂蚁说：那你帮我看看前面是什么路？大象说：你先从我脚上下来。', 'category': '动物笑话'},
    {'joke_cn': '蜗牛和小狗赛跑，蜗牛输了。', 'punchline_cn': '蜗牛不服气：你作弊！你用四条腿，我才用一条！小狗说：那你觉得我用哪条腿才算公平？', 'category': '动物笑话'},
    {'joke_cn': '为什么苍蝇对它的孩子特别严格？', 'punchline_cn': '因为它不想让它们变成小废蝇。', 'category': '动物笑话'},
    {'joke_cn': '章鱼考试为什么总是全对？', 'punchline_cn': '因为它有八只手，可以同时翻八本书。', 'category': '动物笑话'},

    # ===== 生活段子 =====
    {'joke_cn': '去理发店剪头发，理发师问：想剪什么样的？', 'punchline_cn': '我说：剪完让我看起来像没剪过一样。他看了我一眼：那我不剪行不行？', 'category': '生活段子'},
    {'joke_cn': '女朋友问我：如果我和你的游戏同时掉水里，你先救谁？', 'punchline_cn': '我说：游戏可以重开，你不行。她感动了两秒，我补充道：但你也会游泳啊。', 'category': '生活段子'},
    {'joke_cn': '今天在电梯里放了一个屁，特别响。', 'punchline_cn': '旁边的大叔淡定地说：小伙子，你这个手机通知音挺有节奏感的。', 'category': '生活段子'},
    {'joke_cn': '打开外卖App犹豫了20分钟。', 'punchline_cn': '最后选了一家，不是因为好吃，而是满减算下来最划算。结果吃完发现省的钱不够买胃药。', 'category': '生活段子'},
    {'joke_cn': '去超市买水，看到一瓶矿泉水一瓶饮用水。', 'punchline_cn': '我问售货员区别，她说：矿泉水喝完上厕所用矿泉水瓶，饮用水用水龙头。我说：那我买矿泉水。', 'category': '生活段子'},

    # ===== 校园笑话 =====
    {'joke_cn': '老师说：小明，说说津津有味是什么意思？', 'punchline_cn': '小明：就是吃饭很有味道。老师：反义词呢？小明：干干没味。', 'category': '校园笑话'},
    {'joke_cn': '老师问：世界上先有鸡还是先有蛋？', 'punchline_cn': '小明抢答：先有鸡！老师：那鸡哪来的？小明：老师，这是个鸡生蛋蛋生鸡的问题。全班沉默。', 'category': '校园笑话'},
    {'joke_cn': '考试前小明在拜孔子像。同学问：有用吗？', 'punchline_cn': '小明：万一孔子把答案塞我脑子里呢？同学：那你怎么不直接塞课本？小明：课本太硬了。', 'category': '校园笑话'},
    {'joke_cn': '自习课小明一直玩手机。', 'punchline_cn': '班长说：再玩我就告诉老师。小明淡定：我已经把老师朋友圈屏蔽了。班长：……不是这个意思。', 'category': '校园笑话'},
    {'joke_cn': '英语课老师问：teach的过去式是什么？', 'punchline_cn': '小明：taught。老师：buy呢？小明：bought。老师：think呢？小明心想这也太好猜了：thought。', 'category': '校园笑话'},
    {'joke_cn': '化学老师问：什么能溶解几乎所有物质？', 'punchline_cn': '小明：钱！有钱能使鬼推磨。老师说：你出去站着。', 'category': '校园笑话'},

    # ===== 职场幽默 =====
    {'joke_cn': '面试官：你对我们公司有什么了解？', 'punchline_cn': '我：我刚搜了五分钟，大概知道你们不包吃住。', 'category': '职场幽默'},
    {'joke_cn': '同事请病假三天回来。', 'punchline_cn': '我们问他怎么了，他说：参加了一个三天的高效工作培训班，结果累病了。', 'category': '职场幽默'},
    {'joke_cn': '老板群里发：明天团建，大家有什么建议？', 'punchline_cn': '全群安静半小时。最后一人回：建议取消。然后秒撤回。老板说：我看到了。', 'category': '职场幽默'},
    {'joke_cn': '新同事问老员工：加班有加班费吗？', 'punchline_cn': '老员工：有啊，加了班费。新人：班费是什么？老员工：我也不知道，但老板说听起来比加班费好听。', 'category': '职场幽默'},
    {'joke_cn': '为什么周一总是特别累？', 'punchline_cn': '因为周一把你上周五攒的那点快乐，在早上九点就全消耗完了。', 'category': '职场幽默'},
    {'joke_cn': '领导说：我们不提倡加班，希望大家按时下班。', 'punchline_cn': '然后他把会议安排在了17:55。', 'category': '职场幽默'},

    # ===== 奇葩问答 =====
    {'joke_cn': '问：如果把冰箱里的灯拆了，冰箱还会制冷吗？', 'punchline_cn': '答：会。但它会害怕。', 'category': '奇葩问答'},
    {'joke_cn': '问：如果贾宝玉娶了林黛玉，孩子叫什么？', 'punchline_cn': '答：宝黛洗发水的宝黛。', 'category': '奇葩问答'},
    {'joke_cn': '问：上厕所为什么要关门？', 'punchline_cn': '答：因为门开着的话，马桶会害羞。', 'category': '奇葩问答'},
    {'joke_cn': '问：为什么孙悟空不用支付宝？', 'punchline_cn': '答：因为他有72变，不需要变来付钱。', 'category': '奇葩问答'},
    {'joke_cn': '问：为什么蚊子从不咬自己？', 'punchline_cn': '答：因为它没有手，挠不了痒。', 'category': '奇葩问答'},
    {'joke_cn': '问：键盘为什么不按ABCD排列？', 'punchline_cn': '答：因为如果按顺序排，你打字的时候会忍不住读出来。', 'category': '奇葩问答'},
    {'joke_cn': '问：为什么镜子里的字是反的？', 'punchline_cn': '答：因为镜子不识字。', 'category': '奇葩问答'},
    {'joke_cn': '问：为什么胖的人容易饿？', 'punchline_cn': '答：因为胃离嘴比较近，闻到香味更快。', 'category': '奇葩问答'},
    {'joke_cn': '问：为什么打电话要说喂？', 'punchline_cn': '答：因为你不可能说吃了吗。', 'category': '奇葩问答'},
    {'joke_cn': '问：向日葵阴天的时候在干嘛？', 'punchline_cn': '答：在等太阳发朋友圈。', 'category': '奇葩问答'},
]

result = add_jokes_batch(NEW_JOKES)
print(f'新增 {result["success"]} 条，失败 {result["failed"]} 条')

from jokes import get_joke_count, get_all_jokes
from collections import Counter
jokes = get_all_jokes()
cats = Counter(j['category'] for j in jokes)
print()
print('各分类最终数量：')
for cat in ['程序员笑话', '冷笑话', '谐音梗', '动物笑话', '生活段子', '校园笑话', '职场幽默', '奇葩问答']:
    n = cats.get(cat, 0)
    bar = '\u2588' * (n // 2) + '\u2591' * max(0, 10 - n // 2)
    print(f'  {cat:<8} {n:>2}条 {bar}')
print(f'\n总计: {get_joke_count()} 条')
