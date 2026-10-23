#!/usr/bin/env python3
"""生成 design-system.html：在「小红书 Design System」（tools/design-system-base.html，Foundations 部分）的基础上，
追加「作业榜组件」：侧栏分组、总览卡片、每个组件一页（变体 + 属性表）。
组件样式直接取自线上页面（见 gallery_data.py），每个标本放进各自的 Shadow DOM。
改完 homework-board.html / comment-page.html 后，先运行 build-board.py，再运行本脚本。
"""
import html, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
sys.path.insert(0, HERE)
import gallery_data as G  # noqa: E402

base = open(os.path.join(HERE, 'design-system-base.html'), encoding='utf-8').read()

# ------------------------------------------------------------------ 数据
GROUP_NAME = dict(G.GROUPS)
comps = []
for c in G.COMPONENTS:
    comps.append({
        'id': c['id'], 'group': c['group'], 'name': c['name'], 'en': c['en'], 'size': c['size'], 'node': c['node'],
        'desc': c['desc'], 'props': c['props'], 'min': c['min'],
        'variants': c['variants'],
    })
DATA = {'components': comps}


def js_safe(s):
    return s.replace('</', '<\\/')


# ------------------------------------------------------------------ 侧栏
side = ''
last = None
for c in comps:
    if c['group'] != last:
        side += '<div class="side-grp">%s</div>' % html.escape(GROUP_NAME[c['group']])
        last = c['group']
    side += '<a class="rail-item" href="#%s" data-page="%s">%s<span class="cnt">%d</span></a>' % (
        c['id'], c['id'], html.escape(c['name']), len(c['variants']))
base = base.replace('</nav></aside>', side + '</nav></aside>', 1)
# 把第一个分组标题加上 Components 前缀
base = base.replace('<div class="side-grp">%s</div>' % html.escape(GROUP_NAME[comps[0]['group']]),
                    '<div class="side-grp">Components · %s</div>' % html.escape(GROUP_NAME[comps[0]['group']]), 1)

# ------------------------------------------------------------------ 总览
cards = ''
for i, c in enumerate(comps):
    cards += ('<a class="cat comp" href="#%s" style="--i:%d"><div class="top"><span class="lbl">%s</span><span class="n">%d</span></div>'
              '<div class="vis"><div class="pvw"><div class="pv" data-pv="%s" aria-hidden="true"></div></div></div></a>') % (
        c['id'], i + 6, html.escape(c['name']), len(c['variants']), c['id'])
overview_add = ('<h2>Components · 作业榜</h2><p class="lead">作业榜用到的 %d 个组件，共 %d 个变体。样式取自正在运行的页面，不是截图。</p>'
                '<div class="cat-grid">%s</div>') % (len(comps), sum(len(c['variants']) for c in comps), cards)
base = base.replace('</a></div></section>\n<section class="page" id="page-color"', '</a></div>' + overview_add + '</section>\n<section class="page" id="page-color"', 1)
assert 'Components · 作业榜</h2>' in base, 'overview anchor not found'

# ------------------------------------------------------------------ 组件页
pages = ''
for c in comps:
    props = ''.join('<tr><td><code>%s</code></td><td>%s</td></tr>' % (html.escape(p[0]), html.escape(p[1])) for p in c['props'])
    meta = '%s · %s' % (html.escape(c['en']), html.escape(c['size']))
    if c['node']:
        meta += ' · Figma %s' % c['node']
    pages += (
        '<section class="page" id="page-%(id)s" data-comp="%(id)s" data-stage="page">'
        '<div class="crumb">Components / %(grp)s</div>'
        '<div class="page-hero"><h1>%(name)s</h1></div>'
        '<p class="meta">%(meta)s</p>'
        '<p class="lead">%(desc)s</p>'
        '<div class="stage-bar"><span class="stage-lbl">舞台底色</span>'
        '<div class="tabs" role="tablist"><button type="button" role="tab" class="tab active" aria-selected="true" onclick="setStage(this,\'page\')">页面底</button>'
        '<button type="button" role="tab" class="tab" aria-selected="false" onclick="setStage(this,\'white\')">白</button>'
        '<button type="button" role="tab" class="tab" aria-selected="false" onclick="setStage(this,\'gray\')">灰</button></div></div>'
        '<h2>变体 Variants<span class="h2n">%(n)d</span></h2>'
        '<div class="vgrid" id="vg-%(id)s" style="--min:%(min)dpx"></div>'
        '<h2>属性 Props</h2><div class="tbl"><table class="spec"><tr><th>属性</th><th>取值</th></tr>%(props)s</table></div>'
        '</section>\n'
    ) % {'id': c['id'], 'grp': html.escape(GROUP_NAME[c['group']]), 'name': html.escape(c['name']), 'meta': meta,
         'desc': html.escape(c['desc']), 'n': len(c['variants']), 'min': c['min'], 'props': props}
marker = '</section>\n    </main>\n  </div>'
assert marker in base
base = base.replace(marker, '</section>\n' + pages + '    </main>\n  </div>', 1)
assert 'id="page-entry"' in base

# ------------------------------------------------------------------ CSS
css_add = '''
  /* ===== Components · 作业榜（追加）：沿用上面的 --ui-* 令牌，不新增色值 ===== */
  .lead { max-width: 62ch; margin: 0 0 var(--space-lg); color: var(--ui-text-2); font-size: var(--fs-md); }
  .h2n { margin-left: var(--space-12); font: var(--fs-xs) var(--ui-mono); color: var(--ui-text-3); border: 1px solid var(--ui-border); border-radius: var(--radius-tag); padding: var(--space-xs) var(--space-sm); vertical-align: middle; font-variant-numeric: tabular-nums; }
  .stage-bar { display: flex; align-items: center; gap: var(--space-12); flex-wrap: wrap; margin-top: var(--space-sm); }
  .stage-lbl { font-size: var(--fs-sm); color: var(--ui-text-3); }
  .vgrid { display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, var(--min, 380px)), 1fr)); gap: var(--space-md); align-items: start; }
  .vcard { border: 1px solid var(--ui-border); border-radius: var(--radius-control); background: var(--ui-bg); overflow: hidden; min-width: 0; }
  .vcard.wide { grid-column: 1 / -1; }
  .vstage { display: flex; align-items: center; justify-content: center; min-height: 120px; padding: var(--space-lg) var(--space-md); overflow-x: auto; background: var(--st, #FFF5EB); }
  .vstage.start { justify-content: flex-start; }
  .vstage .host { display: block; flex: none; }
  .page[data-stage="white"] .vstage { --st: #FFFFFF; }
  .page[data-stage="gray"] .vstage { --st: var(--ui-surface); }
  .vstage.fixed { background: var(--st-fix); }
  .vcap { padding: var(--space-12) var(--space-md) var(--space-md); border-top: 1px solid var(--ui-border); }
  .vcap b { display: block; font-size: var(--fs-sm); font-weight: 600; }
  .vcap span { display: block; margin-top: 2px; font-size: var(--fs-xs); color: var(--ui-text-2); line-height: 1.5; }
  .frame-wrap { flex: none; position: relative; overflow: hidden; border-radius: var(--radius-tag); border: 1px solid var(--ui-border-strong); background: #fff; }
  .frame-wrap iframe { position: absolute; left: 0; top: 0; width: 375px; height: 812px; border: 0; transform-origin: 0 0; background: #fff; }
  /* 总览卡片里的缩略预览：整体缩小，不接受点击 */
  .cat-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); }
  @media (max-width: 1240px) { .cat-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
  @media (max-width: 820px) { .cat-grid { grid-template-columns: minmax(0, 1fr); } }
  .cat { min-width: 0; }
  .cat.comp .vis { flex: none; height: 200px; overflow: hidden; align-items: center; justify-content: center; background: #FFF5EB; border-radius: var(--radius-tag); padding: var(--space-md); }
  .cat .pvw { position: relative; flex: none; overflow: hidden; }
  .cat .pv { pointer-events: none; transform-origin: 0 0; width: max-content; position: absolute; left: 0; top: 0; }
  .cat .pvw.frame { width: 100%; height: 100%; }
  .cat .pvw.frame iframe { position: absolute; left: 50%; top: 0; width: 375px; height: 812px; border: 0; transform-origin: 0 0; pointer-events: none; background: #fff; }
  .page .meta + .lead { margin-top: 0; }
  @media (max-width: 820px) { .h2n { display: none; } }
'''
base = base.replace('</style>', css_add + '</style>', 1)

# ------------------------------------------------------------------ 字体（标本里的 .zh 用 Noto Sans SC）
base = base.replace('<title>小红书 Design System</title>',
                    '<title>小红书 Design System</title>\n<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
                    '<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500&display=swap" rel="stylesheet">', 1)

# ------------------------------------------------------------------ JS
js_add = r'''
  // ===== Components · 作业榜（追加） =====
  (function () {
    const CSS = {board: /*__CSS_BOARD__*/, sheet: /*__CSS_SHEET__*/};
    const DATA = /*__DATA__*/;
    const EXTRA = '.sp{font-family:var(--font-zh);-webkit-font-smoothing:antialiased;color:var(--color-text-primary);display:block;width:max-content}'
      + '.sp .dd,.sp .comment{margin-left:0!important;max-width:none!important}'
      + '.sp .ntag,.sp .fab{position:relative!important;left:auto!important;top:auto!important;bottom:auto!important;opacity:1!important;transform:none!important;transition:none!important}'
      + '.sp .ntag{max-width:none!important;width:343px}.sp .gscroll{margin:0!important}.sp .dframe{scroll-snap-align:none}';
    const el = (tag, cls, h) => { const e = document.createElement(tag); if (cls) e.className = cls; if (h != null) e.innerHTML = h; return e; };
    const byId = Object.fromEntries(DATA.components.map(c => [c.id, c]));
    const roots = new Set();

    function placeHL(root) {
      const dd = root.querySelector('.dd[data-hl]'); if (!dd) return;
      const hls = dd.querySelector('.hls'), body = dd.querySelector('.body'); hls.innerHTML = '';
      const d = dd.getBoundingClientRect(), b = body.getBoundingClientRect(), lh = 20;
      if (!d.width) return;
      body.querySelectorAll('b').forEach(bb => [...bb.getClientRects()].forEach(r => {
        if (r.width < 2) return;
        const line = Math.floor(((r.top + r.height / 2) - b.top) / lh), i = document.createElement('i');
        i.style.left = (r.left - d.left) + 'px'; i.style.top = (b.top - d.top + line * lh + 14) + 'px'; i.style.width = r.width + 'px';
        hls.appendChild(i);
      }));
    }
    const placeAll = () => roots.forEach(placeHL);

    function mount(host, v) {
      const root = host.attachShadow({mode: 'open'});
      const st = document.createElement('style'); st.textContent = CSS[v.key] + EXTRA; root.appendChild(st);
      root.appendChild(el('div', 'sp', v.html));
      roots.add(root); return root;
    }
    function specimen(v) {
      const stage = el('div', 'vstage' + (v.wide ? ' start' : ''));
      if (v.stage) { stage.classList.add('fixed'); stage.style.setProperty('--st-fix', v.stage); }
      if (v.key === 'frame') {
        const s = .62, w = Math.round(375 * s), h = Math.round(812 * s);
        const wrap = el('div', 'frame-wrap'); wrap.style.width = w + 'px'; wrap.style.height = h + 'px';
        const f = document.createElement('iframe'); f.src = v.src; f.title = v.name; f.style.transform = 'scale(' + s + ')';
        f.addEventListener('load', () => { try { const win = f.contentWindow; if (win.setSheetEntry) win.setSheetEntry(v.entry !== false); } catch (e) {} });
        wrap.appendChild(f); stage.appendChild(wrap); return stage;
      }
      const host = el('div', 'host'); mount(host, v); stage.appendChild(host); return stage;
    }

    const rendered = {};
    function renderComp(id) {
      const c = byId[id]; if (!c || rendered[id]) return; rendered[id] = true;
      const grid = document.getElementById('vg-' + id);
      c.variants.forEach(v => {
        const card = el('div', 'vcard' + (v.wide ? ' wide' : ''));
        card.appendChild(specimen(v));
        card.appendChild(el('div', 'vcap', '<b>' + v.name + '</b>' + (v.note ? '<span>' + v.note + '</span>' : '')));
        grid.appendChild(card);
      });
      placeAll();
      if (document.fonts && document.fonts.ready) document.fonts.ready.then(placeAll);
      setTimeout(placeAll, 400);
    }

    // 总览卡片：每个组件放一个缩小的第一变体（评论弹层放缩小的整页，只露出弹层上半部分）
    function fitPreviews() {
      document.querySelectorAll('.pv[data-pv]').forEach(pv => {
        const wrap = pv.parentElement, vis = wrap.parentElement;
        const sp = pv.firstChild && pv.firstChild.shadowRoot && pv.firstChild.shadowRoot.querySelector('.sp');
        if (!sp) return;
        const w = sp.offsetWidth, h = sp.offsetHeight, availW = vis.clientWidth - 32, availH = vis.clientHeight - 32;
        if (!w || !availW) return;
        const s = Math.min(1, availW / w, availH / h);
        pv.style.transform = 'scale(' + s + ')';
        wrap.style.width = Math.round(w * s) + 'px'; wrap.style.height = Math.round(h * s) + 'px';
        placeAll();
      });
    }
    document.querySelectorAll('.pv[data-pv]').forEach(pv => {
      const c = byId[pv.dataset.pv], v = c.variants.find(x => x.key !== 'frame');
      const wrap = pv.parentElement;
      if (!v) {
        const fv = c.variants[0], s = .5;
        wrap.classList.add('frame'); pv.remove();
        const f = document.createElement('iframe'); f.src = fv.src; f.title = c.name; f.tabIndex = -1;
        f.style.transform = 'translate(-50%,-92px) scale(' + s + ')'; f.style.left = '50%';
        f.style.transform = 'translateX(-' + (375 * s / 2) + 'px) translateY(-92px) scale(' + s + ')'; f.style.left = '50%';
        wrap.appendChild(f); return;
      }
      const host = el('div', 'host'); mount(host, v); pv.appendChild(host);
    });
    window.addEventListener('resize', fitPreviews);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(fitPreviews);
    window.addEventListener('load', () => { fitPreviews(); setTimeout(fitPreviews, 300); });
    requestAnimationFrame(fitPreviews);

    // 舞台底色（切换标本背景），沿用页面的滑块 tabs
    window.setStage = function (btn, v) {
      const tabs = btn.parentElement;
      tabs.querySelectorAll('.tab').forEach(t => { t.classList.remove('active'); t.setAttribute('aria-selected', 'false'); });
      btn.classList.add('active'); btn.setAttribute('aria-selected', 'true');
      placeInk(tabs, pointerNav && !reduceMotion());
      btn.closest('.page').setAttribute('data-stage', v);
    };

    // 进入组件页时才渲染标本（页面隐藏时无法量高光位置）
    const baseShow = showPage;
    showPage = function (id) { baseShow(id); renderComp(id); const r = document.querySelector('.rail-item.active'); if (r && r.scrollIntoView) r.scrollIntoView({block: 'nearest', inline: 'center'}); };
    const first = (location.hash || '').slice(1); if (byId[first]) renderComp(first);
  })();
'''
js_add = js_add.replace('/*__CSS_BOARD__*/', js_safe(json.dumps(G.BOARD_CSS, ensure_ascii=False)))
js_add = js_add.replace('/*__CSS_SHEET__*/', js_safe(json.dumps(G.SHEET_CSS, ensure_ascii=False)))
js_add = js_add.replace('/*__DATA__*/', js_safe(json.dumps(DATA, ensure_ascii=False)))
base = base.replace('  route();\n</script>', js_add + '  route();\n</script>', 1)
assert 'Components · 作业榜（追加）' in base

out = os.path.join(ROOT, 'design-system.html')
open(out, 'w', encoding='utf-8').write(base)
print('design-system.html', len(base), 'bytes;', len(comps), '个组件,', sum(len(c['variants']) for c in comps), '个变体')
