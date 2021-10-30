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
Device management is a central part of some MSX Services. After calling this API, user should be able to see a device associated with a given tenant and a given service pack in the tenant-centric workspace of MSX. Devices can display things like description, status, model, version, and a history of all the changes applied to the device.
A device can have live monitoring data (using MSX's monitoring capabilities) and it can be associated with one or more sites.

#### API
POST /manage/api/v8/devices

#### Prerequisites
When specifying a model in the payload, ensure the device model is a device model recognized by MSX.
To verify that the device model of your choosing exists, see Device Models section. You can add a model if it is not already present in MSX.

#### Inputs
The following is a sample payload for creating a device.

```json
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

| Attribute         | Required    | Description |
|-------------------|-------------|-------------|
| attributes        | optional    |  You can use it to store key-value pairs about your device. |
| complianceState   |             | Defaults to UNKNOWN, options are: UNKNOWN, COMPLIANT, NOT_COMPLIANT, NOT_APPLICABLE. |
| tags              | optional    | Defines whether this device needs to be processed by other services (currently only NSO is available), set empty if not. |
| tenantId          | required    |  Ensure the token used to create the request has access to the tenant in question. |
| subscriptionId    | required if serviceType is not set | The subscription\* must be created by the same tenant provided. |
| serviceInstanceId | required if serviceType is not set | Is typically created when a subscription\* is created. |
| serviceType       | optional if subscriptionId and serviceInstanceId are set | This is the unique name of your custom service. |
| serialKey         | required    | Visual identifier for the user. This will be displayed in the devices section of the workspace. |
| managed           | optional    | Can be set to true or false. |
| model             | required    | Model must match the model name in the device models list exactly. See Create device model section. |
| version           |             | Corresponds to the OS version of the device model. Suggestion is to use an accurate version, since this will be used to determine if there are any vulnerability alerts for the given model/version. |
| deviceOnboarding  | system      | This attribute should never be set; it is used exclusively by manageddevice and relies on the presence of vmsservice package in NSO. In the event that you want to add your device to an NSO, your own or the generic NSO provided by MSX, setting this variable will prevent this device from being added to the NSO service. |
| name              |             | This can be whatever you choose to identify the device with. |
| onboardType       |             | Optional if deviceOnboarding is provided. |
| type/subtype      | recommended | The values provided here can be used to filter devices in the ui (i.e. based on type). Setting the types/subtype for your device will enable you to create monitoring commands based on a given type/subtype, rather than having to create a new monitoring profile for each individual device. |

\* Details of a subscription can be retrieved by calling `GET /manage/api/v3/subscriptions` It would include things like subscriptionId, serviceInstanceId and serviceType. See Subscriptions API section.

#### Outputs

```json
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

| Attribute            | Description |
|----------------------|-------------|
| createdOn            | Datestamp of the request. |
| id                   | A unique system generated identifier which will be referenced as deviceId from here on in. |
| vulnerabilityState   | Defaults to NOT_APPLICABLE, options are UNKNOWN, VULNERABLE, NOT_VULNERABLE, NOT_APPLICABLE. |  
| userId               | This field is populated based on the user that was logged in when the auth token was generated. |
| status               | Shows the overall status of the device. |
| statusDetails        | Shows the breakdown of the different status states (e.g. health, lifecycle state, when the status was last modified),  ee the API on updating device status for options. |


| [PREVIOUS](10-catalog-microservice.md) | [NEXT](12-monitor-microservice.md) | [HOME](../index.md#msx-platform-sdk) |
|---|---|---|