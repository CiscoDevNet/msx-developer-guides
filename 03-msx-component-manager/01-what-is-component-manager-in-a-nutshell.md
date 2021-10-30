# What is Component Manager in a Nutshell?
* [Introduction](#introduction)
* [Goals](#goals)
* [Service Primitives](#service-primitives)
* [Service Applications](#service-applications)
* [References](#references)


## Introduction
The Component Manager is a Managed Service Accelerator (MSX) feature that allows third party services developed with the Software Development Kit (SDK) to be onboarded, deployed, and published into MSX. It manages components of various types including:
* service primitives
* service applications


## Goals
* introduce Component Manager
* explain differences between primitives and applications


## Service Primitives
Service primitives provide a domain specific application programming interface (API) that extend MSX functionality. Examples include a weather forecast API and the Two-Line Element Set (TLE) API for tracking orbital elements from NASA. Once a service has been implemented and installed using Component Manager it can be orchestrated with MSX. OpenAPI Specifications are a popular way to define these contracts [(help me)](../03-msx-component-manager/07-working-with-openapi-specifications.md).


## Service Applications
Service applications are services that include a user interface component. They require some additional configuration in the manifest [(help me)](../03-msx-component-manager/02-configuring-the-component-manifest.md).


## References
[OpenAPI Specification](https://swagger.io/docs/specification/about/)

[NASA APIs](https://api.nasa.gov)


| [NEXT](02-configuring-the-component-manifest.md) | [HOME](../index.md#msx-component-manager) |
|---|---|