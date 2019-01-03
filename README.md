# Flask-FTSCursor
An extension to facilitate using FTSCursor with flask

## Installation
`pip3 install flask-ftscursor`

## Mission Statement

This package was inspired by Miguel Grinberg's
[Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world),
specifically [Chapter 16: Full-Text Search](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvi-full-text-search).
Even more specifically, it was this sentence:
>Using the searching capabilities of one of the relational databases could also be a good choice, but given the fact that SQLAlchemy does not support this functionality, I would have to handle the searching with raw SQL statements, or else find a package that provides high-level access to text searches while being able to coexist with SQLAlchemy.

Flask-FTSCursor is such a package. It provides high-level access to text
searches while being able to coexist harmoniously with SQLAlchemy.
