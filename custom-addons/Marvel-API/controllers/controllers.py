# -*- coding: utf-8 -*-
from odoo import http


class Comics(http.Controller):
    @http.route('/comics/', auth='public', website=True)
    def index(self, **kw):
        return http.request.render('Marvel-API.index')

    @http.route('/comics/api', auth='public')
    def ajax(self, **kw):
        response_text = kw.get('text')
        return response_text
