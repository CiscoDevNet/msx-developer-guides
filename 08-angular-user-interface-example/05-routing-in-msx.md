# Routing in MSX
* [Introduction](#introduction)
* [Goals](#goals)
* [How to Route](#how-to-route)
* [Appendix](#appendix)


## Introduction
There are times when a user needs to be redirected to another component within the tenant-centric workspace. This guide describes how to achieve that goal.


## Goals
* manage routing within MSX UI 


## How to Route
The steps below outline how to route between components. Go back to our previous example where we change the status of a device from within `service-details-tile` component. Then update the following function such that it redirects the end user to the devices page after updating the device status.

```typescript
changeDeviceStatus(): void {
  this.deviceForm.formData['Devices'].forEach(element => {
    this.devicesService.updateStatus(element.value, 'healthStatus', this.deviceForm.formData.healthstatus.value, "Hello World")
    this.devicesService.updateStatus(element.value, 'lifeCycleStatus', this.deviceForm.formData.lifecyclestatus.value, "Hello World")			
    this.$state.go('app.tenant_devices', {
      obj: {}
      }, { reload: true });
    });
}
```

That is all that is needed to direct the user to the devices view after updating the status.


## Appendix
The available states to redirect the user to in MSX are:
- app.tenant_workspace
- app.tenant_services
- app.tenant_sites
- app.tenant_siteDetails
- app.tenant_devices
- app.tenant_deviceDetails
- app.service-controls
- app.template-workspace
- app.billing-workspace
- app.template-activity-workspace
- app.tenant_offers
- app.dashboard
- app.select_dashboard
- app.opDashboard
- app.configurationlist


| [PREVIOUS](04-working-with-sites.md) | [NEXT](06-working-with-service-controls.md) | [HOME](../index.md#angular-user-interface-example) |
