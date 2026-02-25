# PRD: 內部用戶與外部用戶網站前端樣式一致性修復

## 問題描述

### 現象
內部用戶（員工）在瀏覽網站前端頁面時，看到的樣式與外部用戶（訪客/Portal用戶）不一致。

### 截圖對比

**內部用戶看到的樣式（有問題）：**
- 左側選單項目顏色被主題色影響
- Mobile navbar 背景被改為灰色
- 部分元素樣式與原生 Odoo 不同

**外部用戶看到的樣式（正確/原生）：**
- 左側選單文字為黑色
- 整體配色為 Odoo 原生的黑/灰/白
- 紫色只出現在特定 accent 元素

### 根本原因

`web_templates.xml` 對所有內部用戶注入 `frontend.css`：

```xml
<t t-if="request.env.user.has_group('base.group_user')">
    <link rel="stylesheet" type="text/css"
          t-attf-href="/color_customizer/frontend.css?v={{ primary_color[1:] }}"/>
</t>
```

`frontend.css` 包含的 CSS 規則影響了網站前端的顯示：

| BUG FIX | 選擇器 | 影響範圍 | 問題 |
|---------|--------|----------|------|
| 34 | `.o_frontend_to_backend_nav` | 編輯模式三角形+按鈕 | 無問題，只影響編輯模式 |
| 40-41 | `.o_frontend_to_backend_nav .fa-th` | 編輯模式按鈕圖標 | 無問題，只影響編輯模式 |
| **42** | `.navbar-toggler-icon` | **整個網站的 hamburger icon** | **影響網站前端** |
| **42** | `.o_header_mobile` | **整個網站的 mobile header** | **影響網站前端** |
| **43** | `.o_sidebar_topbar` | **Sidebar 頂部按鈕** | **影響網站前端** |
| **44** | `.o_menu_toggle` | **選單切換按鈕** | **影響網站前端** |

## 修復目標

**內部用戶在網站前端頁面看到的樣式應該與外部用戶完全一致**

- 自定義主題色只套用在**後台管理介面**
- 網站前端保持 Odoo 原生樣式（紫+黑配色）
- 編輯模式的 launcher（三角形+Apps按鈕）可以保留主題色

## 修復方案

### 方案：移除影響網站前端的 CSS 規則

從 `frontend.css` 中移除以下 CSS 規則：

1. **BUG FIX 42** - Mobile Hamburger Menu Icon
   - 移除 `.navbar-toggler-icon` 規則
   - 移除 `.o_header_mobile` 背景色規則
   - 移除 `.o_navbar_mobile .offcanvas-header` 規則

2. **BUG FIX 43** - Mobile Sidebar Button
   - 移除 `.o_sidebar_topbar` 相關規則

3. **BUG FIX 44** - Mobile Menu Toggle
   - 移除 `.o_menu_toggle` 相關規則

### 保留的 CSS 規則

1. **BUG FIX 34** - Editor Launcher（三角形+Apps按鈕）
   - `.o_frontend_to_backend_nav::before`
   - `.o_frontend_to_backend_nav .o_frontend_to_backend_apps_btn`

2. **BUG FIX 40-41** - Apps Button Icon
   - `.o_frontend_to_backend_nav .fa-th`

這些規則只影響編輯模式的 launcher，不影響網站前端內容。

## 實作步驟

1. [x] 修改 `controllers/main.py` 的 `get_frontend_css()` 方法
2. [x] 移除 BUG FIX 42-44 的 CSS 規則
3. [x] 保留 BUG FIX 34 和 40-41 的 CSS 規則
4. [ ] 更新模組並測試
5. [ ] 驗證內部用戶與外部用戶看到的網站樣式一致

## 測試驗證

### 測試案例

| 測試項目 | 預期結果 |
|----------|----------|
| 外部用戶瀏覽網站首頁 | 看到 Odoo 原生樣式（紫+黑） |
| 內部用戶瀏覽網站首頁 | 看到與外部用戶完全一致的樣式 |
| 內部用戶進入編輯模式 | Editor Launcher 顯示自定義主題色 |
| 內部用戶在後台 | 看到自定義主題色 |
| Mobile 瀏覽網站 | 內外部用戶看到一致的原生樣式 |

## 風險評估

- **低風險**：只移除 CSS 規則，不影響核心功能
- **可回滾**：如有問題可以重新加入移除的規則

---

**建立日期**: 2026-02-25
**狀態**: 實作中
