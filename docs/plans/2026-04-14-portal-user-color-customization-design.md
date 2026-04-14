# Portal User Color Customization Design

**Date:** 2026-04-14
**Status:** Approved

## Summary

Extend the brand color customization from internal users only to **all users** (internal, portal, public/unauthenticated). The admin picks one color in Settings, and it applies everywhere — including portal pages, login/signup pages, and mobile views.

## Requirements

- Portal users see the same brand color as internal users (single `primary_color` setting)
- All portal pages covered: account home, quotations, invoices, projects, tasks, signatures
- Login/signup pages also apply the brand color (public users)
- Mobile portal pages apply the brand color (hamburger menu, responsive elements)
- The "mobo FullSuite" native app header is **out of scope** (not a web element)

## Changes Required

### 1. `views/web_templates.xml`
Remove the `t-if="request.env.user.has_group('base.group_user')"` condition so CSS is injected for all users.

### 2. `controllers/main.py` — `/color_customizer/frontend.css` endpoint
Add CSS rules for portal-specific UI elements:
- Navbar (`.o_frontend_header`, `nav.navbar`)
- Portal home icons and cards (`.o_portal_my_home`)
- Portal sidebar, pagination, badges
- Buttons (`.btn-primary`, `.btn-outline-primary`) in frontend context
- Links (`<a>` tags)
- Login/signup page buttons and form focus states
- Footer links
- Mobile hamburger menu and sidebar

### 3. Documentation
Update README.md and README_zh-TW.md to reflect the new behavior.

## Files NOT Modified

- `models/res_config_settings.py` — No new fields needed
- `static/src/js/color_customizer.js` — Backend JS, not relevant to frontend
- `static/src/scss/color_overrides.scss` — Backend SCSS, not relevant to frontend
