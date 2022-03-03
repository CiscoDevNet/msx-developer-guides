# Common Vault and Consul Configurations

* [Introduction](#introduction)
* [Goals](#goals)
* [Prerequisites](#prerequisites)
* [Prefix Required](#prefix-required)
* [Common Host Configuration Value](#common-host-configuration-value)
* [Common Database Configuration Values](#common-database-configuration-values)
* [Common Swagger Configuration Values](#common-swagger-configuration-values)
* [Common Security Configuration Values](#common-security-configuration-values)

## Introduction

Services and applications need to be passed configuration to control integrations and behaviours. In this section, we will discuss common Consul and Vault configurations used to bootstrap service components.

<br>

## Goals

* understanding Consul and Vault configurations

<br>

## Prerequisites

* access to an MSX environment [(help me)](../01-msx-developer-program-basics/02-getting-access-to-an-msx-environment.md)

<br>

## Prefix Required

Depending on the version of MSX you are using the Consul and Vault path prefixes are different as shown below:

| MSX Version | Consul Prefix        | Vault Prefix                |
|-------------|----------------------|-----------------------------|
| <= 4.0.0    | thirdpartyservices   | secret/thirdpartyservices   |
| >= 4.1.0    | thirdpartycomponents | secret/thirdpartycomponents |

<br>

## Common Host Configuration Value

| Name     | Source   | Path                                      | Description                   |
|----------|----------|-------------------------------------------|-------------------------------|
| DNS Host | Consul   | {prefix}/defaultapplication/msx.dns.host  | the DNS Host Name from Consul |

<br>

## Common Database Configuration Values

The database configuration values can be divided into two categories:

1. Common Configuration for common system values

| Name     | Source | Path                                             | Description                 |
|----------|--------|--------------------------------------------------|-----------------------------|
| Host     | Consul | {prefix}/defaultapplication/db.cockroach.host    | the hostname from Consul    |
| Port     | Consul | {prefix}/defaultapplication/db.cockroach.port    | the port number from Consul |
| SSL Mode | Consul | {prefix}/defaultapplication/db.cockroach.sslmode | the SSL Mode from Consul    |

2. Application Configuration for service specific values

| Name          | Source | Path                                             | Description                                 |
|---------------|--------|--------------------------------------------------|---------------------------------------------|
| Database Name | Consul | {prefix}/{servicename}/db.cockroach.databaseName | the name of database to be read from Consul |
| Username      | Consul | {prefix}/{servicename}/db.cockroach.username     | the username from Consul                    |
| Password      | Vault  | {prefix}/{servicename}/db.cockroach.password     | the password from Vault                     |

<br>

## Common Swagger Configuration Values

The Swagger Configuration values are as follows: 

| Name       | Source | Path                                                      | Description               |
|------------|--------|-----------------------------------------------------------|---------------------------|
| SSO URL    | Consul | {prefix}/defaultapplication/swagger.security.sso.baseUrl  | the SSO URL from Consul   |
| Client ID  | Consul | {prefix}/{servicename}/public.security.clientId           | the client ID from Consul |

<br>

## Common Security Configuration Values

The Security Configuration values used by third-parties to implement RBAC and Tenancy are as follows: 

| Name          | Source | Path                                                      | Description                                          |
|---------------|--------|-----------------------------------------------------------|------------------------------------------------------|
| SSO URL       | Consul | {prefix}/defaultapplication/swagger.security.sso.baseUrl  | the SSO URL from Consul                              |
| Client ID     | Consul | {prefix}/{servicename}/public.security.clientId           | the client ID from Consul                            |
| Client Secret | Vault  | {prefix}/{servicename}/integration.security.clientSecret  | the client secret from Vault                         |
| SSL Verify    | Vault  | {prefix}/{servicename}/integration.security.sslVerify     | the fingerprint to verify SSL Certificate from Vault | 

<br>

| [PREVIOUS](10-accessing-logs-with-kibana.md) | [HOME](../index.md#msx-component-manager) |
