from odoo import http
from odoo.http import request
from werkzeug.exceptions import Forbidden, NotFound


class ClinicLanding(http.Controller):
    def _render_landing(self, preview=False, lang=None):
        # Public rendering always uses public record rules, even for signed-in admins.
        model = request.env['vet.landing.page']
        if not preview:
            model = model.with_user(request.env.ref('base.public_user'))
        available = request.env['res.lang'].get_installed()
        languages = [code for code, _name in available if code in ('es_EC', 'en_US')]
        language = lang if lang in languages else ('es_EC' if 'es_EC' in languages else 'en_US')
        request.update_context(lang=language)
        page = model.with_context(lang=language).search([('key', '=', 'main')], limit=1)
        if not page:
            raise NotFound()
        blocks = request.env['vet.landing.block'].with_user(model.env.user).with_context(lang=language).search([('page_id', '=', page.id)])
        return request.render('pet_clinic_management.landing_page', {
            'page': page, 'blocks': blocks, 'palette': page._palette(),
            'preview': preview, 'language': language, 'languages': languages,
        }, headers={'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff'})

    @http.route('/pet-clinic', type='http', auth='public', methods=['GET'])
    def landing(self, lang=None, **kwargs):
        return self._render_landing(lang=lang)

    @http.route('/pet-clinic/preview', type='http', auth='user', methods=['GET'])
    def preview(self, lang=None, **kwargs):
        if not request.env.user.has_group('pet_clinic_management.group_vet_administrator'):
            raise Forbidden()
        return self._render_landing(preview=True, lang=lang)
