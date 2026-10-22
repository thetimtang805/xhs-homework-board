import re
# 生成 homework-board.html：读取 homework-page.html 和 homework-detail.html，合成列表 + 大图的作业榜页。
# 改作业榜请改这个脚本再运行 `python3 tools/build-board.py`，不要直接改生成后的 homework-board.html。
import os
ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')+'/'
H=open(ROOT+'homework-page.html').read()
D=open(ROOT+'homework-detail.html').read()

css_H=H[H.index('<style>')+7:H.index('</style>')]
css_D=D[D.index('<style>')+7:D.index('</style>')]

# ---------- CSS pieces ----------
part_a=css_H[:css_H.index('/* ===== 滚动区')]
part_dd=css_H[css_H.index('/* ---- 点点 AI'):]
# 点击区域里整个 chip 的伪元素由 .lbl::before 负责
part_dd=part_dd.replace('.chip::before{content:"";position:absolute;inset:-5.5px 0}\n','')
part_dd=part_dd.replace('@media (prefers-reduced-motion:reduce){.chip{transition:none}}\n','')

chip_start=css_D.index('.chip{position:relative')
chip_end=css_D.index('/* ---- pic-carousel')
chip_css=css_D[chip_start:chip_end]
chip_css=chip_css.replace('transition:background .2s,color .2s','transition:background .15s ease,color .15s ease')
chip_css=chip_css.replace('.hf[data-back="show"] .chip.on .rf{display:block}','.page[data-mode="detail"] .chip.on .rf{display:block}')

ntag_start=css_D.index('/* ---- name-tag')
ntag_end=css_D.index('/* ---- button')
ntag_css=css_D[ntag_start:ntag_end]
ntag_css=ntag_css.replace('.ntag .av img{position:absolute;inset:0;width:100%;height:100%;display:block}','.ntag .av img{position:absolute;inset:0;width:100%;height:100%;display:block;border-radius:50%;object-fit:cover}')
# 名字条改成绝对定位
ntag_css=re.sub(r'\.ntag\{[^\n]*\}',
  '.ntag{position:absolute;left:16px;top:650px;display:flex;align-items:center;justify-content:space-between;width:343px;max-width:calc(100% - 32px);padding:var(--space-lg) var(--space-xl);border-radius:var(--radius-container);background:#fdeede}',ntag_css,count=1)

board_css='''
/* ===== 作业榜：列表态 ⇄ 大图态（data-mode）。筛选行固定，列表内容在 .scroll 里 ===== */
.page{--ease:cubic-bezier(.22,.8,.3,1)}
.scroll{position:absolute;left:0;right:0;top:0;bottom:0;overflow-y:auto;overflow-x:hidden;scrollbar-width:none;z-index:2}
.scroll::-webkit-scrollbar{display:none}
.stack{display:flex;flex-direction:column;align-items:stretch;padding-top:160px;padding-bottom:140px}
/* 列表满屏滚动：内容从头部渐变（到 0 透明度）下面穿过，而不是在 y=160 处被硬裁掉。头部渐变盖在内容之上、筛选行/标题之下 */
.band{z-index:3;pointer-events:none}
.page[data-mode="detail"] .band{z-index:1}  /* 大图态：渐变在图片下面，图片顶部不被盖 */
.c1{z-index:3}

/* 筛选行：列表态在 y=95，大图态上移 48px 到 y=47；返回箭头是页面级固定元素，位置不动 */
/* 进大图 380ms、退回 290ms（退出快 20～30%），同一条强 ease-out；--dur 随 data-mode 切换，过渡取目标状态的值 */
.page{--ease-strong:cubic-bezier(.32,.72,0,1);--dur:.29s}
.page[data-mode="detail"]{--dur:.38s}
.hf{position:absolute;left:0;top:95px;width:100%;height:65px;z-index:3;display:flex;align-items:center;translate:0 var(--sy,0px);transition:transform var(--dur) var(--ease-strong),translate var(--dur) var(--ease-strong),opacity .3s ease-out}
/* 列表态：筛选行跟着内容一起滚（--sy 由脚本按滚动位置写入，不做过渡）；上方在头部下面用渐变蒙版隐入；进出大图态时才做过渡 */
.hf.follow{transition:transform var(--dur) var(--ease-strong)}
/* 筛选行滚到头部下面时，用渐变蒙版柔和地隐入（y<95 完全隐藏，到 y=111 完全显示），没有硬切边，也不会和标题重叠；大图态蒙版收起 */
@property --mt{syntax:'<length>';inherits:false;initial-value:95px}
.hfwrap{--mt:95px;position:absolute;inset:0;z-index:3;pointer-events:none;-webkit-mask-image:linear-gradient(to bottom,transparent var(--mt),#000 calc(var(--mt) + 16px));mask-image:linear-gradient(to bottom,transparent var(--mt),#000 calc(var(--mt) + 16px));transition:--mt var(--dur) var(--ease-strong)}
.hfwrap .hf{pointer-events:auto}
.page[data-mode="detail"] .hfwrap{--mt:-16px}
.hf .chips{display:flex;align-items:center;gap:var(--space-sm);flex:1;min-width:0;height:100%;margin-left:0;padding:0 var(--space-xl);overflow-x:auto;scrollbar-width:none;scroll-padding-inline:var(--space-xl);transition:margin-left var(--dur) var(--ease-strong),padding-left var(--dur) var(--ease-strong)}
.hf .chips::-webkit-scrollbar{display:none}
.hf .chips::after{content:"";flex:none;width:1px}
.page[data-mode="detail"] .hf{transform:translateY(-48px)}
/* 箭头占 16～38，右边留 12px 底色，chip 滑到 x=50 处被裁掉 */
.page[data-mode="detail"] .hf .chips{margin-left:50px;padding-left:0;scroll-padding-inline-start:0}

/* 标题栏、彩带、托底：大图态淡出 */
.title,.rule,.dock{transition:opacity .25s ease-out}
.title,.rule,.confetti{pointer-events:none}
.page[data-mode="detail"] .title,.page[data-mode="detail"] .rule,.page[data-mode="detail"] .dock{opacity:0}
.c1,.c2{transition:opacity .25s ease-out}
.page[data-mode="detail"] .c1,.page[data-mode="detail"] .c2{opacity:0}
.scroll{transition:opacity .25s ease-out}
.page[data-mode="detail"] .scroll{opacity:0;pointer-events:none}

/* 点点总结：所有筛选下都展示（data-summary 保留，需要按筛选隐藏时再切回 off）；高度过渡把下面的内容推开 */
.ddw{height:87px;overflow:hidden;flex:none}
.ddw .dd{transition:opacity .2s ease-out}
.page[data-summary="off"] .ddw{height:0}
.page[data-summary="off"] .ddw .dd{opacity:0}

/* 作业画廊：一次滑一组。第一组靠左，第二组居中，最后一组靠右 */
.gscroll{scroll-snap-type:x mandatory;scroll-padding-inline:var(--space-xl);overscroll-behavior-x:contain}
.gcard{scroll-snap-stop:always}
.gcard.g1{scroll-snap-align:start}
.gcard.g2{scroll-snap-align:center}
.gcard.g3{scroll-snap-align:end}
.gcard.is-hidden{visibility:hidden}

/* 评论区的箭头：跟着画廊滚动，指向当前这一组（--tx 由脚本按滚动位置插值） */
.comment .tail{transform:translateX(var(--tx,0px));will-change:transform}

/* ---- 动态内容：点点总结的高亮条、评论卡 ---- */
.dd .hls{position:absolute;inset:0;pointer-events:none}
.dd .hls i{position:absolute;display:block;height:5px;background:var(--color-surface-selected);transform:rotate(-2deg)}
.dd .body,.comment .card,.dd .hls,.gscroll{transition:opacity .14s ease-out}
.comment .av35 img,.comment .av23 img{border-radius:50%;object-fit:cover}
.comment .ct .a{color:var(--color-text-primary)}
.comment .ct .b{color:var(--color-text-secondary)}
.comment .au{display:inline-block;margin-left:var(--space-xs);padding:0 var(--space-xs);border-radius:var(--radius-pill);background:var(--color-bg-brand-soft);color:var(--color-text-accent);font-size:var(--caption-font-size);line-height:var(--caption-line-height);letter-spacing:var(--caption-letter-spacing);vertical-align:1px}
.comment .xwrap{display:grid;grid-template-rows:0fr;margin-top:calc(-1 * var(--space-lg));opacity:0;transition:grid-template-rows .26s var(--ease-strong),opacity .2s ease-out}
.comment .xin{min-height:0;overflow:hidden;display:flex;flex-direction:column;gap:var(--space-lg);padding-top:var(--space-lg)}
.comment .card.expanded .xwrap{grid-template-rows:1fr;opacity:1}
@media (prefers-reduced-motion:reduce){.comment .xwrap{transition-duration:.01s}}

/* ---- 大图态：整框（白边框+图片）作为一个整体横向切换 ---- */
.dstage{position:absolute;inset:0;z-index:2;pointer-events:none;opacity:0;visibility:hidden;transition:opacity .16s ease-out,visibility 0s .16s}
.page[data-mode="detail"] .dstage{opacity:1;visibility:visible;transition:opacity .22s ease-out,visibility 0s}
.dpager{position:absolute;left:0;right:0;top:111px;height:509px;display:flex;gap:var(--space-xl);padding:24px var(--space-xl);overflow-x:auto;overflow-y:hidden;scroll-snap-type:x mandatory;scroll-padding-inline:var(--space-xl);scrollbar-width:none;pointer-events:auto;opacity:0;overscroll-behavior-x:contain}
.dpager::-webkit-scrollbar{display:none}
.dpager.ready{opacity:1}
.dpager{touch-action:pan-x;-webkit-user-select:none;user-select:none}
.dframe{position:relative;flex:none;width:343px;height:461px;scroll-snap-align:start;scroll-snap-stop:always;border:3px solid var(--color-border-subtle);border-radius:var(--radius-container);box-shadow:0 4px 20px 0 rgba(135,67,15,.15)}
.dframe img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;border-radius:var(--radius-container);pointer-events:none;-webkit-user-drag:none}
.ddots{position:absolute;left:var(--space-xl);top:608px;width:343px;height:24px;display:flex;align-items:center;justify-content:center;gap:6px;padding:var(--space-sm) 0}
.ddot{position:relative;flex:none;width:8px;height:8px;padding:0;pointer-events:auto}
.ddot::before{content:"";position:absolute;inset:-8px -3px}
.ddot img{position:absolute;inset:0;width:100%;height:100%;display:block}
.ddot .on{display:none}
.ddot[aria-current="true"] .on{display:block}
.ddot[aria-current="true"] .off{display:none}
.ddot:focus-visible{outline:2px solid var(--color-icon-accent);outline-offset:3px;border-radius:50%}
.ntag{opacity:0;transform:translateY(8px);transition:opacity .25s ease-out,transform .3s var(--ease)}
.page[data-mode="detail"] .ntag{opacity:1;transform:none;transition-delay:.1s}
.ddots{opacity:0;transition:opacity .25s ease-out}
.page[data-mode="detail"] .ddots{opacity:1;transition-delay:.1s}

/* 转场用的「飞行」框：从作业卡原位放大成大图框，或反向收回 */
.hero{position:absolute;z-index:3;box-sizing:border-box;background:var(--color-border-subtle);border-radius:var(--radius-container);box-shadow:0 4px 20px 0 rgba(135,67,15,.15);pointer-events:none;will-change:transform;transition:transform var(--hd,380ms) var(--ease-strong),border-radius var(--hd,380ms) var(--ease-strong)}
.hero img{position:absolute;inset:3px;width:calc(100% - 6px);height:calc(100% - 6px);object-fit:cover;border-radius:inherit;-webkit-user-drag:none}
@media (prefers-reduced-motion:reduce){.hero,.hf,.hf .chips,.ddw,.scroll,.dstage,.ntag,.ddots,.title,.rule,.dock,.c1,.c2{transition-duration:.01s!important;transition-delay:0s!important}}
'''

# ---------- markup ----------
def between(s,a,b):
    i=s.index(a); j=s.index(b,i)
    return s[i:j]

seg_top=between(H,'<div class="page" id="page">','  <!-- 滚动内容')
seg_top=seg_top.replace('<div class="page" id="page">','<div class="page" id="page" data-mode="list" data-summary="on">')
dd_comment=between(H,'      <section class="dd"','    </div>\n  </main>')
dd_comment=dd_comment.replace('      <section class="dd"','      <div class="ddw"><section class="dd"',1)
dd_comment=dd_comment.replace('</section>\n\n      <div class="gscroll"','</section></div>\n\n      <div class="gscroll"',1)
dd_comment=dd_comment.replace('<div class="tail">','<div class="tail" id="tail">',1)
dd_comment=dd_comment.replace(' data-evt="homework:photo"','')
import re as _re
# 点点总结：去掉写死的高亮条和文案，改由脚本按筛选渲染
dd_comment=_re.sub(r'(<section class="dd" aria-label="点点总结">)\s*<div class="hl hl1">.*?</i></div>\n(\s*<div class="who">.*?</p></div>\n)\s*<p class="body zh">.*?</p>',
    lambda m: m.group(1)+'\n        <div class="hls" id="hls"></div>\n'+m.group(2)+'        <p class="body zh" id="ddbody"></p>',dd_comment,count=1,flags=_re.S)
# 评论卡：整张卡由脚本按筛选渲染
dd_comment=_re.sub(r'<div class="card">.*?\n        </div>\n      </section>','<div class="card" id="ccard"></div>\n      </section>',dd_comment,count=1,flags=_re.S)
assert 'id="ddbody"' in dd_comment and 'id="ccard"' in dd_comment
seg_bottom=between(H,'  <!-- 悬浮按钮托底 -->','</div>\n\n<script>')

# 筛选行（取自作业大图页的 chip 结构：div.chip > button.lbl + button.rf），默认选中「全部」
hf_src=between(D,'      <div class="chip all">','    </div>\n\n    <!-- pic-carousel')
hf_src=hf_src.replace('<div class="chip all">','<div class="chip all on">',1).replace('<div class="chip chili on">','<div class="chip chili">',1)
hf_src=hf_src.replace('<button class="lbl" role="tab" aria-selected="true">全部' ,'X')  # (no-op guard)
# aria-selected 同步
hf_src=hf_src.replace('<div class="chip all on">\n        <button class="lbl" role="tab" aria-selected="false">','<div class="chip all on">\n        <button class="lbl" role="tab" aria-selected="true">',1)
hf_src=hf_src.replace('<div class="chip chili">\n        <button class="lbl" role="tab" aria-selected="true">','<div class="chip chili">\n        <button class="lbl" role="tab" aria-selected="false">',1)
hf_html=('  <!-- 筛选行：放在头部渐变的下层空间里，滚动时被头部裁掉（clip），永远不会和标题重叠；大图态解除裁剪并固定在顶部 -->\n  <div class="hfwrap"><div class="hf" id="hf" role="tablist" aria-label="流派筛选">\n    <div class="chips" id="chips">\n'
         +hf_src+'  </div></div>\n\n')

main_html=('  <!-- 列表内容：点点总结 → 画廊 → 评论 -->\n  <main class="scroll" id="scroll">\n    <div class="stack">\n\n'+dd_comment+'    </div>\n  </main>\n\n')

stage_html='''  <!-- 大图态：整框切换的图片、圆点、发布者名字条 -->
  <div class="dstage" id="dstage" aria-hidden="true">
    <div class="dpager" id="dpager" role="group" aria-label="作业大图"></div>
    <div class="ddots" id="ddots"></div>
    <div class="ntag">
      <div class="nl">
        <div class="av"><img id="nav" src="assets/components/comment-avatar-1.png" alt="" width="35" height="35"></div>
        <p class="nm zh" id="nnm">辣妹子很怕拉</p>
      </div>
      <div class="nr">
        <div class="ni"><div class="ic"><img src="assets/before/icon-heart.svg" alt=""></div><span class="en" id="nlk">129</span></div>
        <div class="ni"><div class="ic"><img src="assets/components/nametag-comment.svg" alt=""></div><span class="en" id="ncm">24</span></div>
      </div>
    </div>
  </div>

'''

js=r'''<script src="assets/content.js"></script>
<script>
/* 作业榜：列表态 ⇄ 大图态
   列表：筛选行（默认「全部」，点「川渝麻辣版」出现点点总结）→ 画廊（一次滑一组）→ 评论（箭头指向当前这一组）
   点画廊里的一组：这一组的框原位放大成大图框，筛选行上移，其余内容淡出；大图态里整框（白边框+图片）一起横向切换
   事件（只派发，交给宿主）：homework:back / join / like / dislike / reply / expand / collapse，filter:change / refresh，board:group，board:slide
   全局方法：openGroup(i) / closeGroup() */
(function(){
  var page=document.getElementById('page'),scroll=document.getElementById('scroll');
  var hf=document.getElementById('hf'),chipsEl=document.getElementById('chips');
  var gal=document.querySelector('.gscroll'),cards=[].slice.call(document.querySelectorAll('.gcard'));
  var tail=document.getElementById('tail'),pager=document.getElementById('dpager'),ddots=document.getElementById('ddots');
  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)');
  var OPEN_MS=reduce.matches?10:380,CLOSE_MS=reduce.matches?10:290;
  var GROUPS=[
    {imgs:['assets/gallery/pic-01.jpg','assets/gallery/pic-09.jpg','assets/gallery/pic-11.jpg']},
    {imgs:['assets/gallery/pic-03.jpg','assets/gallery/pic-11.jpg']},
    {imgs:['assets/gallery/pic-04.jpg','assets/gallery/pic-09.jpg']}
  ];
  /* 每个筛选自带 3 组图片：换封面和大图里的图 */
  window.applyImgs=function(t){
    if(!t||!t.images) return;
    t.images.forEach(function(imgs,i){
      if(!GROUPS[i]) return;
      GROUPS[i].imgs=imgs;
      var im=cards[i]&&cards[i].querySelector('.ph img');if(im) im.src=imgs[0];
      var tg=cards[i]&&cards[i].querySelector('.tag p');if(tg) tg.textContent=imgs.length+' 张';
      if(cards[i]) cards[i].setAttribute('aria-label','查看作业，共 '+imgs.length+' 张');
    });
  };
  var BC=(window.BOARD_CONTENT||{}).tabs||{};
  Object.keys(BC).forEach(function(k){(BC[k].images||[]).forEach(function(g){g.forEach(function(u){new Image().src=u;});});});
  applyImgs(BC.all);
  var mode='list',busy=false,group=0,slide=0;
  function emit(name,detail){
    page.dispatchEvent(new CustomEvent(name,{bubbles:true,detail:detail}));
    try{ if(window.parent!==window) window.parent.postMessage({src:'board',type:name,detail:detail||null},'*'); }catch(e){}
  }

  /* ---------- 动态内容：点点总结 + 评论区（数据在 assets/content.js，来自 docs/dynamic-content.md） ---------- */
  var C=window.BOARD_CONTENT||{tabs:{}},KEYS=['all','chili','salt','deluxe','fusion'];
  var ddbody=document.getElementById('ddbody'),hls=document.getElementById('hls'),ccard=document.getElementById('ccard'),ddEl=document.querySelector('.dd');
  var tabKey='all',curGroup=0;
  function esc(t){return String(t).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  function fam(n){return /[\u4e00-\u9fff]/.test(n)?'zh':'en';}
  function nameHTML(r){return esc(r.name)+(r.author?'<span class="au zh">作者</span>':'');}
  function mrow(r){
    return '<div class="mrow"><div class="ml"><div class="d"><p class="en">'+esc(r.date)+'</p><p class="zh">'+esc(r.loc)+'</p></div>'
      +'<button class="r zh" type="button" data-evt="homework:reply" aria-label="回复'+esc(r.name)+'">回复</button></div>'
      +'<div class="mr"><button class="lk" type="button" data-evt="homework:like" aria-label="点赞，'+r.likes+'"><span class="h"><img src="assets/components/comment-heart.svg" alt=""></span><span class="en">'+r.likes+'</span></button>'
      +'<button class="sad" type="button" data-evt="homework:dislike" aria-label="不喜欢"><span class="g"><i><img src="assets/components/comment-sad.svg" alt=""></i></span></button></div></div>';
  }
  function renderComment(t){
    var m=t.main,vis=C.visibleReplies||2;
    var html='<div class="av35"><img src="'+m.avatar+'" alt="" width="35" height="35"></div><div class="col"><div class="blk"><div class="txt zh">'
      +'<p class="nm '+fam(m.name)+'">'+nameHTML(m)+'</p><p class="ct">'+esc(m.text)+'</p></div>'+mrow(m)+'</div>';
    t.replies.forEach(function(r,i){
      var pre=r.replyTo?'<span class="a">回复</span> <span class="b">'+esc(r.replyTo)+'</span> ':'';
      if(i===vis) html+='<div class="xwrap"><div class="xin">';
      html+='<div class="sub"><div class="av23"><img src="'+r.avatar+'" alt="" width="23" height="23"></div><div class="col2"><div class="txt">'
        +'<p class="nm '+fam(r.name)+'">'+nameHTML(r)+'</p><p class="ct zh">'+pre+esc(r.text)+'</p></div>'+mrow(r)+'</div></div>';
    });
    if(t.replies.length>vis) html+='</div></div>';
    html+='<div class="more"><div class="mg"><div class="ln"></div><button class="zh" type="button" data-evt="homework:expand">展开更多回复</button></div>'
      +'<button class="zh" type="button" data-evt="homework:collapse">收起</button></div></div>';
    ccard.innerHTML=html;ccard.classList.remove('expanded');
  }
  /* 高亮条：按 <b> 的实际位置画（跨行的词每行一条），和 Figma 一样略微逆时针 2° */
  function placeHighlights(){
    hls.innerHTML='';
    var dd=ddEl.getBoundingClientRect(),bd=ddbody.getBoundingClientRect(),lh=20;
    [].forEach.call(ddbody.querySelectorAll('b'),function(b){
      [].forEach.call(b.getClientRects(),function(r){
        if(r.width<2) return;
        var line=Math.floor(((r.top+r.height/2)-bd.top)/lh);
        var i=document.createElement('i');
        i.style.left=(r.left-dd.left)+'px';i.style.top=(bd.top-dd.top+line*lh+14)+'px';i.style.width=r.width+'px';
        hls.appendChild(i);
      });
    });
  }
  function renderTab(key){
    var t=C.tabs&&C.tabs[key];if(!t) return;
    tabKey=key;
    if(window.applyImgs) applyImgs(t);
    ddbody.innerHTML=esc(t.summary).replace(/\*\*(.+?)\*\*/g,'<b>$1</b>');
    renderComment(t.groups[curGroup]||t.groups[0]);
    placeHighlights();
  }
  /* 左右切换图片组：底部评论跟着换。旧的朝滑动反方向淡出（110ms ease-in），
     新的从滑动方向淡入（200ms ease-out），中途再切会从当前状态接着走 */
  var swapTimer=0;
  function swapComment(render,dir){
    var rm=reduce.matches,dx=rm?0:10*dir;
    clearTimeout(swapTimer);
    ccard.style.transition='opacity '+(rm?1:110)+'ms ease-in,translate '+(rm?1:110)+'ms ease-in';
    ccard.style.opacity=0;ccard.style.translate=(-dx)+'px 0';
    swapTimer=setTimeout(function(){
      render();
      ccard.style.transition='none';ccard.style.translate=dx+'px 0';ccard.getBoundingClientRect();
      ccard.style.transition='opacity '+(rm?1:200)+'ms var(--ease),translate '+(rm?1:200)+'ms var(--ease)';
      ccard.style.opacity=1;ccard.style.translate='0 0';
    },rm?0:110);
  }
  function setCommentGroup(i){
    if(i===curGroup) return;
    var dir=i>curGroup?1:-1;curGroup=i;
    var t=C.tabs&&C.tabs[tabKey];if(!t) return;
    swapComment(function(){renderComment(t.groups[i]||t.groups[0]);},dir);
  }
  /* 大图模式的名字条 = 该组第 1 条评论的人 */
  function fillNameTag(i){
    var t=C.tabs&&C.tabs[tabKey];var g=t&&(t.groups[i]||t.groups[0]);
    fillNameTagFrom(g);
  }
  function fillNameTagFrom(g){
    if(!g) return;
    var m=g.main;
    document.getElementById('nav').src=m.avatar;
    var nm=document.getElementById('nnm');nm.textContent=m.name;nm.className='nm '+fam(m.name);
    document.getElementById('nlk').textContent=m.likes;
    document.getElementById('ncm').textContent=1+g.replies.length;
  }
  /* 切换筛选：内容直接换，不做渐隐渐现 */
  function swapTab(key){
    if(key===tabKey) return;
    clearTimeout(swapTimer);
    ccard.style.transition='none';ccard.style.opacity=1;ccard.style.translate='0 0';
    renderTab(key);
  }
  renderTab('all');
  if(document.fonts&&document.fonts.ready) document.fonts.ready.then(placeHighlights);
  window.addEventListener('load',placeHighlights);
  window.addEventListener('resize',placeHighlights);

  /* ---------- 筛选行跟着列表滚动 ---------- */
  hf.classList.add('follow');
  function followScroll(){
    if(mode!=='list'||busy) return;
    hf.style.setProperty('--sy',(-scroll.scrollTop)+'px');
  }
  scroll.addEventListener('scroll',followScroll,{passive:true});

  /* ---------- 筛选 ---------- */
  var chips=[].slice.call(chipsEl.querySelectorAll('.chip'));
  chips.forEach(function(c,idx){
    c.querySelector('.lbl').addEventListener('click',function(){
      if(mode==='detail'&&c.classList.contains('on')){refreshImages();emit('filter:refresh',{index:idx});return;}
      chips.forEach(function(x){var on=(x===c);x.classList.toggle('on',on);x.querySelector('.lbl').setAttribute('aria-selected',on?'true':'false');});
            c.scrollIntoView({inline:'nearest',block:'nearest',behavior:reduce.matches?'auto':'smooth'});
      swapTab(KEYS[idx]||'all');
      if(mode==='detail') syncDetail();
      emit('filter:change',{index:idx});
    });
    c.querySelector('.rf').addEventListener('click',function(){if(mode==='detail') refreshImages();emit('filter:refresh',{index:idx});});
  });

  /* 大图模式下再点一次已选中的筛选：这一组随机换图（同一组内不重复，也避开当前这几张） */
  var POOL=[1,2,3,4,5,6,7,8,9,10,11,13,14,15,17].map(function(n){return 'assets/gallery/pic-'+(n<10?'0':'')+n+'.jpg';});
  var refreshing=false;
  /* 大图模式下切换筛选：这一组换成新筛选的图和评论人（淡出换图、名字条同步） */
  function syncDetail(){
    var g=group,imgs=GROUPS[g].imgs,frames=[].slice.call(pager.children),rm=reduce.matches,tag=document.querySelector('.ntag');
    var t=C.tabs&&C.tabs[tabKey],grp=t&&(t.groups[g]||t.groups[0]);
    var loaded=0;
    imgs.forEach(function(u){var im=new Image();im.onload=im.onerror=function(){if(++loaded===imgs.length) go();};im.src=u;});
    function go(){
      frames.forEach(function(f){var im=f.querySelector('img');im.style.transition='opacity '+(rm?1:140)+'ms ease-in';im.style.opacity=0;});
      tag.style.transition='opacity '+(rm?1:140)+'ms ease-in';tag.style.opacity=0;
      setTimeout(function(){
        frames.forEach(function(f,k){var im=f.querySelector('img');if(imgs[k]) im.src=imgs[k];im.style.transition='opacity '+(rm?1:220)+'ms var(--ease)';im.style.opacity=1;});
        fillNameTagFrom(grp);
        tag.style.transition='opacity '+(rm?1:220)+'ms var(--ease)';tag.style.opacity='';
      },rm?1:140);
    }
  }
  function refreshImages(){
    if(mode!=='detail'||busy||opening||refreshing) return;
    var g=group,cur=GROUPS[g].imgs,left=POOL.filter(function(u){return cur.indexOf(u)<0;}),next=[];
    while(next.length<cur.length&&left.length){next.push(left.splice(Math.floor(Math.random()*left.length),1)[0]);}
    if(next.length<cur.length) return;
    refreshing=true;
    var frames=[].slice.call(pager.children),loaded=0;
    next.forEach(function(u){var im=new Image();im.onload=im.onerror=function(){if(++loaded===next.length) apply();};im.src=u;});
    function apply(){
      var ms=reduce.matches?1:160;
      frames.forEach(function(f,k){var im=f.querySelector('img');im.style.transition='opacity '+ms+'ms ease-in';im.style.opacity=0;});
      setTimeout(function(){
        frames.forEach(function(f,k){var im=f.querySelector('img');im.src=next[k];im.style.transition='opacity '+(reduce.matches?1:240)+'ms var(--ease)';im.style.opacity=1;});
        GROUPS[g].imgs=next;
        /* 名字也跟着换：随机换成另一位评论人，这一组的评论区同步成她的评论 */
        var t=C.tabs&&C.tabs[tabKey];
        if(t&&t.groups[g]){
          var curName=t.groups[g].main.name,all=[];
          Object.keys(C.tabs).forEach(function(k){C.tabs[k].groups.forEach(function(x){if(x.main.name!==curName) all.push(x);});});
          if(all.length){
            var pick=all[Math.floor(Math.random()*all.length)];
            t.groups[g]=pick;
            var tag=document.querySelector('.ntag');
            tag.style.transition='opacity .16s ease-in';tag.style.opacity=0;
            setTimeout(function(){fillNameTagFrom(pick);tag.style.transition='opacity .24s var(--ease)';tag.style.opacity='';},reduce.matches?1:160);
            if(curGroup===g) renderComment(pick);
          }
        }
        var ci=cards[g]&&cards[g].querySelector('.ph img');if(ci) ci.src=next[0];
        setTimeout(function(){refreshing=false;},reduce.matches?1:240);
      },ms);
    }
  }

  /* ---------- 画廊：一次一组 + 评论箭头跟随 ---------- */
  var snaps=[],centers=[];
  function measure(){
    var w=gal.clientWidth,max=gal.scrollWidth-w,pad=16;
    snaps=cards.map(function(c,i){
      var left=c.offsetLeft,cw=c.offsetWidth,s;
      if(i===0) s=left-pad;
      else if(i===cards.length-1) s=left+cw-(w-pad);
      else s=left+cw/2-w/2;
      return Math.max(0,Math.min(max,s));
    });
    centers=cards.map(function(c,i){return c.offsetLeft+c.offsetWidth/2-snaps[i];});
    /* 最后一组：照 Figma（33:2613），箭头框右缘离评论卡右缘 81px，尖角在卡内 x=247 */
    centers[centers.length-1]=16+247;
    updateTail();
  }
  function lerp(a,b,t){return a+(b-a)*t;}
  function tailX(s){
    if(s<=snaps[0]) return centers[0];
    for(var i=0;i<snaps.length-1;i++){
      if(s<=snaps[i+1]){ var t=(s-snaps[i])/(snaps[i+1]-snaps[i]||1); return lerp(centers[i],centers[i+1],t); }
    }
    return centers[centers.length-1];
  }
  function nearest(arr,v){var k=0;for(var i=1;i<arr.length;i++)if(Math.abs(arr[i]-v)<Math.abs(arr[k]-v))k=i;return k;}
  var lastGroup=0;
  function updateTail(){
    if(!snaps.length) return;
    /* 评论卡左缘在 x=16，箭头图自身的尖角在图内 x=96 处，即屏幕 x=112 */
    tail.style.setProperty('--tx',(tailX(gal.scrollLeft)-112)+'px');
    var g=nearest(snaps,gal.scrollLeft);
    if(g!==lastGroup){lastGroup=g;setCommentGroup(g);emit('board:group',{index:g});}
  }
  gal.addEventListener('scroll',updateTail,{passive:true});
  window.addEventListener('resize',measure);
  window.addEventListener('load',measure);
  if(window.ResizeObserver) new ResizeObserver(measure).observe(gal);

  /* 鼠标拖动也"一次切一组"（触摸设备用原生滑动 + scroll-snap） */
  function mouseSwipe(el,getSnaps,onClickGuard){
    var down=null;
    el.addEventListener('pointerdown',function(e){
      if(e.pointerType!=='mouse'||e.button!==0) return;
      down={x:e.clientX,left:el.scrollLeft,moved:false,start:nearest(getSnaps(),el.scrollLeft)};
      el.style.scrollSnapType='none';
    });
    window.addEventListener('pointermove',function(e){
      if(!down||pulling) return;
      var dx=e.clientX-down.x;
      if(Math.abs(dx)>4) down.moved=true;
      if(down.moved){ el.scrollLeft=down.left-dx; el.style.cursor='grabbing'; }
    });
    window.addEventListener('pointerup',function(e){
      if(!down) return;
      var d=down; down=null; el.style.cursor='';
      var S=getSnaps(),dx=e.clientX-d.x,idx=d.start;
      if(d.moved){
        if(dx<-40) idx=Math.min(S.length-1,idx+1); else if(dx>40) idx=Math.max(0,idx-1);
        el.scrollTo({left:S[idx],behavior:reduce.matches?'auto':'smooth'});
        el.__dragged=true; setTimeout(function(){el.__dragged=false;},60);
      }
      setTimeout(function(){el.style.scrollSnapType='';},d.moved?420:0);
    });
  }
  mouseSwipe(gal,function(){return snaps;});

  /* ---------- 大图态：飞行框 ---------- */
  function geo(el){
    /* 未旋转的尺寸 + 旋转中心 + 旋转角，坐标相对 .page */
    var pr=page.getBoundingClientRect(),r=el.getBoundingClientRect();
    var m=new DOMMatrixReadOnly(getComputedStyle(el).transform==='none'?undefined:getComputedStyle(el).transform);
    return {cx:r.left-pr.left+r.width/2,cy:r.top-pr.top+r.height/2,w:el.offsetWidth,h:el.offsetHeight,deg:Math.atan2(m.b,m.a)*180/Math.PI};
  }
  /* 放大/收回只动 transform（平移+旋转+缩放）和 border-radius：hero 固定成大图尺寸，缩放到卡片大小；圆角按缩放反补，保证视觉上始终是 16px */
  var FW=343,FH=461,HERO_R=parseFloat(getComputedStyle(cards[0].querySelector('.ph img')).borderTopLeftRadius)||16;
  function place(hero,g){
    var sx=g.w/FW,sy=g.h/FH;
    hero.style.transform='translate('+(g.cx-FINAL.cx)+'px,'+(g.cy-FINAL.cy)+'px) rotate('+g.deg+'deg) scale('+sx+','+sy+')';
    hero.style.borderRadius=(HERO_R/sx)+'px';
  }
  var FINAL={cx:16+343/2,cy:135+461/2,w:343,h:461,deg:0};
  function makeHero(src){
    var h=document.createElement('div');h.className='hero';
    h.style.left=(FINAL.cx-FW/2)+'px';h.style.top=(FINAL.cy-FH/2)+'px';h.style.width=FW+'px';h.style.height=FH+'px';
    var im=document.createElement('img');im.src=src;im.alt='';h.appendChild(im);page.appendChild(h);return h;
  }
  function buildPager(i){
    pager.innerHTML='';ddots.innerHTML='';
    GROUPS[i].imgs.forEach(function(src,k){
      var f=document.createElement('div');f.className='dframe';
      var im=document.createElement('img');im.src=src;im.alt='作业大图 '+(k+1);f.appendChild(im);pager.appendChild(f);
      var d=document.createElement('button');d.className='ddot';d.setAttribute('aria-label','第 '+(k+1)+' 张');
      d.innerHTML='<img class="off" src="assets/components/carousel-dot-off.svg" alt=""><img class="on" src="assets/components/carousel-dot-on.svg" alt="">';
      d.addEventListener('click',function(){gotoSlide(k);});
      ddots.appendChild(d);
    });
    pager.scrollLeft=0;slide=0;markDots(0);
  }
  function pagerSnaps(){var n=pager.children.length,out=[];for(var k=0;k<n;k++)out.push(k*(343+16));return out;}
  function markDots(k){
    [].forEach.call(ddots.children,function(d,j){if(j===k)d.setAttribute('aria-current','true');else d.removeAttribute('aria-current');});
  }
  function gotoSlide(k){pager.scrollTo({left:pagerSnaps()[k],behavior:reduce.matches?'auto':'smooth'});}
  pager.addEventListener('scroll',function(){
    var k=nearest(pagerSnaps(),pager.scrollLeft);
    if(k!==slide){slide=k;markDots(k);emit('board:slide',{group:group,index:k});}
  },{passive:true});
  mouseSwipe(pager,pagerSnaps);

  /* 放大中途可以反向（点返回 / Esc）：hero 的 transform 过渡会从当前位置重新指向卡片 */
  var hero=null,animTimer=0,opening=false,dragHero=null,pulling=false;
  function finishOpen(){
    opening=false;pager.classList.add('ready');if(hero){hero.remove();hero=null;}
    page.removeAttribute('aria-busy');document.getElementById('dstage').removeAttribute('aria-hidden');
  }
  function openGroup(i){
    if(busy||opening||mode!=='list') return;
    opening=true;group=i;mode='detail';fillNameTag(i);
    pager.style.visibility='';
    hf.classList.remove('follow');hf.style.setProperty('--sy','0px');
    var card=cards[i],ph=card.querySelector('.ph');
    buildPager(i);
    var start=geo(ph);
    hero=makeHero(GROUPS[i].imgs[0]);
    hero.style.transition='none';place(hero,start);hero.getBoundingClientRect();hero.style.transition='';
    hero.style.setProperty('--hd',OPEN_MS+'ms');
    card.classList.add('is-hidden');
    page.setAttribute('data-mode','detail');
    page.setAttribute('aria-busy','true');
    hero.getBoundingClientRect();
    place(hero,FINAL);
    animTimer=setTimeout(finishOpen,OPEN_MS);
    emit('board:open',{group:i});
  }
  function closeGroup(){
    if(busy||mode!=='detail') return;
    busy=true;
    var i=group,card=cards[i],ph=card.querySelector('.ph');
    if(dragHero){hero=dragHero;dragHero=null;}
    else if(opening){clearTimeout(animTimer);opening=false;}
    else{
      var f=pager.children[slide],pr=page.getBoundingClientRect(),fr=f.getBoundingClientRect();
      var from={cx:fr.left-pr.left+fr.width/2,cy:fr.top-pr.top+fr.height/2,w:343,h:461,deg:0};
      hero=makeHero(GROUPS[i].imgs[slide]);
      hero.style.transition='none';place(hero,from);hero.getBoundingClientRect();hero.style.transition='';
    }
    pager.classList.remove('ready');
    document.getElementById('dstage').setAttribute('aria-hidden','true');
    var to=geo(ph);
    mode='list';page.setAttribute('data-mode','list');
    hf.style.setProperty('--sy',(-scroll.scrollTop)+'px');
    hero.style.setProperty('--hd',CLOSE_MS+'ms');
    hero.getBoundingClientRect();
    place(hero,to);
    animTimer=setTimeout(function(){pager.style.visibility='';card.classList.remove('is-hidden');hero.remove();hero=null;busy=false;page.removeAttribute('aria-busy');hf.classList.add('follow');followScroll();},CLOSE_MS);
    emit('board:close',{group:i});
  }
  /* 大图下拉返回：按住图片往下拖，图片跟手缩小；拖过 120px（或快速下划）就从当前位置收回列表，否则弹回原位 */
  var ntagEl=document.querySelector('.ntag'),pd=null;
  function pullFrom(){
    var f=pager.children[slide],pr=page.getBoundingClientRect(),fr=f.getBoundingClientRect();
    return {cx:fr.left-pr.left+fr.width/2,cy:fr.top-pr.top+fr.height/2,w:343,h:461,deg:0};
  }
  function pullPlace(h,dx,dy){
    var sc=1-Math.min(Math.max(dy,0)/700,.3);
    h.style.transform='translate('+dx+'px,'+dy+'px) rotate(0deg) scale('+sc+','+sc+')';
    h.style.borderRadius=(HERO_R/sc)+'px';
    var o=String(1-Math.min(Math.max(dy,0)/160,1));
    ntagEl.style.opacity=o;ddots.style.opacity=o;
  }
  pager.addEventListener('pointerdown',function(e){
    if(mode!=='detail'||busy||opening||refreshing||e.button>0) return;
    pd={id:e.pointerId,x:e.clientX,y:e.clientY,t:performance.now(),decided:false,active:false,lastY:e.clientY,lastT:performance.now(),v:0,dy:0};
  });
  window.addEventListener('pointermove',function(e){
    if(!pd||e.pointerId!==pd.id) return;
    var dx=e.clientX-pd.x,dy=e.clientY-pd.y;
    if(!pd.decided){
      if(Math.abs(dx)<6&&Math.abs(dy)<6) return;
      pd.decided=true;
      if(dy>0&&Math.abs(dy)>Math.abs(dx)*1.2){
        pd.active=true;pulling=true;
        dragHero=makeHero(GROUPS[group].imgs[slide]);
        dragHero.style.transition='none';place(dragHero,pullFrom());
        pager.style.visibility='hidden';
        ntagEl.style.transition='none';ddots.style.transition='none';
      } else { pd=null; return; }
    }
    if(!pd.active) return;
    var now=performance.now();
    pd.v=(e.clientY-pd.lastY)/Math.max(now-pd.lastT,1);pd.lastY=e.clientY;pd.lastT=now;
    pd.dy=dy;
    pullPlace(dragHero,dx*.6,dy>0?dy:dy*.2);
  });
  function endPull(e){
    if(!pd||(e&&e.pointerId!==pd.id)) return;
    var d=pd;pd=null;
    if(!d.active){return;}
    pulling=false;
    var commit=e&&e.type==='pointerup'&&(d.dy>120||(d.v>.6&&d.dy>40));
    var h=dragHero;
    ntagEl.style.transition='';ddots.style.transition='';
    if(commit){ ntagEl.style.opacity='';ddots.style.opacity=''; closeGroup(); return; }
    h.style.transition='';h.style.setProperty('--hd',(reduce.matches?10:260)+'ms');
    place(h,FINAL);
    ntagEl.style.opacity='';ddots.style.opacity='';
    setTimeout(function(){pager.style.visibility='';if(dragHero===h){dragHero=null;}h.remove();},reduce.matches?10:260);
  }
  window.addEventListener('pointerup',endPull);
  window.addEventListener('pointercancel',endPull);
  window.openGroup=openGroup;window.closeGroup=closeGroup;

  cards.forEach(function(c,i){
    function open(){ if(gal.__dragged) return; openGroup(i); }
    c.addEventListener('click',open);
    c.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();open();}});
  });

  /* ---------- 返回、我也交作业、评论互动 ---------- */
  document.getElementById('back').addEventListener('click',function(){
    if(mode==='detail') closeGroup(); else emit('homework:back');
  });
  document.getElementById('fab').addEventListener('click',function(){emit('homework:join');});
  /* 评论里的按钮是动态渲染的，用事件委托；展开/收起同时切换隐藏的回复 */
  page.addEventListener('click',function(e){
    var el=e.target.closest&&e.target.closest('[data-evt]');if(!el) return;
    var n=el.getAttribute('data-evt');
    if(n==='homework:expand') ccard.classList.add('expanded');
    else if(n==='homework:collapse') ccard.classList.remove('expanded');
    emit(n);
  });
  document.addEventListener('keydown',function(e){
    if(e.key==='Escape'&&mode==='detail') closeGroup();
  });
  /* ---------- 宿主消息：reset（每次进入都回到「全部」列表态）、escape ---------- */
  function resetBoard(){
    clearTimeout(animTimer);hero=null;opening=false;dragHero=null;pulling=false;pager.style.visibility='';[ntagEl,ddots].forEach(function(e){e.style.opacity='';e.style.transition='';});
    [].forEach.call(document.querySelectorAll('.hero'),function(h){h.remove();});
    pager.classList.remove('ready');
    cards.forEach(function(c){c.classList.remove('is-hidden');});
    mode='list';busy=false;page.setAttribute('data-mode','list');page.removeAttribute('aria-busy');
    document.getElementById('dstage').setAttribute('aria-hidden','true');
    chips.forEach(function(x,k){var on=(k===0);x.classList.toggle('on',on);x.querySelector('.lbl').setAttribute('aria-selected',on?'true':'false');});
    page.setAttribute('data-summary','on');
    curGroup=0;lastGroup=0;
    renderTab('all');
    chipsEl.scrollLeft=0;gal.scrollLeft=0;scroll.scrollTop=0;
    hf.classList.add('follow');hf.style.setProperty('--sy','0px');
    updateTail();
  }
  window.addEventListener('message',function(e){
    var d=e.data||{};
    if(d.cmd==='reset') resetBoard();
    else if(d.cmd==='escape'&&mode==='detail') closeGroup();
    else if(d.cmd==='escape') emit('homework:back');
  });
  measure();
})();
</script>'''

# ---------- assemble ----------
head=H[:H.index('<style>')]
out=(head+'<style>\n'+part_a+chip_css+'\n'+board_css+part_dd+'\n'+ntag_css+'</style>\n</head>\n<body>\n'
     +seg_top+hf_html+main_html+stage_html+seg_bottom+'</div>\n\n'+js+'\n</body>\n</html>\n')
out=out.replace('<title>美食作业榜</title>','<title>美食作业榜（列表与大图）</title>',1)
open(ROOT+'homework-board.html','w').write(out)
print(len(out))
