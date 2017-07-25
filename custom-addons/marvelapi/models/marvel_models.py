# -*- coding: utf-8 -*-
from odoo import models, fields, api
import hashlib
import requests
import time
import json


PUB_KEY = '43829290ac807e18eac5f6ff39759cdd'
PRIV_KEY = '6fcf201684a506dbc13e96ad833c9fa012abaf20'


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
    _sql_constraints = [
        ('name_uniq', 'UNIQUE (name)', 'You can not have two comics with the same name !')
    ]

    name = fields.Char(string='Name')
    description = fields.Text()
    published = fields.Date()
    ean = fields.Char()
    image = fields.Html()


    @api.multi
    def click_request(self):
        print "You click here printing"
        return True


class ComicApiModel(models.TransientModel):
    _name = 'comicapi.model'
    # _sql_constraints = [
    #     ('name_uniq', 'UNIQUE (name)', 'You can not have two comics with the same name !')
    # ]

    name = fields.Char()
    description = fields.Text()
    published = fields.Date()
    ean = fields.Char()
    image = fields.Html()

    def compute_user_todo_count(self):
        pass

    user_todo_count = fields.Integer(
        'User To-Do Count',
        compute='compute_user_todo_count')


    @api.multi
    def create_request(self, **kwargs):
        self.env['comicapi.model'].unlink()
        print "You click finish"
        print(self.display_name)
        comics = request_marvel(self.display_name)

        if comics.get('data').get('count') != 0 and comics.get('status') == 'Ok':
            comics = comics.get('data').get('results')
            for comic in comics:
                self.env['comicapi.model'].create({
                    'name': comic.get('title'),
                    'image': '<html><body><img src="%s.%s" height="40" /></body></html>' %
                             (comic.get('thumbnail').get('path'),
                              comic.get('thumbnail').get('extension')),
                    'description': comic.get('description'),
                    'ean': comic.get('ean'),
                    'published': comic.get('dates')[0].get('date'),
                })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'comicapi.model',
            'view_type': 'form',
            'view_mode': 'tree,form',
        }

    def save_comic_base_db(self):
        self.env['comic.model'].create({
            'name': self.name,
            'image': self.image,
            'description': self.description,
            'ean': self.ean,
            'published': self.published,
        })
        # self.obj_saves(comic, 'comic.model')
        return True


def get_hash(ts, priv_key, pub_key):
    return hashlib.md5(ts+priv_key+pub_key).hexdigest()


def request_marvel(title):
    ts = str(time.time())
    hashes = get_hash(ts, PRIV_KEY, PUB_KEY)
    response = requests.get('http://gateway.marvel.com/v1/public/comics', params={
        'apikey': PUB_KEY,
        'ts': ts,
        'hash': hashes,
        'titleStartsWith': title,
        'limit': 100
    })
    return json.loads(response.content)
