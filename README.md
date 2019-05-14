# Flask-FTSCursor
An extension to facilitate using [FTSCursor](https://github.com/anthony-aylward/ftscursor) with Flask

## Installation
`pip3 install flask-ftscursor`

## Mission Statement

This package was inspired by Miguel Grinberg's
[Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world),
specifically [Chapter 16: Full-Text Search](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvi-full-text-search).
Even more specifically, it was this sentence:
>Using the searching capabilities of one of the relational databases could also be a good choice, but given the fact that SQLAlchemy does not support this functionality, I would have to handle the searching with raw SQL statements, or else find a package that provides high-level access to text searches while being able to coexist with SQLAlchemy.

Flask-FTSCursor is such a package. It provides high-level access to SQLite3
full-text searches while being able to coexist harmoniously with SQLAlchemy.

## Tutorial

This will be a very minimal demonstration of the `FTS` object. For an example of
an app that uses Flask-FTSCursor, see [ucsd-bisb-unofficial](https://github.com/anthony-aylward/ucsd-bisb-unofficial/blob/master/ucsd_bisb_unofficial/models.py).

First import the things we will need
```python
import sqlite3
from flask import Flask
from flask_ftscursor import FTS
```
Create a `FTS` object
```python
fts = FTS()
```
Define an application factory function
```python
def create_app():
    app = Flask(__name__)
    app.config['FTS_DATABASE'] = 'fts.db'
    app.config['FTS_SOURCE_DATABASE'] = 'app.db'
    fts.init_app(app)
    return app
```
Create the app
```python
app = create_app()
```
Put some data in the source database
```python
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
```
Try a search (this will fail, because nothing has been indexed yet)
```python
with app.app_context()
    app.fts.search(table='my_table', query='this test', page=1, per_page=2)
```
Index some rows from the source database (adding them to the FTS database)
```python
with app.app_context()
    app.fts.index(table='my_table', id=1, searchable=('body',))
    app.fts.index(table='my_table', id=2, searchable=('body',))
```
Perform a full-text search
```python
with app.app_context()
    app.fts.search(table='my_table', query='this test', page=1, per_page=2)
```
```python
{'hits': {'total': 1, 'hits': ({'_id': 1},)}}
```
Try a different query
```python
with app.app_context()
    app.fts.search(table='my_table', query='second', page=1, per_page=2)
```
```python
{'hits': {'total': 1, 'hits': ({'_id': 2},)}}
```
Drop the FTS table, removing its contents from the FTS database
```python
with app.app_context()
    app.fts.drop(table='my_table')
```

## Configuration

Flask-FTSCursor relies on two items in the app's configuration: `FTS_DATABASE`
and `FTS_SOURCE_DATABASE`.
The value of `FTS_SOURCE_DATABASE` should be the file path of the app's main
SQLite3 database, or whichever database contains the entries that will be
indexed. The value of `FTS_DATABSE` should be the file path where the database
containing the FTS tables will be kept.

## Abstraction

Flask-FTSCursor provides functions named `add_to_index()`,
`remove_from_index()`, and `query_index()` which can be used in place of the
similarly named functions given in Miguel Grinberg's Flask Mega-Tutorial,
[Chapter 16: Full-Text Search](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvi-full-text-search),
under the section titled "A Full-Text Search Abstraction." For an example of
an app that uses these functions, see [ucsd-bisb-unofficial](https://github.com/anthony-aylward/ucsd-bisb-unofficial/blob/master/ucsd_bisb_unofficial/models.py).
