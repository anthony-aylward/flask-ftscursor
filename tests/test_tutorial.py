import os
import pytest
import sqlite3
from flask import Flask
from flask_ftscursor import FTS

@pytest.fixture(scope="module")
def fts():
    return FTS()

@pytest.fixture(scope="module")
def app(fts):
    app = Flask(__name__)
    app.config['FTS_DATABASE'] = '/tmp/fts.db'
    app.config['FTS_SOURCE_DATABASE'] = '/tmp/app.db'
    fts.init_app(app)
    conn = sqlite3.connect(app.config['FTS_SOURCE_DATABASE'])
    c = conn.cursor()
    c.executescript('''
        CREATE TABLE my_table(id INTEGER, body TEXT);
        INSERT INTO my_table(id, body) VALUES
        (1, 'this is a test'),
        (2, 'a second test');
        '''
    )
    conn.commit()
    yield app
    os.remove(app.config['FTS_DATABASE'])
    os.remove(app.config['FTS_SOURCE_DATABASE'])

def test_search(app):
    with app.app_context():
        try:
            app.fts.search(
                table='my_table',
                query='this test',
                page=1,
                per_page=2
            )
        except ValueError:
            pass

    with app.app_context():
        app.fts.index(table='my_table', id=1, searchable=('body',))
        app.fts.index(table='my_table', id=2, searchable=('body',))
    
    with app.app_context():
        search_result = app.fts.search(
            table='my_table',
            query='this test',
            page=1,
            per_page=2
        )
        assert search_result == {'hits': {'total': 1, 'hits': ({'_id': 1},)}}
        search_result = app.fts.search(
            table='my_table',
            query='second',
            page=1,
            per_page=2
        )
        assert search_result == {'hits': {'total': 1, 'hits': ({'_id': 2},)}}

def test_drop(app):
    with app.app_context():
        app.fts.index(table='my_table', id=1, searchable=('body',))
        app.fts.index(table='my_table', id=2, searchable=('body',))
    
    with app.app_context():
        app.fts.drop('my_table')
