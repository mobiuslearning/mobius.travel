# MÖBIUS 万象漫游

Astro + Tailwind CSS + Three.js 的全球文化旅行网页。从地球进入国家，再按数据源提供的实际行政层级继续探索；以有出处的世界遗产资料与建筑三维查看器呈现文化与自然。

## 运行与验证

```sh
npm install
npm run dev
npm run check
npm test
npm run build
npm run preview
```

使用终端实际显示的预览地址。本项目为静态构建，不需要地图商业 API 密钥或服务端账号。

## 当前数据快照（2026-10-23）

| 内容 | 实际覆盖 |
| --- | --- |
| 全球下级行政区目录 | geoBoundaries 中 208 个国家/地区，484 个可用下级边界图层；深度因国家而异，最深 ADM5 |
| 中国行政区 | 363 份本地边界文件，3,237 个省、市、县级区域索引；DataV 未提供的台湾下级边界使用 geoBoundaries 补充 |
| 主要目的地本地缓存 | 18 个国家/地区、43 个边界图层；包括日本、意大利、美国、法国、英国、印度、柬埔寨、约旦、埃及、希腊、西班牙、秘鲁、墨西哥、澳大利亚、印尼、泰国、土耳其及台湾地区 |
| 全球遗产库 | UNESCO DataHub whc001 的 1,273 条记录，涉及 173 个国家/地区；1,271 条有有效代表坐标，另外 2 条仍可检索 |
| 精细三维资源 | 7 个已核对作者与来源的官方 Sketchfab 外部查看器：长城局部、斗兽场、泰姬陵、吴哥窟、佩特拉卡兹尼神殿、婆罗浮屠、奇琴伊察金字塔 |
| 本地三维意象 | 长城、宫观、水利与自然地形；新增砖石纹理、拱洞、台阶、屋檐、栏杆、植被、阴影及重置/旋转/线框控制 |

原有的六个精选地标继续保留；同一 UNESCO 遗产的文化地标（如青城山与都江堰）可独立展示。因此界面图鉴条目数可能与唯一 UNESCO 名录编号数不同。

## 行政层级行为

- 中国：国家 → 省 → 地级市 → 县级区域；直辖市和没有中间层级的地区按源数据展开。
- 日本：国家 → 都道府县 → 市区町村。
- 意大利：国家 → 大区 → 省/广域市 → 市镇；跳过统计宏观分区。
- 美国：国家 → 州/领地 → 县。
- 西班牙：国家 → 自治区 → 省 → 市镇。
- 其他地区：依据本地行政制度与已发布数据展开；缺失的层级不会虚构。
- 主要国家采用本地缓存，其余图层按目录中的版本 URL 联网加载；超时或失败会保留当前视图并给出提示。
- geoBoundaries 各级文件不提供统一的父子外键。海外父子归属通过下级区域的内部代表点与上级多边形匹配；跨版本边界、飞地和跨区情况可能造成偏差。数据不是当前官方行政登记册。
- 国家视图按缔约国代码保留离岛与跨国遗产；子区域按遗产组成部分坐标匹配。区域浮雕优先展示主陆地，离岛可从完整下级列表进入。

## 图鉴与模型

图鉴支持全球中英文名称搜索、国家筛选、文化/自然/双重遗产分类、精细模型筛选、分页与收藏。部分原始记录没有中文名称或中文简介，会显示来源英文；为中国、日本的少量常见遗产补充了中文显示别名。日本都道府县、京都府市町村、意大利部分地区与美国州提供中文辅助名称，保留原始名称供检索。

外部精细模型通过原平台公开 iframe 流式显示，未下载、改编或重新分发模型资产。详情保留作者、许可链接、模型类别与原站入口。外部网络、设备能力及平台可用性影响加载；本地意象模型单独标注。三维覆盖不等于全部遗产的实测数字孪生。Standard、平台展示条款与 CC BY/NC 等许可不可混同为可自由下载或商用授权。

文字来自 UNESCO 原始资料；影像使用源页面提供的 URL 与署名，加载失败时显示明确的文化遗产示意图。原版六张照片的出处见下方。收藏仅存于本机浏览器。

## 关键文件

- `src/scripts/geography.ts`：国家代码、行政层级、边界提供器和路径解析
- `src/scripts/geometry.ts`：跨日期变更线、多边形孔洞、内部代表点和空间归属
- `src/scripts/localize.ts`：辅助中文名称，保留源名称
- `src/scripts/map.ts`：3D 地球、金色遗产点、地区浮雕及点击
- `src/scripts/data.ts`：精选地标与全球库异步载入
- `src/scripts/app.ts`：目录、搜索、筛选、覆盖表、详情与收藏
- `src/scripts/model.ts`：原创参数化建筑模型
- `public/data/heritage.json`：完整遗产记录快照
- `public/data/model-registry.json`：模型作者、类别、许可与来源登记
- `public/data/boundary-catalog.json`：逐层 URL、来源年份、许可和缓存状态
- `public/data/admin/`：按国家/级别与中国行政代码保存的边界
- `tests/geography.test.mjs`：真实数据上的层级、边界、跨国遗产与覆盖一致性验证

## 数据更新工具

`scripts/prepare-geography.py` 下载并整理中国行政边界；`scripts/prepare-world.mjs` 整理全球目录、国家代码及选定国家的边界；`scripts/prepare-heritage.py` 标准化 UNESCO 资料；`scripts/prepare-models.py` 通过公开 API 核对模型作者和许可。

这些工具使用 `/private/tmp/mobius-boundaries-catalog.json`（geoBoundaries 的 `ALL/ALL` 目录）与 `/private/tmp/mobius-unesco-selected.json`（UNESCO 选择字段的 JSON 导出）作为下载快照输入。运行前需要刷新输入；本地边界已存在时会复用缓存。更换源数据版本时应同时更新对应边界文件，避免新目录与旧几何混用。当前下载快照日期写在各覆盖 JSON 中，更新时需同步调整。

## 来源与精度

- 全球概略边界：Natural Earth / world-atlas（公共领域）
- 全球行政边界：<https://www.geoboundaries.org/api.html>，gbOpen；每层原始来源及许可见目录
- 中国边界：<https://geo.datav.aliyun.com/areas_v3/bound/>
- 遗产资料：<https://data.unesco.org/explore/dataset/whc001/>，各条目附 `https://whc.unesco.org/en/list/{id}/` 来源
- 地表及高程：<https://github.com/turban/webgl-earth/tree/master/images>
- 成都局部高程：<https://registry.opendata.aws/terrain-tiles/>，Terrarium z8 / x201–202 / y104–105
- 外部模型：<https://sketchfab.com/>；各作者、许可与模型 URL 见 `model-registry.json`
- 原版摄影：Unsplash；九寨沟 TravelChinaGuide；都江堰 Civitatis；青城山携程。第三方影像权利归原署名者；这三张为界面演示引用，并非本项目自有影像。

浮雕有艺术化夸张，边界及高程精度受原始数据限制，不用于导航或测绘；实时画面自适应设备像素比，不是固定 8K 输出。全球库当前以世界遗产名录为范围，不是全球所有旅游景点或所有建筑的穷尽清单。网页的“查看实际覆盖”可直接核对当前可用范围。
