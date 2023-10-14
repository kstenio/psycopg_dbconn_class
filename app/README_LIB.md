## psycopg_dbconn_class

A simple class to handle database connections using psycopg2 (PostgreSQL).

### Development background

When I've started to work with Python + PostgreSQL, I have begun using the pysycopg2
library. However, I do prefer working with classes, and the usual connection/cursor
methods were not very functional for my applications.

Eventually, I decided to structure the objects I needed inside a **DataBaseConnection**
class, and created this repository for further improvements.


### Use

To properly use this class, just download/clone the repository and import the
class in your application.

```python
from psycopg_dbconn_class import DataBaseConnection
```

If you get a **ImportError** message, be sure to install **psycopg2-binary** library as well:

```shell
python -m pip install -r requirements.txt 
```
_or_
```shell
python -m pip install pycopg2-binary
```

Then, you can create an object, connect to a server and begin running queries.
By default, parameters for connecting into the server are expected do be in environment variables 
('DBN', 'DBU', 'DBK', 'DBH', 'DBP'), but you can also use a json file (_conn.json_). Finally, 
you may also enter parameters manually.

```python
from app.psycopg_dbconn_class.src.psycopg_dbconn_class import DataBaseConnection

DB = DataBaseConnection(auto_config=False)
DB.update_config_values(name='db', host='127.0.0.0', port="15432", user="postgres", password="PostgresPass")
DB.connect()

if DB.connected:
	# For queries without need of return
	DB.run_query('INSERT INTO colum VALUES (NULL)')
	DB.run_query('INSERT INTO colum VALUES (%s)', [1])
	# For queries that need the return
	result = DB.run_read_query('SELECT * FROM table WHERE val = %s', [2], fetch_all=True)
	print(result)

DB.close()
```

### Warranty

**psycopg_dbconn_class** is an open-source project. It is distributed in the hope that it will be
useful, but *WITHOUT ANY WARRANTY*; without even the implied warranty of *MERCHANTABILITY*
or *FITNESS FOR A PARTICULAR PURPOSE*. See the GNU Lesser General Public License
version 3 attached for more details.

---

Developed by: [Kleydson Stenio](mailto:kleydson.stenio@gmail.com?Subject=psycopg_dbconn_class_QUESTIONS) @ 2023
