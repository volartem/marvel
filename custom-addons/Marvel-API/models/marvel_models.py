# -*- coding: utf-8 -*-
from odoo import models, fields


class ComicModel(models.Model):
    _name = 'comic.model'

    name = fields.Char(string='Name')
    description = fields.Text()
    date = fields.Date()
