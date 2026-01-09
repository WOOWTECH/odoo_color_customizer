# Fix Plan: BUG FIX 18 - Tax Badge Color Bug

## Date: 2026-01-09
## Bug ID: BUG-18

## Problem Statement

Tax badges in quotations (and other many2many tag fields) incorrectly show primary color instead of neutral gray color.

**Location:** https://matt-test-254-odoo.woowtech.io/odoo/sales/{id} (any quotation with products)

**Element:** Tax field "15%" badge in quotation order lines

## Visual Comparison

| Element | Original Odoo | Color Customizer |
|---------|---------------|------------------|
| `span.o_tag.o_tag_color_0` backgroundColor | `rgb(230, 221, 221)` (gray) ✅ | `rgb(233, 231, 240)` (light purple) ❌ |
| `span.o_tag.o_tag_color_0` color | `rgb(60, 60, 60)` (dark gray) ✅ | `rgb(113, 99, 158)` (purple) ❌ |
| `div.o_tag_badge_text` backgroundColor | `rgba(0, 0, 0, 0)` (transparent) ✅ | `rgb(113, 99, 158)` (purple) ❌ |
| `div.o_tag_badge_text` color | `rgb(60, 60, 60)` (dark gray) ✅ | `rgb(255, 255, 255)` (white) ❌ |

## Root Cause Analysis

### HTML Structure of Tax Badge
```html
<span class="o_tag position-relative d-inline-flex align-items-center user-select-none mw-100 o_badge badge rounded-pill lh-1 o_tag_color_0" tabindex="-1" title="15%">
  <div class="o_tag_badge_text text-truncate">15%</div>
</span>
```

### Problematic CSS Rules in `color_overrides.scss`

**Root Cause 1 (lines 351-355):**
```scss
// Default tags use color_0 which is the primary/purple color
.o_tag.o_tag_color_0 {
  background-color: var(--custom-primary-light) !important;
  color: var(--custom-primary) !important;
}
```
**Problem:** WRONG ASSUMPTION! `o_tag_color_0` is NOT the primary/purple color in Odoo. It's actually a neutral gray/beige color (`rgb(230, 221, 221)`).

**Root Cause 2 (lines 357-362):**
```scss
// Solid/filled tags
.o_tag.rounded-pill,
.o_tag_badge_text {
  background-color: var(--custom-primary) !important;
  color: var(--custom-primary-text) !important;
}
```
**Problem:** TOO BROAD! This applies to ALL `.o_tag_badge_text` elements and ALL `.o_tag.rounded-pill` elements. The tax badge has both classes, causing it to incorrectly get primary color.

**Root Cause 3 (lines 364-368):**
```scss
// Many2many tags in form view
.o_field_many2many_tags .o_tag.o_tag_color_0 {
  background-color: var(--custom-primary-light) !important;
  color: var(--custom-primary) !important;
}
```
**Problem:** Same wrong assumption - `o_tag_color_0` is not the primary color.

## Understanding Odoo's Tag Color System

Odoo uses a color system for tags with `o_tag_color_X` classes (X = 0-11):
- `o_tag_color_0` = Neutral gray/beige (NOT primary!)
- `o_tag_color_1` = Orange
- `o_tag_color_2` = Green
- ... and so on

The primary/brand color is applied through different mechanisms:
- `.badge.bg-primary` - Bootstrap primary badge
- `.o_enterprise_label` - Enterprise badge
- `.text-primary` - Primary text color

## Fix Strategy

**REMOVE** the overly broad rules that incorrectly apply primary color to neutral tags.

### Files to Modify
`odoo_color_customizer/static/src/scss/color_overrides.scss`

### Changes Required

**Remove lines 351-368** (the three problematic rule blocks):
```scss
// DELETE THIS SECTION:
// Default tags use color_0 which is the primary/purple color
.o_tag.o_tag_color_0 {
  background-color: var(--custom-primary-light) !important;
  color: var(--custom-primary) !important;
}

// Solid/filled tags
.o_tag.rounded-pill,
.o_tag_badge_text {
  background-color: var(--custom-primary) !important;
  color: var(--custom-primary-text) !important;
}

// Many2many tags in form view
.o_field_many2many_tags .o_tag.o_tag_color_0 {
  background-color: var(--custom-primary-light) !important;
  color: var(--custom-primary) !important;
}
```

## Implementation Steps

### Step 1: Edit SCSS file
Remove the problematic CSS rules (lines 351-368)

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
// Navigate to Quotation page
await page.goto('https://matt-test-254-odoo.woowtech.io/odoo/sales/{id}');

// Check tax badge colors
const result = await page.evaluate(() => {
  const taxBadge = document.querySelector('.o_tag.o_tag_color_0[title="15%"]');
  const innerDiv = taxBadge.querySelector('.o_tag_badge_text');
  return {
    spanBg: getComputedStyle(taxBadge).backgroundColor,
    spanColor: getComputedStyle(taxBadge).color,
    innerBg: getComputedStyle(innerDiv).backgroundColor,
    innerColor: getComputedStyle(innerDiv).color
  };
});

// Expected values (matching Original Odoo):
// spanBg: "rgb(230, 221, 221)" or similar gray
// spanColor: "rgb(60, 60, 60)" or similar dark gray
// innerBg: "rgba(0, 0, 0, 0)" (transparent)
// innerColor: "rgb(60, 60, 60)" or similar dark gray
```

## Verification Checklist

After deployment:
- [ ] Tax badge "15%" has gray/neutral background (NOT purple)
- [ ] Tax badge "15%" has dark gray text (NOT white)
- [ ] Tax badge inner div has transparent background (NOT purple)
- [ ] Matches Original Odoo server appearance
- [ ] Other primary color elements still work correctly (navbar, buttons, etc.)

## Potential Side Effects to Monitor

Removing these rules might affect:
1. "Pending Invitations" badges - need to verify they still look correct
2. Other many2many tag fields - should now use their natural Odoo colors

These should actually be IMPROVEMENTS since we're restoring Odoo's default tag color behavior.

## Rollback Plan

If fix causes issues:
```bash
git checkout HEAD~1 -- odoo_color_customizer/static/src/scss/color_overrides.scss
# Re-deploy
```
