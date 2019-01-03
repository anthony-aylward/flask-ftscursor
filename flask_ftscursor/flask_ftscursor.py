#===============================================================================
# flask_ftscursor.py
#===============================================================================

# Imports ======================================================================

import sqlite3

from datetime import datetime
from flask import current_app, _app_ctx_stack
from ftscursor import FTSCursor




# Classes ======================================================================

class FTS():
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('FTS_DATABASE', ':memory:')
        app.teardown_appcontext(self.teardown)
        app.fts = self

    def connect(self):
        return sqlite3.connect(
            datetime.utcnow().strftime(current_app.config['FTS_DATABASE'])
        )

    def teardown(self, exception):
        ctx = _app_ctx_stack.top
        if hasattr(ctx, 'fts_db'):
            ctx.fts_db.close()

    @property
    def connection(self):
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'fts_db'):
                ctx.fts_db = self.connect()
            return ctx.fts_db

    def index(self, table, id, searchable):
        c = self.connection.cursor(factory=FTSCursor)
        c.attach_source_db(current_app.config['FTS_SOURCE_DATABASE'])
        c.index(table, id, searchable)
        current_app.fts.connection.commit()
        c.detach_source_db()

    def delete(self, table, id):
        c = self.connection.cursor(factory=FTSCursor)
        c.delete(table, id)

    def search(self, table, query, page, per_page):
        c = self.connection.cursor(factory=FTSCursor)
        hits = c.search(table, query)
        return {
            'hits': {
                'total': len(hits),
                'hits': tuple(
                    {'_id': hit} for hit in hits[
                        (page - 1) * per_page:page * per_page
                    ]
                )
            }
        }




# Functions ====================================================================


def search_results(search):
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total']


def add_to_index(index, model):
    if not current_app.fts:
        return
    current_app.fts.index(
        table=index,
        id=model.id,
        searchable=model.__searchable__
    )
    

def remove_from_index(index, model):
    if not current_app.fts:
        return
    current_app.fts.delete(table=index, id=model.id)


def query_index(index, query, page, per_page):
    if not current_app.fts:
        return [], 0
    search = current_app.fts.search(
        table=index,
        query=query,
        page=page,
        per_page=per_page
    )
    return search_results(search)

