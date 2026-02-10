# 設計文件：移除 Color Customizer 對 Website 模組的依賴

## 概述與目標

**專案**：移除 `odoo_color_customizer` 模組對 `website` 模組的依賴

**目標**：
- 移除 `website` 模組依賴，只保留 `base_setup` 和 `web`
- ~~Portal 用戶頁面仍然套用自定義主題色~~ **[已更新]** Portal 用戶保持 Odoo 原始預設樣式
- 只有內部用戶 (`base.group_user`) 在前端頁面才會套用自定義主題色
- 後台功能完全保留

**技術方案**：保留 Controller 端點 + 使用 `web.frontend_layout` 模板注入 CSS（加入用戶群組條件檢查）

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

**[已更新]** 加入 `t-if` 條件，只對內部用戶注入 CSS：

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!--
        Color Customizer Frontend CSS Injection

        繼承 web.frontend_layout（不需要 website 模組）
        只對內部用戶（非 Portal 用戶）注入自定義主題色
        Portal 用戶保持 Odoo 原始預設樣式

        Cache busting: 在 URL 中包含顏色值，確保顏色變更後瀏覽器重新載入 CSS
    -->
    <template id="color_customizer_frontend_css"
              name="Color Customizer Frontend CSS"
              inherit_id="web.frontend_layout" priority="100">
        <xpath expr="//head" position="inside">
            <!-- 只對內部用戶注入自定義 CSS，Portal 用戶保持原始樣式 -->
            <t t-if="request.env.user.has_group('base.group_user')">
                <t t-set="primary_color" t-value="request.env['ir.config_parameter'].sudo().get_param('odoo_color_customizer.primary_color', '#71639e')"/>
                <!-- PWA theme-color for mobile browsers -->
                <meta name="theme-color" t-att-content="primary_color or '#71639e'"/>
                <!-- Load frontend CSS -->
                <link rel="stylesheet" type="text/css"
                      t-attf-href="/color_customizer/frontend.css?v={{ primary_color[1:] if primary_color else '71639e' }}"/>
            </t>
        </xpath>
    </template>
</odoo>
```

### 4. `controllers/main.py` - frontend.css 端點

**[已更新]** 移除 Portal 頁面通用 CSS 規則，因為 Portal 用戶要保持原始樣式。

`frontend.css` 端點只包含以下規則（僅對內部用戶生效）：
- BUG FIX 34: Frontend Editor Launcher (Triangle + Apps Button)
- BUG FIX 40-44: Mobile sidebar and hamburger icon fixes

~~Portal 頁面的紫色元素替換~~ **[已移除]**

## 測試計劃

1. **安裝測試**：在沒有 `website` 模組的 Odoo 實例上安裝此模組
2. **後台測試**：確認後台顏色自定義功能正常運作
3. **Portal 測試**：以 Portal 用戶登入，確認頁面保持 **Odoo 原始預設樣式**（不套用自定義主題色）
4. **內部用戶前端測試**：以內部用戶登入前端頁面，確認套用自定義主題色

## 實作步驟

1. [ ] 修改 `__manifest__.py` - 移除 `website` 依賴
2. [ ] 刪除 `views/website_templates.xml`
3. [ ] 新增 `views/web_templates.xml`
4. [ ] 更新 `controllers/main.py` - 加入 Portal CSS 規則
5. [ ] 部署並測試
