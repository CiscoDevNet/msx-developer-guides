# Common Vault and Consul Configurations

* [Introduction](#introduction)
* [Goals](#goals)
* [Prerequisites](#prerequisites)
* [Prefix Required](#prefix-required)
* [Common Host Configuration Value](#common-host-configuration-value)
* [Common Database Configuration Values](#common-database-configuration-values)
* [Common Swagger Configuration Values](#common-swagger-configuration-values)

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

Depending on the version of MSX you are using, you would be required to use a different prefix.

| MSX Version | Prefix               |
|-------------|----------------------|
| <= 4.0.0    | thirdpartyservices   |
| >= 4.1.0    | thirdpartycomponents |

<br>

## Common Host Configuration Value

|Name      | Source   | Path                                      | Description                   |
|----------|----------|-------------------------------------------|-------------------------------|
| DNS Host | Consul   | {prefix}/defaultapplication/msx.dns.host  | Gets the DNS Host from Consul |

<br>

## Common Database Configuration Values

The database configuration values can be divided into two categories:

1. Common Configuration for common system values

| Name    | Source | Path                                             | Description                     |
|---------|--------|--------------------------------------------------|---------------------------------|
|Host     | Consul | {prefix}/defaultapplication/db.cockroach.host    | Get the hostname from Consul    |
|Port     | Consul | {prefix}/defaultapplication/db.cockroach.port    | Get the port number from Consul |
|SSL Mode | Consul | {prefix}/defaultapplication/db.cockroach.sslmode | Get the SSL Mode from Consul    |

2. Application Configuration for service specific values

| Name          | Source | Path                                             | Description                                     |
|---------------|--------|--------------------------------------------------|-------------------------------------------------|
| Database Name | Consul | {prefix}/{servicename}/db.cockroach.databaseName | Get the name of database to be read from Consul |
| Username      | Consul | {prefix}/{servicename}/db.cockroach.username     | Get the username from Consul                    |
| Password      | Vault  | {prefix}/{servicename}/db.cockroach.password     | Get the password from Vault                     |

<br>

## Common Swagger Configuration Values

The Swagger Configuration values are as follow: 

| Name       | Source | Path                                                      | Description                    |
|------------|--------|-----------------------------------------------------------|--------------------------------|
| SSO URL    | Consul | {prefix}/defaultapplication/swagger.security.sso.baseUrl  | Gets the SSO URL from Consul   |
| Client ID  | Consul | {prefix}/{servicename}/public.security.clientId           | Get the client ID from Consul  |

<br>

| [PREVIOUS](10-accessing-logs-with-kibana.md) | [HOME](../index.md#msx-component-manager) |
