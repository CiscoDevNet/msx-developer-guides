# Persisting Domain Specific Data
* [Introduction](#introduction)
* [Goals](#goals)
* [Prerequisites](#prerequisites)
* [Configuring the Project](#configuring-the-project)
  * [helloworld.yml](#helloworldyml)
  * [manifest.yml](#manifestyml)
  * [config.py](#configpy)
* [Adding the Datastore](#adding-the-datastore)
  * [helpers/cockroach_helper.py](#helperscockroach_helperpy)
  * [controllers/items_controller.py](#internaldatastorecockroachgo)
  * [main.go](#maingo)
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
* [The Missing Pieces](#the-missing-pieces)
* [References](#references)

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
When a service is deployed to MSX it must pick up the database configuration from Consul and Vault. The table below shows where to get those values and exampled values.

| service        | name                                                           | example |
|----------------|----------------------------------------------------------------|---------|
| consul         | thirdpartyservices/defaultapplication/db.cockroach.host        | cockroachdb-public.vms.svc.cluster.local |
| consul         | thirdpartyservices/defaultapplication/db.cockroach.port        | 26257 |
| consul         | thirdpartyservices/defaultapplication/db.cockroach.sslmode     | verify-full |
| consul         | thirdpartyservices/helloworldservice/db.cockroach.databaseName | helloworld |
| consul         | thirdpartyservices/helloworldservice/db.cockroach.username     | helloworldservice_5cf38a82c57b4872b425bb89b0d3250d |
| vault          | thirdpartyservices/helloworldservice                           | vzorfs0UFr124K5zoevP |
| helloworld.yml | cockroach.cacert                                               | /etc/ssl/certs/ca-bundle.crt |

When developing you can run Consul, Vault, and CockroachDB [(help me)](#references). You can pass required CockroachDB configuration in `helloworld.yml` by adding the following.

```yaml
.
.
.
cockroach:
  host: "127.0.0.1"
  port: "26257"
  databasename: "helloworld"
  username: "root"
  sslmode: "require"                     
  cacert: "/etc/ssl/certs/ca-bundle.crt" # Required by MSX.
.
.
.
```

<br>

### manifest.yml
When our service is deployed MSX creates the database for us, and populates Vault and Consul with the correct values. Then in our configuration code we will read those values to create our database connection string. We have to update `manifest.xml` to tell  MSX which database we want to use.

```yaml
.
.
.
Infrastructure:
  Database:
    Type: Cockroach
    Name: "helloworldservice"
.
.
.
```

<br>

### config.py
In previous guides we created `config.py` to bootstrap Consul and Vault into our service. That same module also serves as a common place for us to store other configuration. Update `config.py` to include a structure to store the CockroachDB values. Note that they will be populated from Consul, Vault, and `helloworld.yml`, depending on whether your service is running on local infrastructure or in an MSX environment.

```python
import pkgutil
from os import environ
from collections import namedtuple
import yaml

ConsulConfig = namedtuple("ConsulConfig", ["host", "port", "cacert"])
VaultConfig = namedtuple("VaultConfig", ["scheme", "host", "port", "token", "cacert"])
CockroachConfig = namedtuple("CockroachConfig", ["host", "port", "databasename", "username", "sslmode", "cacert"])


class Config(object):
    def __init__(self, resource_name):
        # Load and parse the configuration.
        resource = pkgutil.get_data(__name__, resource_name)
        config = yaml.safe_load(resource)

        # Apply environment variables and create Consul config object.
        config["consul"]["host"] = environ.get("SPRING_CLOUD_CONSUL_HOST", config["consul"]["host"])
        config["consul"]["port"] = environ.get("SPRING_CLOUD_CONSUL_PORT", config["consul"]["port"])
        self.consul = ConsulConfig(**config["consul"])

        # Apply environment variables and create Vault config object.
        config["vault"]["scheme"] = environ.get("SPRING_CLOUD_VAULT_SCHEME", config["vault"]["scheme"])
        config["vault"]["host"] = environ.get("SPRING_CLOUD_VAULT_HOST", config["vault"]["host"])
        config["vault"]["port"] = environ.get("SPRING_CLOUD_VAULT_PORT", config["vault"]["port"])
        config["vault"]["token"] = environ.get("SPRING_CLOUD_VAULT_TOKEN", config["vault"]["token"])
        self.vault = VaultConfig(**config["vault"])

        # Create cockroach config object.
        self.cockroach = CockroachConfig(**config["cockroach"])
```

## Adding the Datastore
We need to work on a few more files before the database integration is complete.

### helpers/cockroach_helper.py
The module `helpers/cockroach_helper.py` provides the code to connect to CockroachDB and perform CRUD operations.
```python

```

<br>

### controllers/languages_controller.py

### controllers/items_controller.py

### app.py