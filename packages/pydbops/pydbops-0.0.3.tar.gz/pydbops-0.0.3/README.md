# Database Operations

[![PyPI Latest Release](https://img.shields.io/pypi/v/pydbops.svg)](https://pypi.org/project/pydbops/)
[![License](https://img.shields.io/pypi/l/pydbops.svg)](https://github.com/NotShrirang/pydbops/LICENSE)

Library for simplifying database operations.
Contains standard functions for database operations.
<br>

GitHub Page : https://github.com/NotShrirang/pydbops

## Installing pydbops with PyPI :

```sh
pip install pydbops
```

## Importing pydbops:

```sh
from pydbops import *
```

## Methods in Database:

1. <code>openDatabase()</code> - Creates a database and returns a Database object.
2. <code>createTable()</code> - Creates table of given name.
3. <code>addEntry()</code> - Function for inserting values in database.
4. <code>databaseVersion()</code> - Returns sqlite3 version.
5. <code>getFieldNames()</code> - Function for getting field names.
6. <code>getTable()</code> - Creates Table instance.
7. <code>length()</code> - Returns length of database.
8. <code>removeEntry()</code> - Function for removing records from database.
9. <code>searchEntry()</code> - Function for searching in database.
10. <code>tableNames()</code> - Function for retrieving tables in a database.
11. <code>updateEntry()</code> - Function for updating values in database.
