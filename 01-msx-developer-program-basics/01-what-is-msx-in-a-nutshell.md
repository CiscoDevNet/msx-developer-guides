# What is MSX in a Nutshell?
* [Introduction](#introduction)
* [Goals](#goals)
* [MSX](#msx)
  * [MSX Platform](#msx-platform)
  * [MSX Service Packs](#msx-service-packs)


## Introduction
Cisco Managed Service Accelerator (MSX) is a service creation and delivery platform. This guide aims to give an overview of MSX from 30,000 feet.


## Goals
* provide Cisco Managed Service Accelerator (MSX) overview


## MSX
Cisco Managed Service Accelerator (MSX) is a service creation and delivery platform that enables the fast deployment of multi-tenant cloud-based networking services for Enterprise and Service Provider customers. Once deployed, MSX provides a complete self-service user experience that allows you to create, customize, and productize cloud services, on-demand in minutes from a single portal. The MSX solution can orchestrate physical and virtual network devices and functionality to automate end-to-end provisioning for any business use case or service topology. With an MSX solution, service turn-up time could be reduced from 4 to 6 weeks to a few days.


### MSX Platform
The foundation of MSX is a platform, which provides a unified experience with an interface and infrastructure upon which service packs can be deployed, run, and managed. Central to this functionality is a set of microservices APIs which expose MSX functionality that can be leveraged by external devices and network ecosystems.


### MSX Service Packs
Each MSX solution release offers pre-packaged software, called service packs or components, to orchestrate specific use cases. Service packs encapsulate and enable network, security, and business functionality and fully automate end-to-end service creation, which includes ordering, service chaining, orchestration, service assurance, and all necessary virtualized network functionality (VNF). With these service packs, you can quickly enable, control, and monitor the cloud-based managed services offered to customers.

Third parties can develop service packs for MSX using the rich set of APIs provided by the platform. For example, writing a multi-tenant service pack that users can subscribe to on a self-service basis. This series of guides is authored with that purpose, and attempts to answer the questions frequently asked when writing service packs. The topics we cover include:
* API design and stub generation
* integration with infrastructure
* persistence of domain specific data
* component packaging and deployment
* testing and logging
