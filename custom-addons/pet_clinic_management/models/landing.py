import re
from urllib.parse import urlsplit

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


def _contrast(first, second):
    def luminance(color):
        channels = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
        channels = [c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4 for c in channels]
        return sum(c * weight for c, weight in zip(channels, (.2126, .7152, .0722)))
    values = sorted((luminance(first), luminance(second)))
    return (values[1] + .05) / (values[0] + .05)


class VetLandingPage(models.Model):
    _name = 'vet.landing.page'
    _description = 'Clinic Landing Page'

    key = fields.Char(default='main', required=True, readonly=True)
    _single_page = models.Constraint("UNIQUE(key)", 'Only one clinic landing page is allowed.')
    _main_key = models.Constraint("CHECK(key = 'main')", 'Use the main clinic landing page.')
    name = fields.Char(string='Public clinic name', required=True, default='Pet Clinic', translate=True)
    is_published = fields.Boolean(string='Published', default=False)
    logo = fields.Image(max_width=512, max_height=512, attachment=False)
    hero_image = fields.Image(max_width=1600, max_height=1600, attachment=False)
    hero_alt = fields.Char(default='A happy dog and a curious cat', translate=True)
    eyebrow = fields.Char(default='Little paws. A whole lot of love.', translate=True)
    title = fields.Char(required=True, default='Their happy place. Your peace of mind.', translate=True)
    description = fields.Text(default='Thoughtful veterinary care for the ones who make your life a little brighter.', translate=True)
    button_label = fields.Char(default='Get in touch', translate=True)
    services_title = fields.Char(default='Care for every little adventure', translate=True)
    contact_title = fields.Char(default='Let’s talk about your best friend.', translate=True)
    contact_text = fields.Text(string='Public contact details', translate=True,
                               help='Only add information intended for public display: address, opening hours, phone and email.')
    palette = fields.Selection([('sky', 'Sky blue'), ('sage', 'Sage green'), ('peach', 'Warm peach'), ('custom', 'Custom')], default='sky', required=True)
    primary_color = fields.Char(default='#23718A', required=True)
    background_color = fields.Char(default='#EDF7FA', required=True)
    text_color = fields.Char(default='#173943', required=True)
    block_ids = fields.One2many('vet.landing.block', 'page_id', string='Content blocks')

    @api.constrains('primary_color', 'background_color', 'text_color')
    def _check_colors(self):
        for page in self:
            colors = (page.primary_color, page.background_color, page.text_color)
            if any(not re.fullmatch(r'#[0-9a-fA-F]{6}', color or '') for color in colors):
                raise ValidationError(_('Colors must use six-digit hex values, for example #23718A.'))
            if min(_contrast(page.primary_color, '#FFFFFF'),
                   _contrast(page.text_color, page.background_color),
                   _contrast(page.text_color, '#FFFFFF')) < 4.5:
                raise ValidationError(_('Choose colors with at least 4.5:1 contrast: white on primary, and text on both background and white.'))

    def _palette(self):
        self.ensure_one()
        return {
            'sky': ('#23718A', '#EDF7FA', '#173943'),
            'sage': ('#38634C', '#EFF5ED', '#243B30'),
            'peach': ('#9A4930', '#FFF2E9', '#49342D'),
            'custom': (self.primary_color, self.background_color, self.text_color),
        }[self.palette]


class VetLandingBlock(models.Model):
    _name = 'vet.landing.block'
    _description = 'Clinic Landing Content Block'
    _order = 'sequence, id'

    page_id = fields.Many2one('vet.landing.page', required=True, ondelete='cascade')
    sequence = fields.Integer(default=10)
    is_published = fields.Boolean(string='Visible on published page', default=True)
    name = fields.Char(string='Heading', required=True, translate=True)
    body = fields.Text(translate=True)
    layout = fields.Selection([('card', 'Service card'), ('split', 'Image and text'), ('banner', 'Full-width banner')], default='card', required=True)
    image_side = fields.Selection([('left', 'Left'), ('right', 'Right')], default='left', required=True)
    image = fields.Image(max_width=1200, max_height=1200, attachment=False)
    image_alt = fields.Char(translate=True)
    icon = fields.Selection([('paw', 'Paw'), ('heart', 'Heart'), ('plus', 'Medical cross')], default='paw', required=True)
    button_label = fields.Char(translate=True)
    button_url = fields.Char(help='Use an https:// link or #contact.')

    @api.constrains('button_label', 'button_url')
    def _check_button(self):
        for block in self:
            if bool(block.button_label) != bool(block.button_url):
                raise ValidationError(_('Set both a button label and a link, or leave both empty.'))
            url = block.button_url
            if not url or url == '#contact':
                continue
            try:
                parsed = urlsplit(url)
                valid = parsed.scheme == 'https' and parsed.hostname and not parsed.username and not parsed.password
                valid = valid and not any(c.isspace() or ord(c) < 32 for c in url) and '\\' not in url
            except ValueError:
                valid = False
            if not valid:
                raise ValidationError(_('Use an absolute https:// link or #contact.'))
