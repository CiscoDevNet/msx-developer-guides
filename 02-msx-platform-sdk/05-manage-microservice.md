# Manage Microservice
* [Introduction](#introduction)
* [Prerequisites](#prerequisites)
* [Requests](#requests)
    * [Devices](#devices)
    * [Device Templates](#device-templates)
    * [Services](#services)
    * [Sites](#sites)

## Introduction
This microservice lets you order products (exposed in the Catalog Microservice) and returns a service instance. As part of that functionality, this service manages control planes, device templates and connections, geocoding, orchestrators, services, sites, and subscriptions.


## Prerequisites
* access to an MSX environment [(help me)](../01-msx-developer-program-basics/02-getting-access-to-an-msx-environment.md)
* experience with Swagger [(help me)](../01-msx-developer-program-basics/04-using-the-swagger-documentation.md)


## Requests
This guide outlines what is possible with the service, please check back for updates that document how to make each request in detail. If you have access to an MSX environment, you can use Swagger to explore the API [(help me)](#prerequisites).


### Devices
* Create Device
* Get Devices Page
* Get Device
* Get Device Config
* Get Device Templates
* Add Templates to Device
* Update Templates for Device
* Delete Template from Device
* Redeploy Device

### Device Templates
* Create Template
* Get Templates Page
* Get Template
* Update Template
* Delete Template

### Services
* Submit Service Order
* Update Service Order
* Get Services Page
* Get Service
* Delete Service

### Sites
* Create Site
* Get Sites Page
* Get Site
* Update Site
* Delete Site
* Add Device to Site
* Remove Device from Site
