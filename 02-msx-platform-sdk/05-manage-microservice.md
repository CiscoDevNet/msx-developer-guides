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
* [Create Device](#create-device)
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


### Create Device
#### Description
Device management is a central part of some MSX Services. After calling this API, user should be able to see a device associated with a given tenant and a given service pack in the tenant centric workspace of MSX. Device can display things like description, status, model, version as well as a history of all the changes applied to the device.
A device can have live monitoring data (using MSX's monitoring capabilities) and it can be associated with one or more site.
#### API
POST /manage/api/v8/devices
#### Prerequisites
When specifying a model in the payload, ensure the device model is a device model recognized by MSX.
To verify that the device model of your choosing exists, see Device Models section. You can add a model if its not already present in MSX.
#### Inputs
The following is a sample payload for creating a device.
```javascript
{
  attributes: {
    deviceRegistrationInProgress: true,
    deviceTypeName: "CISCO CSR 1000v",
    deviceInterfaces: "[{\"name\":\"GigabitEthernet1\",\"roles\":[\"onboard\",\"wan\"],\"snmp\":\"GigabitEthernet1\",\"nedId\":\"cisco-ios\"}]",
    devicePassword: "$8$MGg7+Cx0syRusnXmOG5STbgXrQccIA+A8Dd7HKl6mrjf4VW3gr+UhpZJoh0VL7o6"
  },
  complianceState: "COMPLIANT",
  managed: false,
  model: "CISCO CSR 1000v",
  name: "CPE-25de466c-7ce7-494b-9817-f4ae8ab31bcb",
  onboardInformation: {},
  onboardType: "",
  serialKey: "FTX1738AJMG",
  serviceInstanceId: "tst310453251-3df577a4d3454c3ab7fedf4d53562231-sda",
  serviceType: "manageddevice",
  subType: "ISR",
  subscriptionId: "tst310453251-3df577a4d3454c3ab7fedf4d53562231-sda",
  tags: {},
  tenantId: "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  type: "CISCO CSR 1000v",
  version: "15.4(3) M1"
}
```
#### Inputs Explained
- attributes: {} : this one is optional. You can use it to store key-value pairs about your device.
- complianceState: defaults to UNKNOWN, but options are: UNKNOWN,COMPLIANT,NOT_COMPLIANT,NOT_APPLICABLE***
- tags: {}  : defines whether or not this device needs to be processed by other services (currently only nso is available) Set empty if not
- tenantId: required to be valid; ensure the token used to create the request has access to the tenant in question
- subscriptionId: required, if serviceType is not set. Subscription*** must be created by the same tenant provided.
- serviceInstanceId: required, if serviceType is not set. Is typically created when a subscription*** is created.
- serviceType: not required if subscriptionId and serviceInstanceId are both provided. This is the unique name of your custom service
- serialKey: required, visual identifier for the user. This will be displayed in the devices section of the workspace
- managed: this is entirely optional; can be set to true or false
- model: required, and model must match exactly the model name in the device models list. See Create device model section
- version: this model corresponds to the OS version of the device model. Suggestion is to use an accurate version, since this will be used to determine if there are any vulnerability alerts for the given model/version
- deviceOnboarding: this attribute should never be set; it is used exclusively by manageddevice and relies on the presence of vmsservice package in nso. In the event that you want to add your device to an NSO (be it your own, or the generic nso provided by MSX), setting this variable will prevent this device from being added to the NSO service.
- name: this can be whatever you choose to identify the device with
- onboardType: this is not needed if deviceOnboarding is provided.
- type/subtype: These two parameters are optional, but recommended. The values provided here can be used to filter devices in the ui (ie based on type). Setting the types/subtype for your device will enable you to create monitoring commands based on a given type/subtype, rather than having to create a new monitoring profile for each individual device.

*** Details of a subscription can be retrieved by calling GET /manage/api/v3/subscriptions It would include things like subscriptionId, serviceInstanceId and serviceType. See subscriptions api section
#### Outputs
```javascript
{
   attributes: { },
   complianceState: "COMPLIANT",
   createdOn: "yyyy-MM-dd'T'HH:mm:ss'Z'",
   id: "uniqueIdentifier",
   managed: false,
   model: "CISCO CSR 1000v",
   modifiedOn: "yyyy-MM-dd'T'HH:mm:ss'Z'",
   name: "nameofyourdevice",
   onboardInformation: { },
   providerId: "3fa85f64-5717-4562-b3fc-2c963f66afa6",
   serialKey: "FTX1738AJMG",
   serviceInstanceId: "tst310453251-3df577a4d3454c3ab7fedf4d53562231-sda",
   serviceType: "helloworld",
   status: {
      lastUpdated: "yyyy-MM-dd'T'HH:mm:ss'Z'",
      lastUpdatedMessage: "Updated by system",
      severity: "1",
      value: "GOOD"
   },
   statusDetails: {
      healthStatus: {
         value: "UP",
         severity: "3",
         lastUpdated: "2020-01-29T09:12:33.001Z",
         lastUpdatedMesage: "Updated by system user"
      },
   },
   subType: "ISR",
   subscriptionId: "tst310453251-3df577a4d3454c3ab7fedf4d53562231-sda",
   tags: {},
   tenantId: "3fa85f64-5717-4562-b3fc-2c963f66afa6",
   type: "CISCO CSR 1000v",
   userId: "3fa85f64-5717-4562-b3fc-2c963f66afa6",
   version: "15.4(3) M1",
   vulnerabilityState: "NOT_APPLICABLE"
}
```
### Outputs Explained
- createdOn: datestamp of the request
- id: uniqueIdentifier, which will be referenced as deviceId from here on in
- vulnerabilityState: will be set to not applicable by default
- userId: this field is populated based on the user that was logged in when the auth token was generated
- status: Shows the overall status of the device
- statusDetails: Shows the breakdown of the different status states (ie health, lifecycle State, etc and when the status was last modified) See the API on updating device status for options

