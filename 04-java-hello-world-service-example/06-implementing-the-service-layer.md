# Implementing the Service Layer

* [Introduction](#introduction)
* [Goals](#goals)
* [Prerequisites](#prerequisites)
* [Writing the Languages Service](#writing-the-languages-service)
* [Writing the Items Service](#writing-the-items-service)
* [Updating the Delegate](#updating-the-delegate)
* [Configuring the Services](#configuring-the-services)
* [Configuring the Controller](#configuring-the-controller)
* [Building and Deploying the Service](#building-and-deploying-the-service)
* [The Missing Pieces](#the-missing-pieces)


## Introduction
In this guide we further abstract the service implementation by moving the mock responses into separate classes for each resource types. This makes the code easier to manage as it further separates the implementation from the interface. If we put all the logic in the delegate, it will become unmanageable as the service grows. Think of it as a plumbing between the interface and the implementation.


## Goals
* create resource service implementations
* plumb them into the service delegate


## Prerequisites
* Java Hello World Service 2 [(help me)](https://github.com/CiscoDevNet/msx-examples/tree/main/java-hello-world-service-2)
* access to an MSX environment [(help me)](../01-msx-developer-program-basics/02-getting-access-to-an-msx-environment.md)
* [Docker Desktop](https://www.docker.com/products/docker-desktop)


## Writing the Languages Service
Start by creating a `service` source folder in the project root and add a class called `LanguagesService` as shown below.
![](images/service-layer-1.png?raw=true)

<br>

Update `LanguagesService` to return the mock responses that we created in an earlier guide.
```javascript
package com.example.helloworldservice.service;

import com.example.helloworldservice.model.Language;
import lombok.RequiredArgsConstructor;

import java.util.Arrays;
import java.util.List;
import java.util.UUID;

@RequiredArgsConstructor
public class LanguagesService {
    // Mock resources.
    private static final Language MOCK_LANGUAGE = new Language()
            .id(UUID.randomUUID())
            .name("English")
            .description("A West Germanic language that uses the Roman alphabet.");

    public Language saveLanguage(Language language) {
        return MOCK_LANGUAGE;
    }

    public Language getLanguage(UUID languageId) {
        return MOCK_LANGUAGE;
    }

    public List<Language> getAllLanguages() {
        return Arrays.asList(MOCK_LANGUAGE);
    }

    public Language updateLanguage(UUID languageId, Language language) {
        return MOCK_LANGUAGE;
    }

    public void deleteLanguage(UUID languageId) {
    }
}
```


## Writing the Items Service
Do the same thing for the `ItemsService` class.
```javascript
package com.example.helloworldservice.service;

import com.example.helloworldservice.model.Item;
import lombok.RequiredArgsConstructor;

import java.util.Arrays;
import java.util.List;
import java.util.UUID;


@RequiredArgsConstructor
public class ItemsService {
    private final LanguagesService languageService;
    
    // Mock resources.
    private static final Item MOCK_ITEM = new Item()
            .id(UUID.randomUUID())
            .languageId(UUID.randomUUID())
            .languageName("English")
            .value("Hello, World!");

    public Item saveGreeting(Item item) {
        return MOCK_ITEM;
    }

    public Item getGreeting(UUID greetingId) {
        return MOCK_ITEM;
    }

    public List<Item> getAllGreetingsByLanguage(UUID languageId) {
        return Arrays.asList(MOCK_ITEM);
    }

    public Item updateGreeting(UUID greetingId, Item item) {
        return MOCK_ITEM;
    }

    public void deleteGreeting(UUID greetingId) {
    }
}
```


## Updating the Delegate
Now we have written the resource services we can call them from the delegate by updating the `HelloworldApiDelegateImpl` class. We use Lombok to create the constructor for us, but you can do it manually if you want to do extra typing.
```javascript
package com.example.helloworldservice.controller;

import com.example.helloworldservice.model.Item;
import com.example.helloworldservice.model.Language;
import com.example.helloworldservice.service.ItemsService;
import com.example.helloworldservice.service.LanguagesService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import java.util.List;
import java.util.UUID;

@RequiredArgsConstructor
public class HelloworldApiDelegateImpl implements HelloworldApiDelegate {
    private final ItemsService itemsService;

    private final LanguagesService languagesService;

    // Languages
    @Override
    public ResponseEntity<Language> createLanguage(Language language) {
        return ResponseEntity
                .status(HttpStatus.CREATED)
                .body(languagesService.saveLanguage(language));
    }

    @Override
    public ResponseEntity<Language> getLanguage(UUID id) {
        return ResponseEntity.ok(languagesService.getLanguage(id));
    }

    @Override
    public ResponseEntity<List<Language>> getLanguages() {
        return ResponseEntity.ok(languagesService.getAllLanguages());
    }

    @Override
    public ResponseEntity<Language> updateLanguage(UUID id, Language language) {
        return ResponseEntity.ok(languagesService.updateLanguage(id, language));
    }

    @Override
    public ResponseEntity<Void> deleteLanguage(UUID id) {
        languagesService.deleteLanguage(id);
        return ResponseEntity.noContent().build();
    }

    // Items
    @Override
    public ResponseEntity<Item> createItem(Item item) {
        return ResponseEntity
                .status(HttpStatus.CREATED)
                .body(itemsService.saveGreeting(item));
    }

    @Override
    public ResponseEntity<Item> getItem(UUID id) {
        return ResponseEntity.ok(itemsService.getGreeting(id));
    }

    @Override
    public ResponseEntity<List<Item>> getItems(UUID languageId) {
        return ResponseEntity.ok(itemsService.getAllGreetingsByLanguage(languageId));
    }

    @Override
    public ResponseEntity<Item> updateItem(UUID id, Item item) {
        return ResponseEntity.ok(itemsService.updateGreeting(id, item));
    }

    @Override
    public ResponseEntity<Void> deleteItem(UUID id) {
        itemsService.deleteGreeting(id);
        return ResponseEntity.noContent().build();
    }
}
```

## Configuring the Services
Before we can configure the controller we need to declare beans for the language and item services to inject. Create a `ServiceConfig` class in the `config` folder and update the contents as shown below.
```javascript
package com.example.helloworldservice.config;

import com.example.helloworldservice.service.ItemsService;
import com.example.helloworldservice.service.LanguagesService;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class ServiceConfig {
    @Bean
    public ItemsService itemsService(LanguagesService languageService) {
        return new ItemsService(languageService);
    }

    @Bean
    public LanguagesService languagesService() {
        return new LanguagesService();
    }
}
```

## Configuring the Controller
The final change we need is to update the "ControllerConfig" class to inject the services into our delegate implementation.
```javascript
package com.example.helloworldservice.config;

import com.example.helloworldservice.controller.HelloworldApiDelegate;
import com.example.helloworldservice.controller.HelloworldApiDelegateImpl;
import com.example.helloworldservice.service.ItemsService;
import com.example.helloworldservice.service.LanguagesService;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class ControllerConfig {
    @Bean
    public HelloworldApiDelegate helloworldApiDelegate(ItemsService itemsService, LanguagesService languagesService) {
        return new HelloworldApiDelegateImpl(itemsService, languagesService);
    }
}
```


## Building and Deploying the Service
We are ready to build and deploy the service again. Note that if you have already deployed HelloWorldService into MSX you will need to delete it using the Component Manager.
![](images/service-layer-2.png?raw=true)

<br>

We build and package the component in the same way as the previous guide with a simple terminal command [(help me)](../04-java-hello-world-service-example/05-building-the-component.md#putting-it-all-together). Deploying components takes a while, so it is worth running the service locally to check it works before you try it on MSX [(help me)](../04-java-hello-world-service-example/04-adding-the-service-delegate.md).


```shell
$ mvn clean install
[INFO] Scanning for projects...
[INFO] 
[INFO] -------------------< com.example:helloworldservice >--------------------
[INFO] Building hello-world-service 1.0.0
[INFO] --------------------------------[ jar ]---------------------------------
[INFO] 
.
.
.
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  50.489 s
[INFO] Finished at: 2020-11-25T14:44:53-05:00
[INFO] ------------------------------------------------------------------------
```


## The Missing Pieces
Despite doing a bunch of work in this guide all we have done is tidy up the project. We still need to complete the following tasks.
* persist domain specific data
* add role based access control
* how Swagger documentation


| [PREVIOUS](05-building-the-component.md) | [NEXT](07-persisting-domain-specific-data.md) | [HOME](../index.md#java-hello-world-service-example) |
|---|---|---|