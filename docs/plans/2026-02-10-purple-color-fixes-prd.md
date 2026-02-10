# PRD: Odoo Color Customizer - Purple Color Fixes

## Problem Statement

The Odoo Color Customizer module is not properly replacing ALL purple color instances (`#714B67`, `#71639e`, `rgb(102, 89, 143)`) with the user's custom color. Several UI elements still show the default Odoo purple instead of the configured custom color.

**Key Principle**: Only replace purple-colored elements. Black/gray text must remain unchanged.

## Affected Areas (From Screenshots)

### 1. PWA Theme Color (Priority: High)
- **Location**: Mobile browser title bar / PWA header
- **Current**: Purple `#714B67`
- **Expected**: User's custom color
- **Root Cause**: `<meta name="theme-color">` not being injected properly or not on all pages

### 2. Login Page (`/web/login`)
- **Affected Elements**:
  - "選擇使用者" (Select User) link - PURPLE ❌
  - "重設新密碼" (Reset Password) link - PURPLE ❌
  - "還沒有帳戶？" (No account?) link - PURPLE ❌
- **Expected**: Custom primary color
- **Note**: Footer links (主頁, 關於我們, etc.) appear CYAN ✅ - working correctly

### 3. Portal Page (`/my/home`)
- **Affected Elements**:
  - "待審閱報價" (Pending Quotes) card - LIGHT PURPLE background ❌
  - Card icons (發票, 工具, 借用, 設備, 維修請求) - PURPLE ❌
  - Card link text - PURPLE ❌
  - Card descriptions - Should remain GRAY (not purple)
- **Expected**:
  - Card background: `--custom-primary-light`
  - Icons: `--custom-primary`
  - Link text: `--custom-primary`
  - Descriptions: GRAY (unchanged)

### 4. Backend Navbar (To Be Fixed)
- **Issue**: Previous fix incorrectly changed ALL navbar text color
- **Expected**:
  - Navbar background: Custom color
  - Text on navbar: Should follow Odoo's default contrast logic
  - Do NOT override text color unless it was originally purple

## Technical Analysis

### CSS Selectors Needed for Login Page

```css
/* Login page links - Odoo uses these classes */
.oe_login_form a,
.oe_login_form .oe_login_link,
a.oe_login_link,
.oe_reset_password_link,
.oe_signup_form a,
form.oe_login_form a:not(.btn) {
    color: var(--custom-primary) !important;
}
```

### CSS Selectors Needed for Portal Page

```css
/* Portal stat card background */
.o_portal_my_home .o_portal_my_doc_table,
.o_portal_my_home .o_portal_doc_card,
.o_portal_docs .card,
.o_portal_my_home .card.bg-100 {
    background-color: var(--custom-primary-light) !important;
}

/* Portal card icons */
.o_portal_my_home .o_portal_doc_card .fa,
.o_portal_my_home .o_portal_doc_card .oi,
.o_portal_my_home .card-body i,
.o_portal_my_home .o_portal_doc_spinner {
    color: var(--custom-primary) !important;
}

/* Portal card links (titles only, not descriptions) */
.o_portal_my_home .o_portal_doc_card a,
.o_portal_my_home .card-body a.h5,
.o_portal_my_home .card-body .card-title a {
    color: var(--custom-primary) !important;
}
```

### Fix Navbar Text Override

**Remove these incorrect rules** (from main.py and color_overrides.scss):
```css
/* REMOVE - This incorrectly changes black text to custom color */
.o_main_navbar .o_menu_brand,
.o_main_navbar .o_nav_entry,
.o_main_navbar .dropdown-toggle,
.o_main_navbar button,
.o_main_navbar a {
    color: var(--custom-primary-text) !important;
}
```

**Keep only**:
```css
/* Navbar BACKGROUND should use custom color */
.o_main_navbar {
    background-color: var(--custom-primary) !important;
}

/* Apps menu dropdown background */
.o_main_navbar .o_navbar_apps_menu .dropdown-toggle {
    background: var(--custom-primary) !important;
}
```

## Implementation Plan

### Step 1: Remove Incorrect Navbar Overrides
- File: `controllers/main.py`
- File: `static/src/scss/color_overrides.scss`
- Action: Remove all `.o_main_navbar` text color overrides
- Keep: Background color overrides only

### Step 2: Add Login Page Selectors
- File: `controllers/main.py` (frontend.css endpoint)
- Add: Login form link selectors

### Step 3: Add Portal Page Selectors
- File: `controllers/main.py` (frontend.css endpoint)
- Add: Portal card, icon, and link selectors

### Step 4: Verify PWA Theme Color
- File: `views/website_templates.xml`
- Ensure: `<meta name="theme-color">` is properly injected
- Check: Inheritance from `web.frontend_layout` works for login page

### Step 5: Test All Pages
- `/web/login` - Login page
- `/my/home` - Portal home
- `/web` - Backend
- PWA installed mode

## Success Criteria

1. PWA title bar shows custom color
2. Login page links use custom color (not purple)
3. Portal cards use light custom color background
4. Portal icons and link text use custom color
5. Black/gray text remains unchanged everywhere
6. Backend navbar shows custom background with proper text contrast

## Files to Modify

1. `controllers/main.py` - Update CSS rules
2. `static/src/scss/color_overrides.scss` - Remove navbar text overrides
3. `views/website_templates.xml` - Verify theme-color injection

## Testing Checklist

- [ ] PWA theme-color shows custom color
- [ ] Login: "選擇使用者" link is custom color
- [ ] Login: "重設新密碼" link is custom color
- [ ] Login: "還沒有帳戶？" link is custom color
- [ ] Portal: Stat card background is light custom color
- [ ] Portal: Card icons are custom color
- [ ] Portal: Card link titles are custom color
- [ ] Portal: Card descriptions remain gray
- [ ] Backend: Navbar background is custom color
- [ ] Backend: Navbar text is readable (proper contrast)
- [ ] No purple (#714B67, #71639e) visible anywhere
