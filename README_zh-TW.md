<p align="center">
  <img src="docs/screenshots/color_settings_red.png" alt="Odoo Color Customizer" width="720"/>
</p>

<h1 align="center">Odoo 品牌色彩自訂模組</h1>

<p align="center">
  <strong>Odoo 18 一鍵品牌色彩自訂</strong><br/>
  從設定面板即可更改整個 Odoo 介面的品牌色彩 — 無需寫程式、無需修改 CSS、即時生效
</p>

<p align="center">
  <a href="#功能特色">功能特色</a> &bull;
  <a href="#系統架構">系統架構</a> &bull;
  <a href="#安裝說明">安裝說明</a> &bull;
  <a href="#功能截圖">功能截圖</a> &bull;
  <a href="#設定指南">設定指南</a> &bull;
  <a href="#css-自訂屬性">CSS 屬性</a> &bull;
  <a href="#javascript-api">JS API</a> &bull;
  <a href="#疑難排解">疑難排解</a> &bull;
  <a href="README.md">English</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Odoo-18.0-purple?logo=odoo" alt="Odoo 18"/>
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python" alt="Python 3.10+"/>
  <img src="https://img.shields.io/badge/License-LGPL--3-green" alt="License"/>
  <img src="https://img.shields.io/badge/Version-18.0.1.4.0-orange" alt="Version"/>
  <img src="https://img.shields.io/badge/涵蓋-30%2B%20UI%20元件-blue" alt="UI Coverage"/>
</p>

---

## 概述

**Odoo Color Customizer** 是一個輕量級、可直接用於生產環境的 Odoo 18 模組，讓系統管理員可以自訂整個 Odoo 介面的主要品牌色彩 — 導覽列、按鈕、連結、表單、徽章、日曆、狀態列以及 30 多個 UI 元件 — 全部透過一般設定中的簡單色彩選擇器完成。

<p align="center">
  <img src="docs/screenshots/color_settings_red.png" alt="色彩設定 - 紅色主題" width="720"/>
</p>

### 為什麼選擇此模組？

| 問題痛點 | 解決方案 |
|----------|----------|
| Odoo 預設紫色與品牌不搭 | 選擇任何色彩 — 介面即時更新 |
| 修改 CSS 需要開發人員 | 設定頁面零程式碼的色彩選擇器 |
| 色彩修改在 Odoo 升級後會壞掉 | 動態 CSS 生成 — 升級安全 |
| 不同環境需要不同品牌色彩 | 不需修改原始碼即可更換色彩 |
| 前後台需要一致的品牌色彩 | 同時涵蓋後台和前台版面 |
| 入口網站用戶不應看到自訂色彩 | 入口網站用戶自動保持 Odoo 預設樣式 |

---

## 功能特色

### 核心能力

- **設定中的色彩選擇器** — 整合 Odoo 原生色彩元件於一般設定中
- **即時預覽** — 使用 CSS 自訂屬性即時看到色彩變更，無需重新載入頁面
- **持久儲存** — 色彩儲存於 `ir.config_parameter`，重啟和升級後仍然保留
- **重設為預設值** — 一鍵還原 Odoo Community 預設紫色 (`#71639e`)
- **自動文字對比** — 符合 WCAG 標準的亮度計算，自動選擇白色或黑色文字
- **快取消除** — CSS URL 中包含色彩值，確保瀏覽器始終載入最新主題

### 全面 UI 涵蓋（30+ 元件）

- **導覽列** — 背景色彩、下拉選單、啟用項目
- **主要按鈕** — 正常、懸停、啟用、停用狀態
- **外框與連結按鈕** — 邊框與文字色彩匹配
- **表單輸入** — 聚焦邊框色彩、核取方塊、單選按鈕
- **清單檢視** — 列選取高亮、懸停狀態
- **看板卡片** — 卡片裝飾和進度指示器
- **日曆事件** — 事件背景色彩
- **狀態列** — 啟用步驟指示器
- **徽章** — 主要徽章樣式
- **分頁標籤** — 啟用分頁指示器
- **下拉選單** — 啟用項目高亮
- **搜尋標籤** — 篩選標記色彩
- **分頁導覽** — 啟用頁面指示器
- **進度條** — 填充色彩
- **Discuss 側邊欄** — 類別高亮
- **前台編輯器** — 啟動按鈕樣式
- **產品設定器** — 選擇指示器
- **更多...** — 34+ 個錯誤修復以確保全面涵蓋

### 智慧用戶處理

- **內部用戶** — 在整個介面中看到自訂品牌色彩
- **入口網站用戶** — 自動保持 Odoo 原始預設樣式（不注入自訂 CSS）

---

## 系統架構

```
┌─────────────────────────────────────────────────────────────────┐
│                  Odoo 品牌色彩自訂模組                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────┐  ┌─────────────────────────────────┐  │
│  │   設定介面            │  │   JavaScript 服務               │  │
│  │                      │  │                                 │  │
│  │ • 色彩選擇器         │  │ • 即時預覽引擎                  │  │
│  │ • 目前色彩值         │  │ • 主題 CSS 載入器               │  │
│  │ • 重設為預設值       │  │ • 色彩工具函式                  │  │
│  │                      │  │ • window.ColorCustomizer API    │  │
│  └──────────┬───────────┘  └──────────┬──────────────────────┘  │
│             │                         │                          │
│             ▼                         ▼                          │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              設定模型 (res.config.settings)               │   │
│  │                                                           │   │
│  │  primary_color 欄位 ──► ir.config_parameter 儲存          │   │
│  │  預設值：#71639e（Odoo Community 紫色）                    │   │
│  └──────────────────────────┬────────────────────────────────┘   │
│                              │                                    │
│  ┌──────────────────────────▼────────────────────────────────┐   │
│  │              CSS 控制器（HTTP 端點）                        │   │
│  │                                                            │   │
│  │  GET /color_customizer/theme.css                           │   │
│  │  ├── 從 ir.config_parameter 讀取 primary_color             │   │
│  │  ├── 計算色彩變體（懸停、啟用、淺色）                       │   │
│  │  ├── 計算對比文字色彩（WCAG 亮度公式）                      │   │
│  │  └── 回傳包含 30+ UI 元件覆蓋的動態 CSS                    │   │
│  │                                                            │   │
│  │  GET /color_customizer/frontend.css                        │   │
│  │  ├── 前台專用 CSS（網站頁面）                               │   │
│  │  └── 行動裝置漢堡選單及編輯器啟動按鈕修復                   │   │
│  └────────────────────────────────────────────────────────────┘   │
│                              │                                    │
│  ┌──────────────────────────▼────────────────────────────────┐   │
│  │              SCSS 覆蓋（web.assets_backend）                │   │
│  │                                                            │   │
│  │  877 行 CSS 自訂屬性規則                                    │   │
│  │  var(--custom-primary), var(--custom-primary-hover), ...   │   │
│  └────────────────────────────────────────────────────────────┘   │
│                                                                   │
├───────────────────────────────────────────────────────────────────┤
│                         Odoo 18 框架                              │
│  base_setup │ web │ ir.config_parameter │ res.config.settings     │
└───────────────────────────────────────────────────────────────────┘
```

### 模組檔案結構

```
odoo_color_customizer/
├── __init__.py
├── __manifest__.py                     # 模組元資料 (v18.0.1.4.0)
├── controllers/
│   ├── __init__.py
│   └── main.py                         # 動態 CSS 端點 (866 行)
│                                       #   GET /color_customizer/theme.css
│                                       #   GET /color_customizer/frontend.css
│                                       #   色彩計算輔助方法
├── models/
│   ├── __init__.py
│   └── res_config_settings.py          # 設定模型與色彩欄位
├── views/
│   ├── res_config_settings_views.xml   # 設定 UI（色彩選擇器 + 重設）
│   └── web_templates.xml               # 前台 CSS 注入模板
├── security/
│   └── ir.model.access.csv            # 存取控制
└── static/src/
    ├── js/
    │   └── color_customizer.js         # 即時預覽與主題載入 (234 行)
    └── scss/
        ├── color_overrides.scss        # CSS 變數覆蓋 (877 行)
        └── frontend_minimal.scss       # 前台頁面樣式
```

### 運作方式 — 資料流程

```
使用者選擇色彩 (#FF0000)
        │
        ▼
┌─────────────────┐    JavaScript 即時更新 CSS
│  色彩選擇器      │───► 自訂屬性（即時預覽）
│  於設定頁面      │
└────────┬────────┘
         │ 儲存
         ▼
┌─────────────────────┐
│  ir.config_parameter │    儲存為：odoo_color_customizer.primary_color
│  （持久儲存）        │
└────────┬────────────┘
         │ 頁面載入時
         ▼
┌─────────────────────────────┐
│  CSS 控制器生成：             │
│                              │
│  --custom-primary: #FF0000   │    主要色彩
│  --custom-primary-hover:     │    加深 10%
│  --custom-primary-active:    │    加深 20%
│  --custom-primary-light:     │    淺化 85%
│  --custom-primary-text:      │    白色（自動計算）
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  SCSS 規則將變數套用至        │    30+ UI 元件透過
│  所有 Odoo UI 元件            │    CSS 自訂屬性更新
└─────────────────────────────┘
```

---

## 功能截圖

### 色彩設定 — 自訂紅色主題

一般設定中的色彩選擇器，已套用紅色 (#ff0000)。整個 Odoo 導覽列、按鈕和 UI 元件立即更新。

<p align="center">
  <img src="docs/screenshots/color_settings_red.png" alt="紅色主題已套用" width="720"/>
</p>

### 色彩設定 — 還原預設紫色

一鍵「重設為預設值」還原 Odoo 原始紫色 (#714B67)。

<p align="center">
  <img src="docs/screenshots/color_settings_default.png" alt="預設紫色已還原" width="720"/>
</p>

### Discuss — 紅色主題套用效果

Discuss 模組套用自訂紅色主題，展示一致的導覽列和按鈕樣式。

<p align="center">
  <img src="docs/screenshots/discuss_red_theme.png" alt="Discuss 紅色主題" width="720"/>
</p>

### 銷售 — 表單檢視自訂色彩

銷售訂單表單展示紅色主題套用至導覽列、主要按鈕（「Send by Email」、「Send message」）、狀態列分頁和操作連結。

<p align="center">
  <img src="docs/screenshots/sales_form_order_lines.png" alt="銷售表單紅色主題" width="720"/>
</p>

### 銷售 — 產品設定器對話框

產品設定器彈窗展示自訂色彩套用於單選按鈕、「Confirm」按鈕和選取邊框。

<p align="center">
  <img src="docs/screenshots/sales_form_product_config.png" alt="產品設定器對話框" width="720"/>
</p>

### 銷售 — 新訂單自訂主題

新銷售報價單表單展示全面的色彩涵蓋：分頁標籤（「Order Lines」、「Optional Products」）、操作連結和表單元素。

<p align="center">
  <img src="docs/screenshots/sales_form_new_order.png" alt="新訂單表單" width="720"/>
</p>

### 預設 Odoo — 未安裝模組

標準 Odoo 18 Community 預設紫色主題。這是安裝 Color Customizer 模組前的 Odoo 外觀。

<p align="center">
  <img src="docs/screenshots/odoo_without_module.png" alt="預設 Odoo 未安裝模組" width="720"/>
</p>

### 預設 Odoo — 設定頁面導覽列（安裝前）

標準 Odoo 18 設定頁面展示預設紫色導覽列，供對比參考。

<p align="center">
  <img src="docs/screenshots/default_odoo_navbar.png" alt="預設 Odoo 導覽列" width="720"/>
</p>

---

## 安裝說明

### 系統需求

- **Odoo 18.0**（社區版或企業版）
- **Python 3.10+**
- 無需額外 Python 套件
- 無需額外系統依賴

### 步驟一：複製倉庫

```bash
git clone https://github.com/WOOWTECH/odoo_color_customizer.git
```

### 步驟二：部署模組

```bash
# 複製模組到 Odoo addons 路徑
cp -r odoo_color_customizer/odoo_color_customizer /path/to/odoo/addons/

# 或在 odoo.conf 中將倉庫根目錄加入 addons 路徑
# addons_path = /path/to/odoo/addons,/path/to/odoo_color_customizer
```

### 步驟三：在 Odoo 中安裝

1. 前往 **應用程式** 選單
2. 點擊 **更新應用程式列表**
3. 搜尋 **「Color Customizer」**
4. 點擊 **啟動**

> **提示：** 若模組未出現，請先啟用開發者模式，然後移除搜尋列中的「應用程式」篩選條件。

---

## 設定指南

### 設定品牌色彩

1. 前往 **設定 > 一般設定**
2. 捲動至頁面底部的 **Color Customization** 區塊
3. 點擊色彩選擇器圓圈選擇您的品牌色彩
4. UI 會立即更新以供預覽
5. 點擊 **儲存** 以持久保存變更

### 重設為預設值

點擊 **Reset to Default** 按鈕還原 Odoo 預設紫色 (`#71639e`)。

### 設定參數

色彩儲存於 `ir.config_parameter`：

| 鍵值 | 預設值 | 說明 |
|------|--------|------|
| `odoo_color_customizer.primary_color` | `#71639e` | 主要品牌色彩（十六進位格式） |

---

## CSS 自訂屬性

模組從您選擇的色彩生成五個 CSS 自訂屬性：

| 屬性 | 計算方式 | 範例 (#FF0000) |
|------|----------|----------------|
| `--custom-primary` | 使用者選擇的色彩 | `#FF0000` |
| `--custom-primary-hover` | 加深 10% | `#E60000` |
| `--custom-primary-active` | 加深 20% | `#CC0000` |
| `--custom-primary-light` | 淺化 85% | `#FFD9D9` |
| `--custom-primary-text` | 白色或黑色（WCAG 亮度） | `#FFFFFF` |

### 文字對比演算法

模組使用 WCAG 相對亮度公式計算文字色彩：

```
亮度 = 0.2126 * R + 0.7152 * G + 0.0722 * B
文字 = 亮度 > 0.5 ? 黑色 : 白色
```

這確保在任何背景色彩上都有可讀的文字。

### 受影響的 UI 元件

| 類別 | 元件 |
|------|------|
| **導覽** | 導覽列背景、下拉切換、啟用項目 |
| **按鈕** | `.btn-primary`（所有狀態）、`.btn-outline-primary`、`.btn-link` |
| **表單** | 聚焦邊框、核取方塊、單選按鈕、切換開關 |
| **清單** | 列選取、懸停高亮 |
| **看板** | 卡片裝飾、進度指示器 |
| **日曆** | 事件背景、日期選取 |
| **狀態列** | 啟用步驟按鈕 |
| **徽章** | `.badge` 主要樣式 |
| **分頁** | 啟用分頁/膠囊指示器 |
| **下拉選單** | 啟用項目背景 |
| **搜尋** | 標籤色彩 |
| **分頁導覽** | 啟用頁面指示器 |
| **進度條** | 填充色彩 |
| **Discuss** | 側邊欄類別高亮 |
| **前台** | 編輯器啟動按鈕、行動裝置漢堡選單 |

---

## JavaScript API

模組透過 `window.ColorCustomizer` 公開全域 JavaScript API：

```javascript
// 即時預覽 — 立即更新 CSS 變數（僅限客戶端）
window.ColorCustomizer.updateLivePreview('#FF5733');

// 從伺服器重新整理主題 CSS（儲存設定後）
await window.ColorCustomizer.refreshThemeCSS();

// 啟動時載入主題 CSS
await window.ColorCustomizer.loadColorTheme();
```

### 色彩工具函式

```javascript
// 十六進位轉 RGB
ColorCustomizer.hexToRgb('#FF0000');  // {r: 255, g: 0, b: 0}

// 按百分比加深色彩
ColorCustomizer.darkenColor('#FF0000', 0.1);  // '#E60000'

// 按百分比淺化色彩
ColorCustomizer.lightenColor('#FF0000', 0.85); // '#FFD9D9'

// 取得對比文字色彩（白色或黑色）
ColorCustomizer.getContrastColor('#FF0000');    // '#FFFFFF'
```

---

## HTTP 端點

| 端點 | 方法 | 說明 |
|------|------|------|
| `/color_customizer/theme.css` | GET | 包含所有色彩覆蓋的動態後台 CSS |
| `/color_customizer/frontend.css` | GET | 網站頁面的動態前台 CSS |

兩個端點都回傳帶有 `no-cache` 標頭的 CSS，以確保即時更新。

---

## 相容性

| | |
|---|---|
| **Odoo 版本** | 18.0 |
| **版本** | 社區版和企業版 |
| **授權** | LGPL-3 |
| **依賴** | `base_setup`、`web`（僅 Odoo 核心模組） |
| **Website 模組** | 可選 — 有無皆可運作 |
| **Python 套件** | 無（僅使用 Odoo 內建） |

---

## 疑難排解

### 儲存後色彩未套用

瀏覽器可能快取了 CSS。請嘗試：
1. 強制重新整理：`Ctrl+Shift+R`（Windows/Linux）或 `Cmd+Shift+R`（Mac）
2. 清除瀏覽器快取
3. 模組透過 URL 中的色彩值進行快取消除，因此正常重新載入應該就能生效

### 模組未出現在應用程式中

1. 啟用開發者模式：**設定 > 開發者工具 > 啟動開發者模式**
2. 前往 **應用程式** 並移除搜尋列中的「應用程式」篩選條件
3. 搜尋「color_customizer」或「Color Customizer」

### 色彩選擇器未顯示在設定中

1. 確認模組已安裝（檢查 **應用程式 > 已安裝**）
2. Color Customization 區塊在一般設定的**底部** — 請往下捲動超過「開發者工具」和「關於」區塊

### 前台頁面未更新

1. 前台 CSS 使用獨立端點 (`/color_customizer/frontend.css`)
2. 模板僅為**內部用戶**（group_user）注入 CSS
3. 入口網站用戶刻意維持 Odoo 預設樣式

---

## 更新日誌

### v18.0.1.4.0 (2026-04)

- **修復：** 入口網站用戶現在保持 Odoo 原始預設樣式 — 不為入口網站/外部用戶注入自訂 CSS
- **修復：** 前台編輯器啟動按鈕三角形色彩修復
- **修復：** 行動裝置漢堡選單圖示樣式
- **修復：** 「All Applications」按鈕文字可見性
- **改善：** 34+ 個錯誤修復以確保全面 UI 元件涵蓋
- **改善：** 移除 Website 模組依賴 — 獨立運作

### v18.0.1.0.0 (2026-01)

- **首次發布：** 一般設定中的色彩選擇器
- **功能：** 透過 CSS 自訂屬性的即時預覽
- **功能：** 帶有色彩變體的動態 CSS 生成
- **功能：** 重設為預設值功能
- **功能：** 涵蓋 30+ UI 元件的全面 SCSS 覆蓋

---

## 技術支援

- **問題回報：** [GitHub Issues](https://github.com/WOOWTECH/odoo_color_customizer/issues)
- **信箱：** gt.apps.odoo@gmail.com

---

## 授權

本模組採用 **GNU 較寬鬆通用公共授權第 3 版 (LGPL-3)**。

詳見 [LICENSE](https://www.gnu.org/licenses/lgpl-3.0.html)。

---

<p align="center">
  <sub>由 <a href="https://github.com/WOOWTECH">WOOWTECH</a> 用心打造 &bull; 基於 Odoo 18</sub>
</p>
