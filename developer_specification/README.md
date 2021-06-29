# Overview

This guide explains MSX from the Service Development Architecture and Design point view. Goal is to give an overview of MSX 
capabilities and features, help understand how to develop for MSX and what can be developed and deployed.

Recommended flow: start with prerequisites section to get familiar with MSX structure, read about types of software components that compose a service, their packaging and deployment. If you have a running MSX instance try developer guides for concrete examples and API calls. Usage Examples section will give ideas of how to go about implement your MSX service.

# Prerequisites

Development for MSX follows MSX architecture. Here is a list of concepts that will help understand MSX structure. 
Service development has to take them into account.

* [What is MSX in a Nutshell?](../01-msx-developer-program-basics/01-what-is-msx-in-a-nutshell.md)
* [Getting Access to an MSX Environment](../01-msx-developer-program-basics/02-getting-access-to-an-msx-environment.md)
* [Navigating the MSX User Interface](../01-msx-developer-program-basics/03-navigating-the-msx-user-interface.md)

* [Tenancy](01-tenancy.md)
* [Users](02-users.md)
* [Roles](03-roles.md)
* [How do Permissions Work in MSX?](04-permissions-combined.md)
* [Service Catalog and Offers](05-catalog.md)
* [Billing](06-billing.md)

# Development

Typical MSX Service development flow.

* Come up with Service Concept
* Describe Service integration with MSX architecture
* [Develop Components](20-components.md)
* [Package and Deploy](../index.md#msx-component-manager)

# Usage Examples

The following example walk you throgh the implementation scenarios of different services. They are structuted towards further detailing development for MSX and have link to concrete code examples.

* [Device Monitoring](40-example-device-monitoring.md)
* [Configuring Device with NSO](41-example-configuring-device-with-nso.md)
* [Viewing Devices accross multiple DNACs](42-example-view-devices-cross-dnac.md)

# Support

* [Support](60-support.md)
