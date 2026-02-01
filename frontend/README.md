# frontend

This template should help get you started developing with Vue 3 in Vite.

## Recommended IDE Setup

[VS Code](https://code.visualstudio.com/) + [Vue (Official)](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Recommended Browser Setup

- Chromium-based browsers (Chrome, Edge, Brave, etc.):
  - [Vue.js devtools](https://chromewebstore.google.com/detail/vuejs-devtools/nhdogjmejiglipccpnnnanhbledajbpd)
  - [Turn on Custom Object Formatter in Chrome DevTools](http://bit.ly/object-formatters)
- Firefox:
  - [Vue.js devtools](https://addons.mozilla.org/en-US/firefox/addon/vue-js-devtools/)
  - [Turn on Custom Object Formatter in Firefox DevTools](https://fxdx.dev/firefox-devtools-custom-object-formatters/)

## Type Support for `.vue` Imports in TS

TypeScript cannot handle type information for `.vue` imports by default, so we replace the `tsc` CLI with `vue-tsc` for type checking. In editors, we need [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) to make the TypeScript language service aware of `.vue` types.

## Customize configuration

See [Vite Configuration Reference](https://vite.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Type-Check, Compile and Minify for Production

```sh
npm run build
```

### Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```




基于 Vue 3 + TypeScript + Vite 构建的项目

🛠️ 前端技术栈
核心框架: Vue 3 (Composition API)
构建工具: Vite
开发语言: TypeScript
UI 组件库: Element Plus
数据可视化: ECharts
路由管理: Vue Router 4
CSS 预处理: Sass / SCSS

📂 目录结构 (Directory Structure)
aplatform/
├── public/                 # 静态资源文件
├── src/
│   ├── assets/             # 项目资源 (CSS, 图片等)
│   ├── components/         # 公共组件
│   │   ├── MainLayout.vue  # 全局布局 (左侧菜单 + 顶部导航)
│   │   └── TrendChart.vue  # 通用 ECharts 趋势图组件 (支持阈值线)
│   ├── router/
│   │   └── index.ts        # 路由配置 (含嵌套路由)
│   ├── views/              # 页面视图
│   │   ├── FleetMonitor.vue    # 【机队监控】卡片式状态展示
│   │   ├── FaultQuery.vue      # 【故障查询】表格 + 弹窗趋势图
│   │   └── FaultDetail.vue     # 【故障详情】详情分析页
│   ├── App.vue             # 根组件
│   ├── main.ts             # 入口文件 (引入 Element Plus, Router 等)
│   └── env.d.ts            # TypeScript 类型声明补充
├── eslint.config.ts        # ESLint 配置文件
├── package.json            # 项目依赖配置
├── tsconfig.json           # TypeScript 配置文件
└── vite.config.ts          # Vite 配置文件

🚀 快速开始 (Getting Started)
1. 环境准备
确保你的本地环境已安装 Node.js (推荐 v16+)。
2. 安装依赖
在项目根目录下运行以下命令安装所需依赖：
npm install
核心依赖清单 (Dependencies):
vue
vue-router (必须安装 v4 版本)
element-plus
@element-plus/icons-vue
echarts
sass (开发依赖)
npm install xlsx
npm install pinia
npm install axios

3. 启动开发服务器
npm run dev
启动成功后，访问控制台输出的地址 (通常是 http://localhost:5173) 即可预览项目。

4. 项目打包
npm run build

✨ 功能模块 (Features)
机队监控 (Fleet Monitor)
  卡片式布局展示飞机状态。
  根据状态 (H/M/G) 动态渲染红/黄/绿不同颜色的边框和标签。
  支持飞机注册号与机型筛选。
故障查询 (Fault Query)
  数据表格展示历史故障记录。
  弹窗分析：点击列表中的异常状态，弹窗显示该航班的参数趋势图。
  跳转详情：支持点击“查看详情”进入独立分析页面。
故障详情 (Fault Detail)
  展示故障元数据（航班号、机号、时间）。
  多图表联动：复用 TrendChart 组件，同时展示起飞和下降阶段的关键参数曲线。
  阈值告警：图表中包含设定阈值的黄色虚线，直观展示超限情况。

❓ 常见问题 (FAQ)
Q1: import { useRoute } ... 出现红色波浪线？
原因：未安装 Vue Router 依赖。 解决：运行命令 npm install vue-router@4，然后重启 IDE。

Q2: env.d.ts 中 {}, any 报错？
原因：ESLint 规则 ban-types 或 no-explicit-any 限制过严。 解决： 方法 A：在 eslint.config.ts 的 rules 中添加 '@typescript-eslint/ban-types': 'off'。 方法 B：修改 env.d.ts，将 {} 替换为 object。

Q3: 样式不生效或报错？
原因：可能未安装 Sass 预处理器。 解决：运行 npm install -D sass。

系统管理员: 如需更改图表阈值或模拟数据，请直接修改 src/views/ 下对应页面的 setup 数据块。