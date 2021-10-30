# Using Python To Get an Access Token With the Password Grant
* [Introduction](#introduction)
* [Goals](#goals)
* [Prerequisites](#prerequisites)
* [Creating the Project](#creating-the-project)
* [Creating the OAuth2 Confidential Security Client](#creating-the-oauth2-confidential-security-client)
* [Adding the MSX Platform Dependency](#adding-the-msx-platform-dependency)
* [Writing the Code](#writing-the-code)
* [Running the Application](#running-the-application)


## Introduction
In this guide we will write a Python application that uses the MSX Platform SDK to get an access token using an OAuth2 password grant. We recommend that you use SSO in production, but the password grant is a quick way to programmatically kick the tires.


## Goals
* get an access token using the password grant


## Prerequisites
* access to an MSX environment[(help me)](../01-msx-developer-program-basics/02-getting-access-to-an-msx-environment.md)
* a confidential security client for your application[(help me)](../01-msx-developer-program-basics/80-configuring-security-clients.md)
* the example source code [(help me)](https://github.com/CiscoDevNet/msx-examples/tree/main/python-password-grant-demo)
* a Python IDE like PyCharm IDEA [(help me)](https://www.jetbrains.com/pycharm/)


## Creating the OAuth2 Confidential Security Client
Before we can create the Java application and write the code we need to create a confidential security client [(help me)](../01-msx-developer-program-basics/80-configuring-security-clients.md). Use this payload to create the security client on your MSX environment using Swagger:
```json
{
    "clientId": "my-test-private-client",
    "clientSecret": "make-up-a-private-client-secret-and-keep-it-safe",
    "grantTypes": [
        "password", 
        "urn:cisco:nfv:oauth:grant-type:switch-tenant", 
        "urn:cisco:nfv:oauth:grant-type:switch-user"
    ],
    "maxTokensPerUser": -1,
    "useSessionTimeout": false,
    "resourceIds": [],
    "scopes": [
        "address",
        "read",
        "phone",
        "openid",
        "profile",
        "write",
        "email",
        "tenant_hierarchy", 
        "token_details"
    ],
    "autoApproveScopes": [
        "address",
        "read",
        "phone",
        "openid",
        "profile",
        "write",
        "email",
        "tenant_hierarchy", 
        "token_details"
    ],
    "authorities": [
        "ROLE_USER"
    ],
    "accessTokenValiditySeconds": 9000,
    "refreshTokenValiditySeconds": 18000,
    "additionalInformation": {
    }
}
```


## Creating the Project
If you want to jump straight to the final solution you can download the example source code  [(help me)](https://github.com/CiscoDevNet/msx-examples/tree/examples/python-password-grant-demo). However, this guide provides step-by-step instructions if you want to work through the example.

Create a new folder then create a project with the following terminal commands:
```shell
$ mkdir python-password-grant-demo
$ cd python-password-grant-demo
```


## Adding the MSX Platform Dependency
The MSX Platform SDK client provides an easy way to make requests. To add this dependency run "pip" like this:
```shell
$ pip3 install git+https://github.com/CiscoDevNet/python-msx-sdk
```


## Writing the Code
Now that the security client has been created, and the project has been configured, we can write "main.py". Make sure you update the constants to match your MSX environment. 

```python
import python_msx_sdk
from python_msx_sdk.api_client import ApiClient
from python_msx_sdk.apis import SecurityApi, TenantsApi
from python_msx_sdk.models import TenantCreate
import uuid
import base64
import urllib3

urllib3.disable_warnings()

MY_SERVER_URL = "https://dev-plt-aio1.lab.ciscomsx.com"

# <DANGER> Do not defeat the SSL certificate in production.
VERIFY_SSL = False
# </DANGER>

MY_CLIENT_ID = "hello-world-service-private-client"
MY_CLIENT_SECRET = "make-up-a-private-client-secret-and-keep-it-safe"
MY_USERNAME = "superuser"
MY_PASSWORD = "FrmedealY((!1[ps=wCBwG!E[%|]Ob7="


def get_api_client(access_token):
    configuration = python_msx_sdk.Configuration(MY_SERVER_URL)
    configuration.verify_ssl = VERIFY_SSL
    api_client = ApiClient(configuration=configuration)
    if access_token:
        api_client.set_default_header("Authorization", "Bearer " + access_token)
    return api_client


def get_access_token(authorization, username, password):
    api_client = get_api_client(access_token=None)
    security_api = SecurityApi(api_client)
    response = security_api.get_access_token(
        authorization=authorization,
        grant_type="password",
        username=username,
        password=password)
    return response.access_token


def format_tenant(x):
    return f"{x.id}: {x.name}"


def main():
    basic_token = base64.b64encode(str.encode(MY_CLIENT_ID + ":" + MY_CLIENT_SECRET))
    basic_authorization = "Basic " + basic_token.decode()

    access_token = get_access_token(authorization=basic_authorization, username=MY_USERNAME, password=MY_PASSWORD)
    print(f"Got Access Token")
    api_client = get_api_client(access_token=access_token)
    tenants_api = TenantsApi(api_client)

    body = TenantCreate(
        name="my_unique_tenant_name_" + str(uuid.uuid4()),
        description="Nobody reaches anywhere by believing. --Osho",
        email="test@example.com",
        url="https://cisco.com")

    tenant1 = tenants_api.create_tenant(body)
    print(f"Created Tenant: {tenant1.id}")

    page0 = tenants_api.get_tenants_page(0, 100)
    print(f"Got Tenants Page")
    print("\n".join(map(lambda x: format_tenant(x), page0.contents)))

    tenants_api.delete_tenant(tenant1.id)
    print(f"Deleted Tenant: {tenant1.id}")


if __name__ == "__main__":
    main()
```


## Running the Application
If you are running against a test environment you will need to uncomment the code that defeats the SSL certificate as they are self-signed. We included this code for convenience but recommend that you do not include it in a real project.
```python
# <DANGER> Do not defeat the SSL certificate in production.
VERIFY_SSL = False  
# </DANGER>
```


Now we can run the app from a terminal window.
```shell
$ python3 main.py 
Got Access Token
Created Tenant: 07430f51-65f7-46f0-8306-0cce8cae147c
Got Tenants Page
1817ec68-e182-4865-8d83-fc13035b4811: Dandelion and Burdock
133815cb-2335-474d-8c10-3e635aba94fd: Coke
07430f51-65f7-46f0-8306-0cce8cae147c: my_unique_tenant_name_8201c582-b55c-4008-a824-5f9dc913d06d
8ab7f288-a663-4983-ab26-c48e7d13ff7d: APITEST-dn-APITEST-c66a0ad7-e3ef-4653-aa43-51d4a5731b51
8b06bda7-61a0-41cf-9aaa-61af86aeaec5: Sprite
838a148f-1175-4a11-8ac2-4e4ee0a8e048: Pepsi
Deleted Tenant: 07430f51-65f7-46f0-8306-0cce8cae147c
```

<br>

If you are having trouble running the application make sure you:
* created the security client on your MSX environment
* updated the global constants to point to your environment
* uncommented the code to defeat the SSL certificate


| [PREVIOUS](03-using-go-to-get-an-access-token-with-the-password-grant.md) | [NEXT](10-catalog-microservice.md) | [HOME](../index.md#msx-platform-sdk) |
