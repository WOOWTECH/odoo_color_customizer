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

    @http.route('/color_customizer/frontend.css', type='http', auth='public', cors='*')
    def get_frontend_css(self):
        """
        Return CSS for frontend pages including:
        - BUG FIX 34: Editor launcher (triangle + apps button)
        - BUG FIX 35: Portal page styling
        - BUG FIX 36: Website frontend elements
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

        # Generate comprehensive frontend CSS
        css = f""":root {{
    --custom-primary: {primary_color};
    --custom-primary-hover: {hover_color};
    --custom-primary-active: {active_color};
    --custom-primary-light: {light_color};
    --custom-primary-text: {text_color};
}}

/* ============================================================================
   BUG FIX 34: Frontend Editor Launcher (Triangle + Apps Button)
   ============================================================================ */
.o_frontend_to_backend_nav::before {{
    border-top-color: {primary_color} !important;
    border-left-color: {primary_color} !important;
}}

.o_frontend_to_backend_nav .o_frontend_to_backend_apps_btn {{
    background-color: {primary_color} !important;
}}

.o_frontend_to_backend_nav .o_frontend_to_backend_apps_btn:hover {{
    background-color: {hover_color} !important;
}}

/* ============================================================================
   BUG FIX 35: Portal Page Styling
   ============================================================================ */

/* Primary buttons */
.btn-primary {{
    background-color: {primary_color} !important;
    border-color: {primary_color} !important;
    color: {text_color} !important;
}}

.btn-primary:hover,
.btn-primary:focus {{
    background-color: {hover_color} !important;
    border-color: {hover_color} !important;
}}

.btn-primary:active {{
    background-color: {active_color} !important;
    border-color: {active_color} !important;
}}

/* Outline buttons */
.btn-outline-primary {{
    color: {primary_color} !important;
    border-color: {primary_color} !important;
}}

.btn-outline-primary:hover,
.btn-outline-primary:focus {{
    background-color: {primary_color} !important;
    color: {text_color} !important;
}}

/* Links - ONLY target links that were originally purple */
/* NOTE: Do NOT use broad selectors like a:not(.btn) - this changes ALL links */
/* Only specific purple links should be changed */
.text-primary a,
a.text-primary {{
    color: {primary_color};
}}

a.text-primary:hover {{
    color: {hover_color};
}}

/* Portal sidebar/nav active states */
.o_portal_my_home .o_portal_doc_card:hover {{
    border-color: {primary_color} !important;
}}

/* Portal stat boxes */
.o_portal_my_home .o_portal_stat {{
    color: {primary_color};
}}

/* Card primary backgrounds */
.bg-primary,
.card-header.bg-primary {{
    background-color: {primary_color} !important;
}}

/* Text primary */
.text-primary {{
    color: {primary_color} !important;
}}

/* Progress bars */
.progress-bar {{
    background-color: {primary_color} !important;
}}

/* Form focus states */
.form-control:focus,
.form-select:focus {{
    border-color: {primary_color} !important;
    box-shadow: 0 0 0 0.2rem {light_color} !important;
}}

/* Checkboxes and radios */
.form-check-input:checked {{
    background-color: {primary_color} !important;
    border-color: {primary_color} !important;
}}

/* Pagination */
.page-item.active .page-link {{
    background-color: {primary_color} !important;
    border-color: {primary_color} !important;
}}

.page-link {{
    color: {primary_color};
}}

.page-link:hover {{
    color: {hover_color};
}}

/* Badges */
.badge.bg-primary {{
    background-color: {primary_color} !important;
}}

/* Website navbar (frontend) */
header#top .navbar {{
    --navbar-brand-color: {primary_color};
}}

/* Footer links */
footer a:not(.btn) {{
    color: {primary_color};
}}

footer a:not(.btn):hover {{
    color: {hover_color};
}}

/* ============================================================================
   BUG FIX 38: Login Page Links
   Replace purple links on /web/login page
   ============================================================================ */

/* Login form links */
.oe_login_form a,
.oe_login_form a:visited,
form.oe_login_form a:not(.btn),
a.oe_login_link,
.oe_reset_password_link,
.oe_signup_link {{
    color: {primary_color} !important;
}}

.oe_login_form a:hover,
a.oe_login_link:hover,
.oe_reset_password_link:hover,
.oe_signup_link:hover {{
    color: {hover_color} !important;
}}

/* Select user dropdown link */
.oe_login_form .oe_login_link,
.oe_login_form [href*="select_user"] {{
    color: {primary_color} !important;
}}

/* ============================================================================
   BUG FIX 39: Portal Page Elements
   Replace purple on /my/home and other portal pages
   ============================================================================ */

/* Portal stat card - light background (the "待審閱報價" card) */
.o_portal_my_home .card.bg-100,
.o_portal_my_home .o_portal_doc_spinner,
.o_portal_my_home .o_portal_docs .card,
.o_portal_my_count .card,
.o_portal_index_card {{
    background-color: {light_color} !important;
}}

/* Portal card icons (發票, 工具, 借用, 設備, 維修請求) */
.o_portal_my_home .card-body i,
.o_portal_my_home .card-body .fa,
.o_portal_my_home .card-body .oi,
.o_portal_my_home .o_portal_doc_spinner i,
.o_portal_index_card i,
.o_portal_index_card .fa,
.o_portal_index_card .oi {{
    color: {primary_color} !important;
}}

/* Portal card link titles - ONLY the main h5/title link, NOT description text */
/* Be VERY specific to only target the main card title links */
.o_portal_my_home .card-title a,
.o_portal_my_home .card-body h5 a,
.o_portal_my_home .card-body .h5 a,
.o_portal_my_home .card-body > h5 > a {{
    color: {primary_color} !important;
}}

.o_portal_my_home .card-title a:hover,
.o_portal_my_home .card-body h5 a:hover,
.o_portal_my_home .card-body .h5 a:hover,
.o_portal_my_home .card-body > h5 > a:hover {{
    color: {hover_color} !important;
}}

/* CRITICAL: Ensure ALL description text stays gray/default - DO NOT color these */
/* This includes paragraphs, small text, and any text that is NOT the main title */
.o_portal_my_home .card-body p,
.o_portal_my_home .card-body p a,
.o_portal_my_home .card-body small,
.o_portal_my_home .card-body small a,
.o_portal_my_home .card-body .text-muted,
.o_portal_my_home .card-body .text-muted a,
.o_portal_my_home .card-body span:not(.badge),
.o_portal_my_home .card-body div:not(.card-title) a:not(:first-child) {{
    color: #6c757d !important;
}}

/* Portal stat number (the "1" in "1 待審閱報價") */
.o_portal_my_home .o_portal_count,
.o_portal_my_count .o_portal_count {{
    color: {primary_color} !important;
}}

/* Portal sidebar active link */
.o_portal_my_home .o_portal_sidebar .active,
.o_portal_my_details a.active {{
    color: {primary_color} !important;
    border-color: {primary_color} !important;
}}
"""

        return request.make_response(
            css,
            headers=[
                ('Content-Type', 'text/css; charset=utf-8'),
                ('Cache-Control', 'no-cache, no-store, must-revalidate'),
                ('Pragma', 'no-cache'),
                ('Expires', '0'),
            ]
        )

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
   NOTE: Navbar TEXT colors are intentionally NOT overridden.
   Odoo's default navbar styling handles text contrast automatically.
   We only override BACKGROUND colors here, not text colors.
   Black text should remain black - only purple elements are changed.
   ============================================================================ */

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
    box-shadow: none !important;
}}

/* ============================================================================
   BUG FIX 3: Activity schedule arrow buttons (Inbox, Today, This Week, etc.)
   NOTE: Removed border-color and ::before overrides - Original Odoo has
   black borders, not primary color borders
   ============================================================================ */
.o_arrow_button_current {{
    background-color: {light_color} !important;
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
    /* NOTE: Removed color override - text should stay dark gray like Original Odoo */
}}

/* CRITICAL FIX: Override the SCSS cached rule that sets purple text on active view switches */
.o_control_panel .o_cp_switch_buttons .btn.active,
.o_control_panel .o_cp_switch_buttons .btn.btn-secondary.active {{
    color: #343a40 !important;
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

/* ============================================================================
   BUG FIX 13: Override --o-input-border-color CSS variable
   This variable controls input border color for required/focused fields
   ============================================================================ */
.o_required_modifier {{
    --o-input-border-color: {primary_color} !important;
    --o-caret-color: {primary_color} !important;
}}

.o_field_widget:focus-within {{
    --o-input-border-color: {primary_color} !important;
    --o-caret-color: {primary_color} !important;
}}

.o_field_widget:hover {{
    --o-input-border-color: {primary_color} !important;
}}

/* ============================================================================
   BUG FIX 14: Calendar mini picker selected/current day colors
   Override the light purple background and purple border
   ============================================================================ */
.o_datetime_picker .o_selected:not(.o_select_start):not(.o_select_end) {{
    background: {light_color} !important;
}}

.o_datetime_picker .o_current::before,
.o_datetime_picker .o_highlighted::before,
.o_datetime_picker .o_select_start::before,
.o_datetime_picker .o_select_end::before {{
    box-shadow: {primary_color} 0px 0px 0px 1px inset !important;
}}

.o_datetime_picker .o_select_start::before,
.o_datetime_picker .o_select_end::before {{
    background: {light_color} !important;
}}

.o_datetime_picker .o_select_start:not(.o_select_end)::after,
.o_datetime_picker .o_select_end:not(.o_select_end)::after,
.o_datetime_picker .o_select_start:not(.o_select_start)::after,
.o_datetime_picker .o_select_end:not(.o_select_start)::after {{
    background: {light_color} !important;
}}

/* ============================================================================
   BUG FIX 15: Search view should NOT have box-shadow on focus
   Original Odoo only has border color change, no box-shadow
   The input INSIDE searchview also needs box-shadow: none
   ============================================================================ */
.o_searchview:focus,
.o_searchview:focus-within,
.o_searchview.form-control:focus,
.o_searchview.form-control:focus-within,
.o_searchview input,
.o_searchview input:focus,
.o_searchview_input,
.o_searchview_input:focus {{
    box-shadow: none !important;
}}

/* ============================================================================
   BUG FIX 16 (Enhanced): Form tabs (notebook) should NOT have primary color borders
   Original Odoo has gray borders: rgb(222, 226, 230) for top/sides
   Uses CSS variable override + maximum specificity selectors to beat SCSS
   ============================================================================ */

/* Override CSS variable that SCSS uses for tab border accent */
.o_notebook {{
    --notebook-link-border-color-active-accent: #dee2e6 !important;
}}

/* Maximum specificity selectors to beat SCSS cached rules (5+ classes) */
html body .o_action .o_form_view .o_notebook .nav-tabs .nav-item .nav-link.active,
.o_web_client .o_action .o_form_view .o_notebook .nav-tabs .nav-item .nav-link.active,
.o_action_manager .o_form_view .o_notebook .nav-tabs .nav-item .nav-link.active,
.o_form_view .o_notebook .nav-tabs .nav-item .nav-link.active,
.o_notebook .nav-tabs .nav-item .nav-link.active {{
    border-top-color: #dee2e6 !important;
    border-left-color: #dee2e6 !important;
    border-right-color: #dee2e6 !important;
    border-bottom-color: transparent !important;
}}

/* ============================================================================
   BUG FIX 19-22: Additional purple color overrides
   These rules provide maximum specificity to override compiled SCSS
   ============================================================================ */

/* BUG FIX 19: Combo product card selection border */
.product-card.selected {{
    border-color: {primary_color} !important;
}}

/* BUG FIX 23: Combo product card hover border */
.product-card:hover {{
    border-color: {primary_color} !important;
}}

/* BUG FIX 20: Product configurator color picker active state */
.o_sale_product_configurator_ptav_color.active {{
    border-color: {primary_color} !important;
}}

/* BUG FIX 20b: Pill-style radio buttons in configurator */
.o_sale_product_configurator_ptav_pills.active label {{
    background-color: {primary_color} !important;
    border-color: {primary_color} !important;
    color: {text_color} !important;
}}

/* BUG FIX 21: Status bar current button */
.o_statusbar_status .o_arrow_button_current {{
    border-color: {primary_color} !important;
}}

.o_statusbar_status .o_arrow_button:hover,
.o_statusbar_status .o_arrow_button:focus {{
    border-color: {primary_color} !important;
}}

/* BUG FIX 22: Required field border in selected rows */
.o_data_row.o_selected_row > .o_data_cell.o_required_modifier:not(.o_readonly_modifier) {{
    border-bottom-color: {primary_color} !important;
}}

/* BUG FIX 19b: All links should use custom primary (with !important) */
a:not(.btn):not(.nav-link):not(.dropdown-item) {{
    color: {primary_color} !important;
}}

a:not(.btn):not(.nav-link):not(.dropdown-item):hover {{
    color: {hover_color} !important;
}}

/* ============================================================================
   BUG FIX 27: Variant price extra badges (e.g., +$111.00)
   Remove box-shadow/outline causing DOUBLE BORDER effect
   ============================================================================ */
.badge.rounded-pill.border,
.badge.border {{
    border-color: {primary_color} !important;
    box-shadow: none !important;
    outline: none !important;
    outline-color: transparent !important;
}}

.o_variant_pills_input_value .badge,
.radio_input_value .badge,
label .badge.rounded-pill.border {{
    border-color: {primary_color} !important;
    box-shadow: none !important;
    outline: none !important;
}}

/* ============================================================================
   BUG FIX 28+32+33: Combo product links in form view embedded lists
   Links inside one2many fields require form view context selectors
   Previous fixes failed because they targeted standalone list views
   BUG FIX 33: Must explicitly target .o_form_uri class which Odoo uses for form links
   Odoo core has: .o_form_view .o_form_uri {{ color: rgb(102, 89, 143) }} - purple!
   ============================================================================ */

/* CRITICAL: Override .o_form_uri which is the class on combo product links */
.o_form_view .o_form_uri,
.o_form_view .o_form_uri:visited,
.o_form_view .o_form_uri > span,
.o_form_view .o_form_uri > span:first-child,
.o_form_view .o_form_uri > span:first-child:visited {{
    color: {primary_color} !important;
}}

.o_form_view .o_form_uri:hover,
.o_form_view .o_form_uri:focus,
.o_form_view .o_form_uri.focus,
.o_form_view .o_form_uri > span:first-child:hover,
.o_form_view .o_form_uri > span:first-child:focus {{
    color: {hover_color} !important;
}}

/* Form view context - embedded one2many list links (CRITICAL for combo products) */
.o_form_view .o_field_one2many a,
.o_form_view .o_field_one2many a:visited,
.o_form_view .o_field_widget a,
.o_form_view .o_field_widget a:visited,
.o_form_view .o_list_renderer a,
.o_form_view .o_list_renderer a:visited,
.o_form_view .o_data_row a,
.o_form_view .o_data_row a:visited,
.o_form_view .o_data_cell a,
.o_form_view .o_data_cell a:visited,
.o_form_view .o_list_table a,
.o_form_view .o_list_table a:visited {{
    color: {primary_color} !important;
}}

/* Form view context - hover states */
.o_form_view .o_field_one2many a:hover,
.o_form_view .o_field_widget a:hover,
.o_form_view .o_list_renderer a:hover,
.o_form_view .o_data_row a:hover,
.o_form_view .o_data_cell a:hover,
.o_form_view .o_list_table a:hover,
.o_form_view .o_field_one2many a:visited:hover,
.o_form_view .o_field_widget a:visited:hover,
.o_form_view .o_list_renderer a:visited:hover,
.o_form_view .o_data_row a:visited:hover,
.o_form_view .o_data_cell a:visited:hover,
.o_form_view .o_list_table a:visited:hover {{
    color: {hover_color} !important;
}}

/* Standalone list view context (for regular list views outside forms) */
.o_list_renderer .o_data_row a,
.o_list_renderer .o_data_row a:visited,
.o_list_view .o_data_row a,
.o_list_view .o_data_row a:visited,
.o_data_row a,
.o_data_row a:visited,
.o_data_cell a,
.o_data_cell a:visited,
.o_list_table a,
.o_list_table a:visited {{
    color: {primary_color} !important;
}}

/* Standalone list view - hover states */
.o_list_renderer .o_data_row a:hover,
.o_list_view .o_data_row a:hover,
.o_data_row a:hover,
.o_data_cell a:hover,
.o_list_table a:hover,
.o_list_renderer .o_data_row a:visited:hover,
.o_list_view .o_data_row a:visited:hover,
.o_data_row a:visited:hover,
.o_data_cell a:visited:hover,
.o_list_table a:visited:hover {{
    color: {hover_color} !important;
}}

/* ============================================================================
   BUG FIX 29: Status bar button borders - override CSS variables + ::before
   ============================================================================ */
.o_statusbar_status {{
    --o-statusbar-border: {primary_color};
    --o-statusbar-border-active: {primary_color};
}}

.o_statusbar_status .o_arrow_button::before {{
    border-color: {primary_color} !important;
}}

.o_statusbar_status .o_arrow_button_current::before {{
    border-color: {primary_color} !important;
    background-color: {light_color} !important;
}}

.o_statusbar_status .o_arrow_button_current,
.o_statusbar_status button.o_arrow_button_current,
.o_statusbar_status .btn.o_arrow_button_current {{
    border-color: {primary_color} !important;
}}

.o_statusbar_status .o_arrow_button:hover,
.o_statusbar_status .o_arrow_button:focus,
.o_statusbar_status button.o_arrow_button:hover,
.o_statusbar_status button.o_arrow_button:focus {{
    border-color: {primary_color} !important;
}}

/* ============================================================================
   BUG FIX 30: Discuss Sidebar Active/Hover States
   ============================================================================ */

/* Override CSS variables for Discuss sidebar */
.o-mail-DiscussSidebar {{
    --mail-DiscussSidebar-itemActiveBgColor: {light_color};
    --mail-DiscussSidebar-itemActiveOutlineColor: {primary_color};
}}

/* Active sidebar items */
.o-mail-DiscussSidebar-item.o-active,
.o-mail-DiscussSidebarChannel.o-active {{
    background-color: {light_color} !important;
    outline-color: {primary_color} !important;
}}

/* Hover state for sidebar items */
.o-mail-DiscussSidebar-item:hover,
.o-mail-DiscussSidebarChannel:hover {{
    background-color: {light_color} !important;
    outline-color: {primary_color} !important;
}}

/* Quick search button active state */
.o-mail-DiscussSidebarCategories-quickSearchBtn.o-active {{
    background-color: {primary_color} !important;
    color: {text_color} !important;
}}

/* Quick search input focus */
.o-mail-DiscussSidebarQuickSearchInput.o-active {{
    outline-color: {primary_color} !important;
}}

/* Category headers with icons */
.o-mail-DiscussSidebarCategory-toggler:hover {{
    color: {primary_color} !important;
}}

/* ============================================================================
   BUG FIX 34: Frontend Editor Launcher (Triangle + Apps Button)
   The triangle and square launcher on website frontend uses $o-enterprise-color
   Source: website/static/src/scss/website.ui.scss lines 14-57
   ============================================================================ */
.o_frontend_to_backend_nav::before {{
    border-top-color: {primary_color} !important;
    border-left-color: {primary_color} !important;
}}

.o_frontend_to_backend_nav .o_frontend_to_backend_apps_btn {{
    background-color: {primary_color} !important;
}}

.o_frontend_to_backend_nav .o_frontend_to_backend_apps_btn:hover {{
    background-color: {hover_color} !important;
}}
"""

        return request.make_response(
            css,
            headers=[
                ('Content-Type', 'text/css; charset=utf-8'),
                ('Cache-Control', 'no-cache, no-store, must-revalidate'),
                ('Pragma', 'no-cache'),
                ('Expires', '0'),
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
