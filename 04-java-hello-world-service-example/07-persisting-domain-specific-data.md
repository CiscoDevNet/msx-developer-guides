# Persisting Domain Specific Data

* [Introduction](#introduction)
* [Goals](#goals)
* [Prerequisites](#prerequisites)
* [Configuring the Project](#configuring-the-project)
  * [pom.xml](#pomxml)
  * [application.yml](#applicationyml)
  * [bootstrap.yml](#bootstrapyml)
  * [bootstrap-legacy.yml](#bootstrap-legacyyml)
  * [manifest.yml](#manifestyml)
* [Adding the Database Model](#adding-the-database-model)
  * [GreetingRow.java](#greetingrowjava)
  * [LanguageRow.java](#languagerowjava)
  * [GreetingsRepository.java](#greetingsrepositoryjava)
  * [LanguagesRepository.java](#languagesrepositoryjava)
  * [ServiceConfig.java](#serviceconfigjava)
* [Writing Data Converters](#writing-data-converters)
  * [GreetingItemConverter.java](#greetingitemconverterjava)
  * [LanguageItemConverter.java](#languageitemconverterjava)
* [Update the Resource Sources](#update-the-resource-services)
  * [ItemsService.java](#itemsservicejava)
  * [LanguagesService.java](#languagesservicejava)
* [Running CockroachDB Locally](#running-cockroachdb-locally)
  * [Starting CockroachDB with Docker Desktop](#starting-cockroachdb-with-docker-desktop)
  * [Creating the Local Database](#creating-the-local-database)
  * [Disabling SSL for CockroachDB](#disabling-ssl-for-cockroachdb)
* [Testing Hello World Service Locally](#testing-hello-world-service-locally)
  * [Creating Languages](#creating-languages)
  * [Getting All Languages](#getting-all-languages)
  * [Getting Single Languages](#getting-single-languages)
  * [Updating Languages](#updating-languages)
  * [Deleting Languages](#deleting-languages)
  * [Creating Greeting Items](#creating-greeting-items)
* [Building and Deploying the Service](#building-and-deploying-the-service)
* [The Missing Pieces](#the-missing-pieces)


## Introduction
So far the HelloWorldService has just returned canned responses that are baked into the implementation. This was a deliberate strategy to demonstrate a minimal application with few dependencies. To make our service more useful we need to store and return real data, which we will now do. 


## Goals
* persist domain specific data
* make real HelloWorldService requests


## Prerequisites
* Java Hello World Service 3 [(help me)](https://github.com/CiscoDevNet/msx-examples/tree/main/java-hello-world-service-3)
* access to an MSX environment [(help me)](../01-msx-developer-program-basics/02-getting-access-to-an-msx-environment.md)
* [Docker Desktop](https://www.docker.com/products/docker-desktop)



## Configuring the Project
Before we can update the service to handle real data we need to update the project dependencies and configuration to the database. In this project we will be using CockrochDB.

### pom.xml
In the interests of brevity we will not include the entire `pom.xml` in this document. It is available in the source download if you do not want to make incremental changes. Add the following to the "dependencies" section of "pom.xml" then reload it. Vault is needed to get credentials from the secure store, and the CockroachDB dependencies are for the database.

```xml
.
.
.
        <!-- Vault -->
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-vault-config</artifactId>
            <exclusions>
                <exclusion>
                    <groupId>org.springframework.vault</groupId>
                    <artifactId>spring-vault-core</artifactId>
                </exclusion>
            </exclusions>
        </dependency>
        <dependency>
            <groupId>org.springframework.vault</groupId>
            <artifactId>spring-vault-core</artifactId>
            <version>2.2.2.RELEASE</version>
        </dependency>

        <!-- CockroachDB -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>
        <dependency>
            <groupId>org.postgresql</groupId>
            <artifactId>postgresql</artifactId>
            <scope>runtime</scope>
        </dependency>
        <dependency>
            <groupId>com.zaxxer</groupId>
            <artifactId>HikariCP</artifactId>
        </dependency>
.
.
.
```

<br>

### application.yml
The file `src/main/resources/application.yml` configures the CockroachDB connection pool, Spring, and JPA properties. Update the contents with the contents below.
```yaml
debug: false

db:
  cockroach:
    databaseName: ${spring.datasource.name}
    username: root
    password:
    host: localhost
    port: 26257
    sslmode: require

spring:
  datasource:
    hikari:
      auto-commit: false
      connection-timeout: 30000
      idle-timeout: 600000
      leak-detection-threshold: 30000
      max-lifetime: 1800000
      maximum-pool-size: 50
      minimum-idle: 25
      pool-name: ServiceConfigManagerHikariPool
      data-source-properties:
        sslmode: ${db.cockroach.sslmode}
        sslfactory: org.postgresql.ssl.DefaultJavaSSLFactory
    name: helloworldservice
    type: com.zaxxer.hikari.HikariDataSource
    url: jdbc:postgresql://${db.cockroach.host}:${db.cockroach.port}/${spring.datasource.name}
    username: ${db.cockroach.username}
    password: ${db.cockroach.password}

  jackson:
    date-format: com.example.helloworldservice.RFC3339DateFormat
    serialization:
      WRITE_DATES_AS_TIMESTAMPS: false

  jpa:
    database-platform: org.hibernate.dialect.PostgreSQL95Dialect
    database: POSTGRESQL
    show-sql: false
    properties:
      hibernate.connection.provider_disables_autocommit: false
      hibernate.cache.use_second_level_cache: false
      hibernate.cache.use_query_cache: false
      hibernate.generate_statistics: false
      javax.persistence.validation.mode: none # skip validation in JPA on saving since already validated in controller/service
      hibernate.hbm2ddl.auto: update
      hibernate.id.new_generator_mappings: true
      hibernate.jdbc.batch_size: 128
      # added per https://github.com/spring-projects/spring-boot/issues/12007#issuecomment-369388646
      hibernate.jdbc.lob.non_contextual_creation: true
      hibernate.order_inserts: true
      hiberante.order_updates: true
```

<br>

### bootstrap.yml
The file `src/main/resources/bootstrap.yml` configures the bootstrap context for *MSX >= 4.1.0*. The bootstrap context is created by Spring to load configuration before starting the application.

```yaml
.
.
.
spring:
  application:
    name: helloworldservice
  cloud:
    consul:
      host: localhost
      port: 8500
      config:
        enabled: true
        prefix: thirdpartycomponents
        defaultContext: defaultapplication
    vault:
      host: localhost
      port: 8200
      scheme: http
      kv:
        default-context: defaultapplication
        enabled: true
        backend: secret/thirdpartycomponents
      authentication: NONE  
.
.
.

```

<br>


### bootstrap-legacy.yml
The file `src/main/resources/bootstrap.yml` configures the bootstrap context for *MSX <= 4.0.0*. The bootstrap context is created by Spring to load configuration before starting the application.

```yaml
.
.
.
spring:
  application:
    name: helloworldservice
  cloud:
    consul:
      host: localhost
      port: 8500
      config:
        enabled: true
        prefix: thirdpartyservices
        defaultContext: defaultapplication
    vault:
      host: localhost
      port: 8200
      scheme: http
      kv:
        default-context: defaultapplication
        enabled: true
        backend: secret/thirdpartyservices
      authentication: TOKEN
      token: replace_with_token_value # replace with actual token value or provide this value via another property source
.
.
.
```

<br>



### manifest.yml
The file "manifest.yml" controls how SLM with deploy a component into MSX. Add the following to the end of the file to configure the database.

```yaml
.
.
.
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
.
.
.
```


## Adding the Database Model
We start by defining the database tables to store our data. The external data model is not always identical to the internal data model, but it is close in this case. Do the following in IntelliJ IDEA or a terminal window:
 * create folder `cockroach` 
 * create folder `cockroach/model` 
 * create folder `cockroach/repository`
 * create classes `cockroach/model/GreetingRow` and `cockroach/model/LanguageRow` 
 * create interfaces `cockroach/repository/GreetingsRepository` and `cockroach/repository/LanguagesRepository`

We will add the contents to the classes and interfaces next, but the structure should look like this:
![](images/persisting-data-1.png?raw=true)

<br>

### GreetingRow.java
This class defines how a greeting row will be stored in CockroachDB.

```javascript
package com.example.helloworldservice.cockroach.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import javax.persistence.*;
import java.util.UUID;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder(toBuilder = true)
@Entity
@Table
public class GreetingRow {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private UUID greetingId;

    @ManyToOne(targetEntity = com.example.helloworldservice.cockroach.model.LanguageRow.class)
    @JoinColumn(name = "language_id")
    private com.example.helloworldservice.cockroach.model.LanguageRow language;

    @Column(length = 128)
    private String value;
}
```

<br>

### LanguageRow.java
This class defines how a language row will be stored in CockroachDB.

```javascript
package com.example.helloworldservice.cockroach.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import javax.persistence.*;
import java.util.UUID;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder(toBuilder = true)
@Entity
@Table(indexes = {@Index(name = "language_name_idx", columnList = "name", unique = true)})
public class LanguageRow {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private UUID languageId;

    @Column(length = 128)
    private String name;

    @Column(length = 512)
    private String description;
}
```

<br>

### GreetingsRepository.java
Spring takes care of the greetings repository for us so all we need to do is declare the interface.

```javascript
package com.example.helloworldservice.cockroach.repository;

import com.example.helloworldservice.cockroach.model.GreetingRow;
import com.example.helloworldservice.cockroach.model.LanguageRow;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.UUID;

public interface GreetingsRepository extends JpaRepository<GreetingRow, UUID> {
    List<GreetingRow> findAllByLanguage(LanguageRow langauge);
}
```

<br>

### LanguagesRepository.java
The same goes for the languages repository.

```javascript
package com.example.helloworldservice.cockroach.repository;

import com.example.helloworldservice.cockroach.model.LanguageRow;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.UUID;

public interface LanguagesRepository extends JpaRepository<LanguageRow, UUID> {
}
```

<br>

### ServiceConfig.java
Now that we have created the repositories we need to pass them to the service beans.

```javascript
package com.example.helloworldservice.config;

import com.example.helloworldservice.cockroach.repository.GreetingsRepository;
import com.example.helloworldservice.cockroach.repository.LanguagesRepository;
import com.example.helloworldservice.service.ItemsService;
import com.example.helloworldservice.service.LanguagesService;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class ServiceConfig {

    @Bean
    public ItemsService itemsService(GreetingsRepository greetingsRepository, LanguagesService languageService) {
        return new ItemsService(greetingsRepository, languageService);
    }

    @Bean
    public LanguagesService languagesService(LanguagesRepository languagesRepository) {
        return new LanguagesService(languagesRepository);
    }
}
```

<br>

## Writing Data Converters
We must write helper classes to translate data from the domain model to data transfer objects (DTO) that will go out on the wire, and vice versa. Create classes `GreetingItemConverter.java` and `LanguageItemConverter.java` as shown.

![](images/persisting-data-2.png?raw=true)

<br>

### GreetingItemConverter.java
```javascript
package com.example.helloworldservice.service;

import com.example.helloworldservice.cockroach.model.GreetingRow;
import com.example.helloworldservice.model.Item;
import com.example.helloworldservice.model.Language;
import org.springframework.util.Assert;

public class GreetingItemConverter {
    // Convert from domain model into DTO.
    public static Item convert(GreetingRow greeting) {
        Item item = new Item()
                .id(greeting.getGreetingId())
                .languageId(greeting.getLanguage().getLanguageId())
                .languageName(greeting.getLanguage().getName())
                .value(greeting.getValue());
        return item;
    }

    // Convert from DTO into domain model.
    public static GreetingRow convert(Item item, Language language) {
        Assert.notNull(item, "Item is a required field for mapping.");
        Assert.notNull(language, "Language is a required field for mapping.");
        Assert.isTrue(item.getLanguageId().equals(language.getId()), "Mismatch between expected and provided language for given item.");

        GreetingRow.GreetingRowBuilder greetingBuilder = GreetingRow.builder();

        if (item.getId() != null) {
            greetingBuilder.greetingId(item.getId());
        }

        greetingBuilder
                .language(LanguageItemConverter.convert(language))
                .value(item.getValue());

        return greetingBuilder.build();
    }
}
```

<br>

### LanguageItemConverter.java
```javascript
package com.example.helloworldservice.service;

import com.example.helloworldservice.cockroach.model.LanguageRow;
import com.example.helloworldservice.model.Language;

public class LanguageItemConverter {
    // Convert from domain model into DTO.
    public static Language convert(LanguageRow languageRow) {
        Language language = new Language()
                .id(languageRow.getLanguageId())
                .name(languageRow.getName())
                .description(languageRow.getDescription());
        return language;
    }

    // Convert from DTO into domain model.
    public static LanguageRow convert(Language language) {
        LanguageRow languageRow = LanguageRow.builder()
                .languageId(language.getId())
                .name(language.getName())
                .description(language.getDescription())
                .build();
        return languageRow;
    }
}
```


## Update the Resource Services
The final step is to update the resource services to persist data to and retrieve data from CockroachDB.

### ItemsService.java
```javascript
package com.example.helloworldservice.service;

import com.example.helloworldservice.cockroach.model.GreetingRow;
import com.example.helloworldservice.cockroach.model.LanguageRow;
import com.example.helloworldservice.cockroach.repository.GreetingsRepository;
import com.example.helloworldservice.model.Item;
import com.example.helloworldservice.model.Language;

import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
public class ItemsService {
    private final GreetingsRepository greetingsRepository;

    private final LanguagesService languagesService;

    public Item saveGreeting(Item item) {
        // Convert the DTO into the domain model.
        Language language = languagesService.getLanguage(item.getLanguageId());
        GreetingRow greetingRow = GreetingItemConverter.convert(item, language);

        // Save domain model object.
        GreetingRow savedGreetingRow = greetingsRepository.save(greetingRow);

        // Convert domain model to DTO in preparation for response.
        Item savedItem = GreetingItemConverter.convert(savedGreetingRow);

        return savedItem;
    }

    public Item getGreeting(UUID greetingId) {
        // Obtain greeting record from database.
        GreetingRow greeting = greetingsRepository.getOne(greetingId);

        // Convert domain model to DTO for response.
        Item item = GreetingItemConverter.convert(greeting);

        return item;
    }

    public List<Item> getAllGreetings() {
        // Obtain records from database.
        List<GreetingRow> greetingRows = greetingsRepository.findAll();

        // Convert records into DTOs.
        List<Item> languages = greetingRows.stream()
                .map(GreetingItemConverter::convert)
                .collect(Collectors.toList());

        return languages;
    }

    public List<Item> getAllGreetingsByLanguage(UUID languageId) {
        // Obtain language.
        LanguageRow language = null;
        if (languageId != null) {
            language = languagesService.getRawLanguage(languageId);
        }

        // Obtain records from database.
        List<GreetingRow> greetingRows = greetingsRepository.findAllByLanguage(language);

        // Convert records into DTOs.
        List<Item> languages = greetingRows.stream()
                .map(GreetingItemConverter::convert)
                .collect(Collectors.toList());

        return languages;
    }

    public Item updateGreeting(UUID greetingId, Item item) {
        // Will throw exception if greeting entry does not exist.
        GreetingRow existingGreetingRow = greetingsRepository.getOne(greetingId);

        // Convert the DTO into the domain model.
        Language language = languagesService.getLanguage(item.getLanguageId());
        GreetingRow greetingRow = GreetingItemConverter.convert(item, language);

        // Set greetingId to overwrite existing record.
        greetingRow.setGreetingId(greetingId);

        // Save domain model object.
        GreetingRow savedGreetingRow = greetingsRepository.save(greetingRow);

        // Convert domain model to DTO in preparation for response
        Item savedItem = GreetingItemConverter.convert(savedGreetingRow);

        return savedItem;
    }

    public void deleteGreeting(UUID greetingId) {
        greetingsRepository.deleteById(greetingId);
    }
}
```

<br>

### LanguagesService.java
```javascript
package com.example.helloworldservice.service;

import com.example.helloworldservice.cockroach.model.LanguageRow;
import com.example.helloworldservice.cockroach.repository.LanguagesRepository;
import com.example.helloworldservice.model.Language;

import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

import lombok.RequiredArgsConstructor;


@RequiredArgsConstructor
public class LanguagesService {
    private final LanguagesRepository languagesRepository;

    public Language saveLanguage(Language language) {
        // Convert from DTO to model to prepare for saving.
        LanguageRow languageRow = LanguageItemConverter.convert(language);

        // Cave to database.
        LanguageRow savedLanguageRow = languagesRepository.save(languageRow);

        // Convert into DTO for response.
        Language savedLanguage = LanguageItemConverter.convert(savedLanguageRow);

        return savedLanguage;
    }

    protected LanguageRow getRawLanguage(UUID languageId) {
        // Get record from database.
        LanguageRow languageRow = languagesRepository.getOne(languageId);
        return languageRow;
    }

    public Language getLanguage(UUID languageId) {
        // Get record from database.
        LanguageRow languageRow = getRawLanguage(languageId);

        // Convert into DTO for response.
        Language language = LanguageItemConverter.convert(languageRow);

        return language;
    }

    public List<Language> getAllLanguages() {
        // Get records from database.
        List<LanguageRow> languageRows = languagesRepository.findAll();

        // Convert into DTO for response.
        List<Language> languages = languageRows.stream()
                .map(LanguageItemConverter::convert)
                .collect(Collectors.toList());

        return languages;
    }

    public Language updateLanguage(UUID languageId, Language language) {
        // Will throw exception if language entry does not exist.
        LanguageRow existingLanguageRow = languagesRepository.getOne(languageId);

        // Convert the DTO into the domain model.
        LanguageRow languageRow = LanguageItemConverter.convert(language);

        // Set greetingId to overwrite existing record.
        languageRow.setLanguageId(languageId);

        // Save domain model object.
        LanguageRow savedLanguageRow = languagesRepository.save(languageRow);

        // Convert domain model to DTO in preparation for response.
        Language savedLanguage = LanguageItemConverter.convert(savedLanguageRow);

        return savedLanguage;
    }

    public void deleteLanguage(UUID languageId) {
        languagesRepository.deleteById(languageId);
    }
}
```


## Running CockroachDB Locally

### Starting CockroachDB with Docker Desktop
We need to install CockroachDB with Docker Desktop and create the database before we can test the service locally.
```shell
$ docker pull cockroachdb/cockroach
Using default tag: latest
latest: Pulling from cockroachdb/cockroach
4753a4528f5f: Pull complete 
c0194df27eff: Pull complete 
bf8415c0986d: Pull complete 
560934714b5b: Pull complete 
e1b05ad8ce98: Pull complete 
5b51353b977c: Pull complete 
a7173bfe08af: Pull complete 
Digest: sha256:5b73a8e3f8fb4ea1a3ff0a58f696272a1424e35951288bcaa44b90fb3f4a7a6e
Status: Downloaded newer image for cockroachdb/cockroach:latest
docker.io/cockroachdb/cockroach:latest

$ docker images -f 'reference=cockroachdb/cockroach'
REPOSITORY              TAG                 IMAGE ID            CREATED             SIZE
cockroachdb/cockroach   latest              01c8b3652986        33 hours ago        327MB

$ docker run -d --name=roach1 \
--hostname=roach1 \
-p 26257:26257 -p 8080:8080 \
 -v "${PWD}/cockroach-data/roach1:/cockroach/cockroach-data"  \
cockroachdb/cockroach start \
--insecure \
--join=roach1,roach2,roach3

$ docker exec -it roach1 ./cockroach init --insecure
Cluster successfully initialized
```
<br>

You can confirm that CockroachDB is running by looking at the Docker Desktop Dashboard. If you intend on testing locally make sure that Consul is running too.
![](images/persisting-data-3.png?raw=true)

<br>

### Creating the Local Database
The database has to exist before we ran start the service locally so connect to CockroachDB and create an empty "helloworldservice" database. The Hello World Service migration step will create the tables, so you do not need to worry about that.
```shell
$ docker exec -it roach1 ./cockroach sql --insecure
#
# Welcome to the CockroachDB SQL shell.
# All statements must be terminated by a semicolon.
# To exit, type: \q.
#
# Server version: CockroachDB CCL v20.2.2 (x86_64-unknown-linux-gnu, built 2020/11/25 14:45:44, go1.13.14) (same version as client)
# Cluster ID: 5e1ab080-734c-453f-9db8-b76fae0bb19d
#
# Enter \? for a brief introduction.
#
root@:26257/defaultdb> CREATE DATABASE helloworldservice;
CREATE DATABASE
Time: 37ms total (execution 36ms / network 1ms)
```

<br>

### Disabling SSL For CockroachDB
As we will be running over HTTP locally not HTTPS we have to disable SSL for CockroachDB. To do this edit the file `application.yml` that we have worked with before and change the `sslmode` from `require` to `disable`. Never disable any security in a production build.
```yaml
# src/main/resources/application.yml
.
.
.
db:
  cockroach:
    databaseName: ${spring.datasource.name}
    username: root
    password:
    host: localhost
    port: 26257
    sslmode: disable
.
.
.
```


## Testing Hello World Service Locally
You can now start Hello World Service by clicking the green play button in the toolbar or by right clicking the "OpenAPI2SSpringBoot" class and selecting "Run OpAPI2SpringBoot". Try the commands below in a terminal window once it has started. Remember we defined the contact for this API as an OpenAPI Specification so refer to that for details of requests [(help me)](../03-msx-component-manager/07-working-with-openapi-specifications.md).

### Creating Languages
Create an entry for the French language with POST request. Note that the "id" returned will be different in your request.
```shell
$ curl --request POST "http://localhost:9515/helloworldservice/helloworld/api/v1/languages" \
--header "Content-Type: application/json" \
--data '{"name": "English", "description": "A West Germanic language that uses the Roman alphabet."}'
{
"id":"dbedcc96-6669-4286-bc72-84fc2c7623b8",
"name":"English",
"description":"A West Germanic language that uses the Roman alphabet."
}

$ curl --request POST "http://localhost:9515/helloworldservice/helloworld/api/v1/languages" \
--header "Content-Type: application/json" \
--data '{"name": "French", "description": "A West Germanic language that uses the Roman alphabet."}'
{
"id":"0e118c70-d000-4acd-8c58-e649ce5d6fe4",
"name":"French",
"description":"A Romance language descended from the Vulgar Latin of the Roman Empire."
}
```

<br>

### Getting All Languages
Get a list of all languages using a GET request.
```shell
$ curl --request GET "http://localhost:9515/helloworldservice/helloworld/api/v1/languages" \
--header "Content-Type: application/json" 
[
{
"id":"0e118c70-d000-4acd-8c58-e649ce5d6fe4",
"name":"French",
"description":"A Romance language descended from the Vulgar Latin of the Roman Empire."
},
{
"id":"dbedcc96-6669-4286-bc72-84fc2c7623b8",
"name":"English",
"description":"A West Germanic language that uses the Roman alphabet."
}
]
```

<br>

### Getting Single Languages
Retrieve a language by copying the "id" returned in the response into a GET request.
```shell
$ curl --request GET "http://localhost:9515/helloworldservice/helloworld/api/v1/languages/0e118c70-d000-4acd-8c58-e649ce5d6fe4" \
--header "Content-Type: application/json" 
{
"id":"0e118c70-d000-4acd-8c58-e649ce5d6fe4",
"name":"French",
"description":"A Romance language descended from the Vulgar Latin of the Roman Empire."
}
```

<br>

### Updating Languages
We can change the description of the language with a PUT request.
```shell
$ curl --request PUT "http://localhost:9515/helloworldservice/helloworld/api/v1/languages/0e118c70-d000-4acd-8c58-e649ce5d6fe4" \
--header "Content-Type: application/json" \
--data '{"name": "French", "description": "French evolved from the Latin spoken in Gaul by Asterix."}'
{
"id":"0e118c70-d000-4acd-8c58-e649ce5d6fe4",
"name":"French",
"description":"French evolved from the Latin spoken in Gaul by Asterix."
}
```

<br>

### Deleting Languages
Finally delete a language with a DELETE request.
```shell
$ curl --request DELETE "http://localhost:9515/helloworldservice/helloworld/api/v1/languages/0e118c70-d000-4acd-8c58-e649ce5d6fe4" 
```

<br>

### Creating Greeting Items
We deleted the French language item but we can still create a greeting item for English.
```shell
$ curl --request POST "http://localhost:9515/helloworldservice/helloworld/api/v1/items" \
--header "Content-Type: application/json" \
--data '{ "languageId": "dbedcc96-6669-4286-bc72-84fc2c7623b8", "value": "Hello, World!"}'
{
"id":"023cd7f6-37ef-4e85-90b8-9441ca2b1163",
"languageId":"dbedcc96-6669-4286-bc72-84fc2c7623b8",
"languageName":"English",
"value":"Hello, World!"
}
```

Now that you know how to make language and greeting requests try adding some languages and greetings of your own.


## Building and Deploying the Service
Once again we are ready to build and deploy the service into MSX. We have covered this in previous guides so will not go over it here [(help me)](../04-java-hello-world-service-example/06-implementing-the-service-layer.md#building-and-deploying-the-service). Note you will need to update `application.yml` to enable SSL before you build.
```yaml
# src/main/resources/application.yml
.
.
.
db:
  cockroach:
    databaseName: ${spring.datasource.name}
    username: root
    password:
    host: localhost
    port: 26257
    sslmode: require
.
.
.
```

Try making the same requests to your MSX environment once the Hello World Service has deployed. You will need to set `MY_MSX_ENVIRONMENT` to point to your MSX and pass the `--insecure` switch to curl.
```shell
$ export MY_MSX_ENVIRONMENT=dev-plt-aio1.lab.ciscomsx.com
$ curl --request GET "https://$MY_MSX_ENVIRONMENT/helloworldservice/helloworld/api/v1/languages" \
--header "Content-Type: application/json" \
--insecure
```

<br>


## The Missing Pieces
We are one step close but still need to do the following:
* register security clients
* add Swagger documentation
* add role based access control


## References
[CockroachDB](https://www.cockroachlabs.com/docs/stable/start-a-local-cluster-in-docker-mac.html)


| [PREVIOUS](06-implementing-the-service-layer.md) | [NEXT](08-creating-the-security-clients.md) | [HOME](../index.md#java-hello-world-service-example) |
