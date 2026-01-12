# Odoo Color Customizer

An Odoo 18 module that allows system administrators to customize the primary brand color used throughout the Odoo interface.

## Features

- **Color Picker in Settings**: Easy-to-use color picker in General Settings
- **Live Preview**: See color changes instantly without page reload
- **Persistent Storage**: Color settings saved to `ir.config_parameter`
- **Reset to Default**: One-click reset to Odoo's default purple (#714B67)
- **Comprehensive Coverage**: Applies to navbar, buttons, links, forms, and more

## Installation

1. Copy the `odoo_color_customizer` folder to your Odoo addons directory
2. Update the apps list: Settings → Apps → Update Apps List
3. Search for "Color Customizer" and click Activate

## Usage

1. Navigate to **Settings → General Settings**
2. Scroll to the **Color Customization** section at the bottom
3. Click the color picker to select a new primary color
4. The UI updates immediately for preview
5. Click **Save** to persist your changes
6. Use **Reset to Default** to restore Odoo's default purple

## Technical Details

### Architecture

```
odoo_color_customizer/
├── __init__.py
├── __manifest__.py
├── controllers/
│   ├── __init__.py
│   └── main.py              # CSS endpoint controller
├── models/
│   ├── __init__.py
│   └── res_config_settings.py
├── static/
│   └── src/
│       ├── js/
│       │   └── color_customizer.js  # Live preview & theme loading
│       └── scss/
│           └── color_overrides.scss # CSS variable overrides
└── views/
    └── res_config_settings_views.xml
```

### How It Works

1. **Settings Model** (`res_config_settings.py`): Extends `res.config.settings` with a `primary_color` field linked to `ir.config_parameter`

2. **CSS Controller** (`controllers/main.py`): Serves dynamic CSS at `/color_customizer/theme.css` with calculated color variants (hover, active, light, contrast text)

3. **JavaScript Service** (`color_customizer.js`):
   - Loads theme CSS on application start
   - Provides live preview via CSS custom properties
   - Exposes `window.ColorCustomizer` API

4. **SCSS Overrides** (`color_overrides.scss`): Comprehensive CSS rules using `var(--custom-primary)` to override Odoo's default styles

### CSS Custom Properties

The module uses CSS custom properties for theming:

| Property | Description |
|----------|-------------|
| `--custom-primary` | Main brand color |
| `--custom-primary-hover` | Darkened by 10% for hover states |
| `--custom-primary-active` | Darkened by 20% for active states |
| `--custom-primary-light` | Lightened by 85% for backgrounds |
| `--custom-primary-text` | White or black based on contrast |

### Affected UI Elements

- Navigation bar
- Primary buttons (`.btn-primary`)
- Outline buttons (`.btn-outline-primary`)
- Links
- Form focus states
- Checkboxes and radio buttons
- List view selection/hover
- Kanban cards
- Progress bars
- Badges
- Calendar events
- Dropdown active items
- Pagination
- Tabs and pills
- Status bars
- Search facets
- And more...

## Configuration

The color is stored in `ir.config_parameter` with the key:
```
odoo_color_customizer.primary_color
```

Default value: `#714B67` (Odoo purple)

## API

The module exposes a JavaScript API via `window.ColorCustomizer`:

```javascript
// Update live preview (client-side only)
window.ColorCustomizer.updateLivePreview('#FF5733');

// Refresh theme CSS from server
await window.ColorCustomizer.refreshThemeCSS();

// Load theme CSS (usually called on startup)
await window.ColorCustomizer.loadColorTheme();
```

## Compatibility

- **Odoo Version**: 18.0
- **Edition**: Community and Enterprise
- **License**: LGPL-3

## Troubleshooting

### Color not applying after save
The browser may cache the CSS. Try:
1. Hard refresh (Ctrl+Shift+R)
2. Clear browser cache
3. The module uses cache-busting, so a page reload should work

### Module not appearing in Apps
1. Enable Developer Mode
2. Remove the "Apps" filter in the search
3. Search for "color_customizer" or "Color Customizer"

## License

This module is licensed under LGPL-3. See the LICENSE file for details.

## Author

Created with Claude Code
