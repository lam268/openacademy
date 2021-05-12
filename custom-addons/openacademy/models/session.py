from odoo import models, fields

class Session(models.Model):
    _name = 'openacademy.session'
    _description = 'Session'

    name = fields.Char(required=True)
    course_id = fields.Many2one(comodel_name='openacademy.course',
                                string='Course ID',
                                required=True,
                                ondelete='cascade')
    attendee_ids = fields.Many2many(comodel_name='res.partner',
                                    string='Attendee')