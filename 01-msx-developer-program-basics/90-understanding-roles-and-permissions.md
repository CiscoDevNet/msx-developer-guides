# Understanding Roles and Permissions
* [Introduction](#introduction)
* [Goals](#goals)
* [Prerequisites](#prerequisites)
* [Creating Custom Permissions](#creating-custom-permissions)
* [Creating Custom Roles](#creating-custom-roles)
* [Creating a User With Custom Roles](#creating-a-user-with-custom-roles)

## Introduction
What you can see and do in MSX is controlled by the Roles assigned to your User. MSX comes preconfigured with multiples Roles, each with a set of Permissions, where Permissions control the level of access to particular resources. For example, there is a one Permission to manage tenants, and one to read tenants. An administrator Role will be able to read and write tenants, but a general user will be restricted to read only access.

The stock roles and permissions will only get you so far. When you write a service for MSX you will need to create Roles and Permissions to support role based access control (RBAC) to the resources it creates. In this guide we show how to do that using Swagger.


# Goals
* understand Roles and Permissions
* create Permissions using Swagger
* create Roles using Swagger
* create Users using Swagger


# Prerequisites
* access to an MSX environment [(help me)](../01-msx-developer-program-basics/02-getting-access-to-an-msx-environment.md)
* experience with Swagger documentation [(help me)](../01-msx-developer-program-basics/04-using-the-swagger-documentation.md)


## Creating Custom Permissions
We will use Swagger to create resources to sidestep some constraints imposed by the user interface [(help me)](../01-msx-developer-program-basics/04-using-the-swagger-documentation.md). Capabilities are synonymous with Permissions in the UI so use the payload below with "Swagger -> IDM Microservice -> Roles -> POST /idm/api/v1/roles/capabilities" to create some custom Permissions.

```json
{
  "capabilities": 
  [
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


## Creating Custom Roles
Now that we have some Permissions we can create an administration Role with read/write access to the Language resources, and a consumer Role with read only access. Create the consumer role with read only access with the following payload and an "owner" of "helloworld" using "Swagger -> IDM Microservice -> Roles -> POST /idm/api/v1/roles".
```json
{
  "roleName" : "HELLOWORLD_CONSUMER",
  "description" : "A consumer role for the Hello World Service.",
  "capabilitylist" : ["HELLOWORLD_READ_LANGUAGE", "HELLOWORLD_READ_ITEM"],
  "displayName" : "Hello World Consumer"
}
```
<br>


Save the response as we will need the "roleid" when we create the user in the next step. Note that the "roleid" from your system will be different. 
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


## Creating a User With Custom Roles
We still need to create a user that is assigned the Role "HELLOWORLD_CONSUMER" but for it to have access to the Cisco MSX Portal we also need to give it the "OPERATOR" role. Use "Swagger -> IDM Microservice -> Roles -> GET /idm/api/v1/roles/{name}" in the  Swagger documentation to look up the role identifier for "OPERATOR". On the system we used that requests looks like this by your access token and response will be different.
```shell
$ curl -k -X GET "https://dev-plt-aio1.lab.ciscomsx.com/idm/api/v1/roles/OPERATOR" -H  "accept: application/json" -H  "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImFuZDBMV3ByYzBUckVSWSJ9.eyJzdWIiOiJzdXBlcnVzZXIiLCJsYXN0TmFtZSI6IlVzZXIiLCJ1c2VyX25hbWUiOiJzdXBlcnVzZXIiLCJyb2xlcyI6WyJTVVBFUlVTRVIiXSwiaXNzIjoiaHR0cHM6Ly9kZXYtcGx0LWFpbzEubGFiLmNpc2NvbXN4LmNvbTo0NDMvaWRtIiwiYXV0aG9yaXRpZXMiOlsiUk9MRV9DTElFTlQiXSwiY2xpZW50X2lkIjoibmZ2LWNsaWVudCIsImZpcnN0TmFtZSI6IlN1cGVyIiwic2NvcGUiOlsiYWRkcmVzcyIsImVtYWlsIiwib3BlbmlkIiwicGhvbmUiLCJwcm9maWxlIiwicmVhZCIsIndyaXRlIl0sInRlbmFudElkIjoiZDY2ZTRhMzAtMzhjZi0xMWViLTk4NDMtMDkxNmU3ZjM2OWUwIiwiZXhwIjoxNjA4MDkyNTk0LCJpYXQiOjE2MDgwNzQ1OTQsImp0aSI6ImFmYTYxMzZkLTdjMjktNDlkYS1iNjNmLTljMDg3NWU2ZTRkNiIsImVtYWlsIjoibm9yZXBseUBjaXNjby5jb20ifQ.LX23Sn4z48Brp0GZ9M2Xhgh7-lyjRHw3mZXafUvLs3TMMiGxIad3bS6bPIjoSUDYKFoBlvF3y68DijQ7lAJKqv5E9iw_iH3l0Hj-cfp1opEwYujNyWPgg57BnlkIy-UyZCjmBeg7oK2On8JM_jlG_kizJLgvwel66OwcavsOaD9ktWQ3TEGCe_MoaMwi-yrsySvBPAz4iV_AXyjS6yhNatBhH3hUqMcm6txZD7c89-weALX_uGoqDY1zChOO3VRRl6jj-W3_JH-nwthYECTL6Az3U1Mso7vUICxUZZ89B4pnti__1G-oJ1cT1UvutkQruN997NfKFQeR1S5wNkLupwfHumJV5noGtHdKioBxpqdXvui3qF65bq7kmv30_x12KZhcsF0XX-Bq1JjlJRDhMGzVht4kSqr9O3FKzMnZEwTKaFZC6Cp1WZYw-S0TlQoonuuvTyxgcQwkKLcelY8b150-zj52PO7O6S-xufx2TU8xVkfcn69YJBA1opZ3ajJTSkENnWWCKpS8gEfYSoAs8TWiZ7IneQK9BZ9ynma4704RNINiZ3beNb-UJzRIKEcOxu0E7yBpOv7Z838Pv3Y7cD0-s0cbzKjAWB1AcXIkq6Q5RVEonh0g2RA875Xn5SoPLSf7ydquJ2iTKfN1IjRfUboxPzhMGEQ9M-YNiBy92BU"
```
<br>


You now have role identifiers for HELLOWORLD_CONSUMER and OPERATOR which we can use to create a user. Expand the Swagger documentation for Users and find "Swagger -> IDM Microservice -> User -> POST /idm/api/v8/users", plug your role identifiers into the payload below, then call it.
```json
{
  "email": "nobody@example.com",
  "firstName": "Jeff",
  "lastName": "Pop",
  "password": "Password@1",
  "passwordPolicyName": "ppolicy_default",
  "roleIds": [
    "1811c107-9433-4285-872b-84d6130c8dcf", "d6660cd0-38cf-11eb-9843-0916e7f369e0"
  ],
  "tenantIds": [
    "3fa85f64-5717-4562-b3fc-2c963f66afa6"
  ],
  "username": "jeff"
}
```
<br>

If everything went according to plan you have created a user called Jeff with roles OPERATOR and HELLOWORLD_CONSUMER with a terrible password of "Password@1". The response from my test environment looks like this, but your identifiers will be different.
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


| [PREVIOUS](80-configuring-security-clients.md) | [HOME](../index.md#msx-developer-program-basics) |

