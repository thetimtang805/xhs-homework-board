# 小红书「作业榜」

评论区作业聚合功能的概念原型（非官方，数据与图片均为虚构）。

- 打开 `index.html` 即可体验：评论区入口 → 作业榜 → magic move 详情
- 设计稿还原：打开 `before.html`（Figma rednote-ds 27:512，375×812 评论半屏，素材在 `assets/before/`）
- 组件还原：打开 `components.html`（Figma rednote-ds：entry、filter、gallery、comment、diandian、button、comment-bottom-sheet、pic-carousel、name-tag，素材在 `assets/components/`）
- 页面框架：打开 `page-detail.html`（Figma rednote-ds page-detail 35:2702，375×812，内容区 `#content` 留空待接入组件，素材在 `assets/page/`）
- 完整页面：打开 `homework-page.html`（Figma rednote-ds page-homework-page 30:1031，375×812：筛选 → 点点总结 → 画廊 → 评论 + 悬浮按钮）
- 评论区入口页：打开 `comment-page.html`（Figma rednote-ds page-comment-entry 27:738，375×812：评论弹窗内含作业榜入口，`setSheetEntry()` 控制入口显示/隐藏，`setSheetOpen()` 控制弹窗开合）
- 文档：`docs/xhs-homework-board-backlog.md`、`docs/PRD-xhs-homework-board.md`
