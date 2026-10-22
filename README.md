# 小红书「作业榜」

评论区作业聚合功能的概念原型（非官方，数据与图片均为虚构）。

- 打开 `index.html` 即可体验：评论区入口 → 作业榜 → magic move 详情
- 设计稿还原：打开 `before.html`（Figma rednote-ds 27:512，375×812 评论半屏，素材在 `assets/before/`）
- 组件还原：打开 `components.html`（Figma rednote-ds：entry、filter、gallery、comment、diandian、button、comment-bottom-sheet、pic-carousel、name-tag，素材在 `assets/components/`）
- 页面框架：打开 `page-detail.html`（Figma rednote-ds page-detail 35:2702，375×812，内容区 `#content` 留空待接入组件，素材在 `assets/page/`）
- 完整页面：打开 `homework-page.html`（Figma rednote-ds page-homework-page 30:1031，375×812：筛选 → 点点总结 → 画廊 → 评论 + 悬浮按钮）
- 评论区入口页：打开 `comment-page.html`（Figma rednote-ds page-comment-entry 27:738，375×812：评论弹窗内含作业榜入口，`setSheetEntry()` 控制入口显示/隐藏，`setSheetOpen()` 控制弹窗开合）
- 大图页：打开 `homework-detail.html`（Figma rednote-ds page-homework-detail 36:3181，375×812：page-detail 模板 + filter（返回箭头/刷新）+ pic-carousel + name-tag + button）
- **动态内容**：点点总结和评论区文案写在 `docs/dynamic-content.md`（每个筛选一份：总结 + 1 条评论 + 4 条回复，含视频作者「作者」回复）；数据源是 `tools/build-content.py`，运行后生成这份文档和原型读取的 `assets/content.js`。头像昵称见 `assets/avatars/`
- **完整流程**：打开 `flow.html`（视频播放页 → 点右下角评论 → 评论浮层占屏 75% → 点作业榜入口 → 作业榜：默认「全部」，滑动/点击筛选，每个筛选下都展示点点总结；画廊一次滑一组，评论区箭头跟着指向当前这一组；点一组 → 该组的框原位放大成大图，整框（白边框+图片）横向切换，返回箭头收回）。外壳用 iframe 装 `video-page.html`、`comment-page.html?embed=1`、`homework-board.html`，用 postMessage 转场；`homework-board.html` 是列表与大图合在一起的作业榜页（可单独打开；由 `tools/build-board.py` 生成，要改请改脚本再运行）
- **在线访问**：合并到 `main` 后由 `.github/workflows/pages.yml` 自动发布到 GitHub Pages，首页就是完整流程（首次需在仓库 Settings → Pages 把 Source 选成 GitHub Actions）
- 视频播放页：打开 `video-page.html`（Figma rednote-ds page-video 36:3546，375×812；设计稿是整屏截图，界面按截图重画；视频画面和头像在 `assets/video/`）
- 文档：`docs/xhs-homework-board-backlog.md`、`docs/PRD-xhs-homework-board.md`
