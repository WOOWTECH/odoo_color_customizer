# PRD: Frontend Launcher Button Fixes

## Problem Statement

The "所有應用程式" (All Applications) button in the frontend launcher has visibility issues:

1. **Hamburger menu icon not visible** - The `.oi-apps` icon is not showing
2. **Text color wrong** - User wants WHITE text, but current calculation returns BLACK

## Root Cause Analysis

### Current State (from CSS endpoint)
```css
--custom-primary: #00ffff;        /* Cyan - bright color */
--custom-primary-text: #000000;   /* Black - calculated as contrast color */
```

### The Problem
The contrast calculation uses luminance formula:
```python
luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
return '#ffffff' if luminance < 0.5 else '#000000'
```

For cyan (#00ffff):
- R=0, G=255, B=255
- luminance = (0.299*0 + 0.587*255 + 0.114*255) / 255 = 0.701
- Since 0.701 > 0.5, it returns BLACK (#000000)

**But the user wants WHITE text on the cyan button!**

## Requirements

### Must Have
1. "所有應用程式" button text must be WHITE (#ffffff)
2. Hamburger menu icon (.oi-apps) must be WHITE and visible
3. These should be hardcoded for the frontend launcher, not depend on contrast calculation

### Nice to Have
- Maintain accessibility for other elements using contrast calculation

## Technical Solution

### Approach: Hardcode white for frontend launcher

The frontend launcher button should ALWAYS have white text/icons regardless of the primary color, because:
1. User explicitly requested white
2. The button background is always the primary color (a "brand" element)
3. White provides better visual impact for a call-to-action button

### Code Changes

**File: `controllers/main.py` - `get_frontend_css()` method**

Change from:
```css
.o_frontend_to_backend_nav .o_frontend_to_backend_apps_btn {
    background-color: {primary_color} !important;
    color: {text_color} !important;  /* This is #000000 for cyan */
}
```

To:
```css
.o_frontend_to_backend_nav .o_frontend_to_backend_apps_btn {
    background-color: {primary_color} !important;
    color: #ffffff !important;  /* ALWAYS white per user requirement */
}
```

### Full CSS Rules to Update

```css
/* Frontend launcher button - ALWAYS white text/icons */
.o_frontend_to_backend_nav .o_frontend_to_backend_apps_btn {
    background-color: {primary_color} !important;
    color: #ffffff !important;
}

.o_frontend_to_backend_nav .o_frontend_to_backend_apps_btn:hover {
    background-color: {hover_color} !important;
    color: #ffffff !important;
}

/* All child elements - text, icons - ALWAYS white */
.o_frontend_to_backend_nav .o_frontend_to_backend_apps_btn span,
.o_frontend_to_backend_nav .o_frontend_to_backend_apps_btn .fa,
.o_frontend_to_backend_nav .o_frontend_to_backend_apps_btn .oi,
.o_frontend_to_backend_nav .o_frontend_to_backend_apps_btn .oi-apps,
.o_frontend_to_backend_nav .o_frontend_to_backend_apps_btn i,
.o_frontend_to_backend_nav .o_frontend_to_backend_apps_btn i::before {
    color: #ffffff !important;
}

/* Hamburger icon must be visible and white */
.o_frontend_to_backend_nav .oi-apps,
.o_frontend_to_backend_nav .oi-apps::before,
.o_frontend_to_backend_apps_btn .oi-apps,
.o_frontend_to_backend_apps_btn .oi-apps::before {
    color: #ffffff !important;
    opacity: 1 !important;
    visibility: visible !important;
    display: inline-block !important;
}
```

## Testing Checklist

- [ ] Navigate to Portal page (/my/home)
- [ ] Verify "所有應用程式" button has cyan background
- [ ] Verify button text is WHITE
- [ ] Verify hamburger menu icon (grid icon) is WHITE and visible
- [ ] Verify hover state maintains white text
- [ ] Test with different primary colors to ensure white always shows

## Implementation Steps

1. Update `controllers/main.py` - Replace `{text_color}` with `#ffffff` for frontend launcher
2. Deploy to Podman container
3. Restart Odoo
4. Clear browser cache and test

## Notes

- Other elements (like .btn-primary) should continue using `{text_color}` for proper contrast
- Only the frontend launcher button is hardcoded to white per user's explicit request
