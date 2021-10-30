# Working With Sites
* [Introduction](#introduction)
* [Goals](#goals)
* [Adding a Site](#adding-a-site)
* [Adding a Device to Site](#adding-a-device-to-a-site)


## Introduction
Sites can be associated with multiple services and devices. In this guide we show how create a site and add a device to it.


## Goals
* create a site
* add a devices to a site


## Adding a Site
Adding a site to MSX is a similar process to adding a device. In `service-details-tile.component.html` the following adds the create-site modal:

```html
<ng-template [ngIf]="showAddSite">
  <msx-create-site *msxModalDialog [tenantId]="tenantId" serviceType="helloworld" (close)="showAddSite = false"
    [completeActions]="onCompleteActions">
  </msx-create-site>
</ng-template>
``` 

Make sure the variable `showAddSite` exists in the typescript file. If  the `tenantId` variable has not been created yet, use the code below to retrieve it from MSX local storage.

```typescript
tenantId = JSON.parse(localStorage.getItem('ngStorage-tenantItem')).tenantId;
```

Complete actions can be set as follows in the typescript file:

```typescript
onCompleteActions = [{
  label: "Add Device",
  buttonClass: "button--primary",
  commonType: "ADD_DEVICE",
  handler: () => {
    console.log("Completing the action of adding Sites. Redirect to add device screen"); 
  }
}];
```

`onCompleteActions` is a set of buttons that are displayed after the site has been successfully added.
In the example above, the user may choose to add a device after creating a site, and the handler will redirect user to the add device screen.

Now that the functionality is there, we can put it all together by calling the add site modal from within the `service-details-tile` component:

```typescript
addSiteModal(): void {
		this.showAddSite = true;
}
```

In `OnInit` add a new button in the register call:

```typescript
{
			label: "Add Site",
			buttonClass: "vms_fi_branch19003-16 button--primary",
			action: this.addSiteModal.bind(this)
}
```

## Add Existing Device To Site
The `HelloworldDeviceActionComponent0` below has been modified to include the functionality needed to enable adding a device to a site
- extract deviceId, tenantId
- retrieve all existing sites and display as a dropdown
- update the site to include the device the user has selected
- close the modal on completion

```typescript
import { Component, Input, Inject, OnInit } from '@angular/core';
import template from './device-action0.component.html';
import { AngularJSProvider } from '@msx/common';
import _ from 'lodash';
import { Form } from '@msx/forms';

@Component({
	selector: 'helloworld-service-site-details',
	template,
	providers: [
		new AngularJSProvider('msx.sitesService'),
	]
})

export class HelloworldDeviceActionComponent0 implements OnInit {
	@Input() modal: any;
	@Input() public resolve: any;
	deviceId: string;

	selectSiteForm = new Form();
	tenantId = JSON.parse(localStorage.getItem('ngStorage-tenantItem')).tenantId;
	constructor(@Inject('msx.sitesService') private sitesService: any) { }
	ngOnInit() {
		this.deviceId = _.get(this.resolve, 'data.devices[0].id');
		this.sitesService.getSitesByTenant(this.tenantId, 0, 100, false, false).then(sites => {
			let allSites = _.get(sites, 'content', []).map(site => {
				return {
					label: site.name,
					value: site.id
				};
			});
			const dropdownSites = {
				"name": "sites",
				"type": "dropdown",
				"validators": [],
				"initialValue": "",
				"properties": {
					"required": true,
					"label": "Select a site to add this device to",
					"items": allSites
				}
			};
			this.selectSiteForm.addFields([dropdownSites]);
		});
	}
	cancel() {
		if (this.modal) {
			this.modal.close();
		}
	}
	assignDeviceToSite() {
		const siteId = this.selectSiteForm.formData['sites'].value;
		this.sitesService.addDevice(siteId, this.deviceId).then(_ => {
			console.log('Success');
		}).catch(_ => {
			console.log('Fail');
		}).finally(() =>
			this.modal.close()
		);
	}
}
```

The corresponding HTML component is:
```html
<div class="modal-title sk-font-modal-title">
	Add Device
</div>
<div class="modal-body sk-font-modal-caption">
	Select the site from the dropdown that you want to add your device to
</div>
<div class="modal-footer">
	<msx-form [form]="selectSiteForm"></msx-form>
	<div class="button-bar center-buttons">
    <button tabindex="0" type="button" 
            class="button button--medium button--secondary" 
            (click)="cancel()"
            msxResourceString="cisco.common.button.cancel">
    </button>
    <button tabindex="0" type="button" 
            class="button button--medium button--cta" 
            (click)="assignDeviceToSite()"
            msxResourceString="cisco.common.button.ok">
    </button>
	</div>
</div>
```


| [PREVIOUS](03-working-with-devices.md) | [NEXT](05-routing-in-msx.md) | [HOME](../index.md#angular-user-interface-example) |
|---|---|---|
