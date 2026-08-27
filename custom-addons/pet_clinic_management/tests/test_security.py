from odoo.exceptions import AccessError
from odoo.tests import common, new_test_user


class TestPetClinicSecurity(common.TransactionCase):
    MODEL_NAMES = (
        'vet.pet',
        'vet.appointment',
        'vet.vaccination',
        'vet.treatment',
        'vet.prescription',
        'vet.prescription.line',
        'vet.vaccine',
        'vet.medicine',
    )
    OPERATIONS = ('read', 'write', 'create', 'unlink')

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.internal_user = new_test_user(
            cls.env,
            login='pet_clinic_internal_user',
            groups='base.group_user',
        )
        cls.receptionist = new_test_user(
            cls.env,
            login='pet_clinic_receptionist',
            groups='pet_clinic_management.group_vet_receptionist',
        )
        cls.veterinarian = new_test_user(
            cls.env,
            login='pet_clinic_veterinarian',
            groups='pet_clinic_management.group_vet_veterinarian',
        )
        cls.administrator = new_test_user(
            cls.env,
            login='pet_clinic_administrator',
            groups='pet_clinic_management.group_vet_administrator',
        )
        owner = cls.env['res.partner'].create({'name': 'Security Test Owner'})
        pet = cls.env['vet.pet'].create({
            'name': 'Security Test Patient',
            'pet_type': 'cat',
            'owner_id': owner.id,
        })
        cls.appointment = cls.env['vet.appointment'].create({
            'pet_id': pet.id,
            'date': '2026-08-27 14:00:00',
            'reason': 'Security regression test',
        })

    def _assert_model_access(self, user, expected_access):
        for model_name in self.MODEL_NAMES:
            for operation in self.OPERATIONS:
                with self.subTest(
                    user=user.login,
                    model=model_name,
                    operation=operation,
                ):
                    expected = operation in expected_access.get(model_name, ())
                    actual = self.env[model_name].with_user(user).has_access(
                        operation
                    )
                    self.assertEqual(actual, expected)

    def test_generic_internal_user_has_no_pet_clinic_access(self):
        self._assert_model_access(self.internal_user, {})
        with self.assertRaises(AccessError):
            self.env['vet.pet'].with_user(self.internal_user).search([])

    def test_receptionist_access(self):
        self._assert_model_access(self.receptionist, {
            'vet.pet': ('read', 'write', 'create'),
            'vet.appointment': ('read', 'write', 'create'),
        })

    def test_veterinarian_access(self):
        clinical_access = ('read', 'write', 'create')
        self._assert_model_access(self.veterinarian, {
            'vet.pet': clinical_access,
            'vet.appointment': clinical_access,
            'vet.vaccination': clinical_access,
            'vet.treatment': clinical_access,
            'vet.prescription': clinical_access,
            'vet.prescription.line': clinical_access,
            'vet.vaccine': ('read',),
            'vet.medicine': ('read',),
        })

    def test_administrator_has_full_access(self):
        self._assert_model_access(
            self.administrator,
            {model_name: self.OPERATIONS for model_name in self.MODEL_NAMES},
        )

    def test_diagnosis_is_hidden_from_receptionist(self):
        receptionist_fields = self.env['vet.appointment'].with_user(
            self.receptionist
        ).fields_get()
        veterinarian_fields = self.env['vet.appointment'].with_user(
            self.veterinarian
        ).fields_get()

        self.assertNotIn('diagnosis', receptionist_fields)
        self.assertIn('diagnosis', veterinarian_fields)

        with self.assertRaises(AccessError):
            self.appointment.with_user(self.receptionist).write({
                'diagnosis': 'Receptionists must not write clinical diagnoses.',
            })
        self.appointment.with_user(self.veterinarian).write({
            'diagnosis': 'Synthetic veterinary diagnosis.',
        })
