# Persisting Domain Specific Data
* [Introduction](#introduction)
* [Goals](#goals)
* [Prerequisites](#prerequisites)
* [Configuring the Project](#configuring-the-project)
  * [helloworld.yml](#helloworldyml)
  * [manifest.yml](#manifestyml)
  * [config.py](#configpy)
  * [Dockerfile](#Dockerfile)
  * [Makefile](#makefile)
  * [requirements.txt](#requirementstxt)
* [Adding the Datastore](#adding-the-datastore)
  * [helpers/cockroach_helper.py](#helperscockroach_helperpy)
  * [models/language.py](#modelslanguagepy)
  * [models/items.py](#modelsitempy)
  * [controllers/languages_controller.py](#controllerslanguages_controllerpy)
  * [controllers/items_controller.py](#controllersitems_controllerpy)
  * [app.py](#apppy)
* [Debugging Locally](#debugging-locally)
* [Testing Locally](#testing-locally)
  * [Creating Languages](#creating-languages)
  * [Getting All Languages](#getting-all-languages)
  * [Getting Single Languages](#getting-single-languages)
  * [Updating Languages](#updating-languages)
  * [Deleting Languages](#deleting-languages)
  * [Creating Greeting Items](#creating-greeting-items)
* [Building the Component](#building-the-component)
* [Deploying the Component](#deploying-the-component)
* [Testing Remotely](#testing-remotely)
* [Conclusion](#conclusion)

## Introduction
So far the HelloWorldService has just returned canned responses that are baked into the implementation. This was a deliberate strategy to demonstrate a minimal application with few dependencies. To make our service more useful we need to store and return real data, which we will now do. 


## Goals
* persist domain specific data
* make real HelloWorldService requests


## Prerequisites
* Python Hello World Service 4 [(help me)](https://github.com/CiscoDevNet/msx-examples/tree/main/python-hello-world-service-4)
* access to an MSX environment [(help me)](../01-msx-developer-program-basics/02-getting-access-to-an-msx-environment.md)


## Configuring the Project
Before we can update the service to handle real data we need to update the project dependencies and configuration to the database. In this project we will be using CockroachDB.

### helloworld.yml
When a service is deployed to MSX it must pick up the database configuration from Consul and Vault. The table below shows where to get those values with values.

| Service        | Name                                                 | Example |
|----------------|------------------------------------------------------|---------|
| consul         | {prefix}/defaultapplication/db.cockroach.host        | cockroachdb-public.vms.svc.cluster.local |
| consul         | {prefix}/defaultapplication/db.cockroach.port        | 26257 |
| consul         | {prefix}/defaultapplication/db.cockroach.sslmode     | verify-full |
| consul         | {prefix}/helloworldservice/db.cockroach.databaseName | helloworld |
| consul         | {prefix}/helloworldservice/db.cockroach.username     | helloworldservice_5cf38a82c57b4872b425bb89b0d3250d |
| vault          | {prefix}/helloworldservice                           | vzorfs0UFr124K5zoevP |
| helloworld.yml | cockroach.cacert                                     | /etc/ssl/certs/ca-bundle.crt |

<br>

The prefix depends on the version of MSX you are running:

| MSX Version | Prefix               |
|-------------|----------------------|
| <= 4.0.0    | thirdpartyservices   |
| >= 4.1.0    | thirdpartycomponents |

<br>

When developing you can run Consul, Vault, and CockroachDB locally [(help me)](../03-msx-component-manager/08-managing-local-infrastructure.md#running-consul-for-development). You can pass the required CockroachDB configuration in `helloworld.yml` by adding the following.

```yaml
.
.
.
cockroach:
  host: "127.0.0.1"
  port: "26257"
  databasename: "helloworld"
  username: "root"
  sslmode: "disable"               
  cacert: "/etc/ssl/certs/ca-bundle.crt" # Required by MSX.
.
.
.
```

<br>

### manifest.yml
When our service is deployed MSX creates the database for us, and populates Vault and Consul with the correct values. Then in our configuration code we will read those values to create our database connection string. We have to update `manifest.yml` to tell  MSX which database we want to use.

```yaml
.
.
.
Infrastructure:
  Database:
    Type: Cockroach
    Name: "helloworld"
.
.
.
```

<br>

### config.py
In previous guides we created `config.py` to bootstrap Consul and Vault into our service. That same module also serves as a common place for us to store other configuration. Update `config.py` to include a structure to store the CockroachDB values. Note that they will be populated from Consul, Vault, and `helloworld.yml`, depending on whether your service is running on local infrastructure or in an MSX environment.

Add a named tuple to `config.py` for the Cockroach configuration:

```python
.
.
.
ConsulConfig = namedtuple("ConsulConfig", ["host", "port", "cacert"])
VaultConfig = namedtuple("VaultConfig", ["scheme", "host", "port", "token", "cacert"])
CockroachConfig = namedtuple("CockroachConfig", ["host", "port", "databasename", "username", "sslmode", "cacert"])
.
.
.
```

Then populate it in the `__init__` method:

```python
    def __init__(self, resource_name):
        .
        .
        .
        # Apply environment variables and create Vault config object.
        config["vault"]["scheme"] = environ.get("SPRING_CLOUD_VAULT_SCHEME", config["vault"]["scheme"])
        config["vault"]["host"] = environ.get("SPRING_CLOUD_VAULT_HOST", config["vault"]["host"])
        config["vault"]["port"] = environ.get("SPRING_CLOUD_VAULT_PORT", config["vault"]["port"])
        config["vault"]["token"] = environ.get("SPRING_CLOUD_VAULT_TOKEN", config["vault"]["token"])
        self.vault = VaultConfig(**config["vault"])

        # Create Cockroach config object.
        self.cockroach = CockroachConfig(**config["cockroach"])
        .
        .
        .
```

<br>

### Dockerfile
No changes are required in the Dockerfile.

<br>

### Makefile
No changes are required in the Makefile.

<br>

### requirements.txt
The code we added above has dependencies on Vault, so we have to update `requirements.txt`.

```
Flask==1.1.2
Flask-Cors==3.0.10
flask-restplus==0.13.0
Werkzeug==0.16.1
PyYAML==5.4.1
python-consul==1.1.0
urllib3==1.24.1
hvac==0.10.14
psycopg2-binary==2.9.1
```

## Adding the Datastore
We need to work on a few more files before the database integration is complete.

### helpers/cockroach_helper.py
The module `helpers/cockroach_helper.py` provides the code to connect to CockroachDB and perform CRUD operations.

```python
import uuid
import logging
import psycopg2

from config import Config
from helpers.consul_helper import ConsulHelper
from helpers.vault_helper import VaultHelper

new_language_dict = {'id': '55f3028f-1b94-4edd-b14f-183b51b33d68',
                     'name': 'Russian',
                     'description': 'An East Slavic language that uses the Cyrillic alphabet.'}

new_item_dict = {'id': '62ef8e5f-628a-4f8b-92c9-485981205d92',
                 'languageid': '55f3028f-1b94-4edd-b14f-183b51b33d68',
                 'languagename': 'Russian',
                 'value': 'Привет мир!'}


class CockroachHelper(object):
    def __init__(self, config: Config):
        consul_helper = ConsulHelper(config.consul)
        vault_helper = VaultHelper(config.vault)
        cockroach_config = config.cockroach

        self._conn = None
        # Common configuration.
        self._host = consul_helper.get_string(
            f"{config.config_prefix}/defaultapplication/db.cockroach.host",
            cockroach_config.host)
        self._port = consul_helper.get_string(
            f"{config.config_prefix}/defaultapplication/db.cockroach.port",
            cockroach_config.port)
        self._sslmode = consul_helper.get_string(
            f"{config.config_prefix}/defaultapplication/db.cockroach.sslmode",
            cockroach_config.sslmode)

        # Application configuration.
        self._databasename = consul_helper.get_string(
            f"{config.config_prefix}/helloworldservice/db.cockroach.databaseName",
            cockroach_config.databasename)
        self._username = consul_helper.get_string(
            f"{config.config_prefix}/helloworldservice/db.cockroach.username",
            cockroach_config.username)
        self._password = vault_helper.get_string(
            f"{config.config_prefix}/helloworldservice",
            "db.cockroach.password",
            "")
        self._cacert = cockroach_config.cacert

    def __enter__(self):
        if self._sslmode == 'disable':
            connection_str = f'postgres://{self._username}:{self._password}@{self._host}:{self._port}/{self._databasename}?sslmode={self._sslmode}'
        else:
            connection_str = f'postgres://{self._username}:{self._password}@{self._host}:{self._port}/{self._databasename}?sslmode={self._sslmode}&sslrootcert={self._cacert}'
        logging.info(f'Opening database connection {connection_str}')
        self._conn = psycopg2.connect(connection_str)
        logging.info(f'Connection status={self._conn.status}')
        return self

    def __exit__(self, ex_type, ex_value, traceback):
        logging.info('Closing database connection ...')
        self._conn.close()
        logging.info('Database connection closed')

        if ex_type:
            logging.info(f'{ex_type}{ex_value}{traceback}')

        return False  # Return True if you want to suppress full exception message and stack trace.

    def log_status(self):
        logging.info(f'Database connection status={self._conn.status}')

    def log_column(self, table, column):
        rows = self.get_rows(table)
        res = [row[column] for row in rows]
        logging.info(f'{column}@{table}= {str(res)}')

    def test(self):
        logging.info(self.create_table('Languages', ['id', 'name', 'description']))
        logging.info(self.create_table('Items', ['id', 'languageid', 'languagename', 'value']))

        self.log_column('Languages', 'name')
        self.log_column('Items', 'languagename')

        row = self.insert_row('Languages', new_language_dict)
        logging.info(row)
        language_id = row['id']

        row = self.insert_row('Items', new_item_dict)
        logging.info(row)
        item_id = row['id']

        self.log_column('Languages', 'name')
        self.log_column('Items', 'languagename')

        self.log_column('Items', 'value')
        logging.info(self.update_row('Items', item_id, {'value': 'Привет рим!'}))
        self.log_column('Items', 'value')

        logging.info(self.delete_row('Languages', language_id))
        logging.info(self.delete_row('Items', item_id))

        self.log_column('Languages', 'name')
        self.log_column('Items', 'languagename')

    def get_rows(self, table_name):
        listof_rows = []
        query = f'SELECT * FROM {table_name}'

        logging.info(f'Database executing={query}')
        with self._conn.cursor() as cur:
            cur.execute(query)
            columns = [desc[0] for desc in cur.description]
            rows = cur.fetchall()
            self._conn.commit()
            for row in rows:
                row_dict = dict(zip(columns, row))
                listof_rows.append(row_dict)
            statusmessage = cur.statusmessage

        logging.info(f'Database status message={statusmessage}')
        return listof_rows

    def get_row(self, tablename, keyvalue):
        query = f"SELECT * FROM {tablename}  where ID='{keyvalue}'"
        row = {}
        logging.info(f'Database executing={query}')
        with self._conn.cursor() as cur:
            cur.execute(query)
            columns = [desc[0] for desc in cur.description]
            dbrow = cur.fetchone()
            self._conn.commit()
            statusmessage = cur.statusmessage
            if dbrow:
                row = dict(zip(columns, dbrow))

        logging.info(f'Database status message={statusmessage}')
        return row

    def update_row(self, tablename, id, row_values_dict):
        l = [k + "='" + v + "'" for (k, v) in row_values_dict.items() if v]
        set_pairs = ','.join(l)
        update_clause = f"UPDATE {tablename} SET {set_pairs} WHERE id = '{id}'"

        logging.info(f'Database executing={update_clause}')
        with self._conn.cursor() as cur:
            cur.execute(update_clause)
            statusmessage = cur.statusmessage

        self._conn.commit()
        logging.info(f'Database status message={statusmessage}')
        return self.get_row(tablename, id)

    def create_table(self, tablename, col_name_list):
        columns = '  STRING, '.join(col_name_list) + '  STRING' + ', PRIMARY KEY (' + col_name_list[0] + ')'
        create_clause = f'CREATE TABLE IF NOT EXISTS {tablename} ({columns})'

        logging.info(f'Database executing={create_clause}')
        with self._conn.cursor() as cur:
            cur.execute(create_clause)
            statusmessage = cur.statusmessage

        self._conn.commit()
        logging.info(f'Database status message={statusmessage}')
        return statusmessage

    def insert_row(self, tablename, row_values_dict):
        row_values_dict['id'] = str(uuid.uuid4())
        columns = ','.join(row_values_dict.keys())
        values = ','.join("'" + key + "'" for key in row_values_dict.values())
        upsert_clause = f'UPSERT INTO {tablename} ({columns}) VALUES ({values})'

        logging.info(f'Database executing={upsert_clause}')
        with self._conn.cursor() as cur:
            cur.execute(upsert_clause)
            statusmessage = cur.statusmessage

        self._conn.commit()
        logging.info(f'Database status message={statusmessage}')
        return row_values_dict

    def delete_row(self, tablename, id):
        delete_clause = f"DELETE FROM {tablename} WHERE ID='{id}'"

        logging.info(f'Database executing={delete_clause}')
        with self._conn.cursor() as cur:
            cur.execute(delete_clause)
            statusmessage = cur.statusmessage

        self._conn.commit()
        logging.info(f'Database status message={statusmessage}')
        return statusmessage

    def delete_rows(self, tablename):
        delete_clause = f"DELETE FROM {tablename}"

        logging.info(f'Database executing={delete_clause}')
        with self._conn.cursor() as cur:
            cur.execute(delete_clause)
            statusmessage = cur.statusmessage

        self._conn.commit()
        logging.info(f'Database status message={statusmessage}')
        return statusmessage
```

<br>

### models/language.py
Update `models/language.py` so that the constructor can populate an instance from a database row.

```python
class Language:
	def __init__(self, id=None, name=None, description=None, row=None):
		if row:
			self._id = row["id"]
			self._name = row["name"]
			self._description = row["description"]
		else:
			self._id = id
			self._name = name
			self._description = description

	def to_dict(self):
		return {
			"id": self._id,
			"name": self._name,
			"description": self._description
		}
```

<br>

### models/item.py
Update `models/item.py` so that the constructor can populate an instance from a database row.

```python
class Item:
	def __init__(self, id=None, language_id=None, language_name=None, value=None, row=None):
		if row:
			self._id = row.get("id", None)
			self._language_id = row.get("languageid", None)
			self._language_name = row.get("languagename", None)
			self._value = row.get("value", None)
		else:
			self._id = id
			self._language_id = language_id
			self._language_name = language_name
			self._value = value

	def to_dict(self):
		return {
			"id": self._id,
			"languageId": self._language_id,
			"languageName": self._language_name,
			"value": self._value
		}
```

<br>

### controllers/languages_controller.py
Update `controllers/languages_controller.py` to perform database operations instead of returning fixed responses.

```python
import http
import logging
from flask_restplus import Resource
from flask_restplus import reqparse
from models.language import Language
from helpers.cockroach_helper import CockroachHelper

LANGUAGE_INPUT_ARGUMENTS = ['name', 'description']

LANGUAGE_NOT_FOUND = 'Language not found'


class LanguagesApi(Resource):
    def __init__(self, *args, **kwargs):
        self._config = kwargs["config"]
        
    def get(self):
        with CockroachHelper(self._config) as db:
            rows = db.get_rows('Languages')
            logging.info(rows)

        languages = [Language(row=x) for x in rows]
        return [x.to_dict() for x in languages], http.HTTPStatus.OK

    def post(self):
        parser = reqparse.RequestParser()
        [parser.add_argument(arg) for arg in LANGUAGE_INPUT_ARGUMENTS]
        args = parser.parse_args()
        logging.info(args)

        with CockroachHelper(self._config) as db:
            row = db.insert_row('Languages', args)
            return Language(row=row).to_dict(), http.HTTPStatus.CREATED


class LanguageApi(Resource):
    def get(self, id):
        with CockroachHelper(self._config) as db:
            row = db.get_row('Languages', id)
            if not row:
                return LANGUAGE_NOT_FOUND, http.HTTPStatus.NOT_FOUND

            return Language(row=row).to_dict(), http.HTTPStatus.OK

    def put(self, id):
        parser = reqparse.RequestParser()
        [parser.add_argument(arg) for arg in LANGUAGE_INPUT_ARGUMENTS]
        args = parser.parse_args()
        logging.info(args)        

        with CockroachHelper(self._config) as db:
            row = db.update_row('Languages', id, args)
            if not row:
                return LANGUAGE_NOT_FOUND, http.HTTPStatus.NOT_FOUND

            return Language(row=row).to_dict(), http.HTTPStatus.OK

    def delete(self, id):
        with CockroachHelper(self._config) as db:
            result = db.delete_row("Languages", id)
            if result == "DELETE 1":
                 return None, http.HTTPStatus.NO_CONTENT

            return LANGUAGE_NOT_FOUND, http.HTTPStatus.NOT_FOUND



```

<br>

### controllers/items_controller.py
Update `controllers/languages_controller.py` to perform database operations instead of returning fixed responses.

```python
import http
import logging
from flask_restplus import Resource
from flask_restplus import reqparse
from helpers.cockroach_helper import CockroachHelper
from models.item import Item

ITEM_INPUT_ARGUMENTS = ['languageId', 'value']

ITEM_NOT_FOUND = 'Item not found'

LANGUAGE_NOT_FOUND = 'Language not found'

LANGUAGE_ID_IS_REQUIRED = 'Language id is required'


class ItemsApi(Resource):
    def __init__(self, *args, **kwargs):
        self._config = kwargs["config"]
        
    def get(self):
        with CockroachHelper(self._config) as db:
            rows = db.get_rows('Items')
            logging.info(rows)

        items = [Item(row=x) for x in rows]
        return [x.to_dict() for x in items], http.HTTPStatus.OK

    def post(self):
        parser = reqparse.RequestParser()
        [parser.add_argument(arg) for arg in ITEM_INPUT_ARGUMENTS]
        args = parser.parse_args()
        logging.info(args)        
        
        if "languageId" not in args or not args["languageId"]:
            return LANGUAGE_ID_IS_REQUIRED, http.HTTPStatus.BAD_REQUEST
        args['languageid'] = args.pop('languageId')

        with CockroachHelper(self._config) as db:
            language_row = db.get_row('Languages', args["languageid"])
            logging.info(language_row)
            if not language_row:
                return LANGUAGE_NOT_FOUND, http.HTTPStatus.BAD_REQUEST
            args["languagename"] = language_row["name"]

            row = db.insert_row('Items', args)
            return Item(row=row).to_dict(), http.HTTPStatus.CREATED
        return None, http.HTTPStatus.INTERNAL_SERVER_ERROR


class ItemApi(Resource):
    def get(self, id):
        with CockroachHelper(self._config) as db:
            row = db.get_row('Items', id)
            if not row:
                return ITEM_NOT_FOUND, http.HTTPStatus.NOT_FOUND

            return Item(row=row).to_dict(), http.HTTPStatus.OK

    def put(self, id):
        parser = reqparse.RequestParser()
        [parser.add_argument(arg) for arg in ITEM_INPUT_ARGUMENTS]
        args = parser.parse_args()
        logging.info(args)

        if 'languageId' not in args or not args['languageId']:
            return LANGUAGE_ID_IS_REQUIRED, http.HTTPStatus.BAD_REQUEST
        args['languageid'] = args.pop('languageId')

        with CockroachHelper(self._config) as db:
            language_row = db.get_row('Languages', args["languageid"])
            if not language_row:
                return LANGUAGE_NOT_FOUND, http.HTTPStatus.BAD_REQUEST
            args["languagename"] = language_row["name"]

            row = db.update_row('Items', id, args)
            if not row:
                return ITEM_NOT_FOUND, http.HTTPStatus.NOT_FOUND
            return Item(row=row).to_dict(), http.HTTPStatus.OK

    def delete(self, id):
        with CockroachHelper(self._config) as db:
            result = db.delete_row('Items', id)
            if result != 'DELETE 1':
                return ITEM_NOT_FOUND, http.HTTPStatus.NOT_FOUND

            return result, http.HTTPStatus.NO_CONTENT
```

<br>

### app.py
The controllers above needs the application configuration in order to connect to the database. Pass that configuration to the controllers in `app.py` as shown below. 

```python
.
.
.
with CockroachHelper(config) as db:
    db.test()

api = Api(app)
api.add_resource(ItemsApi, "/helloworld/api/v1/items", resource_class_kwargs={"config": config})
api.add_resource(ItemApi, "/helloworld/api/v1/items/<id>", resource_class_kwargs={"config": config})
api.add_resource(LanguagesApi, "/helloworld/api/v1/languages", resource_class_kwargs={"config": config})
api.add_resource(LanguageApi, "/helloworld/api/v1/languages/<id>", resource_class_kwargs={"config": config})
.
.
.
```


## Debugging Locally
At this juncture we are code complete, and all that remains is to test. If you are feeling lucky build, package, and deploy the component into MSX and cross your fingers that everything is correct. However running the service locally makes it easier to debug. First spin up Consul, Vault, and CockroachDB using Docker Desktop instances, then create the "helloworld" database [(help me)](../03-msx-component-manager/08-managing-local-infrastructure.md#starting-cockroachdb-locally).


## Testing Locally
Once Hello World Service is running, experiment with commands below in a terminal window. Remember we defined the contract for this API as an OpenAPI Specification so refer to that for details of requests [(help me)](../03-msx-component-manager/07-working-with-openapi-specifications.md).

### Creating Languages
Create an entry for the French language with POST request. Note that the "id" returned will be different in your request.

```bash
$ curl --request POST "http://localhost:8080/helloworld/api/v1/languages" \
--header "Content-Type: application/json" \
--data '{"name": "English", "description": "A West Germanic language that uses the Roman alphabet."}'

RESPONSE HTTP-201 Created
{
  "id":"dbedcc96-6669-4286-bc72-84fc2c7623b8",
  "name":"English",
  "description":"A West Germanic language that uses the Roman alphabet."
}

$ curl --request POST "http://localhost:8080/helloworld/api/v1/languages" \
--header "Content-Type: application/json" \
--data '{"name": "French", "description": "A West Germanic language that uses the Roman alphabet."}'

RESPONSE HTTP-201 Created
{
  "id":"0e118c70-d000-4acd-8c58-e649ce5d6fe4",
  "name":"French",
  "description":"A Romance language descended from the Vulgar Latin of the Roman Empire."
}
```

<br>

### Getting All Languages
Get a list of all languages using a GET request.

```bash
$ curl --request GET "http://localhost:8080/helloworld/api/v1/languages" \
--header "Content-Type: application/json" 

RESPONSE HTTP-200 OK
[
  {
    "id":"0e118c70-d000-4acd-8c58-e649ce5d6fe4",
    "name":"French",
    "description":"A Romance language descended from the Vulgar Latin of the Roman Empire."
  },
  {
    "id":"dbedcc96-6669-4286-bc72-84fc2c7623b8",
    "name":"English",
    "description":"A West Germanic language that uses the Roman alphabet."
  }
]
```


<br>

### Getting Single Languages
Retrieve a language by copying the "id" returned by the GET request.

```bash
$ curl --request GET "http://localhost:8080/helloworld/api/v1/languages/0e118c70-d000-4acd-8c58-e649ce5d6fe4" \
--header "Content-Type: application/json" 

RESPONSE HTTP-200 OK
{
  "id":"0e118c70-d000-4acd-8c58-e649ce5d6fe4",
  "name":"French",
  "description":"A Romance language descended from the Vulgar Latin of the Roman Empire."
}
```

<br>

### Updating Languages
We can change the description of the language with a PUT request.

```bash
$ curl --request PUT "http://localhost:8080/helloworld/api/v1/languages/0e118c70-d000-4acd-8c58-e649ce5d6fe4" \
--header "Content-Type: application/json" \
--data '{"name": "French", "description": "French evolved from the Latin spoken in Gaul by Asterix."}'

RESPONSE HTTP-200 OK
{
  "id":"0e118c70-d000-4acd-8c58-e649ce5d6fe4",
  "name":"French",
  "description":"French evolved from the Latin spoken in Gaul by Asterix."
}
```

<br>

### Deleting Languages
Finally, delete a language with a DELETE request.

```bash
$ curl --request DELETE "http://localhost:8080/helloworld/api/v1/languages/0e118c70-d000-4acd-8c58-e649ce5d6fe4" 

RESPONSE HTTP-204 No Content
```

<br>

### Creating Greeting Items
We deleted the French language item, but we can still create a greeting item for English.

```bash
$ curl --request POST "http://localhost:8080/helloworld/api/v1/items" \
--header "Content-Type: application/json" \
--data '{ "languageId": "dbedcc96-6669-4286-bc72-84fc2c7623b8", "value": "Hello, World!"}'

RESPONSE HTTP-201 OK
{
"id":"023cd7f6-37ef-4e85-90b8-9441ca2b1163",
"languageId":"dbedcc96-6669-4286-bc72-84fc2c7623b8",
"languageName":"English",
"value":"Hello, World!"
}
```

Now that you know how to make language and greeting requests try adding some languages and greetings of your own.

## Building the Component
Like we did in earlier guides build the component `helloworldservice-1.0.0-component.tar.gz` by calling make with component "NAME" and "VERSION" parameters. If you do not see `helloworld.yml` being added to the tarball you need to back and check the Makefile.

```bash
$ make NAME=helloworldservice VERSION=1.0.0
.
.
.
docker save helloworldservice:1.0.0 | gzip > helloworldservice-1.0.0.tar.gz
tar -czvf helloworldservice-1.0.0-component.tar.gz manifest.yml helloworld.yml helloworldservice-1.0.0.tar.gz
a manifest.yml
a helloworld.yml
a helloworldservice-1.0.0.tar.gz
rm -f helloworldservice-1.0.0.tar.gz
```


## Deploying the Component
Log in to your MSX environment and deploy `helloworldservice-1.0.0-component.tar.gz` using **MSX UI->Settings->Components** [(help me)](../03-msx-component-manager/04-onboarding-and-deploying-components.md). If the helloworldservice is already deployed, delete it before uploading it again.


## Testing Remotely
Now that you have deployed your service to an MSX environment you can make remote calls but there is a wrinkle, you need to pass a valid access token in the request. The best way to iron that out is to complete the Swagger guide [(help me)](09-adding-swagger-support.md), but before you can do that you have to create the SSO Security Clients [(help me)](08-creating-the-security-clients.md).


## Conclusion
In this guide we persisted domain specific data to CockroachDB. We walked through testing locally, which is better for development purposes, but also deploying to a real system.


| [PREVIOUS](05-adding-vault-configuration.md) | [NEXT](08-creating-the-security-clients.md) | [HOME](../index.md#python-hello-world-service-example) |
