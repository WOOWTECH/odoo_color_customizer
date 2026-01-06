---
name: odoo-color-customizer
description: Odoo 18 module enabling system administrators to replace the default purple primary color with a custom color across the entire UI
status: backlog
created: 2026-01-06T16:12:26Z
updated: 2026-01-06T16:30:13Z
---

# PRD: Odoo Color Customizer Module

## Executive Summary

The **odoo_color_customizer** module enables Odoo 18 system administrators to replace the default Odoo purple (`#714B67`) primary color with a custom brand color across the entire web client interface. Changes apply in real-time using CSS custom properties, requiring no page reload. This allows organizations to align Odoo's appearance with their corporate branding without modifying core Odoo code.

## Problem Statement

### The Problem
Odoo's default purple color (`#714B67`) is deeply integrated throughout the web client UI—buttons, links, highlights, selections, and various UI components. Organizations using Odoo often need to match their corporate brand colors, but currently there is no user-friendly way to change this primary color without:
- Modifying SCSS source files directly
- Creating complex custom themes
- Rebuilding assets after every Odoo upgrade

### Why This Matters Now
- **Brand consistency**: Companies need their internal tools to reflect brand identity
- **User adoption**: Familiar brand colors improve user comfort and adoption rates
- **Maintenance burden**: Manual SCSS modifications break on Odoo upgrades
- **Odoo 18 opportunity**: Odoo 18's improved CSS variable support makes dynamic theming more feasible

## User Stories

### Primary Persona: System Administrator
**Role**: IT/System Administrator responsible for Odoo configuration
**Goal**: Customize Odoo's appearance to match corporate branding
**Pain Point**: No simple way to change primary color without developer intervention

#### User Story 1: Setting Primary Color
> As a **System Administrator**,
> I want to **select a custom primary color from a color picker**,
> So that **Odoo's UI matches our company's brand guidelines**.

**Acceptance Criteria:**
- [ ] Color picker widget accessible in General Settings
- [ ] Can select any color via visual picker or hex input
- [ ] Preview shows selected color before saving
- [ ] Color saves to system parameters

#### User Story 2: Immediate Visual Feedback
> As a **System Administrator**,
> I want to **see color changes applied immediately without page reload**,
> So that **I can quickly iterate to find the right shade**.

**Acceptance Criteria:**
- [ ] Color updates live as user adjusts picker
- [ ] All purple-themed elements update simultaneously
- [ ] No page refresh required
- [ ] Performance remains smooth during adjustment

#### User Story 3: Persistent Configuration
> As a **System Administrator**,
> I want **the custom color to persist across sessions and users**,
> So that **all users see the branded interface consistently**.

**Acceptance Criteria:**
- [ ] Color setting stored in ir.config_parameter
- [ ] Applied globally to all users
- [ ] Survives module updates and server restarts
- [ ] New user sessions load with custom color

#### User Story 4: Reset to Default
> As a **System Administrator**,
> I want to **easily reset to Odoo's default purple**,
> So that **I can revert changes if needed**.

**Acceptance Criteria:**
- [ ] "Reset to Default" button available
- [ ] Clicking resets to `#714B67`
- [ ] Confirmation prompt before reset

## Requirements

### Functional Requirements

#### FR1: Color Configuration Interface
| ID | Requirement | Priority |
|----|-------------|----------|
| FR1.1 | Add color picker field to Settings > General Settings | Must Have |
| FR1.2 | Color picker supports visual selection and hex input | Must Have |
| FR1.3 | Display current color preview swatch | Must Have |
| FR1.4 | Include "Reset to Default" button | Should Have |
| FR1.5 | Show hex value of selected color | Should Have |

#### FR2: CSS Variable Injection
| ID | Requirement | Priority |
|----|-------------|----------|
| FR2.1 | Override `--primary` CSS variable with selected color | Must Have |
| FR2.2 | Calculate and set complementary variables (hover states, shadows) | Must Have |
| FR2.3 | Inject styles via controller on page load | Must Have |
| FR2.4 | Apply changes dynamically without reload | Must Have |

#### FR3: Color Coverage
| ID | Requirement | Priority |
|----|-------------|----------|
| FR3.1 | Primary buttons (`.btn-primary`) | Must Have |
| FR3.2 | Links and interactive text | Must Have |
| FR3.3 | Navbar/header accents | Must Have |
| FR3.4 | Selection highlights | Must Have |
| FR3.5 | Form field focus states | Must Have |
| FR3.6 | Kanban card accents | Should Have |
| FR3.7 | Calendar event colors | Should Have |
| FR3.8 | Checkbox/radio accents | Should Have |

#### FR4: Data Persistence
| ID | Requirement | Priority |
|----|-------------|----------|
| FR4.1 | Store color in `ir.config_parameter` | Must Have |
| FR4.2 | Load color on session initialization | Must Have |
| FR4.3 | Handle missing/invalid values gracefully (fallback to default) | Must Have |

### Non-Functional Requirements

#### NFR1: Performance
- Color changes must render within 100ms
- No visible flicker on page load
- Minimal impact on initial page load time (<50ms overhead)

#### NFR2: Compatibility
- Compatible with Odoo 18 Community and Enterprise
- Works with standard Odoo themes
- No conflicts with common third-party modules

#### NFR3: Accessibility
- Ensure sufficient contrast ratios when custom color is applied
- Warn user if selected color may cause accessibility issues (WCAG AA)

#### NFR4: Security
- Only users with `Settings` access group can modify color
- Sanitize color input to prevent CSS injection

#### NFR5: Maintainability
- Use Odoo's standard module structure
- Leverage CSS custom properties (not SCSS compilation)
- Document all overridden CSS variables

## Technical Approach

### Architecture Overview
```
┌─────────────────────────────────────────────────────────┐
│                    Odoo Web Client                       │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌──────────────────────────────┐   │
│  │   Settings  │    │    CSS Variable Override     │   │
│  │   Color     │───▶│  :root { --primary: #xxx }   │   │
│  │   Picker    │    │  Injected via <style> tag    │   │
│  └─────────────┘    └──────────────────────────────┘   │
│         │                        ▲                      │
│         ▼                        │                      │
│  ┌─────────────┐    ┌──────────────────────────────┐   │
│  │  ir.config  │    │   /web/color_customizer/css  │   │
│  │  _parameter │◀───│   Controller endpoint        │   │
│  └─────────────┘    └──────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### Key Components

1. **Model Extension**: `res.config.settings` with color field
2. **System Parameter**: `odoo_color_customizer.primary_color`
3. **JS Widget**: Color picker with live preview
4. **Controller**: `/web/color_customizer/css` returns dynamic CSS
5. **Asset Bundle**: Injects CSS override on web client load

### CSS Variables to Override
```css
:root {
  --primary: #714B67;           /* Main purple - OVERRIDE THIS */
  --primary-hover: #5a3c52;     /* Calculated: darken 10% */
  --primary-active: #4a3244;    /* Calculated: darken 20% */
  --primary-light: #f0e8ed;     /* Calculated: lighten 90% */
  --primary-text: #ffffff;      /* Auto: white or black based on contrast */
}
```

## Testing Strategy

### Overview
All module functionality must be validated against a **live Odoo 18 instance** using **Playwright MCP in headed mode**. This enables real browser testing with visual verification and diagnostic screenshots.

### Test Environment

| Component | Requirement |
|-----------|-------------|
| Odoo Version | 18.0 (Community or Enterprise) |
| Browser | Chromium (headed mode for visual inspection) |
| Test Framework | Playwright MCP |
| Screenshots | Required for all test steps |

### Test Configuration
```javascript
// Playwright MCP headed mode configuration
{
  "browser": "chromium",
  "headless": false,  // MUST be headed for visual verification
  "viewport": { "width": 1920, "height": 1080 },
  "screenshotOnFailure": true,
  "screenshotDir": "./test-screenshots"
}
```

### Test Scenarios

#### TS1: Module Installation
| Step | Action | Expected Result | Screenshot |
|------|--------|-----------------|------------|
| 1.1 | Navigate to Apps menu | Apps list loads | `ts1-1-apps-menu.png` |
| 1.2 | Search "odoo_color_customizer" | Module appears in results | `ts1-2-search-result.png` |
| 1.3 | Click Install button | Installation completes without errors | `ts1-3-installed.png` |
| 1.4 | Verify module in installed list | Module shows as installed | `ts1-4-verified.png` |

#### TS2: Color Picker Access
| Step | Action | Expected Result | Screenshot |
|------|--------|-----------------|------------|
| 2.1 | Navigate to Settings > General Settings | Settings page loads | `ts2-1-settings.png` |
| 2.2 | Scroll to Color Customization section | Color picker field visible | `ts2-2-color-section.png` |
| 2.3 | Click color picker field | Color picker widget opens | `ts2-3-picker-open.png` |
| 2.4 | Verify hex input field present | Hex input shows current color | `ts2-4-hex-input.png` |

#### TS3: Color Selection & Live Preview
| Step | Action | Expected Result | Screenshot |
|------|--------|-----------------|------------|
| 3.1 | Select a new color (e.g., #FF5733) | Picker shows selected color | `ts3-1-color-selected.png` |
| 3.2 | Observe UI elements | Primary buttons change color immediately | `ts3-2-buttons-changed.png` |
| 3.3 | Check navbar/header | Header accents reflect new color | `ts3-3-navbar.png` |
| 3.4 | Verify no page reload occurred | URL unchanged, no loading indicator | `ts3-4-no-reload.png` |

#### TS4: Color Coverage Audit
| Step | Action | Expected Result | Screenshot |
|------|--------|-----------------|------------|
| 4.1 | Navigate to Contacts | View loads with custom color | `ts4-1-contacts.png` |
| 4.2 | Open kanban view | Kanban cards show custom color accents | `ts4-2-kanban.png` |
| 4.3 | Open form view | Form buttons use custom color | `ts4-3-form.png` |
| 4.4 | Check selection/focus states | Focus rings use custom color | `ts4-4-focus.png` |
| 4.5 | Navigate to Calendar | Calendar elements show custom color | `ts4-5-calendar.png` |
| 4.6 | Check checkboxes/radios | Custom color on checked state | `ts4-6-checkboxes.png` |

#### TS5: Color Persistence
| Step | Action | Expected Result | Screenshot |
|------|--------|-----------------|------------|
| 5.1 | Save settings | Settings saved successfully | `ts5-1-saved.png` |
| 5.2 | Hard refresh page (Ctrl+F5) | Custom color persists | `ts5-2-after-refresh.png` |
| 5.3 | Logout and login again | Custom color loads on login | `ts5-3-after-login.png` |
| 5.4 | Login as different user | Same custom color visible | `ts5-4-different-user.png` |

#### TS6: Reset to Default
| Step | Action | Expected Result | Screenshot |
|------|--------|-----------------|------------|
| 6.1 | Click "Reset to Default" button | Confirmation dialog appears | `ts6-1-confirm-dialog.png` |
| 6.2 | Confirm reset | Color resets to #714B67 | `ts6-2-reset-complete.png` |
| 6.3 | Verify all elements | All UI elements show default purple | `ts6-3-default-restored.png` |

#### TS7: Edge Cases & Error Handling
| Step | Action | Expected Result | Screenshot |
|------|--------|-----------------|------------|
| 7.1 | Enter invalid hex (#GGGGGG) | Validation error shown | `ts7-1-invalid-hex.png` |
| 7.2 | Enter 3-char hex (#F00) | Expands to 6-char or shows error | `ts7-2-short-hex.png` |
| 7.3 | Clear color field | Falls back to default color | `ts7-3-empty-field.png` |
| 7.4 | Test very light color (#FFFFFF) | Contrast warning shown | `ts7-4-contrast-warning.png` |
| 7.5 | Test very dark color (#000000) | Contrast warning shown | `ts7-5-dark-warning.png` |

#### TS8: Performance Verification
| Step | Action | Expected Result | Screenshot |
|------|--------|-----------------|------------|
| 8.1 | Open browser DevTools | DevTools panel visible | `ts8-1-devtools.png` |
| 8.2 | Measure page load with module | Load time < 50ms overhead | `ts8-2-load-time.png` |
| 8.3 | Measure color change rendering | < 100ms to apply new color | `ts8-3-render-time.png` |
| 8.4 | Check console for errors | No JS errors or warnings | `ts8-4-console-clean.png` |

#### TS9: Cross-View Validation
| Step | Action | Expected Result | Screenshot |
|------|--------|-----------------|------------|
| 9.1 | Test List view | Custom color on headers/selections | `ts9-1-list-view.png` |
| 9.2 | Test Pivot view | Custom color on headers | `ts9-2-pivot-view.png` |
| 9.3 | Test Graph view | Custom color on chart elements | `ts9-3-graph-view.png` |
| 9.4 | Test Activity view | Custom color on activity icons | `ts9-4-activity-view.png` |
| 9.5 | Test Search panel | Custom color on filters/groupby | `ts9-5-search-panel.png` |

### Screenshot Naming Convention
```
{test-scenario}-{step}-{description}.png
Example: ts3-2-buttons-changed.png
```

### Test Execution Commands
```bash
# Run all tests with Playwright MCP headed mode
# Screenshots saved to ./test-screenshots/

# Prerequisites:
# 1. Live Odoo 18 instance running (e.g., http://localhost:8069)
# 2. Admin credentials available
# 3. Module deployed to addons path
```

### Test Report Requirements
After test execution, generate a report including:
- Total tests: Pass/Fail count
- Screenshot gallery for each scenario
- Console errors captured
- Performance metrics summary
- Recommendations for any failures

## Success Criteria

### Key Metrics
| Metric | Target | Measurement |
|--------|--------|-------------|
| Setup time | < 2 minutes | Time from install to custom color visible |
| Color coverage | > 95% of purple elements | Visual audit |
| Performance impact | < 50ms added load time | Browser DevTools |
| User satisfaction | > 4/5 rating | Admin feedback |

### Definition of Done
- [ ] Module installs without errors on Odoo 18 CE/EE
- [ ] Color picker accessible in General Settings
- [ ] Selected color applies to all primary UI elements
- [ ] Changes visible immediately without page reload
- [ ] Color persists across sessions
- [ ] Reset to default works correctly
- [ ] No console errors or warnings
- [ ] Documentation complete

## Constraints & Assumptions

### Constraints
- **Odoo 18 only**: Uses CSS custom properties and OWL 2 patterns
- **No SCSS compilation**: Must work without asset rebuild
- **Admin-only**: No per-user customization in v1.0
- **Single color**: Only primary color in v1.0 (not full theme)

### Assumptions
- Odoo 18's web client uses CSS custom properties for primary color
- Users have modern browsers supporting CSS custom properties
- System administrators have access to General Settings

## Out of Scope

The following are explicitly **NOT** included in this version:

- ❌ Per-user color preferences
- ❌ Per-company color settings
- ❌ Secondary/accent color customization
- ❌ Logo/favicon customization
- ❌ Dark mode support
- ❌ Preset color themes/palettes
- ❌ Color export/import functionality
- ❌ Mobile app theming
- ❌ PDF/report color theming
- ❌ Email template theming

## Dependencies

### Internal Dependencies
- Odoo 18 `web` module
- Odoo 18 `base_setup` module (for settings)

### External Dependencies
- None (no external libraries required)

### Technical Prerequisites
- Odoo 18.0 installed
- Browser supporting CSS Custom Properties (all modern browsers)

## Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Odoo CSS variable changes in updates | High | Medium | Document which variables are overridden; test on updates |
| Color contrast accessibility issues | Medium | High | Add contrast ratio warning in color picker |
| Performance impact on page load | Medium | Low | Lazy load CSS; cache generated styles |
| Conflicts with custom themes | Medium | Medium | Test with common themes; document limitations |

## Bug Resolution Process

### ⚠️ MANDATORY PROCESS

**All bugs MUST follow this 5-step process to ensure 100% resolution. No exceptions.**

### Reference Architecture
```
📁 /mnt/c/Users/Matt/Desktop/CLAUDE專案/ODOO相關/Odoo_18_Environment_Architecture
```
Always consult this reference for Odoo 18 environment architecture details when debugging.

### Step 1: Deep Research 🔍

**Objective:** Understand the root cause completely before attempting any fix.

| Task | Description | Output |
|------|-------------|--------|
| 1.1 Reproduce | Consistently reproduce the bug | Steps to reproduce documented |
| 1.2 Analyze logs | Check Odoo server logs, browser console | Relevant error messages captured |
| 1.3 Trace code flow | Follow execution path through codebase | Identify exact failure point |
| 1.4 Check architecture | Reference Odoo 18 Environment Architecture | Understand system context |
| 1.5 Root cause | Identify WHY the bug occurs | Root cause statement |

**Research Checklist:**
```markdown
- [ ] Bug consistently reproduced
- [ ] Error messages captured (server + browser)
- [ ] Code execution path traced
- [ ] Odoo architecture reference consulted
- [ ] Root cause identified and documented
- [ ] Related components identified
```

**Research Output Template:**
```markdown
## Bug Research: [Bug Title]

### Reproduction Steps
1. ...
2. ...

### Error Evidence
- Server log: `[paste relevant log]`
- Browser console: `[paste relevant errors]`

### Code Flow Analysis
- Entry point: `[file:line]`
- Failure point: `[file:line]`
- Related files: [list]

### Root Cause
[Clear statement of why the bug occurs]

### Architecture Reference
Consulted: `/mnt/c/Users/Matt/Desktop/CLAUDE專案/ODOO相關/Odoo_18_Environment_Architecture`
Relevant sections: [list]
```

### Step 2: Create Fix Plan 📋

**Objective:** Design a complete solution before writing any code.

| Task | Description | Output |
|------|-------------|--------|
| 2.1 Solution design | Outline the fix approach | Technical solution document |
| 2.2 Impact analysis | Identify what else might be affected | Impact assessment |
| 2.3 Test cases | Define how to verify the fix | Test case list |
| 2.4 Rollback plan | How to revert if fix fails | Rollback procedure |

**Fix Plan Template:**
```markdown
## Fix Plan: [Bug Title]

### Proposed Solution
[Describe the fix approach]

### Files to Modify
| File | Change Description |
|------|-------------------|
| `path/to/file.py` | [what changes] |

### Impact Assessment
- Direct impact: [components directly affected]
- Side effects: [potential side effects]
- Risk level: [Low/Medium/High]

### Test Cases
1. [ ] [Test case 1]
2. [ ] [Test case 2]
3. [ ] [Regression test]

### Rollback Plan
[Steps to revert changes if needed]
```

### Step 3: Review Fix Plan 👀

**Objective:** Validate the plan before implementation.

| Task | Description | Criteria |
|------|-------------|----------|
| 3.1 Self-review | Review own plan critically | Logical and complete |
| 3.2 Architecture check | Verify against Odoo patterns | Follows Odoo conventions |
| 3.3 Edge cases | Consider boundary conditions | All edge cases handled |
| 3.4 Approval gate | Confirm plan is ready | Ready to implement |

**Review Checklist:**
```markdown
- [ ] Solution addresses root cause (not just symptoms)
- [ ] Changes follow Odoo 18 conventions
- [ ] No unnecessary changes included
- [ ] Test cases cover all scenarios
- [ ] Rollback plan is viable
- [ ] Impact is acceptable
```

### Step 4: Implement Fix Plan 🛠️

**Objective:** Execute the plan exactly as designed.

| Task | Description | Output |
|------|-------------|--------|
| 4.1 Create branch | Bug fix branch | `bugfix/[bug-name]` |
| 4.2 Implement | Code the fix | Modified files |
| 4.3 Unit test | Run local tests | Test results |
| 4.4 Commit | Commit with proper message | Git commit |

**Implementation Rules:**
1. **Follow the plan** - Do not deviate without re-planning
2. **Atomic commits** - One logical change per commit
3. **Comment changes** - Explain non-obvious fixes
4. **No scope creep** - Only fix the bug, nothing else

**Commit Message Format:**
```
[bugfix] Brief description of fix

Root cause: [what caused the bug]
Fix: [what the fix does]

Resolves: [bug reference if any]

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

### Step 5: Deploy & Test 🚀

**Objective:** Verify the fix works in a live Odoo 18 environment.

| Task | Description | Output |
|------|-------------|--------|
| 5.1 Deploy | Deploy to test environment | Module updated |
| 5.2 Verify fix | Run through reproduction steps | Bug no longer occurs |
| 5.3 Regression test | Test related functionality | No new issues |
| 5.4 Playwright test | Run automated tests (headed mode) | Screenshots captured |
| 5.5 Sign-off | Confirm bug is resolved | Closure confirmation |

**Test Verification Checklist:**
```markdown
- [ ] Bug reproduction steps now pass
- [ ] All test cases from fix plan pass
- [ ] No regression in related functionality
- [ ] Playwright tests pass with screenshots
- [ ] No new console errors
- [ ] Performance not degraded
```

**Closure Documentation:**
```markdown
## Bug Resolution: [Bug Title]

### Status: ✅ RESOLVED

### Fix Summary
[Brief description of what was fixed]

### Verification
- Tested on: [Odoo version, browser]
- Test date: [datetime]
- Test evidence: [screenshot paths]

### Commits
- `[commit hash]` - [message]

### Lessons Learned
[Optional: what to do differently next time]
```

### Process Flowchart

```
┌─────────────────┐
│   BUG FOUND     │
└────────┬────────┘
         ▼
┌─────────────────┐
│ 1. DEEP RESEARCH│◀─── Reference: Odoo_18_Environment_Architecture
│    - Reproduce  │
│    - Analyze    │
│    - Root cause │
└────────┬────────┘
         ▼
┌─────────────────┐
│ 2. FIX PLAN     │
│    - Design     │
│    - Impact     │
│    - Test cases │
└────────┬────────┘
         ▼
┌─────────────────┐     ┌─────────────────┐
│ 3. REVIEW PLAN  │────▶│  Plan rejected? │
│    - Validate   │     │  Go back to #2  │
│    - Approve    │     └─────────────────┘
└────────┬────────┘
         ▼
┌─────────────────┐
│ 4. IMPLEMENT    │
│    - Code fix   │
│    - Test local │
│    - Commit     │
└────────┬────────┘
         ▼
┌─────────────────┐     ┌─────────────────┐
│ 5. DEPLOY TEST  │────▶│  Test failed?   │
│    - Deploy     │     │  Go back to #1  │
│    - Verify     │     └─────────────────┘
│    - Sign-off   │
└────────┬────────┘
         ▼
┌─────────────────┐
│  ✅ BUG CLOSED  │
└─────────────────┘
```

### Critical Rules

1. **NO SKIPPING STEPS** - Each step must be completed in order
2. **DOCUMENT EVERYTHING** - Create artifacts for each step
3. **VERIFY ROOT CAUSE** - Never fix symptoms only
4. **TEST THOROUGHLY** - Use Playwright headed mode with screenshots
5. **REFERENCE ARCHITECTURE** - Always consult Odoo_18_Environment_Architecture

## Development Workflow

### Git Branching Strategy

| Branch Type | Naming Convention | Purpose |
|-------------|-------------------|---------|
| Main | `main` | Production-ready code |
| Feature | `feature/odoo-color-customizer` | Active development |
| Epic | `epic/odoo-color-customizer` | Long-running feature work |

### Branch Management
```bash
# Create feature branch from main
git checkout main
git pull origin main
git checkout -b feature/odoo-color-customizer

# Push branch with upstream tracking
git push -u origin feature/odoo-color-customizer
```

### Commit Policy

**Commit on every file change**, including:
- Module Python files (`*.py`)
- XML views and data (`*.xml`)
- JavaScript/OWL components (`*.js`, `*.owl`)
- CSS/SCSS styles (`*.css`, `*.scss`)
- Documentation and manifests
- **All `.claude/` directory files** (PRDs, epics, progress)

### Commit Message Format
```
[component] Brief description

- Detail 1
- Detail 2

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

**Component prefixes:**
- `[prd]` - PRD changes
- `[epic]` - Epic/task updates
- `[model]` - Python model changes
- `[view]` - XML view changes
- `[js]` - JavaScript/OWL changes
- `[css]` - Style changes
- `[test]` - Test additions/changes
- `[docs]` - Documentation updates

### Commit Examples
```bash
# PRD update
git add .claude/prds/odoo-color-customizer.md
git commit -m "[prd] Add testing strategy and git workflow sections"

# Module code change
git add odoo_color_customizer/models/res_config_settings.py
git commit -m "[model] Add primary_color field to settings"

# Multiple related files
git add odoo_color_customizer/static/src/js/*.js
git commit -m "[js] Implement color picker OWL component"
```

### File Change Tracking

Track all changes in `.claude/` directory:
```bash
# After any PRD/epic/task update
git add .claude/
git commit -m "[docs] Update project management files"

# Or more specific
git add .claude/prds/odoo-color-customizer.md
git commit -m "[prd] Add development workflow requirements"
```

### Branch Hygiene

1. **Regular commits**: Commit after each logical unit of work
2. **Descriptive messages**: Explain *why* not just *what*
3. **Atomic changes**: One concern per commit
4. **No dangling changes**: Always commit before switching context
5. **Include .claude/**: Project management files are part of the codebase

### Merge Strategy
```bash
# When feature is complete
git checkout main
git pull origin main
git merge feature/odoo-color-customizer --no-ff
git push origin main

# Clean up feature branch
git branch -d feature/odoo-color-customizer
git push origin --delete feature/odoo-color-customizer
```

## Future Considerations (v2.0+)

- Per-company color settings for multi-company
- Preset color palettes (professional, vibrant, minimal)
- Secondary color customization
- Dark mode color variants
- Color accessibility audit tool
- Import/export theme settings

## Appendix

### Odoo 18 Primary Color Locations
Based on analysis of Odoo 18 web client, the primary purple appears in:
- `addons/web/static/src/core/` - Core UI components
- `addons/web/static/src/views/` - View-specific styles
- `addons/web/static/src/webclient/` - Web client chrome

### Default Color Reference
- **Primary Purple**: `#714B67`
- **Primary Hover**: `#5a3c52` (approx -10% lightness)
- **Primary Light**: `#f0e8ed` (for backgrounds)

### Related Odoo CSS Variables
```css
--o-brand-odoo: #714B67;
--o-brand-primary: #714B67;
--primary: #714B67;
```
