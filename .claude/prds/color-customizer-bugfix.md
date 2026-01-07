---
name: color-customizer-bugfix
description: Fix critical bugs in odoo_color_customizer module - incorrect default color and incomplete coverage
status: backlog
created: 2026-01-07T04:58:16Z
updated: 2026-01-07T05:20:38Z
---

# PRD: Color Customizer Bug Fixes

## Executive Summary

The `odoo_color_customizer` Odoo 18 module has critical bugs that prevent it from functioning correctly in production. The module uses the **wrong default color** (`#714B67` Enterprise color instead of `#71639e` Community color), causing the reset function to produce a different appearance than a clean Odoo installation. Additionally, some UI elements are not properly overridden when changing colors. This PRD defines the requirements to fix all known bugs and ensure 100% functionality.

## Problem Statement

### What problem are we solving?

The color customizer module is broken in two major ways:

1. **Wrong Default Color**: The module uses `#714B67` (Odoo Enterprise purple) as the default, but Odoo 18 Community Edition uses `#71639e` as its actual default color. This causes reset to look different from a clean installation.

2. **Incomplete Color Coverage**: When users change the primary color (e.g., to red #ff0000), some UI sections still show the original purple color, creating an inconsistent appearance.

### Root Cause Analysis (From Investigation)

**Critical Finding from Odoo 18 Source Code** (`primary_variables.scss`):
```scss
$o-community-color: #71639e !default;   // <-- Actual Community default
$o-enterprise-color: #714B67 !default;  // <-- What module incorrectly uses

$o-brand-odoo: $o-community-color !default;
$o-brand-primary: $o-community-color !default;
```

The current module hardcodes `#714B67` everywhere, which is the **Enterprise** color, not the Community color that Odoo 18 Community Edition actually uses.

### Why is this important now?

- The module is currently unusable in production environments
- Reset function produces visibly different results from clean Odoo
- Users cannot trust the module to match their Odoo's actual default appearance
- These bugs undermine user confidence and prevent adoption

### Evidence from Screenshots

| Screenshot | Issue Observed |
|------------|----------------|
| `after_change_color.png` | Color changed to red (#ff0000) but some sections may still show purple |
| `after_reset_to_default.png` | After reset shows #714B67 (Enterprise purple) |
| `another_odoo_server_never_install_module.png` | Clean Odoo shows #71639e (Community purple) - visibly different |

## Technical Investigation Results

### Verified Odoo 18 Community Default Colors

From live testing on clean Odoo server (matt-test-6-odoo.woowtech.io):

| Color | Hex Value | RGB Value | Usage |
|-------|-----------|-----------|-------|
| **Primary Purple** | `#71639e` | `rgb(113, 99, 158)` | Navbar, buttons, links |
| **Primary Hover** | `#66598f` | `rgb(102, 89, 143)` | Hover states |

### Elements Using Default Purple Color (Verified)

From browser inspection of clean Odoo 18 Community:

**Background Color (`rgb(113, 99, 158)`):**
1. `.o_main_navbar` - Main navigation bar
2. `.btn-primary` - Primary buttons (Save, Invite, New, etc.)
3. `.o-dropdown.dropdown-toggle` - Dropdown toggles in navbar
4. `.o_searchview_facet_label` - Search filter badges
5. `.form-check-input:checked` - Checked checkboxes/radios
6. `.badge.text-bg-primary` - Primary badges (like "Enterprise" label)

**Text/Border Color (`rgb(113, 99, 158)` or `rgb(102, 89, 143)`):**
1. `.text-primary` - Primary text color utility
2. `.btn-link` with primary styling - Link-style buttons
3. `.o-mail-ActivityButton` - Activity buttons
4. Search facet borders
5. Active view switcher borders

### Elements NOT Using Purple (Should NOT Be Overridden)

**Gray Section Headers** (`rgb(233, 236, 239)` / `#e9ecef`):
- Settings page section headers (Users, Languages, Companies, etc.)
- These are **intentionally gray**, NOT purple - do NOT override

**Other Non-Purple Elements:**
- Developer mode links (these are special action links)
- General text content
- Most borders and dividers

## User Stories

### US1: Correct Default Color
**As a** Odoo 18 Community user
**I want** the module to use the correct default color (#71639e)
**So that** reset produces the same appearance as a clean Odoo installation

**Acceptance Criteria:**
- [ ] Default color constant changed from `#714B67` to `#71639e`
- [ ] Reset function produces identical appearance to clean Odoo
- [ ] No visual difference between "reset" state and "never installed module"

### US2: Complete Color Application
**As a** company administrator
**I want** the primary color change to apply to ALL purple UI elements
**So that** my company's branding is consistent throughout the interface

**Acceptance Criteria:**
- [ ] Navbar background uses custom color
- [ ] All `.btn-primary` buttons use custom color
- [ ] Search facet badges use custom color
- [ ] Checked checkboxes/radios use custom color
- [ ] Primary badges use custom color
- [ ] Link buttons with primary styling use custom color
- [ ] No purple (`#71639e`) remains visible after color change

### US3: Preserve Non-Purple Elements
**As a** user
**I want** non-purple UI elements to remain unchanged
**So that** the interface looks correct and professional

**Acceptance Criteria:**
- [ ] Gray section headers remain gray (NOT overridden to custom color)
- [ ] Non-primary buttons retain their original styling
- [ ] General text and borders are not affected

## Requirements

### Functional Requirements

#### FR1: Correct Default Color Value
Update all hardcoded default color values:

**Files to Update:**
1. `controllers/main.py`: `DEFAULT_PRIMARY_COLOR = '#71639e'`
2. `models/res_config_settings.py`: `DEFAULT_PRIMARY_COLOR = '#71639e'`
3. `static/src/scss/color_overrides.scss`: Update fallback values

#### FR2: Complete CSS Coverage for Purple Elements

The SCSS/CSS must override these specific purple elements:

**Navbar & Header:**
- `.o_main_navbar` - background color
- `.o-dropdown.dropdown-toggle.dropdown` in navbar - background

**Buttons:**
- `.btn-primary` - all states (normal, hover, active, disabled)
- `.btn-outline-primary` - all states
- `.o-kanban-button-new` - Kanban "New" button

**Form Elements:**
- `.form-check-input:checked` - checked state background and border
- `.form-check-input:focus` - focus ring

**Search & Filters:**
- `.o_searchview_facet_label` - filter badge background
- `.o_searchview` border when focused
- `.o_searchview_dropdown_toggler` border

**Badges:**
- `.badge.text-bg-primary` - background
- `.badge.bg-primary` - background

**View Switchers:**
- `.o_switch_view.active` - border color

**Links & Text:**
- `.text-primary` - text color
- Activity button colors

#### FR3: Do NOT Override These Elements

**Explicitly exclude from overrides:**
- Section headers (h2 elements in settings) - these are gray, not purple
- `.o_settings_container h2` - keep default gray background
- Developer mode links - keep default styling
- Non-primary button variants

#### FR4: Reset to True Default
When reset is triggered:

1. Set color parameter to `#71639e` (correct Community default)
2. CSS endpoint returns the default color values
3. UI should be visually identical to clean Odoo installation

### Non-Functional Requirements

#### NFR1: Performance
- CSS file should be under 10KB
- No perceptible delay when loading theme
- Live preview updates should feel instant (<100ms)

#### NFR2: Compatibility
- Must work with Odoo 18 Community Edition
- Must work in Chrome, Firefox, Safari, Edge
- Must not conflict with other Odoo modules

#### NFR3: Maintainability
- Use CSS custom properties for easy value propagation
- Document which elements are intentionally NOT overridden
- Keep selectors specific but not overly fragile

## Success Criteria

### SC1: Reset Accuracy Test
After clicking "Reset to Default":
- Visual comparison against clean Odoo installation shows identical appearance
- Navbar color matches exactly: `rgb(113, 99, 158)` / `#71639e`
- Pass rate: 100% visual match

### SC2: Color Change Test
After changing primary color to red (#ff0000):
- All purple elements now show red
- Gray elements (section headers) remain gray
- No residual purple visible
- Pass rate: 100% of purple elements correctly themed

### SC3: Live Preview Test
When previewing colors:
- All visible purple elements update immediately
- Preview matches final saved result
- No flickering or partial updates

## Constraints & Assumptions

### Constraints

1. **Odoo 18 Specificity**: CSS selectors must work with Odoo 18's DOM structure
2. **No Core Modification**: Cannot modify Odoo core files
3. **Asset Bundling**: Must work within Odoo's asset compilation system
4. **CSS Specificity**: May need `!important` to override Odoo's default styles

### Assumptions

1. **Odoo 18 Community default is `#71639e`** (verified from source code and live server)
2. **Section headers are intentionally gray** (not a color to override)
3. The `/color_customizer/theme.css` endpoint approach is viable
4. Browser support for CSS custom properties is sufficient

## Out of Scope

The following are explicitly NOT part of this bugfix:

- Adding new color customization options (secondary color, accent color)
- Dark mode support
- Per-user color preferences
- Color scheme presets/templates
- PDF/report color customization
- Website/eCommerce frontend customization
- Color accessibility validation/warnings

## Dependencies

### Internal Dependencies
- Existing module structure (models, controllers, views, static assets)
- Odoo's `ir.config_parameter` for storing settings

### External Dependencies
- Odoo 18 Community Edition
- Odoo's asset bundling (`web.assets_backend`)

## Appendix

### A1: Correct Color Variables (After Fix)
```css
:root {
  --custom-primary: #71639e;           /* Changed from #714B67 */
  --custom-primary-hover: #66598f;     /* Recalculated */
  --custom-primary-active: #5b4f80;    /* Recalculated */
  --custom-primary-light: #eeedF2;     /* Recalculated */
  --custom-primary-text: #ffffff;
}
```

### A2: CSS Selectors to Override (Complete List)

```scss
// Navbar
.o_main_navbar { background-color: var(--custom-primary) !important; }

// Primary Buttons
.btn-primary {
  background-color: var(--custom-primary) !important;
  border-color: var(--custom-primary) !important;
}

// Search Facets
.o_searchview_facet_label { background-color: var(--custom-primary) !important; }

// Checkboxes/Radios
.form-check-input:checked {
  background-color: var(--custom-primary) !important;
  border-color: var(--custom-primary) !important;
}

// Badges
.badge.text-bg-primary,
.badge.bg-primary { background-color: var(--custom-primary) !important; }

// Text
.text-primary { color: var(--custom-primary) !important; }

// Active view switcher
.o_switch_view.active { border-color: var(--custom-primary) !important; }
```

### A3: Test Checklist
Manual testing checklist for verification:
- [ ] Compare reset state to clean Odoo server - should be identical
- [ ] Change to red (#ff0000) - verify navbar, buttons, badges change
- [ ] Verify section headers remain gray (not colored)
- [ ] Verify checkboxes/radios use custom color when checked
- [ ] Verify search filter badges use custom color
- [ ] Refresh page after change - verify persistence
- [ ] Clear browser cache - verify CSS loads correctly

### A4: Reference URLs
- Clean Odoo 18 Server: https://matt-test-6-odoo.woowtech.io/ (admin/admin)
- Test Server with Module: https://matt-test-254-odoo.woowtech.io/ (admin/admin)
