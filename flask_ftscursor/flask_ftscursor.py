#===============================================================================
# flask_ftscursor.py
#===============================================================================
import sqlite3

from datetime import datetime
from flask import current_app, _app_ctx_stack


class FTS():
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('FTS_DATABASE', ':memory:')
        app.teardown_appcontext(self.teardown)
        app.fts4 = self.connection

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
