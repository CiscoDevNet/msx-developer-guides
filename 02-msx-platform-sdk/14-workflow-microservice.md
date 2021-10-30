# Workflow Microservice
* [Introduction](#introduction)
* [Prerequisites](#prerequisites)
* [Requests](#requests)
    * [Workflows](#workflows)
    * [Workflow Categories](#workflow-categories)
    * [Workflow Events](#workflow-events)
    * [Workflow Instances](#workflow-instances)
    * [Workflow Schemas](#workflow-schemas)
    * [Workflow Targets](#workflow-targets)

## Introduction
This microservice manages MSX workflows and supports the various CRUD actions as well as execution and execution history for a given Tenant.

## Prerequisites
* access to an MSX environment [(help me)](../01-msx-developer-program-basics/02-getting-access-to-an-msx-environment.md)
* experience with Swagger [(help me)](../01-msx-developer-program-basics/04-using-the-swagger-documentation.md)


## Requests
This guide outlines what is possible with the service, please check back for updates that document how to make each request in detail. If you have access to an MSX environment, you can use Swagger to explore the API [(help me)](#prerequisites).
### Workflows
* Import Workflow
* Get Workflows List
* Get Workflow
* Update Workflow
* Delete Workflow
* Export Workflow
* Start Workflow
* Get Workflow Start Config
* Validate Workflow
* Get Workflow Variables
* Get Workflow Mapping by Unique Name

### Workflow Categories
* Create Category
* Get Categories List
* Get Category
* Update Category
* Delete Category

### Workflow Events
* Create Event
* Get Events List
* Get Event
* Update Event
* Delete Event

### Workflow Instances
* Get Instances List
* Get Instance
* Delete Instance
* Get Instance Action
* Cancel Instance

### Workflow Schemas
* Get Schemas List
* Get Schema

### Workflow Targets
* Create Target
* Get Targets List
* Get Target
* Update Target
* Delete Target


| [PREVIOUS](13-user-management-microservice.md) | [HOME](../index.md#msx-platform-sdk) |
|---|---|