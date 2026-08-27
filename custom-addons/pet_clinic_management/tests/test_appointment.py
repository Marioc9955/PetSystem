from odoo.tests import common


class TestAppointment(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        owner = cls.env['res.partner'].create({'name': 'Synthetic Pet Owner'})
        cls.pet = cls.env['vet.pet'].create({
            'name': 'Synthetic Patient',
            'pet_type': 'dog',
            'owner_id': owner.id,
        })

    def _appointment_values(self, hour):
        return {
            'pet_id': self.pet.id,
            'date': f'2026-08-27 {hour:02d}:00:00',
            'reason': 'Routine examination',
        }

    def test_create_single_appointment_uses_sequence(self):
        appointment = self.env['vet.appointment'].create(
            self._appointment_values(9)
        )

        self.assertTrue(appointment.name.startswith('PET'))
        self.assertNotEqual(appointment.name, 'New')

    def test_create_multiple_appointments_uses_distinct_sequences(self):
        appointments = self.env['vet.appointment'].create([
            self._appointment_values(10),
            self._appointment_values(11),
        ])

        self.assertEqual(len(appointments), 2)
        self.assertNotEqual(appointments[0].name, appointments[1].name)

    def test_explicit_appointment_name_is_preserved(self):
        appointment = self.env['vet.appointment'].create({
            **self._appointment_values(12),
            'name': 'LEGACY-APPOINTMENT-001',
        })

        self.assertEqual(appointment.name, 'LEGACY-APPOINTMENT-001')
