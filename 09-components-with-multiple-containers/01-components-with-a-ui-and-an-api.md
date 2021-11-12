# Components with Angular UI and Java API
* [Introduction](#introduction)
* [Goals](#goals)
* [Prerequisites](#prerequisites)
* [Generating the Angular UI](#generating-the-angular-ui)
* [Building the Angular UI](#building-the-angular-ui)
* [Building the Java Hello World Service](#building-the-java-hello-world-service)
* [Unpacking the MSX Components](#unpacking-the-msx-components)
* [Assembling the Required Files](#assembling-the-required-files)
* [Updating the Manifest](#updating-the-manifest)
* [Making the MSX Component](#making-the-msx-component)
* [Deploying the Component](#deploying-the-msx-component)
* [Testing the Component](#testing-the-msx-component)


## Introduction
All the guides so far have focussed on either building a user interface or a microservice. What if you want to deploy a single MSX Component that provides both? In this guide we walk through how to combine some earlier components into such an artifact.


## Goals
* generate an MSX native Angular interface
* build a Java Hello World microservice
* write a single MSX component manifest for them
* package and deploy the resulting component
* test that both containers got spun up


# Prerequisites
* access to an MSX environment [(help me)](../01-msx-developer-program-basics/02-getting-access-to-an-msx-environment.md)
* a generated MSX native angular UI [(help me)](../07-angular-user-interface-example/01-introduction-to-tenant-centric-ui.md)
* Java Hello World Service 4 [(help me)](https://github.com/CiscoDevNet/msx-examples/tree/main/java-hello-world-service-4)


## Generating the Angular UI
This is covered in an earlier guide [(help me)](../07-angular-user-interface-example/01-introduction-to-tenant-centric-ui.md) but we will run through the basics here. Once you have downloaded the generator open a terminal window in the `angular9-msx-service-pack-ui-generator` folder and run the following command (changing the output folder as required).

```shell
$ ./createTemplate.sh -project-name="HaemishTest1" \
-project-description="My Awesome UI for HaemishTest1" \
-image-file="./sample-image/sample.svg" \
-output-dir="/Users/hagraham/Projects/HaemishTest1"
.
.
.
                                  haemishtest1/src/ui/routed-page/routed-page.module.ts   675 bytes          [emitted]  
                                                          haemishtest1/src/ui/routes.ts   286 bytes          [emitted]  
                                                      haemishtest1/src/ui/tcui-hooks.ts    11.1 KiB          [emitted]  
                                                         haemishtest1/src/ui/ui-info.ts   707 bytes          [emitted]  
                                                             haemishtest1/tsconfig.json   450 bytes          [emitted]  
Entrypoint main = _temp.js
[0] ./src/index.js 0 bytes {0} [built]
Created base project at: [/Users/hagraham/Projects/HaemishTest1]
```

The generator creates a lot of files, but we do not need to worry about them all for the purposes of this exercise. If you navigate to the output folder it should look like this:

```
└── haemishtest1
    ├── Dockerfile
    ├── bin
    │   ├── build-dev.sh
    │   └── build.sh
    ├── config
    │   ├── manifest.yml
    │   └── nginx.conf
    ├── package.json
    ├── rollup.config.js
    ├── src
    │   ├── metadata
    │   │   └── catalogMetadata.json
    │   └── ui
    │       ├── config
    │       │   ├── devices
    │       │   │   ├── actions
    │       │   │   │   ├── components
    │       │   │   │   │   ├── device-action0.component.html
    │       │   │   │   │   └── device-action0.component.ts
    │       │   │   │   ├── device-actions.module.ts
    │       │   │   │   └── device-actions.ts
    │       │   │   ├── details
    │       │   │   │   ├── components
    │       │   │   │   │   ├── device-details-side-tile1.component.ts
    │       │   │   │   │   ├── device-details-side-tile2.component.ts
    │       │   │   │   │   ├── device-details-side-tile3.component.ts
    │       │   │   │   │   ├── device-details-tile0.component.ts
    │       │   │   │   │   ├── device-details-tile1.component.ts
    │       │   │   │   │   ├── device-details-tile2.component.ts
    │       │   │   │   │   ├── device-details-tile3.component.ts
    │       │   │   │   │   └── device-details-tiles.module.ts
    │       │   │   │   └── device-details.ts
    │       │   │   └── summary
    │       │   │       └── device-properties.ts
    │       │   ├── navigation
    │       │   │   └── service
    │       │   │       └── service-navigation.ts
    │       │   ├── service_configuration
    │       │   │   └── settings
    │       │   │       ├── service-settings.component.html
    │       │   │       ├── service-settings.component.ts
    │       │   │       └── settings.module.ts
    │       │   ├── services
    │       │   │   ├── components
    │       │   │   │   └── tiles
    │       │   │   │       ├── service-details-tile
    │       │   │   │       │   ├── service-details-tile.component.html
    │       │   │   │       │   ├── service-details-tile.component.scss
    │       │   │   │       │   └── service-details-tile.component.ts
    │       │   │   │       ├── service-subtitle-tile
    │       │   │   │       │   ├── service-subtitle-tile.component.html
    │       │   │   │       │   └── service-subtitle-tile.component.ts
    │       │   │   │       └── service-summary-tile
    │       │   │   │           ├── service-summary-tile.component.html
    │       │   │   │           └── service-summary-tile.component.ts
    │       │   │   └── service-tiles.module.ts
    │       │   ├── sites
    │       │   │   └── details
    │       │   │       ├── components
    │       │   │       │   ├── service-site-details.component.html
    │       │   │       │   ├── service-site-details.component.scss
    │       │   │       │   ├── service-site-details.component.ts
    │       │   │       │   └── site-details-tiles.module.ts
    │       │   │       └── site-details.ts
    │       │   └── subscription
    │       │       ├── pre
    │       │       │   ├── pre-subscription-form.component.html
    │       │       │   ├── pre-subscription-form.component.scss
    │       │       │   └── pre-subscription-form.component.ts
    │       │       └── subscription.module.ts
    │       ├── declarations.d.ts
    │       ├── help
    │       │   └── help.json
    │       ├── i18n
    │       │   └── i18n.json
    │       ├── manager
    │       │   └── subscription-manager.ts
    │       ├── routed-page
    │       │   ├── index.ts
    │       │   ├── routed-page.component.html
    │       │   ├── routed-page.component.ts
    │       │   └── routed-page.module.ts
    │       ├── routes.ts
    │       ├── tcui-hooks.ts
    │       └── ui-info.ts
    └── tsconfig.json
```


## Building the Angular UI
The generated project already contains everything required to build and package the application as an MSX component. Run the command below in the project folder. For me that was `/Users/hagraham/Projects/HaemishTest1/haemishtest1`:

```bash
$ npm run build
.
.
.
  adding: services/i18n/i18n.json (deflated 70%)
  adding: services/_tslib-3cd77c45.js (deflated 46%)
  adding: services/routes.js.map (deflated 39%)
  adding: services/help/ (stored 0%)
  adding: services/help/help.json (deflated 54%)
  adding: services/ui-info.js.map (deflated 47%)
  adding: slmimage-haemishtest1-1.0.0.tar.gz (deflated 2%)
```

The output of this command is a deployable MSX component. Copy the file `build/haemishtest_slm_deployable.tar.gz` to another folder.


## Building the Java Hello World Service
All you need to do for this step is download the example [(help me)](https://github.com/CiscoDevNet/msx-examples/tree/main/java-hello-world-service-4) and build it by running Maven:

```shell
$ mvn clean package
.
.
.
docker save helloworldservice:1.0.0 | gzip > helloworldservice-1.0.0.tar.gz
tar -czvf helloworldservice-1.0.0-component.tar.gz manifest.yml helloworldservice-1.0.0.tar.gz
a manifest.yml
a helloworldservice-1.0.0.tar.gz
rm -f manifest.yml
rm -f helloworldservice-1.0.0.tar.gz
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  51.251 s
[INFO] Finished at: 2021-11-11T15:05:29-05:00
[INFO] ------------------------------------------------------------------------
```

As for the Angular UI component, the output of this command is a deployable MSX component, only this time it implements a RESTful API. Copy the file `helloworldservice-1.0.0-component.tar.gz` to a different folder.


## Unpacking the MSX Components
You should now have a file called `haemishtest_slm_deployable.tar.gz` in one folder and another one called `helloworldservice-1.0.0-component.tar.gz` in a different folder. The names do not matter but `api` and `ui` are good choices. Unpack both components to get at the images and manifests.

```
$ cd api

$ tar xvfz helloworldservice-1.0.0-component.tar.gz
x manifest.yml
x helloworldservice-1.0.0.tar.gz

$ cd ../ui

$ tar xvfz haemishtest1_slm_deployable.tar.gz 
x catalogMetadata.json
x manifest.yml
x slmimage-haemishtest1-1.0.0.tar.gz
```

The structure will now look like this:
```
.
├── api
│   ├── helloworldservice-1.0.0-component.tar.gz
│   ├── helloworldservice-1.0.0.tar.gz
│   └── manifest.yml
└── ui
    ├── catalogMetadata.json
    ├── haemishtest1_slm_deployable.tar.gz
    ├── manifest.yml
    └── slmimage-haemishtest1-1.0.0.tar.gz
```

## Assembling the Required Files
We now need to assemble the required files into a new folder, so start by making a new folder called `final`. Copy the following files to the new folder as shown. Note that we only copy `manifest.yml` from the `api` folder.

```shell
$ mkdir final
$ cp api/helloworldservice-1.0.0.tar.gz final
$ cp api/manifest.yml final
$ cp ui/catalogMetadata.json final
$ cp ui/slmimage-haemishtest1-1.0.0.tar.gz final
```

## Updating the Manifest
We now have a folder that contains all the files we need, but we need to update `manifest.yml` so that it knows about both containers. Copy the container entry in `ui/manifest.yml` to `final/manifest.yml` so that it looks like this:

```yaml
#
# Copyright (c) 2021 Cisco Systems, Inc and its affiliates
# All Rights reserved
#
---
# Metadata for the service to be deployed consisting of name, description, version, and type of service.
Name: "helloworldservice"
Description: "Hello World service with support for multiple languages."
Version: "1.0.0"
Type: Internal

# Wrapper for containers making up the service to be deployed.  Each service must have at least one container section
# which describes the Docker image to be used for the service.
Containers:
  - Name: "helloworldservice"
    Version: "1.0.0"
    Artifact: "helloworldservice-1.0.0.tar.gz"
    Port: 9515 #Service listening Port
    ContextPath: /helloworldservice # Context path to configure the application routing with

    # Collection of tags which will be inserted into Consul.  These tags can be used to query and offer specific functionality
    # to the service.  Certain (required) tags are automatically appended by the deployment process.  Others are highly
    # recommended and required if services need to show inside the MSX UI.  Here are some of the tags that you should consider
    # including:
    #      - "buildNumber=1.0.19"
    #      - "instanceUuid=45b40541-35c2-4c47-9f14-5ec511b7c365"
    #      - "buildDateTime=2020-10-10T17:51:34.965122Z"
    #      - "componentAttributes=serviceName:testservice~context:test~name:Test Service~description:Test Service~parent:platform~type:platform"
    #      - "name=Test Service"
    #      - "version=1.0.19"
    Tags:
      - "3.10.0"
      - "4.0.0"
      - "4.1.0"
      - "4.2.0"
      - "buildNumber=1.0.0"
      - "name=helloworldservice"
      - "version=1.0.0"
      - "swaggerPath=/"
      - "buildDateTime=@timestamp@"
      - "application=helloworldservice"
      - "componentAttributes=serviceName:helloworldservice~context:/helloworldservice~name:helloworldservice~description:Hello World service with support for multiple languages."


    # Health check configurations.  Each container needs 1 health endpoint configured.  If a service has a specific
    # health endpoint implemented, please use the Http configuration along with the common health check section.  Otherwise,
    # for services that don't have a dedicated health endpoint implemented please configure the Tcp block and the host
    # will be pinged by the health checks instead.
    Check:
      Http:
        Scheme: "http"
        Host: "127.0.0.1" #FQDN or IP of service host if internal can be 127.0.0.1
        Path: "/helloworldservice"
      IntervalSec: 30 # how often (in seconds) should the system check if your service is up
      InitialDelaySec: 5 # initialization delay - how many seconds should the system wait after application is started before firing off the first health check request
      TimeoutSec: 30
      Port: 9515 # port to use for health checks if different from application's default listening port

    # In this section you need to specify the hardware requirements for your application.
    Limits:
      Memory: "384Mi"  # amount of memory/RAM that the application needs.  In this case the example asks for 512MB of RAM.  You should specify what your application needs based on your profiling findings.
      CPU: "1"  # number of virtual CPUs that the application needs

    # Command to use to start the application.
    Command:
      - "/service/dockerlaunch.sh"
      # Set the profile for MSX <= 4.0
      # - "-Dspring.profiles.active=legacy"
      
  - Name: "haemishtest1"
    Version: "1.0.0"
    Artifact: "slmimage-haemishtest1-1.0.0.tar.gz"
    Port: 4200
    ContextPath: "/haemishtest1ui"
    Tags:
      - "productUI"
      - "buildNumber=1.0.0"
      - "instanceUuid=8b1bde18-59d0-43a9-bd32-0c916353d19a"
      - "buildDateTime=2021-11-11T19:48:37.569Z"
      - "name=haemishtest1"
      - "version=1.0.0"
    Check:
      Http:
        Host: "127.0.0.1"
        Scheme: "http"
        Path: "/haemishtest1ui/haemishtest1.css"
      IntervalSec: 60
      InitialDelaySec: 30
      TimeoutSec: 30
    Limits:
      Memory: "256Mi"
      CPU: "1"
    Command:
      - "/docker-entrypoint.sh"
      - "nginx"
      - "-g"
      - "daemon off;"
    Endpoints:
      - "/haemishtest1ui"

# [Optional] Configuration section for infrastructure needs such as database for your application.
# List of required infra services required all are optional
# Consul and Vault access granted by default restricted to /<servicename> path in KV
# Population of Env defaults (e.g. cassandra address) will be done by onboarding service
Infrastructure:
  # Database configuration section.  The details for the account that was created for your service can be retrieved from Consul.
  # If your application needs Cassandra, the following configurations can be retrieved from Consul at startup/runtime:
  # - db.cassandra.username
  # - db.cassandra.password
  # - db.cassandra.keyspaceName
  #
  # If your application needs CockroachDB, the following configurations can be retrieved from Consul at startup/runtime:
  # - db.cockroach.username
  # - db.cockroach.password
  # - db.cockroach.databaseName
  Database:
    Type: Cockroach
    Name: "helloworldservice"
```

That might seem overwhelming but all we have done is copy the details of the UI container to the API manifest. The process is the same if our microservice is written in Java, Go, or Python. Just make sure you copy any resource files your project requires into the `final` folder.

> **GOTCHA**
>
> The `Name` field at the top of the manifest is important as it controls where MSX will write Vault and Consul configuration. If this does not match were you microservice looks for such config then your microservice will fail to spin up.


## Making the MSX Component
An MSX component is just a collection of:
* docker images
* resource files
* a manifest

So now we can bundle the contents of the `final` folder into a tarball and we are done:"

```shell
$ cd final
$ tar cvfz ../final.tar.gz *
```


## Deploying the MSX Component
Deploying an MSX component that contains multiple images is no different than deploying one with a single image [(help me)](../03-msx-component-manager/04-onboarding-and-deploying-components.md). Sign in to your MSX environment and onboard and deploy your component. As our components contains catalog metadata MSX will offer to make the catalog entries for us when it is deployed.


## Testing the MSX Component
Once the component has been onboarded and deployed wait 5 minutes for the system to spin the containers up then refresh the MSX-UI. Then go to `Tenant Workplace -> Offer Catalog` to subscribe to the Angular UI or make some `curl` requests from the command line to test the microservice [(helpme)](https://ciscodevnet.github.io/msx-developer-guides/04-java-hello-world-service-example/05-building-the-component.html#running-it-remotely). Note the Java example we used does not have Swagger integration, so it will not be accessible from the Swagger page.


| [HOME](../index.md#components-with-multiple-containers) |

