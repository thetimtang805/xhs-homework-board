#!/usr/bin/env python3
"""作业榜组件的标本数据（供 build-design-system.py 使用）。
组件的样式直接取自正在使用的页面（homework-board.html、comment-page.html），所以展示的就是线上真实的组件。
"""
import json, os, re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')


def read(p):
    return open(os.path.join(ROOT, p), encoding='utf-8').read()


def first_style(html):
    m = re.search(r'<style>(.*?)</style>', html, re.S)
    return m.group(1)


def to_shadow(css):
    css = css.replace(':root{', ':host{').replace(':root {', ':host {')
    css = re.sub(r'@property[^{]*\{[^}]*\}', '', css)
    return css


BOARD_CSS = to_shadow(first_style(read('homework-board.html')))
SHEET_CSS = to_shadow(first_style(read('comment-page.html')))

# ------------------------------------------------------------------ 标本片段
IMG = 'assets/gallery/pic-%02d.jpg'


def chip(kind, on=False, refresh=False):
    em = {
        'all': None,
        'chili': ('19px', '19px', 'filter-chili.png', 'left:-31.58%;top:-23.68%;width:147.37%;height:147.37%', '川渝麻辣版', True),
        'salt': ('17.434px', '22.228px', 'filter-salt.png', 'left:-33.33%;top:-15.36%;width:155.56%;height:122.01%', '极简原料', False),
        'deluxe': ('25.099px', '19px', 'filter-deluxe.png', 'left:-8.05%;top:-23.68%;width:111.56%;height:147.37%', '加料豪华版', False),
        'fusion': ('22.047px', '19px', 'filter-fusion.png', 'left:0;top:-12.53%;width:104.98%;height:121.82%', '', False),
    }[kind]
    rf = '<button class="rf" aria-label="刷新"><span class="rg"><span class="gp"><i><img src="assets/components/filter-refresh.svg" alt=""></i></span></span></button>'
    cls = 'chip %s%s' % (kind, ' on' if on else '')
    sel = 'true' if on else 'false'
    if kind == 'all':
        return '<div class="%s"><button class="lbl" role="tab" aria-selected="%s"><p class="zh">全部</p></button>%s</div>' % (cls, sel, rf)
    w, h, png, style, label, has_sel = em
    sel_img = '<img class="sel" src="assets/components/filter-chili-selected.png" alt="">' if has_sel else ''
    emcls = 'em has-sel' if has_sel else 'em'
    text = '<p class="zh">%s</p>' % label if kind != 'fusion' else '<span class="t"><p class="grad zh">中西</p><p class="en">Fusion</p></span>'
    return ('<div class="%s"><button class="lbl" role="tab" aria-selected="%s"><span class="%s" style="width:%s;height:%s">'
            '<span class="clip"><img src="assets/components/%s" alt="" style="%s"></span>%s</span>%s</button>%s</div>') % (
        cls, sel, emcls, w, h, png, style, sel_img, text, rf)


def chips(selected, detail=False, only=None):
    kinds = ['all', 'chili', 'salt', 'deluxe', 'fusion']
    if only:
        kinds = only
    return ''.join(chip(k, on=(k == selected)) for k in kinds)


def filter_bar(selected, detail=False, back=False):
    arrow = ('<img src="assets/page/header-back.svg" alt="返回" style="width:22px;height:22px;flex:none;margin:0 12px 0 16px">' if back else '')
    pad = '0' if back else '0 16px'
    inner = ('<div class="hf" style="position:static;height:49px;width:375px;translate:none;transform:none">'
             '%s<div class="chips" style="padding:%s;margin-left:%s;overflow-x:auto;height:100%%;flex:1">%s</div></div>') % (
        arrow, pad, '0', chips(selected))
    mode = 'detail' if detail else 'list'
    return '<div class="page" data-mode="%s" style="width:375px;height:49px;overflow:hidden;background:none;position:relative">%s</div>' % (mode, inner)


def gcard(i, pic, n):
    return ('<div class="gcard g%d"><div class="plate"></div><div class="slot"><div class="ph"><img src="%s" alt=""></div></div>'
            '<div class="tag"><p class="zh">%s</p></div></div>') % (i, IMG % pic, n)


AV = 'assets/avatars/avatar-%02d.png'


def mrow(date, loc, likes):
    return ('<div class="mrow"><div class="ml"><div class="d"><p class="en">%s</p><p class="zh">%s</p></div><button class="r zh" type="button">回复</button></div>'
            '<div class="mr"><button class="lk" type="button"><span class="h"><img src="assets/components/comment-heart.svg" alt=""></span><span class="en">%s</span></button>'
            '<button class="sad" type="button"><span class="g"><i><img src="assets/components/comment-sad.svg" alt=""></i></span></button></div></div>') % (date, loc, likes)


def sub(av, name, text, date, loc, likes, to=None, author=False):
    au = '<span class="au zh">作者</span>' if author else ''
    pre = '<span class="a">回复</span> <span class="b">%s</span> ' % to if to else ''
    return ('<div class="sub"><div class="av23"><img src="%s" alt="" width="23" height="23"></div><div class="col2"><div class="txt">'
            '<p class="nm zh">%s%s</p><p class="ct zh">%s%s</p></div>%s</div></div>') % (av, name, au, pre, text, mrow(date, loc, likes))


MAIN = ('assets/components/comment-avatar-1.png', '辣妹子很怕拉',
        '对老几太好了，加了超量的辣椒，还加了巨多的肉、洋葱和胡萝卜碎，直接变成肉夹馍，超级爆炸满足！！', '10-04', '四川', 129)
SUBS = [
    (AV % 5, '露洁', '红油是自己炒的吗？看着好香', '10-04', '重庆', 18, '辣妹子很怕拉', False),
    ('assets/video/avatar.jpg', '曼食慢语', '用二荆条和小米辣，油烧到六成热淋上去就很香了', '10-05', '福建', 74, '露洁', True),
    (AV % 7, 'Ada', '不能吃辣的可以少放点辣椒面吗？', '10-05', '北京', 7, None, False),
    (AV % 4, '罐罐儿', '可以的，我第二张只放了一半，麻味更突出', '10-05', '四川', 11, 'Ada', False),
]


def comment(subs=2, expanded=False, tip=172, with_more=True, main=MAIN, author_main=False):
    av, name, text, date, loc, likes = main
    au = '<span class="au zh">作者</span>' if author_main else ''
    h = '<div class="comment"><div class="tail" style="--tx:%spx"><img src="assets/components/comment-tail.svg" alt=""></div>' % (tip - 96)
    h += '<div class="card%s"><div class="cin"><div class="av35"><img src="%s" alt="" width="35" height="35"></div><div class="col"><div class="blk"><div class="txt zh"><p class="nm zh">%s%s</p><p class="ct">%s</p></div>%s</div>' % (
        ' expanded' if expanded else '', av, name, au, text, mrow(date, loc, likes))
    shown = SUBS[:subs]
    vis = 2
    for i, s in enumerate(shown):
        if i == vis:
            h += '<div class="xwrap"><div class="xin">'
        h += sub(*s)
    if len(shown) > vis:
        h += '</div></div>'
    if with_more and len(shown) > vis:
        h += ('<div class="more"><div class="mg"><div class="ln"></div><button class="zh" type="button">展开更多回复</button></div>'
              '<button class="zh" type="button">收起</button></div>')
    h += '</div></div></div></div>'
    return h


def dd(summary):
    html = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', summary)
    return ('<section class="dd" data-hl><div class="hls"></div><div class="who"><div class="ic"><img src="assets/components/diandian-icon.png" alt=""></div><p class="zh">点点</p></div>'
            '<p class="body zh">%s</p></section>') % html


def dframe(pic, lq=None, loading=False, hidden_img=False):
    st = ' style="--lq:url(%s)"' % lq if lq else ''
    im = '<img src="%s" alt="" style="opacity:0">' % (IMG % pic) if hidden_img else '<img src="%s" alt="">' % (IMG % pic)
    return '<div class="dframe"%s>%s</div>' % (st, im)


def dots(active):
    out = ''
    for k in range(2):
        cur = ' aria-current="true"' if k == active else ''
        out += '<button class="ddot"%s><img class="off" src="assets/components/carousel-dot-off.svg" alt=""><img class="on" src="assets/components/carousel-dot-on.svg" alt=""></button>' % cur
    return '<div class="ddots" style="position:static;opacity:1;width:343px;margin-top:8px">%s</div>' % out


def carousel(pic, active=0, loading=False, lq=None, hidden_img=False):
    cls = 'dpager loading' if loading else 'dpager'
    return ('<div style="width:343px"><div class="%s" style="position:static;height:auto;opacity:1;padding:0;display:block;overflow:visible">%s</div>%s</div>') % (
        cls, dframe(pic, lq, hidden_img=hidden_img), dots(active))


def ntag(av, name, likes, cmts):
    return ('<div class="ntag"><div class="nl"><div class="av"><img src="%s" alt="" width="35" height="35"></div><p class="nm zh">%s</p></div>'
            '<div class="nr"><div class="ni"><div class="ic"><img src="assets/before/icon-heart.svg" alt=""></div><span class="en">%s</span></div>'
            '<div class="ni"><div class="ic"><img src="assets/components/nametag-comment.svg" alt=""></div><span class="en">%s</span></div></div></div>') % (av, name, likes, cmts)


FAB = ('<button class="fab" aria-label="我也交作业"><span class="inset"></span><span class="label"><img src="assets/components/button-label.png" alt=""></span>'
       '<span class="pan"><img src="assets/components/button-icon.png" alt=""></span></button>')


def entry(pics, count):
    pw = ''
    for k, p in enumerate(pics):
        soft = ' soft' if k == 3 else ''
        pw += '<div class="pw pw%d"><div class="ph%s"><img src="%s" alt=""></div></div>' % (k + 1, soft, IMG % p)
    return ('<div class="entry" role="button" tabindex="0" aria-label="美食作业榜，全部 %s"><div class="bg1"></div><div class="bg2"></div>'
            '<div class="glow gl1"><i><img src="assets/components/entry-glow-1.svg" alt=""></i></div><div class="glow gl2"><i><img src="assets/components/entry-glow-2.svg" alt=""></i></div>'
            '<div class="wash"></div><div class="prow">%s</div><div class="eh"><div class="el"><div class="eicon"><img src="assets/page/header-confetti-2.png" alt=""></div>'
            '<div class="etitle"><img src="assets/components/entry-title-v2.png" alt="美食作业榜"></div></div>'
            '<div class="er"><div class="ecnt"><p class="zh">全部</p><p class="en">%s</p></div><div class="echev"><img src="assets/components/entry-chevron.svg" alt=""></div></div></div></div>') % (count, pw, count)


# 低清占位：直接复用 content.js 里生成的 base64
LQ = {}
m = re.search(r'"lqip":\s*(\{.*?\})\s*,\s*"tabs"', read('assets/content.js'), re.S)
if m:
    LQ = json.loads(m.group(1))
lq1 = LQ.get('assets/gallery/pic-01.jpg')

SUMMARIES = [
    ('全部', '39 份作业里**川渝麻辣**最多，**极简原料**、**加料豪华**和**中西混搭**也各有人爱，酱一换就是新口味！'),
    ('川渝麻辣版', '酱换成**郫县豆瓣酱**，刷**红油**撒**二荆条辣椒面**和**花椒面**，辣里带麻，多放肉和洋葱，比原版重口得多！'),
    ('极简原料', '只留**面粉**、**葱花**和一点**盐**，酱换成少量**生抽**，干烙不放油，吃得出麦香，清爽没负担！'),
    ('加料豪华版', '饼里加了**芝士**、**培根**和**溏心蛋**，酱里拌**黑胡椒**，一口料满满，当正餐也够了！'),
    ('中西 Fusion', '酱换成**泰式甜辣酱**，铺**芝士**撒**罗勒**和**黑胡椒**，像饼又像披萨，混搭意外地搭！'),
]

# ------------------------------------------------------------------ 组件清单
# key: board / sheet / frame；w：标本宽度（px）；min：网格列最小宽度
COMPONENTS = [
    {
        'group': 'nav', 'id': 'entry', 'name': '作业榜入口卡', 'en': 'entry', 'size': '341 × 167', 'node': '36:3524', 'min': 380,
        'desc': '放在评论弹窗顶部，用一排缩略图和总数告诉用户「这条笔记下有作业」，点击进入作业榜。',
        'props': [('图片数', '5 张（默认）/ 3 张'), ('数量', '「全部 39」，数字用英文数字字体'), ('交互', '整张卡可点，键盘 Enter / 空格')],
        'variants': [
            {'name': '默认', 'note': '5 张缩略图，第 4 张叠浅粉底', 'key': 'sheet', 'html': entry([1, 5, 17, 7, 11], 39)},
            {'name': '3 张图', 'note': '作业较少时缩略图数量减少，保持居中', 'key': 'sheet', 'html': entry([1, 5, 17], 39)},
            {'name': '数量较多', 'note': '三位数不撑破右侧', 'key': 'sheet', 'html': entry([3, 9, 6, 8, 13], 128)},
        ],
    },
    {
        'group': 'nav', 'id': 'filter', 'name': '流派筛选', 'en': 'filter / chip', 'size': '375 × 49', 'node': '32:1795', 'min': 400,
        'desc': '横向可滚动的筛选栏。每个流派有自己的配色和图标；选中后变为实心，大图态下选中项出现刷新图标。',
        'props': [('流派', '全部 / 川渝麻辣版 / 极简原料 / 加料豪华版 / 中西 Fusion'), ('状态', '未选中（85% 半透明底）/ 选中'), ('场景', '列表态 / 大图态（返回箭头 + 刷新）')],
        'variants': [
            {'name': '列表态 · 全部', 'note': '默认选中「全部」', 'key': 'board', 'html': filter_bar('all')},
            {'name': '列表态 · 川渝麻辣版', 'note': '选中后背景实心，图标换为选中图', 'key': 'board', 'html': filter_bar('chili')},
            {'name': '列表态 · 极简原料', 'note': '', 'key': 'board', 'html': filter_bar('salt')},
            {'name': '大图态', 'note': '返回箭头右侧留 12px 底色，选中项显示刷新图标', 'key': 'board', 'html': filter_bar('chili', detail=True, back=True)},
            {'name': '全部流派 · 状态对照', 'note': '每个流派的未选中 / 选中', 'key': 'board', 'wide': True,
             'html': '<div style="display:flex;flex-direction:column;gap:10px;padding:4px 0">'
                     + '<div class="hf" style="position:static;height:auto;width:auto;translate:none;transform:none"><div class="chips" style="padding:0;overflow:visible;height:auto">%s</div></div>' % ''.join(chip(k) for k in ['all', 'chili', 'salt', 'deluxe', 'fusion'])
                     + '<div class="hf" style="position:static;height:auto;width:auto;translate:none;transform:none"><div class="chips" style="padding:0;overflow:visible;height:auto">%s</div></div>' % ''.join(chip(k, on=True) for k in ['all', 'chili', 'salt', 'deluxe', 'fusion'])
                     + '</div>'},
        ],
    },
    {
        'group': 'content', 'id': 'gallery', 'name': '作业画廊', 'en': 'gallery', 'size': '三张卡 · 每张约 175 × 230', 'node': None, 'min': 380,
        'desc': '一次滑一组的作业卡片，每张卡带一点旋转，右下角标注图片张数。点击后原位放大进入大图。',
        'props': [('旋转', '−5° / 4° / −3°，三张各不同'), ('角标', '「N 张」'), ('滑动', '一次一组，第 3 组停在右侧')],
        'variants': [
            {'name': '第 1 组', 'note': '向左倾 5°', 'key': 'board', 'html': gcard(1, 1, '2 张')},
            {'name': '第 2 组', 'note': '向右倾 4°，投影更重', 'key': 'board', 'html': gcard(2, 3, '2 张')},
            {'name': '第 3 组', 'note': '向左倾 3°', 'key': 'board', 'html': gcard(3, 4, '2 张')},
            {'name': '多张角标', 'note': '张数不同只改文案', 'key': 'board', 'html': gcard(1, 6, '9 张')},
        ],
    },
    {
        'group': 'content', 'id': 'diandian', 'name': '点点总结', 'en': 'diandian', 'size': '343 × 87', 'node': None, 'min': 380,
        'desc': 'AI 对当前流派的一句话总结，两行内，关键词用红色标出并垫一条斜着的浅粉高光。',
        'props': [('长度', '45 字以内，两行'), ('高亮', '3～4 个关键词，每行一条，逆时针 2°'), ('来源', '每个流派一份')],
        'variants': [{'name': s[0], 'note': '', 'key': 'board', 'html': dd(s[1])} for s in SUMMARIES],
    },
    {
        'group': 'content', 'id': 'carousel', 'name': '大图轮播', 'en': 'pic-carousel', 'size': '343 × 497', 'node': '36:3423', 'min': 380,
        'desc': '大图态里的整框图片：白边框和图片是一个整体，左右整体切换，下方圆点指示。',
        'props': [('框', '3px 浅色边框，16px 圆角，柔和投影'), ('状态', '正常 / 加载中 / 低清占位'), ('圆点', '当前点为品牌红')],
        'variants': [
            {'name': '第 1 张', 'note': '', 'key': 'board', 'html': carousel(1, 0)},
            {'name': '第 2 张', 'note': '', 'key': 'board', 'html': carousel(9, 1)},
            {'name': '加载中', 'note': '超过 300ms 才出现：旧图变暗，扫一道高光', 'key': 'board', 'html': carousel(1, 0, loading=True)},
            {'name': '低清占位', 'note': '首次打开、大图还没到时，先显示模糊的预览', 'key': 'board', 'html': carousel(1, 0, lq=lq1, hidden_img=True)},
        ],
    },
    {
        'group': 'interact', 'id': 'comment', 'name': '评论与回复', 'en': 'comment', 'size': '343 × 313', 'node': '33:2612', 'min': 380,
        'desc': '图片组下方的评论卡。顶部的小三角指向当前图片组；回复默认显示 2 条，其余收在「展开更多回复」里。',
        'props': [('回复数', '0 / 2 / 4'), ('折叠', '收起（前 2 条）/ 展开（全部）'), ('箭头', '三个位置：靠左 / 居中 / 靠右（右侧留 81px）'), ('作者', '视频作者的回复带「作者」标')],
        'variants': [
            {'name': '收起', 'note': '默认：主评论 + 2 条回复 + 展开入口', 'key': 'board', 'html': comment(4, False)},
            {'name': '展开', 'note': '点「展开更多回复」后显示全部 4 条', 'key': 'board', 'html': comment(4, True)},
            {'name': '仅主评论', 'note': '没有回复时不显示展开入口', 'key': 'board', 'html': comment(0, False)},
            {'name': '箭头 · 靠左', 'note': '指向第 1 组', 'key': 'board', 'html': comment(2, False, tip=90)},
            {'name': '箭头 · 居中', 'note': '指向第 2 组', 'key': 'board', 'html': comment(2, False, tip=172)},
            {'name': '箭头 · 靠右', 'note': '指向第 3 组，尖角在卡内 247px', 'key': 'board', 'html': comment(2, False, tip=247)},
        ],
    },
    {
        'group': 'interact', 'id': 'nametag', 'name': '名字条', 'en': 'name-tag', 'size': '343 × 59', 'node': '36:3429', 'min': 380,
        'desc': '大图下方的发布者信息：头像、昵称、点赞数和评论数。右侧两个图标与评论区的图标右对齐。',
        'props': [('头像', '35px 正圆'), ('数字', '等宽数字，右侧留 12px'), ('内容', '取自该组第 1 条评论的人')],
        'variants': [
            {'name': '默认', 'note': '', 'key': 'board', 'html': ntag(AV % 17, '小星星', 64, 4)},
            {'name': '数字较大', 'note': '点赞数四位', 'key': 'board', 'html': ntag(AV % 5, '露洁', '1,208', 36)},
            {'name': '昵称较长', 'note': '长昵称不挤压右侧数字', 'key': 'board', 'html': ntag(AV % 20, '東方神韵不吃香菜', 88, 12)},
        ],
    },
    {
        'group': 'interact', 'id': 'button', 'name': '悬浮按钮', 'en': 'button', 'size': '191 × 43', 'node': '33:2689', 'min': 300,
        'desc': '「我也交作业」悬浮在列表底部。图标和文字在内阴影之上，不受内阴影影响。',
        'props': [('图层', '底色 → 内阴影 → 文字 / 图标'), ('位置', '底部居中，安全区上方 29px'), ('托底', '下方用渐进模糊托住，保持按钮清晰')],
        'variants': [
            {'name': '在页面底色上', 'note': '', 'key': 'board', 'stage': '#fff5eb', 'html': '<div style="padding:18px 24px 6px">%s</div>' % FAB},
            {'name': '在评论卡底色上', 'note': '', 'key': 'board', 'stage': '#fdeede', 'html': '<div style="padding:18px 24px 6px">%s</div>' % FAB},
            {'name': '在图片上', 'note': '深色背景下仍清晰', 'key': 'board', 'stage': '#3b2a20', 'html': '<div style="padding:18px 24px 6px">%s</div>' % FAB},
        ],
    },
    {
        'group': 'container', 'id': 'sheet', 'name': '评论弹层', 'en': 'comment-bottom-sheet', 'size': '375 × 1066（隐藏入口卡 875）', 'node': '35:2854', 'min': 340,
        'desc': '评论弹窗，占屏幕下方 75%。顶部可以放作业榜入口卡；底部是评论输入条。',
        'props': [('入口卡', '显示 / 隐藏'), ('输入条', '左右各 16px，弹窗出现时无动画'), ('关闭', '遮罩 / 关闭按钮 / Esc')],
        'variants': [
            {'name': '带作业榜入口', 'note': '', 'key': 'frame', 'src': 'comment-page.html', 'entry': True},
            {'name': '隐藏入口卡', 'note': '没有作业或作业少于 3 份时，入口卡连同间距一起移除', 'key': 'frame', 'src': 'comment-page.html?entry=hide', 'entry': False},
        ],
    },
]

GROUPS = [
    ('nav', '入口与导航'),
    ('content', '内容展示'),
    ('interact', '互动与评论'),
    ('container', '浮层与容器'),
]
