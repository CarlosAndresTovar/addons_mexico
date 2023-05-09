# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    category_partner = fields.Selection(string='Company Type',
                                        selection=[('employee', 'Employee'),
                                                   ('associated', 'Associated'),
                                                   ('associate_library', 'Associate_library'),
                                                   ('customer', 'Customer'),
                                                   ('visitor', 'Visitor')],
                                        default="employee")
    quality_partner = fields.Many2one('quality.partner', string='Quality',
                                      domain="[('category', '=', category_partner)]",
                                      required=True)
    client_number = fields.Char(string='Client number', copy=False,
                                default=lambda self: _('New'), required=True)
    id_partner = fields.Char(string='Id')
    application_date = fields.Date(string='Application date')
    partner_code = fields.Char(string='Partner code')
    partner_quality = fields.Char(string='Partner quality')
    name_partner = fields.Char(string="Name partner")
    last_name = fields.Char(string="Last name")
    home = fields.Char(string="Home")
    municipality = fields.Char(string="Municipality")
    department = fields.Char(string="Department")
    place_of_birth = fields.Char(string="Place of birth")
    birthdate = fields.Date(string='Birthdate')
    dui = fields.Char(string='DUI')
    nationality = fields.Char(string='Nationality')
    passport_number = fields.Char(string='Passport number')
    expiration_date = fields.Date(string='Expiration date')
    sex = fields.Selection(string='Sex', selection=[('male', 'Male'),
                                                    ('female', 'Female')],
                           default="female")
    civil_status = fields.Selection(string='civil_status',
                                    selection=[('single', 'Single'),
                                               ('married', 'Married'),
                                               ('divorced', 'Divorced'),
                                               ('widower', 'Widower'),
                                               ('free_union', 'Free_union')],
                                    default="single")
    profession = fields.Char(string='Profession')
    phone_contact = fields.Char(string='Phone contact')
    contact_cell = fields.Char(string='Contact cell')
    contact_email = fields.Char(string='Contact email')
    company_name = fields.Char(string='Company name')
    position_held = fields.Char(string='Position held')
    company_address = fields.Char(string='Company address')
    company_phone = fields.Char(string='Company phone')
    company_email = fields.Char(string='Company email')
    relationship = fields.Char(string='Relationship')
    high_date = fields.Date(string='High date')
    approval_class = fields.Char(string='Approval class')
    act_num = fields.Char(string='Act num')
    affiliation_number = fields.Char(string='Affiliation number')
    document_to_issue = fields.Char(string='Document to issue')
    exempt = fields.Char(string='Exempt')
    billing_name = fields.Char(string='Billing name')
    nrc = fields.Char(string='NRC')
    nit = fields.Char(string='NIT')
    low_date = fields.Date(string='Low date')
    low_reason = fields.Char(string='Low reason')
    readmission_date = fields.Date(string='Readmission date')
    low_readmission = fields.Char(string='Low readmission')
    category_membership = fields.Selection(string = 'Category membership',
                                           selection=[('number', 'Number'),
                                                      ('community', 'Community'),
                                                      ('passerby', 'Passerby'),
                                                      ('taxpayer', 'Taxpayer'),
                                                      ('youth', 'Youth'),
                                                      ('grandson', 'Grandson')])

    @api.model
    def create(self, vals):
        if 'client_number' not in vals or vals['client_number'] == _('New'):
            query_sequence =\
                self.env['quality.partner'].search([('id', '=',
                                                     vals['quality_partner'])])
            code_sequence = query_sequence.secuence.code
            vals['client_number'] = self.env['ir.sequence'].next_by_code(code_sequence) or _('New')

        return super(ResPartner, self).create(vals)

    @api.onchange('category_partner')
    def _clear_quality(self):
        for line in self:
            line.quality_partner = False

    def write(self, vals):
        if 'quality_partner' in vals:
            query_sequence =\
                self.env['quality.partner'].search([('id', '=',
                                                     vals['quality_partner'])])
            code_sequence = query_sequence.secuence.code
            vals['client_number'] = self.env['ir.sequence'].next_by_code(code_sequence) or _('New')

        return super(ResPartner, self).write(vals)


class QualityPartner(models.Model):
    _name = 'quality.partner'

    name = fields.Char(string='name', required=True)
    category = fields.Selection(string='Company Type', required=True,
                                selection=[('employee', 'Employee'),
                                           ('associated', 'Associated'),
                                           ('associate_library', 'Associate_library'),
                                           ('customer', 'Customer'),
                                           ('visitor', 'Visitor')])
    secuence = fields.Many2one('ir.sequence', string='Secuence', required=True)

    @api.model
    def create(self, vals_list):
        query_name_category_secuence = self.env['quality.partner'].search(
            [('name', '=', vals_list['name']),
             ('category', '=', vals_list['category']),
             ('secuence', '=', vals_list['secuence'])]
        )
        query_name_categroy = self.env['quality.partner'].search(
            [('name', '=', vals_list['name']),
             ('category', '=', vals_list['category'])]
        )
        query_secuence = self.env['quality.partner'].search(
            [('secuence', '=', vals_list['secuence'])])
        if query_name_category_secuence or query_name_categroy or query_secuence:
             raise UserError(_("You cannot have more than two or more "
                               "sequences with the same name and category"))
        res = super(QualityPartner, self).create(vals_list)
        return res
    #No puedes tener mas de dos o mas secuencias con el mismo nombre y categoria