#!/usr/bin/env python3
"""作业榜的动态内容（点点总结 + 评论区）。
改这里的数据，再运行 `python3 tools/build-content.py`，会同时生成：
  - docs/dynamic-content.md   给人读的内容稿
  - assets/content.js         原型（homework-board.html）读取的数据
文案里的 **粗体** 会在点点总结里渲染成红色高亮词。
"""
import json, os, re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
AUTHOR = {'name': '曼食慢语', 'avatar': 'assets/video/avatar.jpg'}   # 视频作者（评论里带「作者」标）

# 头像与昵称不对应，按出现顺序分配（头像见 assets/avatars/）
AVATAR = {n: f'assets/avatars/avatar-{i:02d}.png' for i, n in enumerate(
    ['马vv', '曼食慢语', 'Neil', '罐罐儿', '露洁', '财正', 'Ada', 'Kiki', '欢欢', '斯淇',
     '三三姐', 'HY', '星星', 'Molly', 'ian', '金灵', '小星星', '芯芯向荣', 'CCC', '東方神韵'], 1)}
AVATAR['曼食慢语'] = AUTHOR['avatar']
AVATAR['辣妹子很怕拉'] = 'assets/components/comment-avatar-1.png'   # 原稿评论，保留


def u(name, text, date, loc, likes, to=None, author=False):
    return {'name': name, 'avatar': AVATAR[name], 'text': text, 'date': date, 'loc': loc,
            'likes': likes, 'replyTo': to, 'author': author}


TABS = [
    {
        'key': 'all', 'label': '全部',
        'summary': '39 份作业里**川渝麻辣**最多，**极简原料**、**加料豪华**和**中西混搭**也各有人爱，酱一换就是新口味！',
        'main': u('马vv', '跟着阿老师做了第一次酱香饼，居然没翻车！皮脆酱香，小朋友一口气吃了两张～', '10-04', '浙江', 129),
        'replies': [
            u('曼食慢语', '成功啦！刷酱记得每道缝都刷到，会更香哦', '10-04', '福建', 86, to='马vv', author=True),
            u('Neil', '饼皮是现成的还是自己擀的呀？', '10-05', '上海', 12),
            u('罐罐儿', '我用的现成手抓饼皮，十分钟就搞定', '10-05', '广东', 9, to='Neil'),
            u('曼食慢语', '自己擀当然更脆，现成的也可以，出锅别放太久就行', '10-05', '福建', 21, to='Neil', author=True),
        ],
    },
    {
        'key': 'chili', 'label': '川渝麻辣版',
        'summary': '酱换成**郫县豆瓣酱**，刷**红油**撒**二荆条辣椒面**和**花椒面**，辣里带麻，多放肉和洋葱，比原版重口得多！',
        'main': u('辣妹子很怕拉', '对老几太好了，加了超量的辣椒，还加了巨多的肉、洋葱和胡萝卜碎，直接变成肉夹馍，超级爆炸满足！！', '10-04', '四川', 129),
        'replies': [
            u('财正', '红油是自己炒的吗？看着好香', '10-04', '重庆', 18, to='辣妹子很怕拉'),
            u('曼食慢语', '用二荆条和小米辣，油烧到六成热淋上去就很香了', '10-05', '福建', 74, to='财正', author=True),
            u('Ada', '不能吃辣的可以少放点辣椒面吗？', '10-05', '北京', 7),
            u('辣妹子很怕拉', '可以的，我第二张只放了一半，麻味更突出', '10-05', '四川', 11, to='Ada'),
        ],
    },
    {
        'key': 'salt', 'label': '极简原料',
        'summary': '只留**面粉**、**葱花**和一点**盐**，酱换成少量**生抽**，干烙不放油，吃得出麦香，清爽没负担！',
        'main': u('Kiki', '不放油，平底锅干烙，麦香特别明显，减脂期也敢吃一整张', '10-05', '浙江', 98),
        'replies': [
            u('欢欢', '干烙会不会很硬呀？', '10-05', '江苏', 14),
            u('曼食慢语', '面团醒够20分钟，烙的时候盖上盖子焖一下，就是软脆的', '10-06', '福建', 52, to='欢欢', author=True),
            u('斯淇', '少油少盐版给我爸妈做的，他们说刚刚好', '10-06', '山东', 33),
            u('Kiki', '这个口味配一杯无糖豆浆绝了', '10-06', '浙江', 6, to='斯淇'),
        ],
    },
    {
        'key': 'deluxe', 'label': '加料豪华版',
        'summary': '饼里加了**芝士**、**培根**和**溏心蛋**，酱里拌**黑胡椒**，一口料满满，当正餐也够了！',
        'main': u('三三姐', '加了芝士和培根，出锅直接拉丝！老公说比外面买的还好吃', '10-04', '广东', 176),
        'replies': [
            u('HY', '芝士用的什么呀？', '10-05', '北京', 10),
            u('三三姐', '马苏里拉，撕碎了铺在饼上再卷起来', '10-05', '广东', 24, to='HY'),
            u('曼食慢语', '溏心蛋最后放，不然会煎老，这个搭配太豪华了', '10-06', '福建', 61, to='三三姐', author=True),
            u('星星', '热量爆炸但是好快乐', '10-06', '上海', 45),
        ],
    },
    {
        'key': 'fusion', 'label': '中西 Fusion',
        'summary': '酱换成**泰式甜辣酱**，铺**芝士**撒**罗勒**和**黑胡椒**，像饼又像披萨，混搭意外地搭！',
        'main': u('Molly', '试了泰式甜辣酱加罗勒和黑胡椒，像饼又像披萨，意外地搭', '10-05', '中国香港', 142),
        'replies': [
            u('ian', '甜辣酱会不会太甜？', '10-06', '深圳', 8),
            u('Molly', '加了黑胡椒中和一下，刚刚好', '10-06', '中国香港', 15, to='ian'),
            u('曼食慢语', '这个混搭太有创意了，下期我也试试', '10-06', '福建', 88, to='Molly', author=True),
            u('金灵', '能不能再加点洋葱圈？', '10-07', '四川', 6),
        ],
    },
]
VISIBLE_REPLIES = 2   # 评论区默认显示的回复条数，其余点「展开更多回复」后出现


def plain(s):
    return re.sub(r'\*\*', '', s)


def build_md():
    out = ['# 作业榜 · 动态内容', '',
           '> 原型读取的数据在 `assets/content.js`，由 `tools/build-content.py` 生成；这份文档与它同源。',
           '> 点点总结用 **粗体** 标出红色高亮词；头像与昵称不对应，头像见 `assets/avatars/`。', '',
           '## 写法约定', '',
           '- **点点总结**：两行内（约 45 字），先说“酱换成什么”，再点名关键食材（高亮 3～4 个），最后一句口语化的感受，参考川渝麻辣版。',
           '- **评论区**：每个筛选下 1 条评论 + 4 条回复；其中一条回复来自视频作者「曼食慢语」（带「作者」标）；回复之间有人互相 @。默认展示前 2 条，其余点「展开更多回复」后出现。',
           '- 昵称、地区、日期、点赞数都是示例数据。', '']
    for t in TABS:
        out += [f'## {t["label"]}', '', '**点点总结**', '', f'> {t["summary"]}', '',
                f'（{len(plain(t["summary"]))} 字）', '', '**评论区**', '',
                '| # | 谁 | 内容 | 日期 · 地区 | 赞 |', '|---|---|---|---|---|']
        rows = [('评论', t['main'])] + [(f'回复{i+1}', r) for i, r in enumerate(t['replies'])]
        for i, (tag, r) in enumerate(rows):
            who = r['name'] + ('（作者）' if r['author'] else '')
            txt = (f'回复 {r["replyTo"]}：' if r['replyTo'] else '') + r['text']
            shown = '' if i == 0 or i <= VISIBLE_REPLIES else '（展开后）'
            out.append(f'| {tag}{shown} | {who} | {txt} | {r["date"]} · {r["loc"]} | {r["likes"]} |')
        out.append('')
    return '\n'.join(out)


def build_js():
    data = {'author': AUTHOR, 'visibleReplies': VISIBLE_REPLIES,
            'tabs': {t['key']: {'label': t['label'], 'summary': t['summary'], 'main': t['main'], 'replies': t['replies']} for t in TABS}}
    return '/* 由 tools/build-content.py 生成，请改那边的数据 */\nwindow.BOARD_CONTENT=' + json.dumps(data, ensure_ascii=False, indent=1) + ';\n'


if __name__ == '__main__':
    open(os.path.join(ROOT, 'docs/dynamic-content.md'), 'w').write(build_md())
    open(os.path.join(ROOT, 'assets/content.js'), 'w').write(build_js())
    for t in TABS:
        n = len(plain(t['summary']))
        print(t['label'], n, '字', '' if n <= 48 else '← 偏长')
