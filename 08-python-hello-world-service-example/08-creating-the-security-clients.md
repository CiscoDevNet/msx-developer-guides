# Creating the Security Clients

* [Introduction](#introduction)
* [Goals](#goals)
* [Prerequisites](#prerequisites)
* [Creating the Public Security Client](#creating-the-public-security-client)
* [Creating the Private Security Client](#creating-the-public-security-client)


## Introduction
In order to integrate the Hello World Service into the security mechanisms provided by MSX we need to create two security clients. These clients will enable us to show Swagger documentation, provide Single Sign On (SSO) flows, and enforce Role Based Access Control rules for the requests.


## Goals
* create a public security client for Hello World Service
* create a confidential security for Hello World Service


## Prerequisites
* [Configuring Security Clients](../01-msx-developer-program-basics/80-configuring-security-clients.md)
* [Understanding Roles and Permissions](../01-msx-developer-program-basics/90-understanding-roles-and-permissions.md)


## Creating the Public Security Client
We need a public security client to integrate the Swagger documentation for our service. We will also use this client to support Single Sign On (SSO) flows with Proof Key Code Exchange (PKCE) to allow us to write user interfaces and mobile applications in future guides. Use the JSON below to create a public security client for the Hello World Service using the Swagger interface in the Cisco MSX Portal [(help me)](../01-msx-developer-program-basics/80-configuring-security-clients.md).

```json
{
    "clientId":"hello-world-service-public-client",
    "grantTypes":[
        "refresh_token",
        "authorization_code"
    ],
    "maxTokensPerUser":-1,
    "useSessionTimeout":false,
    "resourceIds":[
    ],
    "scopes":[
        "address",
        "read",
        "phone",
        "openid",
        "profile",
        "write",
        "email"
    ],
    "autoApproveScopes":[
        "address",
        "read",
        "phone",
        "openid",
        "profile",
        "write",
        "email"
    ],
    "authorities":[
        "ROLE_USER",
        "ROLE_PUBLIC"
    ],
    "registeredRedirectUris":[
        "/**/swagger-sso-redirect.html"
    ],
    "accessTokenValiditySeconds":9000,
    "refreshTokenValiditySeconds":18000,
    "additionalInformation":{
    }
}
```


## Creating the Private Security Client
The confidential security client is used to validate access tokens over a secure back channel. You cannot use the Cisco MSX Portal to look up the client secret once you have created the confidential security client, so make sure you store it in a safe place. Note you should never use a confidential security client in a situation that would require you to store the client secret insecurely, for example in a user interface. 

When we deploy the secure Hello World Service with SLM [(help me)](../03-msx-component-manager/01-what-is-component-manager-in-a-nutshell.md) we will update `manifest.xml` to set the client identifiers in Consul and the client secret in Vault. In a future release SLM will take care of creating and configuring the confidential security client automatically. This is a planned improvement that will remove the need to manually handle client secrets.

```json
{
    "clientId": "hello-world-service-private-client",
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

## The Missing Pieces
With that administrative task out of the way, we can move on to adding Swagger support.
* add Swagger documentation
* add Role Based Access Control
