# -*- coding: utf-8 -*-
from odoo import models, fields


class CharacterModel(models.Model):
    _name = 'character.model'

    name = fields.Char()


class StoryModel(models.Model):
    _name = 'story.model'

    name = fields.Char()


class ImageModel(models.Model):
    _name = 'image.model'

    name = fields.Char()
    url = fields.Char()


class ComicModel(models.Model):
    _name = 'comic.model'

    name = fields.Char(string='Name')
    description = fields.Text()
    published = fields.Date()
    thumbnail_url = fields.Char()
    ean = fields.Char()
    character = fields.Many2many('character.model')
    story = fields.Many2many('story.model')
    image = fields.Many2many('image.model')

