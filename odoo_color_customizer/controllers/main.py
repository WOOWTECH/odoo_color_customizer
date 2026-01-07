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

        # Generate CSS with custom properties
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
