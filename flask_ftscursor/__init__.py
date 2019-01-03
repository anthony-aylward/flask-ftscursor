"""An extension to facilitate using FTSCursor with Flask

Classes
-------
FTS
    a class providing database connections and FTS operations

Functions
---------
add_to_index
    add a row to the FTS index
remove_from_index
    remove a row from the FTS index
query_index
    perform a query against an FTS index
"""


from flask_ftscursor.flask_ftscursor import (
  FTS,
  add_to_index,
  remove_from_index,
  query_index
)
