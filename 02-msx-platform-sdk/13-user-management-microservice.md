# User Management Microservice
* [Introduction](#introduction)
* [Prerequisites](#prerequisites)
* [Requests](#requests)
    * [Roles](#roles)
    * [Security](#security)
    * [Tenants](#tenants)
    * [Users](#users)

## Introduction
This microservice manages MSX users, user roles, and tenants. This service also manages identity providers, secrets, and other date related to authentication and authorisation. 

## Prerequisites
* access to an MSX environment [(help me)](../01-msx-developer-program-basics/02-getting-access-to-an-msx-environment.md)
* experience with Swagger [(help me)](../01-msx-developer-program-basics/04-using-the-swagger-documentation.md)


## Requests
This guide outlines what is possible with the service, please check back for updates that document how to make each request in detail. If you have access to an MSX environment, you can use Swagger to explore the API [(help me)](#prerequisites).
### Roles
* Get Roles List
* Get Role by Name

### Security
* Get Access Token
* Switch User
* Switch Tenant

### Tenants
* Create Tenant
* Get Tenants Page
* Get Tenants List
* Get Tenant
* Update Tenant
* Delete Tenant

### Users
* Create User
* Get Users
* Get User
* Update User
* Delete User
* Update Password
* Get Current User


| [PREVIOUS](12-monitor-microservice.md) | [NEXT](14-workflow-microservice.md) | [HOME](../index.md#msx-platform-sdk) |
|---|---|---|