from odoo.exceptions import AccessError, ValidationError
from odoo.tests import HttpCase, new_test_user, tagged


@tagged('post_install', '-at_install')
class TestLanding(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # A Spanish-first clean install may leave English inactive.
        cls.env['res.lang'].with_context(active_test=False).search([('code', '=', 'en_US')]).active = True
        cls.page = cls.env.ref('pet_clinic_management.landing_main').with_context(lang='en_US')
        cls.admin = new_test_user(cls.env, login='landing_admin', groups='pet_clinic_management.group_vet_administrator')
        cls.staff = new_test_user(cls.env, login='landing_staff', groups='pet_clinic_management.group_vet_receptionist')
        cls.vet = new_test_user(cls.env, login='landing_vet', groups='pet_clinic_management.group_vet_veterinarian')
        cls.internal = new_test_user(cls.env, login='landing_internal', groups='base.group_user')
        cls.public = cls.env.ref('base.public_user')

    def test_publication_and_roles(self):
        self.page.write({'is_published': False})
        for user in (self.public, self.staff, self.vet, self.internal):
            self.assertFalse(self.env['vet.landing.page'].with_user(user).search([]))
            self.assertFalse(self.env['vet.landing.block'].with_user(user).search([]))
            for model in ('vet.landing.page', 'vet.landing.block'):
                for operation in ('create', 'write', 'unlink'):
                    self.assertFalse(self.env[model].with_user(user).has_access(operation))
            with self.assertRaises(AccessError):
                self.page.with_user(user).write({'is_published': True})
        self.page.with_user(self.admin).write({'is_published': True})
        hidden = self.page.block_ids[0]
        hidden.write({'is_published': False})
        self.assertEqual(self.env['vet.landing.page'].with_user(self.public).search([]), self.page)
        self.assertNotIn(hidden, self.env['vet.landing.block'].with_user(self.public).search([]))
        with self.assertRaises(AccessError):
            hidden.with_user(self.public).read(['body'])
        with self.assertRaises(AccessError):
            self.env['vet.pet'].with_user(self.public).search([])

    def test_color_and_link_validation(self):
        for value in ('red', '#fff;display:none', '#ffffff'):
            with self.assertRaises(ValidationError), self.cr.savepoint():
                self.page.write({'primary_color': value})
        block = self.page.block_ids[0]
        for url in ('javascript:alert(1)', '//example.com', 'https://user:pass@example.com', 'https://exa\nmple.com', 'https://[invalid'):
            with self.assertRaises(ValidationError), self.cr.savepoint():
                block.write({'button_label': 'Unsafe', 'button_url': url})
        block.write({'button_label': 'Contact', 'button_url': '#contact'})

    def test_public_http_and_preview(self):
        self.page.write({'is_published': False})
        self.assertEqual(self.url_open('/pet-clinic').status_code, 404)
        self.page.write({'is_published': True, 'title': '<script>test marker</script>'})
        hidden = self.page.block_ids[0]
        hidden.write({'is_published': False, 'name': 'HIDDEN BLOCK MARKER'})
        response = self.url_open('/pet-clinic?lang=en_US')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('&lt;script&gt;test marker&lt;/script&gt;' in response.text,
                        'The English hero title must be HTML-escaped.')
        self.assertNotIn('HIDDEN BLOCK MARKER', response.text)
        self.assertIn('pc-split', response.text)
        self.assertIn('pc-banner', response.text)
        self.authenticate('landing_staff', 'landing_staff')
        self.assertEqual(self.url_open('/pet-clinic/preview').status_code, 403)
        self.authenticate('landing_admin', 'landing_admin')
        self.page.write({'is_published': False})
        self.assertEqual(self.url_open('/pet-clinic').status_code, 404)
        preview = self.url_open('/pet-clinic/preview?lang=en_US')
        self.assertEqual(preview.status_code, 200)
        self.assertIn('HIDDEN BLOCK MARKER', preview.text)
