# Database Operations

[![PyPI Latest Release](https://img.shields.io/pypi/v/pydbops.svg)](https://pypi.org/project/pydbops/)
[![License](https://img.shields.io/pypi/l/pydbops.svg)](https://github.com/NotShrirang/pydbops/LICENSE)

Library for simplifying database operations.
Contains standard functions for database operations.
<br>

GitHub Page : https://github.com/NotShrirang/pydbops

## Importing pydbops:

```sh
from pydbops import *
```

## Methods in Database:

(You will need to call openDatabase() method using db.)

## Methods in Database:

1. <code>openDatabase()</code> - Creates a database and returns a Database object.
2. <code>createTable()</code> - Creates table of given name.
3. <code>addEntry()</code> - Function for inserting values in database.
4. <code>databaseVersion()</code> - Returns sqlite3 version.
5. <code>dropTable()</code> - Function for deleting table.
6. <code>fetchInOrder()</code> - Function for fetching database entries in given order.
7. <code>getFieldNames()</code> - Function for getting field names.
8. <code>getTable()</code> - Creates Table instance.
9. <code>length()</code> - Returns length of database.
10. <code>removeEntry()</code> - Function for removing records from database.
11. <code>searchEntry()</code> - Function for searching in database.
12. <code>tableNames()</code> - Function for retrieving tables in a database.
13. <code>updateEntry()</code> - Function for updating values in database.

For printing data in database, you can use default print() method by passing Database object in it.
