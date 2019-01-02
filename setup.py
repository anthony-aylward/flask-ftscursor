"""
Flask-FTSCursor
-------------

An extension to facilitate using FTSCursor with flask
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='Flask-SQLite3',
    version='0.0.1',
    url='http://example.com/flask-sqlite3/',
    license='MIT',
    author='Your Name',
    author_email='your-email@example.com',
    description='An extension to facilitate using FTSCursor with flask',
    long_description=long_description,
    packages=setuptools.find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)