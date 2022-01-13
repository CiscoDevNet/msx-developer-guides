# Onboarding and Deploying Components
* [Introduction](#introduction)
* [Goals](#goals)
* [Prerequisites](#prerequisites)
* [An Example Component](#an-example-component)
* [Deploying the Component](#deploying-the-component)


## Introduction
In this guide we show how to onboard and deploy a third party component using the Cisco MSX Portal.


## Goals
* onboard and deploy a third party component into MSX


## Prerequisites
* access to an MSX environment [(help me)](../01-msx-developer-program-basics/02-getting-access-to-an-msx-environment.md)
* an MSX Component tarball [(help me)](artifacts/helloworldservice-1.0.0-component.tar.gz)


## An Example Component
First you must make or download an MSX Component before you can deploy it. They are distributed as tarballs containing a manifest and container(s), for convenience you can download one [here](artifacts/helloworldservice-1.0.0-component.tar.gz).


## Deploying the Component
Open Cisco MSX Portal and log in as superuser then navigate to "Settings->Component Manager".

![](images/deploying-component-1.png?raw=true)

<br>
Select "Add Component" and pick the file "helloworldservice-1.0.0-component.tar.gz" then click "Upload" and follow the instructions.

![](images/deploying-component-2.png?raw=true)

<br>
Once the upload has finished, a message box will appear prompting whether to install the component.

![](images/deploying-component-3.png?raw=true)

<br>
You can choose to install the component or upload another version of the component following the steps above.

![](images/deploying-component-4.png?raw=true)

<br>
To install the component, click on the ellipsis and select "Install"

![](images/deploying-component-5.png?raw=true)

<br>
Once the installation has finished, a message box will appear indicating success or failure.

![](images/deploying-component-6.png?raw=True)

<br>
After the message box has been dismissed, the installed component will have state "K8S_DEPLOYMENT_DONE".

![](images/deploying-component-7.png?raw=True)

Note that while you can upload multiple versions of a component, you are only allowed to install one version.


| [PREVIOUS](03-service-containerization-and-packaging.md) | [NEXT](05-service-offers-and-subscriptions.md) |  [HOME](../index.md#msx-component-manager) |
