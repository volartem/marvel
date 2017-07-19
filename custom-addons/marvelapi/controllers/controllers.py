# -*- coding: utf-8 -*-
from odoo import http
import hashlib
import requests
import time
import json
from config import PRIV_KEY, PUB_KEY


class Comics(http.Controller):
    @http.route('/comics/', auth='public', website=True)
    def index(self, **kw):
        return http.request.render('marvelapi.index')

    @http.route('/comics/api', auth='public')
    def ajax(self, **kw):
        name = kw.get('text')
        if name:
            resp = request_marvel(name)
        else:
            resp = []
        return json.dumps(resp)

    @http.route('/comics/api/save', auth='public', methods=['POST'],
                website=True, csrf=False)
    def save_comic(self, **kw):
        """
        save comic after ajax request from client
        """
        comic = json.loads(kw.get('comic'))
        queries = http.request.env['comic.model'].\
            search([('name', '=', comic.get('title'))])
        if not queries:
            obj = http.request.env['comic.model'].create({
                'name': comic.get('title'),
                'description': comic.get('description'),
                'ean': comic.get('ean'),
                'published': comic.get('dates')[0].get('date'),
                'thumbnail_url': '%s.%s' %
                                 (comic.get('thumbnail').get('path'),
                                  comic.get('thumbnail').get('extension')),

            })

        return 'ok'


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
