# Fix Plan: BUG FIX 17 - Form Tab Border Specificity Issue

## Date: 2026-01-09
## Bug ID: BUG-17 (supersedes incomplete BUG FIX 16)

## Problem Statement

Form tabs (notebook tabs) in Odoo still show purple primary color borders instead of neutral gray borders.

**Location:** https://matt-test-254-odoo.woowtech.io/odoo/sales/123 (any quotation/form)

**Current State:**
- `borderTopColor: rgb(113, 99, 158)` (purple) ❌
- Expected: `rgb(222, 226, 230)` (gray) ✅

## Root Cause Analysis

### 1. CSS Specificity Issue
The SCSS file `color_overrides.scss` has a rule with higher specificity than BUG FIX 16:

**SCSS Rule (4 class selectors):**
```scss
.o_form_view .o_notebook .nav-tabs .nav-item .nav-link.active {
    border-top-color: var(--custom-primary) !important;
}
```

**BUG FIX 16 Current Rule (3-4 class selectors):**
```css
.o_notebook .nav-tabs .nav-item .nav-link.active {
    border-top-color: #dee2e6 !important;
}
```

### 2. CSS Variable Override Needed
Odoo uses the CSS variable `--notebook-link-border-color-active-accent` which defaults to the primary color. This variable is applied via SCSS.

## Detailed CSS Rule Analysis

From `browser_evaluate` inspection of the active tab element:

```
Matched Rules (specificity order):
1. .o_form_view .o_notebook .nav-tabs .nav-item .nav-link.active
   - border-top-color: var(--custom-primary)
   - Source: SCSS cached asset

2. .o_notebook .nav-tabs .nav-link.active
   - border-top-color: #dee2e6  (our BUG FIX 16)
   - Source: dynamic CSS (/color_customizer/theme.css)
   - LOSES to higher specificity SCSS
```

## Fix Strategy

### Option A: Maximum Specificity Selector (Recommended)
Add more specificity to the dynamic CSS selector to beat SCSS:

```css
/* Need 5+ class selectors to beat SCSS's 4 */
html body .o_action .o_form_view .o_notebook .nav-tabs .nav-item .nav-link.active,
.o_web_client .o_action .o_form_view .o_notebook .nav-tabs .nav-item .nav-link.active {
    border-top-color: #dee2e6 !important;
    border-left-color: #dee2e6 !important;
    border-right-color: #dee2e6 !important;
    border-bottom-color: transparent !important;
}
```

### Option B: CSS Variable Override
Override the CSS variable at root level:

```css
:root {
    --notebook-link-border-color-active-accent: #dee2e6 !important;
}

.o_notebook {
    --notebook-link-border-color-active-accent: #dee2e6 !important;
}
```

### Option C: Combined Approach (Most Robust)
Use both CSS variable override AND high-specificity selectors for maximum reliability.

## Implementation Plan

### Step 1: Update BUG FIX 16 in main.py

Replace current BUG FIX 16 with enhanced version:

```python
/* ============================================================================
   BUG FIX 16 (Enhanced): Form tabs (notebook) should NOT have primary color borders
   Original Odoo has gray borders: rgb(222, 226, 230) for top/sides
   Using CSS variable override + maximum specificity selectors
   ============================================================================ */

/* Override CSS variable that SCSS uses */
:root {{
    --notebook-link-border-color-active-accent: #dee2e6 !important;
}}

.o_notebook {{
    --notebook-link-border-color-active-accent: #dee2e6 !important;
}}

/* Maximum specificity selectors to beat SCSS cached rules */
html body .o_action .o_form_view .o_notebook .nav-tabs .nav-item .nav-link.active,
.o_web_client .o_action .o_form_view .o_notebook .nav-tabs .nav-item .nav-link.active,
.o_action_manager .o_form_view .o_notebook .nav-tabs .nav-item .nav-link.active,
.o_form_view .o_notebook .nav-tabs .nav-item .nav-link.active {{
    border-top-color: #dee2e6 !important;
    border-left-color: #dee2e6 !important;
    border-right-color: #dee2e6 !important;
    border-bottom-color: transparent !important;
}}
```

### Step 2: Deploy
```bash
cd /mnt/c/Users/Matt/Desktop/CLAUDE專案/ODOO相關/odoo_color_customizer && \
tar czf - odoo_color_customizer | \
ssh ha-192-168-2-254 "cd /addon_configs/local_odoo/odoo_custom_addons && rm -rf odoo_color_customizer && tar xzf -"
```

### Step 3: Restart Odoo
```bash
ssh ha-192-168-2-254 "docker restart addon_local_odoo"
```

### Step 4: Verify with Playwright
```javascript
// Check form tab borderTopColor
await page.goto('https://matt-test-254-odoo.woowtech.io/odoo/sales');
// Click on a quotation
// Check .nav-link.active element
const borderColor = await page.evaluate(() => {
    const tab = document.querySelector('.o_notebook .nav-link.active');
    return getComputedStyle(tab).borderTopColor;
});
// Expected: "rgb(222, 226, 230)"
```

## Verification Checklist

After deployment:
- [ ] Form tab `borderTopColor` is `rgb(222, 226, 230)` (gray)
- [ ] Form tab `borderLeftColor` is `rgb(222, 226, 230)` (gray)
- [ ] Form tab `borderRightColor` is `rgb(222, 226, 230)` (gray)
- [ ] Form tab `borderBottomColor` is `transparent` or `rgb(255, 255, 255)`
- [ ] Matches Original Odoo server appearance

## Rollback Plan

If fix fails:
```bash
git checkout HEAD~1 -- odoo_color_customizer/controllers/main.py
# Re-deploy
```

## Related Bugs

- BUG FIX 16 (incomplete) - Initial attempt, insufficient specificity
- Bug 1 (search box-shadow) - FIXED in this session
