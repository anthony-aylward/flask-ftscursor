#===============================================================================
# flask_ftscursor.py
#===============================================================================

"""An extension to facilitate using FTSCursor with Flask"""




# Imports ======================================================================

import sqlite3

from datetime import datetime
from flask import current_app, _app_ctx_stack
from ftscursor import FTSCursor




# Classes ======================================================================

class FTS():
    """a class providing database connections and FTS operations"""

    def __init__(self, app=None):
        """as in http://flask.pocoo.org/docs/1.0/extensiondev/"""

        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """as in http://flask.pocoo.org/docs/1.0/extensiondev/"""

        app.config.setdefault('FTS_DATABASE', ':memory:')
        app.teardown_appcontext(self.teardown)
        app.fts = self

    def connect(self):
        """as in http://flask.pocoo.org/docs/1.0/extensiondev/"""

        return sqlite3.connect(
            datetime.utcnow().strftime(current_app.config['FTS_DATABASE'])
        )

    def teardown(self, exception):
        """as in http://flask.pocoo.org/docs/1.0/extensiondev/"""

        ctx = _app_ctx_stack.top
        if hasattr(ctx, 'fts_db'):
            ctx.fts_db.close()

    @property
    def connection(self):
        """as in http://flask.pocoo.org/docs/1.0/extensiondev/"""
        
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'fts_db'):
                ctx.fts_db = self.connect()
            return ctx.fts_db

    def index(self, table: str, id: int, searchable):
        """Add a row to the FTS index

        Parameters
        ----------
        table : str
            the name of the table that will be added to (or created)
        id : int
            rowid of the row to delete
        """

        c = self.connection.cursor(factory=FTSCursor)
        c.attach_source_db(current_app.config['FTS_SOURCE_DATABASE'])
        c.index(table, id, searchable)
        self.connection.commit()
        c.detach_source_db()

    def delete(self, table: str, id: int):
        """Remove a row from the FTS index

        Parameters
        ----------
        table : str
            the name of the table that a row will be delted from
        id : int
            rowid of the row to delete
        """

        c = self.connection.cursor(factory=FTSCursor)
        c.delete(table, id)

    def search(self, table: str, query: str, page: int, per_page: int):
        """Perform a query against a FTS table

        Parameters
        ----------
        index : str
            the name of the FTS table to search
        query : str
            the FTS query string
        page : int
            the page of results that will be returned
        per_page : int
            the number of results per page
        """

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
    
    def drop(self, table: str):
        """Drop a FTS table

        Parameters
        ----------
        table : str
            the name of the table that will be dropped
        """

        c = self.connection.cursor(factory=FTSCursor)
        c.drop(table)




# Functions ====================================================================


def _search_results(search: dict):
    """Process the value of FTS.search() to prepare it for return in
    query_index()

    Parameters
    ----------
    search : dict
        the value returned by FTS.search()
    
    Returns
    -------
    list, int
        a list of the rowids of the results, and an int giving the total number
        of results
    """

    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total']


def add_to_index(index: str, model):
    """add a row to the FTS index

    Parameters
    ----------
    index : str
        the name of the table that will be added to (or created)
    model
        An instance of a SQLAlchemy model, representing the row to add
    """

    if not current_app.fts:
        return
    current_app.fts.index(
        table=index,
        id=model.id,
        searchable=model.__searchable__
    )
    

def remove_from_index(index: str, model):
    """remove a row from the FTS index

    Parameters
    ----------
    index : str
        the name of the table that a row will be delted from
    model
        An instance of a SQLAlchemy model, representing the row to remove
    """

    if not current_app.fts:
        return
    current_app.fts.delete(table=index, id=model.id)


def query_index(index: str, query: str, page: int, per_page: int):
    """perform a query against an FTS index

    Parameters
    ----------
    index : str
        the name of the FTS table to search
    query : str
        the FTS query string
    page : int
        the page of results that will be returned
    per_page : int
        the number of results per page

    Returns
    -------
    list, int
        a list of the rowids of the results, and an int giving the total number
        of results
    """

    if not current_app.fts:
        return [], 0
    search = current_app.fts.search(
        table=index,
        query=query,
        page=page,
        per_page=per_page
    )
    return _search_results(search)

