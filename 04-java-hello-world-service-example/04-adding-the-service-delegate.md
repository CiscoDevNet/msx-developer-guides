# Adding the Service Delegate

* [Introduction](#introduction)
* [Goals](#goals)
* [Prerequisites](#prerequisites)
* [Configuring the Project](#configuring-the-project)
    * [pom.xml](pomxml)
* [The Service Delegate](#the-service-delegate)
* [Plumbing the Service Delegate](#plumbing-the-service-delegate)
* [Running it Locally](#running-it-locally)
  * [Building the Service](#building-the-service)
  * [Starting Consul](#starting-consul)
  * [Starting the Service](#starting-the-service)
  * [Testing the Service](#testing-the-service)


## Introduction
In this guide we will add the Hello World Service delegate. This is how we hook a service implementation into the generated controllers. We will just return canned responses for now, so we jump ahead to running the code.


## Goals
* create a mock Hello World Service delegate

## Prerequisites
* Java Hello World Service 1 [(help me)](https://github.com/CiscoDevNet/msx-examples/tree/main/java-hello-world-service-1)
* [Docker Desktop](https://www.docker.com/products/docker-desktop)
* [Hashicorp Consul](https://learn.hashicorp.com/tutorials/consul/docker-container-agents)
* [Lombok Plugin](https://plugins.jetbrains.com/plugin/6317-lombok)


## Configuring the Project

### pom.xml
Start by adding **Lombok** as a dependency to `pom.xml`.

```xml
.
.
.
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>
.
.
.
```

After saving `pom.xml` right-click it and select **Maven->Reload project** from the context menu.

![Reload Project](images/reload-project-1.png?raw=true)

<br>


## The Service Delegate
OpenAPI Generator created all the plumbing we need to implement our service. 

Create a Java class called `com.example.helloworldservice.controller.HelloworldApiDelegateImpl` as shown below to implement the service delegate.
<br>

![](images/service-delegate-1.png?raw=true)

Copy the code into the file and rebuild the project. The class creates some mock resources and return them irrespective of the input. We now have enough to package up and deploy to MSX.
```javascript
package com.example.helloworldservice.controller;

import com.example.helloworldservice.model.Item;
import com.example.helloworldservice.model.Language;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import java.util.Arrays;
import java.util.List;
import java.util.UUID;

/**
 * Implementation of service delegate for language and greeting items.
 */
@RequiredArgsConstructor
public class HelloworldApiDelegateImpl implements HelloworldApiDelegate {
    // Mock resources.
    private static final Language MOCK_LANGUAGE = new Language()
            .id(UUID.randomUUID())
            .name("English");

    private static final Item MOCK_ITEM = new Item()
            .id(UUID.randomUUID())
            .languageId(UUID.randomUUID())
            .languageName("English")
            .value("Hello, World!");

    // Languages
    @Override
    public ResponseEntity<Language> createLanguage(Language language) {
        return ResponseEntity
                .status(HttpStatus.CREATED)
                .body(MOCK_LANGUAGE);
    }

    @Override
    public ResponseEntity<Language> getLanguage(UUID id) {
        return ResponseEntity.ok(MOCK_LANGUAGE);
    }

    @Override
    public ResponseEntity<List<Language>> getLanguages() {
        return ResponseEntity.ok(Arrays.asList(MOCK_LANGUAGE));
    }

    @Override
    public ResponseEntity<Language> updateLanguage(UUID id, Language language) {
        return ResponseEntity.ok(MOCK_LANGUAGE);
    }

    @Override
    public ResponseEntity<Void> deleteLanguage(UUID id) {
        return ResponseEntity.noContent().build();
    }

    // Items
    @Override
    public ResponseEntity<Item> createItem(Item item) {
        return ResponseEntity
                .status(HttpStatus.CREATED)
                .body(MOCK_ITEM);
    }

    @Override
    public ResponseEntity<Item> getItem(UUID id) {
        return ResponseEntity.ok(MOCK_ITEM);
    }

    @Override
    public ResponseEntity<List<Item>> getItems(UUID languageId) {
        return ResponseEntity.ok(Arrays.asList(MOCK_ITEM));
    }

    @Override
    public ResponseEntity<Void> deleteItem(UUID id) {
        return ResponseEntity.noContent().build();
    }

    @Override
    public ResponseEntity<Item> updateItem(UUID id, Item item) {
        return ResponseEntity.ok(MOCK_ITEM);
    }
}
```



## Plumbing the Service Delegate

We still need to connect the delegate implementation to the delegate. Create the class `ControllerConfig` in the config folder as shown.

![](images/service-delegate-2.png?raw=true)



Then copy the contents below to the new config file.

```javascript
package com.example.helloworldservice.config;

import com.example.helloworldservice.controller.HelloworldApiDelegate;
import com.example.helloworldservice.controller.HelloworldApiDelegateImpl;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class ControllerConfig {
    @Bean
    public HelloworldApiDelegate helloworldApiDelegate() {
        return new HelloworldApiDelegateImpl();
    }
}
```


## Running It Locally

### Building the Service
Build the service with **Maven** from IntelliJ or a terminal window:
```shell
$ mvn clean install
.
.
.
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  3.773 s
[INFO] Finished at: 2021-02-01T11:33:58-08:00
[INFO] ------------------------------------------------------------------------
```

<br>

### Starting Consul 
Install Docker Desktop if you have not already [(help me)](https://www.docker.com/products/docker-desktop). Then use Docker to fetch and start Consul in a terminal window [(help me)](https://learn.hashicorp.com/tutorials/consul/docker-container-agents).

```shell
# Fetch the recent Docker image for Consul.
$ docker pull consul
Using default tag: latest
latest: Pulling from library/consul
Digest: sha256:6476d32fd71d3d740593068bc950672fe6835f462500cf4d01ccadaf42c8788c
Status: Image is up to date for consul:latest
docker.io/library/consul:latest

# Check that Consul Docker image exists.
$ docker images -f 'reference=consul'
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
consul              latest              7c239afe7006        13 hours ago        120MB

# Start Consul.
$ docker run \
    -d \
    -p 8500:8500 \
    -p 8600:8600/udp \
    --name=badger \
    consul agent -server -ui -node=server-1 -bootstrap-expect=1 -client=0.0.0.0

# Confirm that Consul is running.
$ docker ps
4a40948178e5        consul              "docker-entrypoint.s…"   5 seconds ago       
Up 3 seconds        8300-8302/tcp, 8600/tcp, 
8301-8302/udp, 0.0.0.0:8500->8500/tcp, 0.0.0.0:8600->8600/udp
```

<br>

### Starting the Service
Run the service by right-clicking `OpenApi2SpringBoot.java` in the IDE and selecting `Run OpenApi2SpringBoot`.

![](images/service-delegate-4.png?raw=true)

 <br>

### Testing the Service
Now that the service is running you can make a local request using curl in a terminal window.
```shell 
$ curl -X GET "http://localhost:9515/helloworldservice/helloworld/api/v1/languages"
[
  {
    "id": "af04e132-737f-4221-a72d-cd76622e8235",
    "name": "English",
    "description": "A West Germanic language that uses the Roman alphabet."
  }
]
```

Change the mock objects at the top of the class "HelloworldApiDelegateImpl" and restart the service before running the request again. You should see the change you made in the response.


## The Missing Pieces
Running the service locally is a good start but there are still a number of missing pieces before our service is useful:
* containerize the service
* package the service
* deploy the service
* persist domain specific data
* add role based access control
* create Swagger documentation


| [PREVIOUS](03-creating-a-hello-world-service-in-java.md) | [NEXT](05-building-the-component.md) | [HOME](../index.md#java-hello-world-service-example) |

