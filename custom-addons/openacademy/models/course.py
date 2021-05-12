from odoo import models, fields, api

class Course(models.Model):
    _name = 'openacademy.course'
    _description = 'Opencademy Courses'

    name = fields.Char(string="Title", required = True)
    description = fields.Text()
    responsive_id = fields.Many2one(comodel_name='res.users')
    session_ids = fields.One2many(comodel_name='openacademy.session', string='Session IDs', inverse_name='course_id' )

    _sql_constraints = [
        ('name_description_check',
         'CHECK(name !=description',
         "The title of the course should not be the description"),

        ('name_unique',
        'UNIQUE(name)',
        "The course title must be unique")
    ]

