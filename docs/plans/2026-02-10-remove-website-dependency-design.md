# 設計文件：移除 Color Customizer 對 Website 模組的依賴

## 概述與目標

**專案**：移除 `odoo_color_customizer` 模組對 `website` 模組的依賴

**目標**：
- 移除 `website` 模組依賴，只保留 `base_setup` 和 `web`
- Portal 用戶頁面仍然套用自定義主題色
- 後台功能完全保留

**技術方案**：保留 Controller 端點 + 使用 `web.frontend_layout` 模板注入 CSS

## 修改範圍

| 檔案 | 動作 |
|------|------|
| `__manifest__.py` | 移除 `website` 依賴，移除 `website_templates.xml` 引用，新增 `web_templates.xml` 引用 |
| `views/website_templates.xml` | **刪除**此檔案 |
| `views/web_templates.xml` | **新增** - 繼承 `web.frontend_layout` 注入 CSS |
| `controllers/main.py` | 保留 `frontend.css` 端點，加入 Portal 頁面 CSS 規則 |

## 實作細節

### 1. `__manifest__.py` 修改

```python
# 修改前
'depends': ['base_setup', 'web', 'website'],
'data': [
    'security/ir.model.access.csv',
    'views/res_config_settings_views.xml',
    'views/website_templates.xml',
],

# 修改後
'depends': ['base_setup', 'web'],
'data': [
    'security/ir.model.access.csv',
    'views/res_config_settings_views.xml',
    'views/web_templates.xml',
],
```

### 2. 刪除 `views/website_templates.xml`

整個檔案刪除（繼承 `website.layout` 的模板）。

### 3. 新增 `views/web_templates.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!--
        Color Customizer Frontend CSS Injection

        繼承 web.frontend_layout（不需要 website 模組）
        用於 Portal 頁面和其他前端頁面的主題色自定義

        Cache busting: 在 URL 中包含顏色值，確保顏色變更後瀏覽器重新載入 CSS
    -->
    <template id="color_customizer_frontend_css"
              name="Color Customizer Frontend CSS"
              inherit_id="web.frontend_layout" priority="100">
        <xpath expr="//head" position="inside">
            <t t-set="primary_color" t-value="request.env['ir.config_parameter'].sudo().get_param('odoo_color_customizer.primary_color', '#71639e')"/>
            <!-- PWA theme-color for mobile browsers -->
            <meta name="theme-color" t-att-content="primary_color or '#71639e'"/>
            <!-- Load frontend CSS -->
            <link rel="stylesheet" type="text/css"
                  t-attf-href="/color_customizer/frontend.css?v={{ primary_color[1:] if primary_color else '71639e' }}"/>
        </xpath>
    </template>
</odoo>
```

### 4. `controllers/main.py` - 加入 Portal 頁面 CSS 規則

`frontend.css` 端點需要包含 Portal 頁面的紫色元素替換：

| 元素 | CSS 選擇器 | 說明 |
|------|-----------|------|
| 主要按鈕 | `.btn-primary` | 背景色、邊框色 |
| 外框按鈕 | `.btn-outline-primary` | 文字色、邊框色 |
| 連結 | `a.text-primary` | 文字色 |
| 文字 | `.text-primary` | 文字色 |
| 背景 | `.bg-primary` | 背景色 |
| 表單焦點 | `.form-control:focus` | 邊框色 |
| 核取方塊 | `.form-check-input:checked` | 背景色 |
| 分頁 | `.page-item.active .page-link` | 背景色 |
| 徽章 | `.badge.bg-primary` | 背景色 |
| 進度條 | `.progress-bar` | 背景色 |

## 測試計劃

1. **安裝測試**：在沒有 `website` 模組的 Odoo 實例上安裝此模組
2. **後台測試**：確認後台顏色自定義功能正常運作
3. **Portal 測試**：以 Portal 用戶登入，確認頁面套用自定義主題色
4. **顏色變更測試**：更改主題色後，確認 Portal 頁面立即生效

## 實作步驟

1. [ ] 修改 `__manifest__.py` - 移除 `website` 依賴
2. [ ] 刪除 `views/website_templates.xml`
3. [ ] 新增 `views/web_templates.xml`
4. [ ] 更新 `controllers/main.py` - 加入 Portal CSS 規則
5. [ ] 部署並測試
