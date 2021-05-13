from odoo import models, fields, api, exceptions
from datetime import timedelta

class Session(models.Model):
    _name = 'openacademy.session'
    _description = 'Openacademy Session'

    name = fields.Char(required=True)
    start_date = fields.Date(string='Start Date', default=fields.Date.today)
    end_date = fields.Date(string="End Date",store=True ,compute='_compute_end_date', inverse='_compute_duration')
    durations = fields.Integer(help='Duration in days')
    seats = fields.Integer(string='Number of seats')
    taken_seats = fields.Float(string='Taken Seats', compute='_compute_taken_seat')
    course_id = fields.Many2one(comodel_name='openacademy.course',
                                string='Course ID',
                                required=True,
                                ondelete='cascade')
    attendee_ids = fields.Many2many(comodel_name='res.partner',
                                    string='Attendee')
    instructor_id = fields.Many2one(comodel_name='res.partner',
                                    string='Instructor',
                                    domain=['|', ('instructor', '=', True),
                                            ('category_id.name', 'like', 'Formateur')])
    active = fields.Boolean(default=True)
    attendees_count = fields.Integer(string="Attendees_count", store=True, compute="_compute_attendees_count")

    @api.depends('seats', 'attendee_ids')
    def _compute_taken_seat(self):
        for r in self:
            if not r.seats:
                r.taken_seats = 0.0
            else:
                r.taken_seats = 100 * len(r.attendee_ids) / r.seats

    @api.depends('start_date','durations')
    def _compute_end_date(self):
        for r in self:
            start = fields.Datetime.from_string(r.start_date)
            duration = timedelta(days=r.durations-1)
            r.end_date = start + duration

    def _compute_duration(self):
        for r in self:
            start = fields.Datetime.from_string(r.start_date)
            end = fields.Datetime.from_string(r.end_date)
            r.durations = end - start -1

    @api.depends('attendee_ids')
    def _compute_attendees_count(self):
        for r in self:
            r.attendees_count = len(r.attendee_ids)

    @api.onchange('seats', 'attendee_ids')
    def _verify_valid_seat(self):
        if self.seats < 0:
            return {
                'warning': {
                    'title': "Incorrect seat value",
                    'message': "Seats should not be negative"
                }
            }
        if len(self.attendee_ids) > self.seats:
            return {
                'warning': {
                    'title': "Too many attendees",
                    'message': "Increase seats or remove excess attendees"
                }
            }

    @api.constrains('instructor_id', 'attendee_ids')
    def _verify_instructor_id_attendees_id(self):
        for r in self:
            if r.instructor_id and r.instructor_id in r.attendee_ids:
                raise exceptions.ValidationError("Instructor should not be in attendees")
