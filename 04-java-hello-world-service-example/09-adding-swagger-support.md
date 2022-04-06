# Adding Swagger Support

* [Introduction](#introduction)
* [Goals](#goals)
* [Prerequisites](#prerequisites)
* [Configuring the Project](#configuring-the-project)
    * [pom.xml](#pomxml)
    * [logback.xml](#logbackxml)
    * [application.yml](#applicationyml)
    * [manifest.yml](#manifestyml)
    * [SwaggerConfig.java](#swaggerconfigjava)
* [Building and Deploying the Service](#building-and-deploying-the-service)
* [Finding the Swagger Documentation](#finding-the-swagger-documentation)
* [The Missing Pieces](#the-missing-pieces)


## Introduction
Swagger is an important tool that allows users to explore an API [(help me)](../01-msx-developer-program-basics/04-using-the-swagger-documentation.md). In this guide we will update Hello World Service so that we can browse its Swagger documentation in the Cisco MSX Portal. 


## Goals
* browse Hello World Service Swagger documentation 


## Prerequisites
* Java Hello World Service 4 [(help me)](https://github.com/CiscoDevNet/msx-examples/tree/main/java-hello-world-service-4)
* access to an MSX environment [(help me)](../01-msx-developer-program-basics/02-getting-access-to-an-msx-environment.md)
* [Docker Desktop](https://www.docker.com/products/docker-desktop)



## Configuring the Project
Lucky for us we generated our server stubs from an OpenAPI Specification [(help me)](../04-java-hello-world-service-example/03-creating-a-hello-world-service-in-java.md), so our API controller and model already have the required annotations.

### pom.xml
Update the "pom.xml" to include the dependencies below, noting that it requires that you also add a custom repository. The full text of the file is available in the source code for the project [(help me)](hhttps://github.com/CiscoDevNet/msx-examples/tree/main/java-hello-world-service-5/pom.xml).
```xml
.
.
.
        <!-- Swagger -->
        <dependency>
            <groupId>com.github.ciscodevnet</groupId>
            <artifactId>java-msx-swagger</artifactId>
            <version>v1.0.0</version>
        </dependency>

        <dependency>
            <groupId>org.openapitools</groupId>
            <artifactId>jackson-databind-nullable</artifactId>
            <version>0.1.0</version>
        </dependency>
    </dependencies>

    <repositories>
        <repository>
            <id>jitpack.io</id>
            <url>https://jitpack.io</url>
        </repository>
    </repositories>
.
.
.
```

<br>

### logback.xml
Let's now create a `logback.xml` file to configure the logging for the example.
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<configuration debug="false" scan="true">

    <!-- Spring Boot's defaults.xml sets up color, ROOT logger, properties -->
    <include resource="org/springframework/boot/logging/logback/defaults.xml"/>

    <!-- Skip printing incoming status messages. -->
    <statusListener class="ch.qos.logback.core.status.NopStatusListener" />

    <!-- Enable JMX implementation of LoggerContextListener to listen to events related to lifecycle or logger context. -->
    <jmxConfigurator/>

    <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
            <pattern>%relative [%thread] %-5level %logger{35} - %msg%n</pattern>
        </encoder>
    </appender>

    <appender name="FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <encoder>
            <pattern>%relative [%thread] %-5level %logger{35} - %msg%n</pattern>
        </encoder>
        <file>${LOG_FILE}</file>
        <rollingPolicy class="ch.qos.logback.core.rolling.SizeAndTimeBasedRollingPolicy">
            <cleanHistoryOnStart>${LOG_FILE_CLEAN_HISTORY_ON_START:-false}</cleanHistoryOnStart>
            <fileNamePattern>${ROLLING_FILE_NAME_PATTERN:-${LOG_FILE}.%d{yyyy-MM-dd}.%i.gz}</fileNamePattern>
            <maxFileSize>${LOG_FILE_MAX_SIZE:-10MB}</maxFileSize>
            <maxHistory>${LOG_FILE_MAX_HISTORY:-7}</maxHistory>
            <totalSizeCap>${LOG_FILE_TOTAL_SIZE_CAP:-0}</totalSizeCap>
        </rollingPolicy>
    </appender>

    <!-- default logging levels, unless we overwrite then use INFO-->
    <root>
        <level value="INFO"/>
        <!-- CONSOLE appender always enabled -->
        <appender-ref ref="CONSOLE"/>
        <!-- FILE appender enabled IF these profiles exist -->
        <springProfile name="fileLogging, jsonFileLogging">
            <appender-ref ref="FILE"/>
        </springProfile>
    </root>

    <logger name="org.springframework" level="DEBUG"/>
<!--    <logger name="org.springframework.security.oauth2" level="INFO"/>-->
<!--    <logger name="org.springframework.integration" level="OFF"/>-->
<!--    <logger name="org.springframework.oxm" level="OFF"/>-->
<!--    <logger name="org.springframework.http" level="ERROR"/>-->

    <logger name="org.apache.catalina.startup.DigesterFactory" level="ERROR"/>
    <logger name="org.apache.catalina.util.LifecycleBase" level="ERROR"/>
    <logger name="org.apache.coyote.http11.Http11NioProtocol" level="WARN"/>
    <logger name="org.apache.sshd.common.util.SecurityUtils" level="WARN"/>
    <logger name="org.apache.tomcat.util.net.NioSelectorPool" level="WARN"/>
    <logger name="org.hibernate.validator.internal.util.Version" level="WARN"/>

    <logger name="com.example.helloworldservice" level="DEBUG" />

    <logger name="org.springframework.vault.core" level="TRACE" />
    <logger name="org.springframework.vault" level="TRACE" />

</configuration>
```
<br>

### application.yml
We have already configured  Spring, CockroachDB connection pool, and JPA properties in `application.yml`. Now we tell the application about the public security client, and the pattern to integrate the Swagger documentation.
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
      javax.persistence.validation.mode: none # skip validation in JPA on saving - double validation since already validated in controller/service
      hibernate.hbm2ddl.auto: update
      hibernate.id.new_generator_mappings: true
      hibernate.jdbc.batch_size: 128
      # added per https://github.com/spring-projects/spring-boot/issues/12007#issuecomment-369388646
      hibernate.jdbc.lob.non_contextual_creation: true
      hibernate.order_inserts: true
      hiberante.order_updates: true

public:
  security:
    # The public client identifier for the service.
    clientId: hello-world-service-public-client

swagger:
  security:
    sso:
      clientId: ${public.security.clientId}

security:
  resources:
    rules:
      -
        # "/v2/api-docs" required for Swagger documentation.
        patterns: "/v2/api-docs"
        expr: "hasRole('ROLE_CLIENT') and hasAuthority('SCOPE_read') and hasAuthority('SCOPE_write')"
```

<br>

### manifest.yml
Update `manifest.yml` to tell SLM the public security client identifier, but do not change the name of the Consul key as that is where the Swagger library will look for it.
```yaml
.
.
.
# [Optional] General configuration section for your application for values to be stored in Consul and be available to your application
# during startup and runtime.  The service configurations are in a sandbox with restricted access. Multiple name:value
# pairs can be specified.
ConsulKeys:
  - Name: "public.security.clientId"
    Value: "hello-world-service-public-client"
.
.
.
```

<br>

### SwaggerConfig.java
Create the class `SwaggerConfig` in the package `com.example.helloworldservice.config` and add the contents. You can set extra information in `configureApiInfo` such as terms and conditions, licence details, and support contacts.
```javascript
package com.example.helloworldservice.config;

import com.cisco.msx.swagger.SwaggerConfigurer;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import springfox.documentation.builders.ApiInfoBuilder;
import springfox.documentation.spring.web.plugins.Docket;

import java.util.function.Predicate;

import static springfox.documentation.builders.PathSelectors.regex;

@Configuration
public class SwaggerConfig implements SwaggerConfigurer {

    @Value("${info.app.name}")
    private String appName;

    @Value("${info.app.description}")
    private String appDescription;

    @Value("${info.app.version}")
    private String appVersion;

    @Value("${info.app.attributes.parent:platform}")
    private String componentGroup;

    @Value("${server.servlet.context-path}")
    private String contextPath;

    @Override
    public Docket configure(Docket docket) {
        return docket.groupName(componentGroup);
    }

    @Override
    public ApiInfoBuilder configureApiInfo(ApiInfoBuilder apiInfo) {

        return apiInfo
                .title("MSX API Documentation for " + appName)
                .description(appDescription)
                .version(appVersion);
    }

    public Predicate<String> configureApiPathSelector(Predicate<String> apiPathSelector) {
        return apiPathSelector.or(regex(contextPath + "/helloworld/api/v1.*"));
    }
}

```

## Building and Deploying the Service
Run the command below from a terminal window in the same folder as `pom.xml`, then deploy the resulting tarball into MSX using the Cisco MSX Portal.
```
$ mvn clean install
.
.
.
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  01:09 min
[INFO] Finished at: 2021-03-13T11:27:03-05:00
[INFO] ------------------------------------------------------------------------
```


## Finding the Swagger Documentation
There are two ways to find the Swagger documentation for Hello World Service in the Cisco MSX Portal. The first is to browse to this URL once you have changed the hostname.
```
https://dev-plt-aio1.lab.ciscomsx.com/helloworldservice/swagger
```

The second is to use the Cisco MSX Portal to navigate to the Swagger documentation for all services [(help me)](../01-msx-developer-program-basics/04-using-the-swagger-documentation.md) Whichever path you take once you get there it will look like this.


![](images/finding-swagger-4.png?raw=true)

<br>

This Swagger page is interactive and can be used to try out the API. You can fetch and delete language and item resources created in earlier guides or create some new ones and fetch and delete them. This ability to try the API is a powerful tool than can help you refine your service before you ship it. Take this opportunity to play around with Swagger if you have not used it before.


## The Missing Pieces
Now we have Swagger documentation the last piece of the puzzle is:
* add role based access control


| [PREVIOUS](08-creating-the-security-clients.md) | [NEXT](10-implementing-role-based-access-control.md) | [HOME](../index.md#java-hello-world-service-example) |
