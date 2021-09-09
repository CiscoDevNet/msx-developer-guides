# Introducing the MSX Platform SDK
* [Introduction](#introduction)
* [Goals](#goals)
* [Prerequisites](#prerequisites)
* [Java MSX Dependency](#java-msx-dependency)
* [Go MSX Dependency](#go-msx-dependency)
* [Python MSX Dependency](#python-msx-dependency)
* [MSX Microservices](#msx-microservices)
* [References](#references)


## Introduction
The MSX Platform SDK provides an interface to interact with MSX. It can be used to manage resources like tenants, users, sites, and devices. You can send HTTP requests to the microservices directly, but the recommended way to interact with MSX programmatically is via an SDK client. To make that easy we will show how to include the MSX Platform SDK client as a dependency.


## Goals
* list the microservices provided by the SDK
* describe how to include the client as a dependency


## Prerequisites
* knowledge of common build systems
* understanding of Go modules


## Java MSX Dependency
To include the MSX Platform SDK in a Java Maven project add the following to "pom.xml":
```xml
.
.
.
    <repositories>
        <repository>
            <id>jitpack.io</id>
            <url>https://jitpack.io</url>
        </repository>
    </repositories>

    <dependencies>
        <dependency>
            <groupId>com.github.CiscoDevNet</groupId>
            <artifactId>java-msx-sdk</artifactId>
            <version>v1.0.1</version>
            <scope>compile</scope>
        </dependency>
    </dependencies>
.
.
.
```


## Go MSX Dependency
To add the MSX Platform SDK to a Go project run the following:
```shell
$ go get -u github.com/CiscoDevNet/go-msx-sdk
```

Then the "require" section in "go.mod" should look something like this:
```
.
.
.
require (
	github.com/CiscoDevNet/go-msx-sdk v1.0.1 // indirect
	github.com/golang/protobuf v1.4.3 // indirect
	golang.org/x/net v0.0.0-20210226172049-e18ecbb05110 // indirect
	golang.org/x/oauth2 v0.0.0-20210311163135-5366d9dc1934 // indirect
	google.golang.org/appengine v1.6.7 // indirect
)
.
.
.
``` 


## Python MSX Dependency
To install the latest Python MSX SDK client run pip as shown:
```shell
$ pip3 install git+https://github.com/CiscoDevNet/python-msx-sdk
```

If you need to declare a dependency in `requirements.txt` so that can initialize a container you can do so by adding this:
```python
python-msx-sdk @ git+https://github.com/CiscoDevNet/python-msx-sdk@v1.0.2
```

## MSX Microservices
The MSX Platform SDK is composed of the following microservices:
* [Catalog Microservice](../02-msx-platform-sdk/10-catalog-microservice.md)
* [Manage Microservice](../02-msx-platform-sdk/11-manage-microservice.md)
* [Monitor Microservice](../02-msx-platform-sdk/12-monitor-microservice.md)
* [User Management Microservice](../02-msx-platform-sdk/13-user-management-microservice.md)
* [Workflow Microservice](../02-msx-platform-sdk/14-workflow-microservice.md)


## References
[Apache Maven](https://maven.apache.org)

[Using Go Modules](https://blog.golang.org/using-go-modules)
