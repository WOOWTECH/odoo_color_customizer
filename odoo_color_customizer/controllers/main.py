# -*- coding: utf-8 -*-
"""
Color Customizer - CSS Controller
Serves dynamic CSS with custom primary color variables.
"""
from odoo import http
from odoo.http import request

# Default Odoo Community purple color (from primary_variables.scss: $o-community-color)
DEFAULT_PRIMARY_COLOR = '#71639e'


class ColorCustomizerController(http.Controller):
    """Controller for serving dynamic theme CSS."""

    @http.route('/color_customizer/theme.css', type='http', auth='public', cors='*')
    def get_theme_css(self):
        """
        Return dynamic CSS with custom primary color variables.

        The CSS overrides Odoo's default brand colors with the user-configured
        primary color. Calculated variants (hover, active, light) are generated
        automatically.

        Returns:
            HTTP Response with CSS content and caching headers.
        """
        # Get configured color or fall back to default
        primary_color = request.env['ir.config_parameter'].sudo().get_param(
            'odoo_color_customizer.primary_color',
            DEFAULT_PRIMARY_COLOR
        )

        # Validate color format
        if not primary_color or not self._is_valid_hex_color(primary_color):
            primary_color = DEFAULT_PRIMARY_COLOR

        # Calculate color variants
        hover_color = self._darken_color(primary_color, 0.1)
        active_color = self._darken_color(primary_color, 0.2)
        light_color = self._lighten_color(primary_color, 0.85)
        text_color = self._get_contrast_color(primary_color)

        # Generate CSS with custom properties and critical overrides
        css = f""":root {{
    /* Custom primary color */
    --custom-primary: {primary_color};
    --custom-primary-hover: {hover_color};
    --custom-primary-active: {active_color};
    --custom-primary-light: {light_color};
    --custom-primary-text: {text_color};

    /* Override Odoo brand colors */
    --o-brand-odoo: {primary_color};
    --o-brand-primary: {primary_color};
}}

/* ============================================================================
   CRITICAL: Navbar dropdown toggle overrides
   These rules are served dynamically to ensure they override Odoo's defaults
   ============================================================================ */

/* Set CSS variable on navbar to override Odoo's fallback */
.o_main_navbar {{
    --NavBar-entry-backgroundColor: {primary_color};
    --NavBar-entry-backgroundColor--hover: {hover_color};
    --NavBar-entry-backgroundColor--focus: {hover_color};
    --NavBar-entry-backgroundColor--active: {active_color};
    border-bottom-color: {primary_color} !important;
}}

/* Dropdown toggle buttons in menu sections */
.o_main_navbar .o_menu_sections .dropdown-toggle,
.o_main_navbar .o_menu_sections .o-dropdown.dropdown-toggle,
.o_main_navbar .o_menu_sections button.dropdown-toggle,
.o_main_navbar .o_menu_sections .o-dropdown {{
    background: {primary_color} !important;
}}

.o_main_navbar .o_menu_sections .dropdown-toggle:hover,
.o_main_navbar .o_menu_sections .dropdown-toggle:focus,
.o_main_navbar .o_menu_sections .o-dropdown:hover,
.o_main_navbar .o_menu_sections .o-dropdown:focus {{
    background: {hover_color} !important;
}}

.o_main_navbar .o_menu_sections .dropdown-toggle.show,
.o_main_navbar .o_menu_sections .dropdown-toggle[aria-expanded="true"],
.o_main_navbar .o_menu_sections .o-dropdown.show,
.o_main_navbar .o_menu_sections .o-dropdown[aria-expanded="true"] {{
    background: {active_color} !important;
}}

/* Apps menu dropdown */
.o_main_navbar .o_navbar_apps_menu .dropdown-toggle,
.o_main_navbar .o_navbar_apps_menu .o-dropdown {{
    background: {primary_color} !important;
}}

.o_main_navbar .o_navbar_apps_menu .dropdown-toggle:hover,
.o_main_navbar .o_navbar_apps_menu .dropdown-toggle:focus {{
    background: {hover_color} !important;
}}

/* ============================================================================
   BUG FIX 1: Email badge/tag outline color
   Elements like "123@123" and "testuser@example.com" in Settings
   ============================================================================ */
.badge.border-primary,
.badge.text-primary {{
    outline-color: {primary_color} !important;
}}

/* ============================================================================
   BUG FIX 2: Focused input field border color
   When clicking any input field, the border should use primary color
   ============================================================================ */
.o_input:focus,
.o_input:focus-within,
textarea.o_input:focus,
input.o_input:focus,
.o_field_widget input:focus,
.o_field_widget textarea:focus {{
    border-color: {primary_color} !important;
    box-shadow: 0 0 0 0.2rem {light_color} !important;
}}

/* ============================================================================
   BUG FIX 3: Activity schedule arrow buttons (Inbox, Today, This Week, etc.)
   The ::before pseudo-element creates the arrow shape background
   ============================================================================ */
.o_arrow_button_current {{
    background-color: {light_color} !important;
    border-color: {primary_color} !important;
}}

.o_arrow_button_current::before {{
    background-color: {primary_color} !important;
}}

/* ============================================================================
   BUG FIX 4: Calendar current day indicator (mini calendar)
   The ::before creates the circular background on today's date
   ============================================================================ */
.o_today::before,
.o_datetime_picker .o_today::before,
.o_date_item_cell.o_today::before {{
    background-color: {light_color} !important;
}}

.o_selected.o_today::before {{
    background-color: {primary_color} !important;
}}

/* ============================================================================
   BUG FIX 5 & 6: View switch buttons and graph buttons (active state)
   These appear in Sales, Purchase Analysis, and other list/graph views
   ============================================================================ */
.o_switch_view.active,
.o_graph_button.active,
.btn-secondary.o_switch_view.active,
.btn-secondary.o_graph_button.active {{
    background-color: {light_color} !important;
    border-color: {primary_color} !important;
    color: {primary_color} !important;
}}

.o_switch_view.active:hover,
.o_switch_view.active:focus,
.o_graph_button.active:hover,
.o_graph_button.active:focus {{
    background-color: {light_color} !important;
    border-color: {hover_color} !important;
}}

/* ============================================================================
   BUG FIX 7: Input field HOVER border color
   When hovering any input field, the border should use primary color
   ============================================================================ */
.form-check:hover,
.form-check:hover .form-check-input:not(:disabled) {{
    border-color: {primary_color} !important;
}}

.form-select:where(:not(:disabled)):hover {{
    border-color: {primary_color} !important;
}}

.form-switch.o_switch_toggle:hover .form-check-input:not(:disabled) {{
    border-color: {primary_color} !important;
}}

/* ============================================================================
   BUG FIX 8: .btn-light active state (Toggle chatter button, etc.)
   Override Bootstrap CSS variables for btn-light active state
   ============================================================================ */
.btn-light {{
    --btn-active-bg: {light_color} !important;
    --btn-active-border-color: {primary_color} !important;
}}

.btn-light:active,
.btn-light.active,
.btn-light:focus {{
    background-color: {light_color} !important;
    border-color: {primary_color} !important;
}}

/* ============================================================================
   BUG FIX 9: Calendar/DatePicker day hover and selected states
   When hovering or clicking on calendar days
   ============================================================================ */
.o_datetime_picker .o_date_item_picker .o_datetime_button.o_selected:not(.o_select_start):not(.o_select_end),
.o_datetime_picker .o_date_item_picker .o_datetime_button:hover:not(.o_select_start):not(.o_select_end),
.o_datetime_picker .o_date_item_picker .o_datetime_button.o_today:not(.o_selected):hover:not(.o_select_start):not(.o_select_end) {{
    background: {light_color} !important;
    color: {primary_color} !important;
}}

/* ============================================================================
   BUG FIX 10: Tour pointer tip (guided tour tooltip)
   Override CSS variables for tour pointer background color
   ============================================================================ */
.o_tour_pointer {{
    --TourPointer__color: {primary_color} !important;
    --TourPointer__color-accent: {hover_color} !important;
}}

.o_tour_pointer .o_tour_pointer_tip {{
    background-color: {primary_color} !important;
}}

.o_tour_pointer .o_tour_pointer_tip::before {{
    border-color: {primary_color} transparent transparent transparent !important;
}}

/* ============================================================================
   BUG FIX 11: Primary link hover/focus colors
   Links with btn-primary or text-primary class
   ============================================================================ */
.btn-link.btn-primary:hover,
.btn-link.btn-primary:focus,
.btn-link.text-primary:hover,
.btn-link.text-primary:focus {{
    color: {hover_color} !important;
}}

/* ============================================================================
   BUG FIX 12: Field widget focus-within border
   Parent container when child input is focused
   ============================================================================ */
.o_field_widget:focus-within {{
    border-color: {primary_color} !important;
}}
"""

        return request.make_response(
            css,
            headers=[
                ('Content-Type', 'text/css; charset=utf-8'),
                ('Cache-Control', 'public, max-age=3600'),
            ]
        )

    def _is_valid_hex_color(self, color):
        """Check if string is a valid hex color."""
        if not color or len(color) != 7 or color[0] != '#':
            return False
        try:
            int(color[1:], 16)
            return True
        except ValueError:
            return False

    def _hex_to_rgb(self, hex_color):
        """Convert hex color string to RGB tuple."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def _rgb_to_hex(self, rgb):
        """Convert RGB tuple to hex color string."""
        r, g, b = [max(0, min(255, int(c))) for c in rgb]
        return f'#{r:02x}{g:02x}{b:02x}'

    def _darken_color(self, hex_color, amount):
        """
        Darken a hex color by a percentage.

        Args:
            hex_color: Hex color string (e.g., '#71639e')
            amount: Percentage to darken (0.0 to 1.0)

        Returns:
            Darkened hex color string
        """
        r, g, b = self._hex_to_rgb(hex_color)
        factor = 1 - amount
        return self._rgb_to_hex((r * factor, g * factor, b * factor))

    def _lighten_color(self, hex_color, amount):
        """
        Lighten a hex color by a percentage.

        Args:
            hex_color: Hex color string (e.g., '#71639e')
            amount: Percentage to lighten (0.0 to 1.0)

        Returns:
            Lightened hex color string
        """
        r, g, b = self._hex_to_rgb(hex_color)
        return self._rgb_to_hex((
            r + (255 - r) * amount,
            g + (255 - g) * amount,
            b + (255 - b) * amount
        ))

    def _get_contrast_color(self, hex_color):
        """
        Return white or black based on background luminance.

        Uses relative luminance formula to determine optimal text color
        for accessibility.

        Args:
            hex_color: Background hex color string

        Returns:
            '#ffffff' for dark backgrounds, '#000000' for light backgrounds
        """
        r, g, b = self._hex_to_rgb(hex_color)
        # Calculate relative luminance
        luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        return '#ffffff' if luminance < 0.5 else '#000000'
