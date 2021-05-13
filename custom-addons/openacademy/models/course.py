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
         'CHECK(name != description)',
         "The title of the course should not be the description"),

        ('name_unique',
         'UNIQUE(name)',
         "The course title must be unique"),
    ]

    def copy(self, default = None):
        default = dict(default or {})

        copied_count = self.search_count(
            [('name', '=like', 'Copy of %{}'.format(self.name))]
        )
        if not copied_count:
            new = ('Copy of {}').format(self.name)
        else:
            new = ("Copy of {} ({})").format(self.name, copied_count)
        default['name'] = new
        return super(Course, self).copy(default)


