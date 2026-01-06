---
name: odoo-color-customizer
status: backlog
created: 2026-01-06T16:34:33Z
updated: 2026-01-06T16:46:18Z
progress: 0%
prd: .claude/prds/odoo-color-customizer.md
github: [Will be updated when synced to GitHub]
---

# Epic: Odoo Color Customizer Module

## Overview

Implement an Odoo 18 module that enables system administrators to replace the default Odoo purple (`#714B67`) with a custom primary color. The solution leverages CSS custom properties for real-time color application without page reload or SCSS recompilation.

**Key Simplification**: Instead of building complex custom widgets, we'll use Odoo's built-in color field type and extend it minimally. The CSS injection uses a simple controller endpoint that returns dynamic CSS based on stored system parameters.

## Architecture Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Color Storage | `ir.config_parameter` | Standard Odoo pattern for system-wide settings |
| Color Field | Odoo `Char` field with color widget | Reuse existing Odoo color picker, no custom JS needed |
| CSS Injection | Controller returning CSS | Lightweight, cacheable, no asset rebuild |
| Live Preview | JavaScript CSS variable update | Minimal JS, leverages browser's native CSS variable support |
| Settings Location | `res.config.settings` | Standard location for system configuration |

## Technical Approach

### Simplified Architecture
```
┌──────────────────────────────────────────────────────────────┐
│                     Odoo 18 Web Client                        │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  Settings Page              CSS Override (injected on load)   │
│  ┌─────────────────┐       ┌─────────────────────────────┐   │
│  │ [Color Picker]  │──────▶│ <style id="color-override"> │   │
│  │  #FF5733        │  JS   │ :root { --primary: #FF5733 }│   │
│  │ [Reset Default] │       │ </style>                     │   │
│  └─────────────────┘       └─────────────────────────────┘   │
│          │                              ▲                     │
│          ▼                              │                     │
│  ┌─────────────────┐       ┌─────────────────────────────┐   │
│  │ ir.config       │       │ /color_customizer/theme.css │   │
│  │ _parameter      │◀──────│ (Controller endpoint)        │   │
│  │ primary_color   │       └─────────────────────────────┘   │
│  └─────────────────┘                                          │
└──────────────────────────────────────────────────────────────┘
```

### Components (Minimal)

1. **`__manifest__.py`** - Module definition, depends on `base_setup`, `web`
2. **`models/res_config_settings.py`** - Extends settings with color field
3. **`views/res_config_settings_views.xml`** - Adds color picker to Settings UI
4. **`controllers/main.py`** - Serves dynamic CSS with color variables
5. **`static/src/js/color_customizer.js`** - Live preview + CSS injection on load
6. **`static/src/scss/color_overrides.scss`** - CSS variable definitions and overrides

### CSS Variables Strategy

Override these Odoo 18 CSS variables:
```css
:root {
  --o-brand-odoo: var(--custom-primary, #714B67);
  --o-brand-primary: var(--custom-primary, #714B67);
  --primary: var(--custom-primary, #714B67);
}
```

**Calculated variants** (generated server-side):
- `--custom-primary-hover`: Darken 10%
- `--custom-primary-active`: Darken 20%
- `--custom-primary-light`: Lighten 85%
- `--custom-primary-text`: White or black based on contrast

## Implementation Strategy

### Phase 1: Core Functionality (Tasks 1-4)
- Module structure and manifest
- Settings model and view
- Controller for CSS generation
- Basic CSS variable overrides

### Phase 2: Live Preview & Polish (Tasks 5-6)
- JavaScript for live color updates
- Complete CSS coverage for all UI elements

### Phase 3: Testing & Validation (Tasks 7-8)
- Playwright automated testing
- Manual verification across views

## Task Breakdown

| # | Task | Description | Files | Parallel Group |
|---|------|-------------|-------|----------------|
| 1 | Module scaffold | Create module structure, manifest, `__init__.py` | `__manifest__.py`, `__init__.py`, `models/__init__.py` | A |
| 2 | Settings model | Extend `res.config.settings` with color field | `models/res_config_settings.py` | A |
| 3 | Settings view | Add color picker to General Settings UI | `views/res_config_settings_views.xml` | B |
| 4 | CSS controller | Create endpoint returning dynamic CSS | `controllers/__init__.py`, `controllers/main.py` | A |
| 5 | CSS overrides | Define all CSS variable overrides | `static/src/scss/color_overrides.scss` | B |
| 6 | Live preview JS | JavaScript for real-time color updates | `static/src/js/color_customizer.js` | B |
| 7 | Integration test | Playwright tests for all scenarios | `tests/` (Playwright MCP) | - |
| 8 | Documentation | README, inline docs, usage guide | `README.md`, code comments | - |

### Task Dependencies
```
Task 1 (Scaffold) ──┬──▶ Task 2 (Model) ──▶ Task 4 (Controller)
                    │
                    └──▶ Task 3 (View) ──┬──▶ Task 5 (CSS)
                                         │
                                         └──▶ Task 6 (JS)
                                                   │
                                                   ▼
                                            Task 7 (Test)
                                                   │
                                                   ▼
                                            Task 8 (Docs)
```

### Parallel Execution Plan
- **Group A** (Backend): Tasks 1, 2, 4 - Sequential
- **Group B** (Frontend): Tasks 3, 5, 6 - Can parallel with Group A after Task 1
- **Sequential**: Tasks 7, 8 - After all above complete

## Dependencies

### Internal (Odoo Modules)
- `base` - Core framework
- `base_setup` - Settings infrastructure
- `web` - Web client, CSS variables

### External
- None - Pure Odoo implementation

### Reference
- Odoo 18 Environment Architecture: `../Odoo_18_Environment_Architecture/`

## Success Criteria (Technical)

| Criteria | Metric | Validation |
|----------|--------|------------|
| Module installs | No errors | `odoo -i odoo_color_customizer` |
| Color picker works | Opens, selects colors | Manual test |
| Live preview | <100ms update | Browser DevTools |
| Persistence | Survives restart | Logout/login test |
| Coverage | >95% purple elements | Visual audit |
| Performance | <50ms load overhead | Network tab |
| No errors | Clean console | DevTools console |

## Estimated Effort

| Task | Complexity | Estimate |
|------|------------|----------|
| 1. Module scaffold | Low | Quick |
| 2. Settings model | Low | Quick |
| 3. Settings view | Low | Quick |
| 4. CSS controller | Medium | Moderate |
| 5. CSS overrides | Medium | Moderate |
| 6. Live preview JS | Medium | Moderate |
| 7. Integration test | Medium | Moderate |
| 8. Documentation | Low | Quick |

**Critical Path**: Tasks 1 → 2 → 4 → 6 → 7

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| CSS variables not applied | Test each Odoo view type individually |
| Color calculation errors | Use proven color manipulation library (or simple HSL math) |
| Settings not persisting | Verify `ir.config_parameter` write/read |
| Performance issues | Cache CSS output, minimize DOM operations |

## File Structure

```
odoo_color_customizer/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── res_config_settings.py
├── views/
│   └── res_config_settings_views.xml
├── controllers/
│   ├── __init__.py
│   └── main.py
├── static/
│   └── src/
│       ├── js/
│       │   └── color_customizer.js
│       └── scss/
│           └── color_overrides.scss
├── security/
│   └── ir.model.access.csv
└── README.md
```

## Deployment Environment

### Target Infrastructure
| Component | Details |
|-----------|---------|
| Host | Home Assistant (192.168.2.254) |
| Container | `addon_local_odoo` |
| Odoo Version | 18.0 |
| Config Path | `/addon_config/odoo/conf/odoo.conf` |
| Database | `odoo` |
| HTTP Port | 18070 |

### Access Commands

#### 1. SSH to Home Assistant
```bash
ssh ha-192-168-2-254
```

#### 2. Access Odoo Container (Interactive Shell)
```bash
docker exec -it addon_local_odoo /bin/bash
```

#### 3. Access Odoo Shell (Python REPL)
```bash
docker exec -it addon_local_odoo bash -lc \
  "odoo shell -c /addon_config/odoo/conf/odoo.conf -d odoo --http-port=18070"
```

### Deployment Steps

#### Step 1: Copy Module to Addons Path
```bash
# From local machine, copy module to Home Assistant
scp -r odoo_color_customizer ha-192-168-2-254:/tmp/

# SSH into Home Assistant
ssh ha-192-168-2-254

# Copy module into Docker container's addons path
docker cp /tmp/odoo_color_customizer addon_local_odoo:/opt/odoo/addons/
```

#### Step 2: Update Addons List
```bash
# Access Odoo shell
docker exec -it addon_local_odoo bash -lc \
  "odoo shell -c /addon_config/odoo/conf/odoo.conf -d odoo --http-port=18070"

# In Odoo shell, update apps list
>>> env['ir.module.module'].update_list()
>>> env.cr.commit()
>>> exit()
```

#### Step 3: Install Module
```bash
# Option A: Via Odoo shell
docker exec -it addon_local_odoo bash -lc \
  "odoo -c /addon_config/odoo/conf/odoo.conf -d odoo -i odoo_color_customizer --stop-after-init"

# Option B: Via Web UI
# Navigate to Apps > Update Apps List > Search "odoo_color_customizer" > Install
```

#### Step 4: Restart Odoo (if needed)
```bash
# Restart the Odoo container
docker restart addon_local_odoo
```

### Verification
```bash
# Check module is installed
docker exec -it addon_local_odoo bash -lc \
  "odoo shell -c /addon_config/odoo/conf/odoo.conf -d odoo --http-port=18070" << 'EOF'
module = env['ir.module.module'].search([('name', '=', 'odoo_color_customizer')])
print(f"Module state: {module.state}")
exit()
EOF
```

### Quick Deploy Script
```bash
#!/bin/bash
# deploy.sh - Deploy odoo_color_customizer to Home Assistant Odoo

set -e

MODULE_NAME="odoo_color_customizer"
HA_HOST="ha-192-168-2-254"
CONTAINER="addon_local_odoo"
ADDONS_PATH="/opt/odoo/addons"

echo "📦 Copying module to Home Assistant..."
scp -r ${MODULE_NAME} ${HA_HOST}:/tmp/

echo "🐳 Copying module into Docker container..."
ssh ${HA_HOST} "docker cp /tmp/${MODULE_NAME} ${CONTAINER}:${ADDONS_PATH}/"

echo "🔄 Updating addons list..."
ssh ${HA_HOST} "docker exec ${CONTAINER} bash -lc 'odoo -c /addon_config/odoo/conf/odoo.conf -d odoo -u ${MODULE_NAME} --stop-after-init'"

echo "✅ Deployment complete! Access Odoo at http://192.168.2.254:18070"
```

### Odoo Web Access

| Field | Value |
|-------|-------|
| **URL** | https://matt-test-254-odoo.woowtech.io/ |
| **Username** | `admin` |
| **Password** | `admin` |
| **Local URL** | http://192.168.2.254:18070 |
| **Settings Path** | Settings > General Settings > Color Customization |

## Notes

- **Leverage existing Odoo color widget** - Don't build custom color picker
- **Use CSS custom properties** - No SCSS compilation needed at runtime
- **Keep it simple** - 8 tasks max, focus on core functionality
- **Test with Playwright MCP** - Headed mode with screenshots per PRD
- **Deploy via Docker** - Use provided commands to deploy to Home Assistant Odoo

## Tasks Created

| # | Task | Parallel | Depends On | Size |
|---|------|----------|------------|------|
| 001 | Module Scaffold | No | - | S |
| 002 | Settings Model | Yes | 001 | S |
| 003 | Settings View | Yes | 001 | S |
| 004 | CSS Controller | Yes | 001, 002 | M |
| 005 | CSS Overrides | Yes | 001 | M |
| 006 | Live Preview JavaScript | Yes | 001, 004 | M |
| 007 | Integration Testing | No | 001-006 | M |
| 008 | Documentation | No | 007 | S |

### Summary
- **Total tasks**: 8
- **Parallel tasks**: 5 (tasks 002-006 can run in parallel groups)
- **Sequential tasks**: 3 (001, 007, 008)
- **Estimated total effort**: ~12 hours

### Execution Order
```
001 (Scaffold)
    ├──▶ 002 (Model) ──┬──▶ 004 (Controller) ──┐
    │                  │                        │
    ├──▶ 003 (View) ───┤                        ├──▶ 007 (Test) ──▶ 008 (Docs)
    │                  │                        │
    └──▶ 005 (CSS) ────┴──▶ 006 (JS) ──────────┘
```
