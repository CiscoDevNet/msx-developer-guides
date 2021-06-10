# Implementing Role Based Access Control
* [Introduction](#introduction)
* [Goals](#goals)
* [Prerequisites](#prerequisites)
* [Configuring the Project](#configuring-the-project)
    * [requirements.txt](#requirementstxt)
    * [models/error.py](#modelserrorpy)
    * [Dockerfile](#dockerfile)
    * [controllers/languages_controller.py](#controllerslanguages_controllerpy)
    * [app.py](#apppy)
* [Building the Component](#building-the-component)
* [Deploying the Component](#deploying-the-component)
* [Testing the Component](#testing-the-component)
    * [Creating Custom Permissions](#creating-custom-permissions)
    * [Creating Custom Roles](#creating-custom-roles)
    * [Creating a Special User](#creating-a-special-user)
    * [Making Requests As Jeff](#making-requests-as-jeff)
* [The Missing Pieces](#the-missing-pieces)



## Introduction
All the Hello World Service requests we have made so were insecure because we have not passed an access token in the header. In this guide, we will add that security and show how to validate the access token and get a list of permissions associated with it.

<br>

## Goals
* secure the API requests
* validate the access token
* define and enforce RBAC rules

<br>

## Prerequisites
* Python Hello World Service 6 [(help me)](https://github.com/CiscoDevNet/msx-examples/tree/main/python-hello-world-service-6)
* access to an MSX environment [(help me)](../01-msx-developer-program-basics/02-getting-access-to-an-msx-environment.md)

<br>

## Configuring the Project
Adding security to the Hello World Service is an exercise in configuration. In addition to updating some existing files, we will also add some new ones. Take note of the vertical ellipsis which are used to demarcate partial updates.

<br>

### requirements.txt
An MSX integration library is required to support RBAC (roles based access control) and Tenancy. We declare that dependency in `requirements.txt` as shown:
```python
Flask==1.1.2
Flask-Cors==3.0.10
flask-restplus==0.13.0
Werkzeug==0.16.1
urllib3~=1.24.1
msxswagger @ git+https://github.com/CiscoDevNet/python-msx-swagger@v0.6.0
msxsecurity @ git+https://github.com/CiscoDevNet/python-msx-security@v0.1.0
```

<br>

### models/error.py
So far all the Hello World Service responses have been fixed. As we are going to introduce RBAC we need to declare the error model defined in the contract, so we return suitable responses.
```python
class Error:
    def __init__(self, code=None, message=None):
        self._code = code
        self._message = message

    def to_dict(self):
        return {
            "code": self._code,
            "message": self._message,
        }
```

<br>

### Dockerfile
We need to update `Dockerfile` to copy `models/error.py` to our container.
```dockerfile
.
.
.
COPY models/item.py models/item.py
COPY models/language.py models/language.py
COPY models/error.py models/error.py 
.
.
.
```

<br>

### controllers/languages_controller.py
Hello World Service uses `GET /helloworld/api/v1/items` for the health check, so we cannot add security to that endpoint. Instead, we secure the `Languages` controller updating it as follows:
```python
import flask
from flask_restplus import Resource
from models.error import Error
from models.language import Language


LANGUAGE_ENGLISH = Language(
    id="01f643a5-7e34-4366-af1a-9cce5e5c68e8",
    name="English",
    description="A West Germanic language that uses the Roman alphabet.")


LANGUAGE_RUSSIAN = Language(
    id="55f3028f-1b94-4edd-b14f-183b51b33d68",
    name="Russian",
    description="An East Slavic language that uses the Cyrillic alphabet.")


def get_access_token():
    # Authorization: Bearer MY_ACCESS_TOKEN
    return flask.request.headers.get("Authorization", "")[7:]


class LanguagesApi(Resource):
    def __init__(self, *args, **kwargs):
        self._security = kwargs["security"]

    def get(self):
        if self._security.has_permission("HELLOWORLD_READ_LANGUAGE", get_access_token()):
            return [LANGUAGE_ENGLISH.to_dict(), LANGUAGE_RUSSIAN.to_dict()], 200
        return Error(code="my_error_code", message="permission denied").to_dict(), 403

    def post(self):
        if self._security.has_permission("HELLOWORLD_WRITE_LANGUAGE", get_access_token()):
            return LANGUAGE_ENGLISH.to_dict(), 201
        return Error(code="my_error_code", message="permission denied").to_dict(), 403


class LanguageApi(Resource):
    def __init__(self, *args, **kwargs):
        self._security = kwargs["security"]

    def get(self, id):
        if self._security.has_permission("HELLOWORLD_READ_LANGUAGE", get_access_token()):
            return LANGUAGE_ENGLISH.to_dict(), 200
        return Error(code="my_error_code", message="permission denied").to_dict(), 403

    def put(self, id):
        if self._security.has_permission("HELLOWORLD_WRITE_LANGUAGE", get_access_token()):
            return LANGUAGE_ENGLISH.to_dict(), 200
        return Error(code="my_error_code", message="permission denied").to_dict(), 403

    def delete(self, id):
        if self._security.has_permission("HELLOWORLD_WRITE_LANGUAGE", get_access_token()):
            return "", 204
        return Error(code="my_error_code", message="permission denied").to_dict(), 403
```

We have added `__init__` methods to both classes, which take an `MSXSecurity` object as an argument. The convenience method `has_permission` checks if the user has a given permission, takes the permission name and MSX access token as arguments. You can pull the MSX access token out of the HTTP Authorization header.

If you want to implement Tenancy use `has_tenant`, passing it the tenant identifier you care about.

<br>

### app.py
We update the `Languages` controller to take an `MSXSecurity` object, but we have not created it yet. The update to `app.py` below configures that instance and passes it to the controller.

Update the constants declared at the start of `app.py` to match your MSX environment and security clients [(help me)](../08-python-hello-world-service-example/08-creating-the-security-clients.md). It is possible to pull these details from Consul/Vault, so you do not need to hardcode them. This will be covered in a future example.

```python
from flask import Flask
from msxsecurity import MSXSecurity, MSXSecurityConfig
from msxswagger import MSXSwaggerConfig, Security, DocumentationConfig, Sso
from controllers.items_controller import ItemsApi, ItemApi
from controllers.languages_controller import LanguageApi, LanguagesApi

SSO_URL = "https://MY_MSX_HOSTNAME/idm"
PUBLIC_CLIENT_ID = "hello-world-service-public-client"
PRIVATE_CLIENT_ID = "hello-world-service-private-client"
PRIVATE_CLIENT_SECRET = "make-up-a-private-client-secret-and-keep-it-safe"

app = Flask(__name__)

swagger_config = DocumentationConfig(
	root_path='/helloworld',
	security=Security(True, Sso(base_url=SSO_URL, client_id=PUBLIC_CLIENT_ID)))

swagger = MSXSwaggerConfig(
	app,
	swagger_config,
	swagger_resource="swagger.json")

security = MSXSecurity(MSXSecurityConfig(
    sso_url=SSO_URL,
    client_id=PRIVATE_CLIENT_ID,
    client_secret=PRIVATE_CLIENT_SECRET,
	cache_enabled=True,
	cache_ttl_seconds=300))

swagger.api.add_resource(ItemsApi, "/api/v1/items")
swagger.api.add_resource(ItemApi, "/api/v1/items/<id>")
swagger.api.add_resource(LanguagesApi, "/api/v1/languages", resource_class_kwargs={"security": security})
swagger.api.add_resource(LanguageApi, "/api/v1/languages/<id>", resource_class_kwargs={"security": security})
app.register_blueprint(swagger.api.blueprint)

if __name__ == '__main__':
	app.run()
```

<br>

## Building the Component
Like we did in earlier guides, build the component `helloworldservice-1.0.0-component.tar.gz` by calling make with component "NAME" and "VERSION" parameters.

```bash
$ make NAME=helloworldservice VERSION=1.0.0 
.
.
.
docker save helloworldservice:1.0.0 | gzip > helloworldservice-1.0.0.tar.gz
tar -czvf helloworldservice-1.0.0-component.tar.gz manifest.yml helloworldservice-1.0.0.tar.gz
a manifest.yml
a helloworldservice-1.0.0.tar.gz
rm -f helloworldservice-1.0.0.tar.gz
```

<br>

## Deploying the Component
Log in to your MSX environment and deploy `helloworldservice-1.0.0-component.tar.gz` using **MSX UI -> Settings -> Components** [(help me)](../03-msx-component-manager/04-onboarding-and-deploying-components.md). If the helloworldservice is already deployed, delete it before uploading it again.

<br>


## Testing the Component
Looking at the code above in `app.py` you can see that we only secured the Languages controller. So you can still make insecure Item requests like this.

```bash
$ export MY_MSX_HOSTNAME=dev-plt-aio1.lab.ciscomsx.com
$ curl --insecure --request GET https://$MY_MSX_HOSTNAME/helloworld/api/v1/items
[
  {
    "id": "68963944-a88c-4e39-98fd-d77878231d81", 
    "language_id": "01f643a5-7e34-4366-af1a-9cce5e5c68e8", 
    "language_name": "English", "value": "Hello, World!"
  }, 
  {
    "id": "62ef8e5f-628a-4f8b-92c9-485981205d92", 
    "language_id": "55f3028f-1b94-4edd-b14f-183b51b33d68", 
    "language_name": "Russian", 
    "value": "\u041f\u0440\u0438\u0432\u0435\u0442 \u043c\u0438\u0440!"}
]
```

However, if you try to get a collection of Languages without passing an access token, you will get an "permission denied" response.

```bash
$ export MY_MSX_HOSTNAME=dev-plt-aio1.lab.ciscomsx.com
$ curl --insecure --request GET https://$MY_MSX_HOSTNAME/helloworld/api/v1/languages
{
  "code": "my_error_code", 
  "message": "permission denied"
}
```

If you log in to the Cisco MSX Portal as superuser and go to the Swagger documentation for the Hello World Service, you will be able to make a request that works because the superuser can do everything. To restrict access to the API, we need to create some roles and permissions then assign them to a user.

<br>


### Creating Custom Permissions
To keep things simple, we will use Swagger to create the Permissions.

Capabilities are synonymous with Permissions in the UI, so use the payload below with **Swagger -> IDM Microservice -> Roles -> POST /idm/api/v1/roles/capabilities** to create the Permissions.

```json
{
  "capabilities": [
    {
      "name": "HELLOWORLD_WRITE_LANGUAGE",
      "displayName": "com.example.helloworldservice.HELLOWORLD_WRITE_LANGUAGE",
      "description": "Permission to write Hello World Language resources."
    },
    {
      "name": "HELLOWORLD_READ_LANGUAGE",
      "displayName": "com.example.helloworldservice.HELLOWORLD_READ_LANGUAGE",
      "description": "Permission to read Hello World Language resources."
    },
    {
      "name": "HELLOWORLD_WRITE_ITEM",
      "displayName": "com.example.helloworldservice.HELLOWORLD_WRITE_ITEM",
      "description": "Permission to write Hello World Item resources."
    },
    {
      "name": "HELLOWORLD_READ_ITEM",
      "displayName": "com.example.helloworldservice.HELLOWORLD_READ_ITEM",
      "description": "Permission to read Hello World Item resources."
    }
  ]
}
```

<br>

The response will look like this but with different identifiers.

```json
{
  "capabilities": [
    {
      "id": "2c6cfb30-3f2d-11eb-8762-6dbfa7fa7420",
      "name": "HELLOWORLD_WRITE_LANGUAGE",
      "displayName": "com.example.helloworldservice.HELLOWORLD_WRITE_LANGUAGE",
      "description": "Permission to write Hello World Language resources.",
      "isSeeded": "false",
      "owner": "system",
      "category": null,
      "objectName": null,
      "operation": null,
      "isDefault": null,
      "resources": null
    },
    {
      "id": "2c722b50-3f2d-11eb-8762-6dbfa7fa7420",
      "name": "HELLOWORLD_READ_LANGUAGE",
      "displayName": "com.example.helloworldservice.HELLOWORLD_READ_LANGUAGE",
      "description": "Permission to read Hello World Language resources.",
      "isSeeded": "false",
      "owner": "system",
      "category": null,
      "objectName": null,
      "operation": null,
      "isDefault": null,
      "resources": null
    },
    {
      "id": "2c73b1f0-3f2d-11eb-8762-6dbfa7fa7420",
      "name": "HELLOWORLD_WRITE_ITEM",
      "displayName": "com.example.helloworldservice.HELLOWORLD_WRITE_ITEM",
      "description": "Permission to write Hello World Item resources.",
      "isSeeded": "false",
      "owner": "system",
      "category": null,
      "objectName": null,
      "operation": null,
      "isDefault": null,
      "resources": null
    },
    {
      "id": "2c755fa0-3f2d-11eb-8762-6dbfa7fa7420",
      "name": "HELLOWORLD_READ_ITEM",
      "displayName": "com.example.helloworldservice.HELLOWORLD_READ_ITEM",
      "description": "Permission to read Hello World Item resources.",
      "isSeeded": "false",
      "owner": "system",
      "category": null,
      "objectName": null,
      "operation": null,
      "isDefault": null,
      "resources": null
    }
  ]
}
```

<br>

### Creating Custom Roles
Now that we have some Permissions we can create an administration role with read/write access to the Language resources, and a consumer role with read-only access.

Create the consumer role with read-only access with the following payload, and an `owner` of `helloworld` using **Swagger -> IDM Microservice -> Roles -> POST /idm/api/v1/roles**.

```json
{
  "roleName": "HELLOWORLD_CONSUMER",
  "description": "A consumer role for the Hello World Service.",
  "capabilitylist": [
    "HELLOWORLD_READ_LANGUAGE",
    "HELLOWORLD_READ_ITEM"
  ],
  "displayName": "Hello World Consumer"
}
```

Save the response, as we will need the `roleid` when we create the user in the next step. Note that the `roleid` from your system will be different.

```json
{
  "status": "Success",
  "href": "/v1/roles/HELLOWORLD_CONSUMER",
  "roleid": "1811c107-9433-4285-872b-84d6130c8dcf",
  "roleName": "HELLOWORLD_CONSUMER",
  "capabilitylist": [
    "HELLOWORLD_READ_ITEM",
    "HELLOWORLD_READ_LANGUAGE"
  ],
  "displayName": "Hello World Consumer",
  "description": "A consumer role for the Hello World Service.",
  "isSeeded": "false",
  "owner": "helloworld",
  "resourceDescriptor": null
}
```

Creating the administration role is left as an exercise for the reader. You need to update the name and description in the original payload and add the other Permissions.

<br>

### Creating a Special User
We still need to create a user that is assigned the Role `HELLOWORLD_CONSUMER`, but for it to have access to the Cisco MSX Portal we also need to give it the `OPERATOR` role.

Use **Swagger -> IDM Microservice -> Roles -> GET /idm/api/v1/roles/{name}** in the Swagger documentation to look up the role identifier for `OPERATOR`. On the system we used that requests looks like as follows, but your access token and response will be different.

```bash
$ export MY_MSX_HOSTNAME=dev-plt-aio1.lab.ciscomsx.com
$ curl -k -X GET "https://$MY_MSX_HOSTNAME/idm/api/v1/roles/OPERATOR" \
-H  "accept: application/json" \
-H  "Authorization: Bearer eyJhb…truncated…abc"
```

You now have role identifiers for `HELLOWORLD_CONSUMER` and `OPERATOR` which we can use to create a user.

Expand the Swagger documentation for Users and find **Swagger -> IDM Microservice -> User -> POST /idm/api/v8/user**”, plug your role identifiers into the payload below, then call it.

```json
{
  "email": "nobody@example.com",
  "firstName": "Jeff",
  "lastName": "Pop",
  "password": "Password@1",
  "passwordPolicyName": "ppolicy_default",
  "roleIds": [
    "1811c107-9433-4285-872b-84d6130c8dcf",
    "d6660cd0-38cf-11eb-9843-0916e7f369e0"
  ],
  "username": "jeff"
}
```

If everything went according to plan you have created a user called `Jeff` with roles `OPERATOR` and `HELLOWORLD_CONSUMER`, and a terrible password of `Password@1`. The response from our test environment looks like the following, but your identifiers will be different.

```json
{
  "id": "9bce0e6e-6902-4254-b939-8758c51c8e87",
  "status": "true",
  "deleted": "false",
  "username": "jeff",
  "firstName": "Jeff",
  "lastName": "Pop",
  "email": "nobody@example.com",
  "roleIds": [
    "d6660cd0-38cf-11eb-9843-0916e7f369e0",
    "1811c107-9433-4285-872b-84d6130c8dcf"
  ],
  "tenantIds": [
    "d66e4a30-38cf-11eb-9843-0916e7f369e0"
  ],
  "passwordPolicyName": "ppolicy_default",
  "password": null
}
```

## Making Requests As Jeff
If you have not used Swagger much, the last few steps might have seemed like a chore, but we hope you made it. We will cover scripting the creation of roles and permissions in a future guide to take the sting out of it.

We are now ready to make some requests as Jeff. Open the Cisco MSX Portal in an incognito browser window and login in a `jeff` with password `Password@1`.

Once you logged in navigate to the Hello World Service Swagger documentation
[(help me)](../01-msx-developer-program-basics/04-using-the-swagger-documentation.md).

![](images/requesting-jeff-1.png)

<br>

Our implementation only enforces RBAC rules on the language resources and `HELLOWORLD_CONSUMER` can only read language resources, so we should be able to do a `GET` but not `POST`, `PUT`, or `DELETE`. Here is a screenshot showing a successful `GET` request.

![](images/requesting-jeff-2.png)

<br>

The RBAC rules will prevent Jeff from creating a new language; Poor Jeff. _Aut viam inveniam aut faciam._

![](images/requesting-jeff-3.png)

<br>


## The Missing Pieces
That is it folks. We created a service from an OpenAPI Specification that integrates with MSX Swagger, and MSX Security. Then we containerized, packaged, deployed, and tested it in a production-like MSX environment.

Please check back periodically for new MSX development guides.