---
name: color-customizer-bugfix
status: backlog
created: 2026-01-07T05:43:25Z
updated: 2026-01-07T05:44:53Z
progress: 0%
prd: .claude/prds/color-customizer-bugfix.md
github: [Will be updated when synced to GitHub]
---

# Epic: Color Customizer Bug Fixes

## Overview

Fix two critical bugs in the `odoo_color_customizer` Odoo 18 module:
1. **Wrong default color**: Module uses `#714B67` (Enterprise) instead of `#71639e` (Community)
2. **Incomplete coverage**: Some purple elements not overridden when color changes

The fix is straightforward: update the hardcoded default color constant in 3 files and verify CSS selectors cover all purple elements identified in the investigation.

## Architecture Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Default Color | `#71639e` | Verified from Odoo 18 source (`$o-community-color`) and live clean server |
| Fix Approach | Constant update + CSS audit | Minimal code change, maximum impact |
| Testing | Playwright headed mode | Visual verification against clean Odoo server |
| Rollback | Git revert | Simple rollback via git checkout |

## Technical Approach

### Root Cause
The module hardcodes `DEFAULT_PRIMARY_COLOR = '#714B67'` in two Python files. This is the **Enterprise** color, but Odoo 18 Community uses `#71639e`.

### Fix Strategy

**File Changes Required:**

1. **`controllers/main.py`** (line 10):
   - Change: `DEFAULT_PRIMARY_COLOR = '#714B67'` → `'#71639e'`

2. **`models/res_config_settings.py`** (line 9):
   - Change: `DEFAULT_PRIMARY_COLOR = '#714B67'` → `'#71639e'`

3. **`static/src/scss/color_overrides.scss`** (lines 11-15):
   - Update fallback color values to match new default

### CSS Coverage Verification

The current CSS selectors should already cover the necessary elements. The investigation confirmed these elements need to be purple-themed:
- `.o_main_navbar` ✓ (covered)
- `.btn-primary` ✓ (covered)
- `.form-check-input:checked` ✓ (covered)
- `.badge.bg-primary` ✓ (covered)
- `.text-primary` ✓ (covered)

**Elements that should NOT be overridden** (already correct):
- Section headers (gray `#e9ecef`) - not targeted by CSS

## Implementation Strategy

### Phase 1: Fix Default Color (Tasks 1-2)
- Update Python constants
- Update SCSS fallback values

### Phase 2: Deploy & Test (Task 3)
- Deploy to test server
- Playwright headed mode testing
- Compare against clean Odoo server

### Mandatory Bug Resolution Process

Per PRD requirements, follow the 5-step process:
1. **Research** - COMPLETED (root cause identified in PRD)
2. **Plan** - This epic serves as the fix plan
3. **Review** - Validate plan covers all requirements
4. **Implement** - Execute code changes
5. **Deploy Test** - Playwright headed mode verification

## Task Breakdown

| # | Task | Description | Files | Effort |
|---|------|-------------|-------|--------|
| 1 | Fix default color constants | Update `#714B67` → `#71639e` in Python files | `controllers/main.py`, `models/res_config_settings.py` | S |
| 2 | Update SCSS fallback values | Update fallback colors in SCSS to match new default | `static/src/scss/color_overrides.scss` | S |
| 3 | Deploy and test | Deploy to test server, Playwright headed mode testing against clean Odoo | - | M |

### Task Dependencies
```
Task 1 (Python) ──┬──▶ Task 3 (Deploy & Test)
Task 2 (SCSS) ────┘
```

Tasks 1 and 2 can run in parallel, Task 3 requires both to complete.

## Dependencies

### Internal
- Existing module files (already implemented)
- PRD research findings (completed)

### External
- Test server: https://matt-test-254-odoo.woowtech.io/
- Clean Odoo reference: https://matt-test-6-odoo.woowtech.io/
- SSH access: `ssh ha-192-168-2-254`

## Success Criteria (Technical)

| Criteria | Validation Method |
|----------|-------------------|
| Default color is `#71639e` | Code inspection |
| Reset matches clean Odoo | Visual comparison via Playwright |
| All purple elements themed | Playwright screenshot comparison |
| Section headers stay gray | Visual verification |
| No console errors | Browser DevTools check |

## Estimated Effort

| Task | Effort |
|------|--------|
| Task 1: Fix Python constants | 5 min |
| Task 2: Update SCSS fallbacks | 5 min |
| Task 3: Deploy and test | 30 min |
| **Total** | ~40 min |

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Fix doesn't resolve issue | Rollback via `git checkout HEAD~1`, return to research |
| CSS selectors insufficient | Add missing selectors based on Playwright findings |
| Deployment fails | Use alternative tar-based deployment method |

## Rollback Procedure

If Playwright testing fails:
```bash
# Revert code changes
git checkout HEAD~1 -- odoo_color_customizer/

# Re-deploy
scp -r odoo_color_customizer/ ha-192-168-2-254:/addon_configs/local_odoo/odoo_custom_addons/
ssh ha-192-168-2-254 "docker exec addon_local_odoo supervisorctl restart odoo"
```

## Tasks Created

| # | Task | Parallel | Depends On | Size |
|---|------|----------|------------|------|
| 001 | Fix default color constants in Python files | Yes | - | S |
| 002 | Update SCSS fallback color values | Yes | - | S |
| 003 | Deploy and test with Playwright headed mode | No | 001, 002 | M |

### Summary
- **Total tasks**: 3
- **Parallel tasks**: 2 (tasks 001, 002 can run simultaneously)
- **Sequential tasks**: 1 (task 003 depends on 001+002)
- **Estimated total effort**: ~1 hour

### Execution Order
```
001 (Python constants) ──┬──▶ 003 (Deploy & Test)
002 (SCSS fallbacks) ────┘
```

## Notes

- This is a minimal, surgical fix - only changing the hardcoded color constant
- The existing CSS coverage appears sufficient based on PRD investigation
- Section headers are intentionally gray and should NOT be themed
- All testing must be done with Playwright in headed mode per PRD requirements
