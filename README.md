# MÖBIUS 万象漫游

基于 Astro、Tailwind CSS 与 Three.js 的 3D 文化旅行体验。

## 本地运行

```sh
npm install
npm run dev
```

以终端实际显示的 URL 为准。生产预览：`npm run build && npm run preview`。
验证：`npm run check`、`npm run build`。

## 已实现

- 可拖动旋转、滚轮缩放、自动旋转、重置、全屏的 WebGL 地球。
- 地球上的国家可通过坐标与真实边界命中；国家与地区标签支持键盘点击。
- 中国 → 省 → 市 → 县级行政区逐级探索；本地内置中国、四川、成都、都江堰边界，其余中国区域从 DataV 按需获取。
- 全球地表与高程纹理；中国区域浮雕采样高程，成都及周边使用本地 Terrarium 地形瓦片。
- 六个精选目的地图鉴，介绍、遗产年份、外部权威来源、实景照片与可旋转原创意象模型。
- 中英文目的地搜索、地区直接定位、分类筛选、收藏与 localStorage 持久保存、四川文化灵感路线。
- 桌面与移动布局，原生 dialog 焦点管理、键盘快捷键与减少动效偏好支持。

## 数据覆盖与精度

当前为精选体验版。海外国家提供国家浮雕和精选图鉴，尚未接入各国完整省市县层级。文化内容不是全球完整数据库。小尺度浮雕具有地形夸张，不用于测绘导航。建筑为原创意象模型，非实测重建；实时渲染自适应设备，当前不是固定 8K 输出。

## 来源

- 全球边界：Natural Earth / `world-atlas`（公共领域）
- 中国边界：阿里云 DataV GeoAtlas（`https://geo.datav.aliyun.com/areas_v3/bound/`）
- 地球影像与高程：`https://github.com/turban/webgl-earth/tree/master/images`
- 成都局部地形：AWS Open Data Terrain Tiles，Terrarium 编码，z8，x201–202 / y104–105；`https://registry.opendata.aws/terrain-tiles/`。上游高程精度和来源随区域而异。
- 遗产内容：UNESCO 世界遗产中心，编号 438、688、91、637、1001。每个图鉴附有直接来源链接。
- 摄影：Unsplash；九寨沟 TravelChinaGuide；都江堰 Civitatis；青城山 携程。准确出处见网页“地图与内容说明”。后面三张为演示引用图片，商业发布前需要确认相应授权。

## 主要文件

- `src/pages/index.astro`：页面结构、搜索与详情弹窗
- `src/styles/global.css`：视觉设计和响应式布局
- `src/scripts/map.ts`：Three.js 地球、边界点击和分层浮雕
- `src/scripts/app.ts`：导航、数据交互、搜索与收藏
- `src/scripts/data.ts`：精选景点与来源
- `src/scripts/model.ts`：原创建筑、水利与自然意象模型
