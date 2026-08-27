from lxml import etree

from odoo.tests import common


class TestPetViews(common.TransactionCase):
    def test_pet_kanban_uses_odoo_19_card_template(self):
        view = self.env.ref('pet_clinic_management.vet_pet_kanban')
        arch = etree.fromstring(view.arch_db)

        self.assertTrue(arch.xpath(".//t[@t-name='card']"))
        self.assertNotIn('kanban_image', view.arch_db)
