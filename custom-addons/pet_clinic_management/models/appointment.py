from odoo import _, api, fields, models
from odoo.exceptions import UserError


class Appointment(models.Model):
    _name = 'vet.appointment'
    _description = 'Pet Appointment'

    name = fields.Char(
        string='Appointment ID',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New'),
    )
    pet_id = fields.Many2one('vet.pet', string='Pet', required=True)
    owner_id = fields.Many2one(related='pet_id.owner_id', string='Owner', store=True)
    breed = fields.Char(related='pet_id.breed', string='Breed', store=True)
    age = fields.Integer(related='pet_id.age', string='Age', store=True)
    date = fields.Datetime(string='Appointment Date', required=True)
    reason = fields.Text(string='Reason for Visit')
    diagnosis = fields.Text(
        string='Diagnosis',
        groups='pet_clinic_management.group_vet_veterinarian',
    )

    @api.model_create_multi
    def create(self, vals_list):
        default_name = _('New')
        for vals in vals_list:
            if not vals.get('name') or vals['name'] == default_name:
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'vet.appointment'
                )
                if not vals['name']:
                    raise UserError(
                        _('The appointment number sequence is not configured.')
                    )
        return super().create(vals_list)
