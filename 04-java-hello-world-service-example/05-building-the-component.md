# Building the Component

* [Introduction](#introduction)
* [Goals](#goals)
* [Prerequisites](#prerequisites)
* [Writing the Component Manager Manifest](#writing-the-component-manager-manifest)
* [Writing the Docker File](#writing-the-docker-file)
* [Writing the Docker Launch Script](#writing-the-docker-launch-script)
* [Writing the Makefile](#writing-the-makefile)
* [Updating the Project Configuration](#updating-the-project-configuration)
* [Putting It All Together](#putting-it-all-together)
* [Deploying the Component](#deploying-the-component)
* [Running It Remotely](#running-it-remotely)
* [The Missing Pieces](#the-missing-pieces)


## Introduction
Before we install the Hello World Service in MSX we need to containerize it and write a Component Manager manifest. In this guide we show how to write the manifest and automate creation of the component.


## Goals
* containerize Hello World Service
* write a Component Manager manifest
* create a Component Manager component


## Prerequisites
* Java Hello World Service 1 [(help me)](https://github.com/CiscoDevNet/msx-examples/tree/main/java-hello-world-service-1)
* access to an MSX environment [(help me)](../01-msx-developer-program-basics/02-getting-access-to-an-msx-environment.md)
* basic understanding of SLM [(help me)](../03-msx-component-manager/01-what-is-component-manager-in-a-nutshell.md)
* [Docker Desktop](https://www.docker.com/products/docker-desktop)


## Writing the Component Manager Manifest
The ComponentManager manifest has to be written before we can package it up with the container. 

To get started, create a new resource folder called `src/main/java/resources-filtered` and create a `manifest.yml` in it. Then use the menu item **File->Project Structure...->Modules** to make it a **resource folder**.

![](images/building-component-1.png?raw=true)

Next copy the contents below into `rc/main/java/resources-filtered/manifest.yml`. 
```yaml
---
#
# Copyright (c) 2021 Cisco Systems, Inc and its affiliates
# All Rights reserved
#

# Metadata for the service to be deployed consisting of name, description, version, and type of service.
Name: "@project.artifactId@"
Description: "@project.description@"
Version: "@project.version@"
Type: Internal

# Wrapper for containers making up the service to be deployed.  Each service must have at least one container section
# which describes the Docker image to be used for the service.
Containers:
  - Name: "@project.artifactId@"
    Version: "@project.version@"
    Artifact: "@project.build.finalName@-@project.version@.tar.gz"
    Port: @server.port@ #Service listening Port
    ContextPath: @server.contextpath@ # Context path to configure the application routing with

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
      - "managedMicroservice"
      - "buildNumber=@project.version@"
      - "name=@project.artifactId@"
      - "version=@project.version@"
      - "swaggerPath=/"
      - "buildDateTime=@timestamp@"
      - "application=@project.artifactId@"
      - "componentAttributes=serviceName:@project.artifactId@~context:@server.contextpath@~name:@project.artifactId@~description:@project.description@"


    # Health check configurations.  Each container needs 1 health endpoint configured.  If a service has a specific
    # health endpoint implemented, please use the Http configuration along with the common health check section.  Otherwise,
    # for services that don't have a dedicated health endpoint implemented please configure the Tcp block and the host
    # will be pinged by the health checks instead.
    Check:
      Http:
        Scheme: "http"
        Host: "127.0.0.1" #FQDN or IP of service host if internal can be 127.0.0.1
        Path: "@server.contextpath@"
      IntervalSec: 30 # how often (in seconds) should the system check if your service is up
      InitialDelaySec: 5 # initialization delay - how many seconds should the system wait after application is started before firing off the first health check request
      TimeoutSec: 30
      Port: @server.port@ # port to use for health checks if different from application's default listening port

    # In this section you need to specify the hardware requirements for your application.
    Limits:
      Memory: "384Mi"  # amount of memory/RAM that the application needs.  In this case the example asks for 512MB of RAM.  You should specify what your application needs based on your profiling findings.
      CPU: "1"  # number of virtual CPUs that the application needs

    # Command to use to start the application.
    Command:
      - "/service/dockerlaunch.sh"
      # Set the profile for MSX <= 4.0.0
      # - "-Dspring.profiles.active=legacy"
```

> **GOTCHA**
> 
> To target MSX <= 4.0.0 you must set the active spring profile to `legacy` by uncommenting the last line in the example above. Note you can use the same image in two tarballs with different manifests to support MSX <= 4.0 and MSX >= 4.1 from a single build.


## Writing the Docker File
Create `Dockerfile` in the root folder of the project, to instruct Docker how to create the container.

![](images/building-component-2.png?raw=true)

Refer to the Docker reference documentation if you need to make changes. The only thing you might have to change is the port the service will be available on.

Copy and paste the following to the `Dockerfile` that you just created.

```dockerfile
ARG BASE_VERSION=3.10.0-12
FROM dockerhub.cisco.com/vms-platform-dev-docker/vms-java:$BASE_VERSION

EXPOSE 9515

# Rebuild cacerts as JKS (as required by not-going-to-be-commons-ssl for SAML) until a fix for
# Debian bug #898678 is published or we mount the truststore to a different location
RUN sed -i -e 's/keystore.type=pkcs12/keystore.type=jks/' /etc/java-11-openjdk/security/java.security &&\
    rm /etc/ssl/certs/java/cacerts &&\
    update-ca-certificates -f

ENV SERVICE_JAR helloworldservice.jar

COPY bin/dockerlaunch.sh /service/dockerlaunch.sh
RUN chmod 755 /service/dockerlaunch.sh
ENTRYPOINT ["/service/dockerlaunch.sh"]

COPY target/$SERVICE_JAR /service/
```


## Writing the Docker Launch Script
We need to write a script that tells Docker how to start our service, so create `bin/dockerlaunch.sh`.

![](images/building-component-3.png?raw=true)

You do not need to make any changes to the contents below for this example service, but you can use it to tune the Java environment if you need to.

Copy and paste the following code onto the `bin/dockerlaunch.sh` that you just created.

```shell
#!/bin/bash
# Supported ENV variables:
# * SERVICE_JAR: Name of the jar file to execute (required)
# * JAVA_OPTS: A set of options that will be passed to the java command (optional)
#
# Arguments to this script will be passed as arguments to the Java application.

if [ "$SERVICE_JAR" = "" ]; then
    echo "Environment variable SERVICE_JAR not set or empty"
    exit 1
fi

JAVA_OPTS=${JAVA_OPTS:-" \\
  -Xss512K \\
  -Xms128M \\
  -Xmx256M \\
  -XX:MaxMetaspaceSize=128M \\
  -XX:MaxRAMPercentage=75 -XX:MinRAMPercentage=50 \\
  -XX:MaxHeapFreeRatio=15 -XX:MinHeapFreeRatio=10 \\
  -XX:ReservedCodeCacheSize=64M \\
  -XX:+UseStringDeduplication \\
  -XX:+HeapDumpOnOutOfMemoryError \\
  -XX:HeapDumpPath=/data/conf/dump.hprof"}

CMD="exec java -Djavax.net.ssl.trustStore=/keystore/msxtruststore.jks $@ $JAVA_OPTS -jar /service/$SERVICE_JAR"

echo "$CMD"
eval "$CMD"
```


## Writing the Makefile
The last thing we need to do is to create a `Makefile` in the project root folder. 

![](images/building-component-4.png?raw=true)

`Makefile` is used by Maven to copy properties to the ComponentManager manifest, run Docker to create the container, then package them into a component tarball. You do not need to make any changes here, just copy the following script to the `Makefile` that you just created.

```
IMAGE = ${NAME}-${VERSION}.tar.gz
OUTPUT = ${NAME}-${VERSION}-component.tar.gz

build: clean package

set-up-build: clean
	cp $(PWD)/target/classes/manifest.yml $(PWD)/manifest.yml

package: set-up-build
	docker build -t ${NAME}:${VERSION} .
	docker save ${NAME}:${VERSION} | gzip > ${NAME}-${VERSION}.tar.gz
	tar -czvf ${OUTPUT} manifest.yml ${IMAGE}
	rm -f manifest.yml
	rm -f ${IMAGE}

clean:
	rm -f manifest.yml
	rm -f ${IMAGE}
	rm -f ${OUTPUT}
```


## Updating the Project Configuration
We need to update `pom.xml` so that it knows what to do with all files we added above. We include the complete file below for convenience.

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>helloworldservice</artifactId>
    <packaging>jar</packaging>
    <name>hello-world-service</name>
    <version>1.0.0</version>
    <description>Hello World service with support for multiple languages.</description>

    <properties>
        <java.version>11</java.version>
        <maven.compiler.source>${java.version}</maven.compiler.source>
        <maven.compiler.target>${java.version}</maven.compiler.target>
        <spring-cloud.version>Hoxton.SR8</spring-cloud.version>
        <springfox-version>2.9.2</springfox-version>
        <server.port>9515</server.port>
        <server.contextpath>/helloworldservice</server.contextpath>
    </properties>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>2.3.4.RELEASE</version>
    </parent>

    <build>
        <finalName>helloworldservice</finalName>
        <sourceDirectory>src/main/java</sourceDirectory>

        <!-- Populate manifest file template for SLM. -->
        <resources>
            <resource>
                <directory>src/main/resources</directory>
                <filtering>true</filtering>
            </resource>
            <resource>
                <directory>src/main/resources-filtered</directory>
                <filtering>true</filtering>
            </resource>
        </resources>

        <plugins>
            <!-- Include resources in output Jar. -->
            <plugin>
                <artifactId>maven-resources-plugin</artifactId>
                <version>3.2.0</version>
                <executions>
                    <execution>
                        <id>copy-resources</id>
                        <phase>initialize</phase>
                        <goals>
                            <goal>copy-resources</goal>
                        </goals>
                        <configuration>
                            <outputDirectory>${basedir}/target/extra-resources</outputDirectory>
                            <resources>
                                <resource>
                                    <directory>${basedir}/resources</directory>
                                    <filtering>true</filtering>
                                </resource>
                            </resources>
                        </configuration>
                    </execution>
                </executions>
            </plugin>

            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <executions>
                    <execution>
                        <goals>
                            <goal>repackage</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>

            <!-- Create Docker image of the service. -->
            <plugin>
                <groupId>com.spotify</groupId>
                <artifactId>dockerfile-maven-plugin</artifactId>
                <version>1.4.13</version>
                <executions>
                    <execution>
                        <id>default</id>
                        <goals>
                            <goal>build</goal>
                            <goal>push</goal>
                        </goals>
                    </execution>
                </executions>
                <configuration>
                    <dockerfile>Dockerfile</dockerfile>
                    <repository>${project.artifactId}</repository>
                    <tag>${project.version}</tag>
                    <buildArgs>
                        <JAR_FILE>target/${project.build.finalName}.jar</JAR_FILE>
                    </buildArgs>
                </configuration>
            </plugin>

            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-resources-plugin</artifactId>
                <version>3.2.0</version>
                <configuration>
                    <delimiters>
                        <delimiter>@</delimiter>
                    </delimiters>
                    <useDefaultDelimiters>false</useDefaultDelimiters>
                </configuration>
            </plugin>

            <!-- Execute Makefile to package the contents into tar.gz for SLM deployment. //-->
            <plugin>
                <groupId>org.codehaus.mojo</groupId>
                <artifactId>exec-maven-plugin</artifactId>
                <version>1.6.0</version>
                <executions>
                    <execution>
                        <id>slm-packaging-cleanup</id>
                        <phase>clean</phase>
                        <goals>
                            <goal>exec</goal>
                        </goals>
                        <configuration>
                            <executable>/usr/bin/make</executable>
                            <workingDirectory>${basedir}</workingDirectory>
                            <arguments>
                                <argument>clean</argument>
                                <argument>NAME=${project.build.finalName}</argument>
                                <argument>VERSION=${project.version}</argument>
                            </arguments>
                        </configuration>
                    </execution>
                    <execution>
                        <id>slm-packaging</id>
                        <phase>package</phase>
                        <goals>
                            <goal>exec</goal>
                        </goals>
                        <configuration>
                            <executable>/usr/bin/make</executable>
                            <workingDirectory>${basedir}</workingDirectory>
                            <arguments>
                                <argument>package</argument>
                                <argument>NAME=${project.build.finalName}</argument>
                                <argument>VERSION=${project.version}</argument>
                            </arguments>
                        </configuration>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>

    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.springframework.cloud</groupId>
                <artifactId>spring-cloud-dependencies</artifactId>
                <version>${spring-cloud.version}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>

        <dependency>
            <groupId>org.springframework.data</groupId>
            <artifactId>spring-data-commons</artifactId>
        </dependency>

        <!-- Consul -->
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-consul-config</artifactId>
        </dependency>
        
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-consul-discovery</artifactId>
        </dependency>

        <!-- SpringFox -->
        <dependency>
            <groupId>io.springfox</groupId>
            <artifactId>springfox-swagger2</artifactId>
            <version>${springfox-version}</version>
        </dependency>
        <dependency>
            <groupId>io.springfox</groupId>
            <artifactId>springfox-swagger-ui</artifactId>
            <version>${springfox-version}</version>
        </dependency>
        <dependency>
            <groupId>javax.xml.bind</groupId>
            <artifactId>jaxb-api</artifactId>
            <version>2.2.11</version>
        </dependency>
        <dependency>
            <groupId>com.fasterxml.jackson.datatype</groupId>
            <artifactId>jackson-datatype-jsr310</artifactId>
        </dependency>
        <dependency>
            <groupId>org.openapitools</groupId>
            <artifactId>jackson-databind-nullable</artifactId>
            <version>0.1.0</version>
        </dependency>

        <!-- Bean Validation -->
        <dependency>
            <groupId>javax.validation</groupId>
            <artifactId>validation-api</artifactId>
        </dependency>

        <!-- Lombok -->
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>
    </dependencies>
</project>
```

Once you have finished editing `pom.xml` right click it in the project navigation panel and select the menu item **Maven->Reload project**.


## Putting It All Together

> **GOTCHA**
>
> Make sure that Docker is running, or the containerization will fail.

The `pom.xml` configures plugins that will **build**, **containerize**, and package the component Run `mvn clean package` to create the component tarball.

```shell
$ mvn clean package
[INFO] Scanning for projects...
[INFO] 
[INFO] -------------------< com.example:helloworldservice >--------------------
[INFO] Building hello-world-service 1.0.0
[INFO] --------------------------------[ jar ]---------------------------------
.
.
.
Successfully built 553391efa11d
Successfully tagged helloworldservice:1.0.0
docker save helloworldservice:1.0.0 | gzip > helloworldservice-1.0.0.tar.gz
tar -czvf gohelloworldservice-1.0.0-component.tar.gz manifest.yml helloworldservice-1.0.0.tar.gz
a manifest.yml
a helloworldservice-1.0.0.tar.gz
rm -rf helloworldservice-1.0.0.tar.gz
rm -f manifest.yml
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  50.489 s
[INFO] Finished at: 2020-11-25T14:44:53-05:00
[INFO] ------------------------------------------------------------------------
```

<br>

If the process completed successfully, you will now have a file called "helloworldservice-1.0.0-component.tar.gz" in the root folder of the project. This is the file we will use to deploy the service to MSX.
```shell
$ ls -al | grep hello
-rw-r--r--   1 user  staff  101177292 Feb  8 17:20 helloworldservice-1.0.0-component.tar.gz
```


## Deploying the Component
Open the **Cisco MSX Portal** and log in as **superuser** then navigate to **Settings->Component Manager**.

![](images/deploying-component-1.png?raw=true)

<br>

Select **Upload Component** and pick the file `helloworldservice-1.0.0-component.tar.gz` you just created, and then click **Upload** and follow the instructions.

![](images/deploying-component-2.png?raw=true)

<br>
Once the upload has finished a message box will indicating success of failure.

![](images/deploying-component-3.png?raw=true)

<br>
After the message box has been dismissed the new component will appear in the list.

![](images/deploying-component-4.png?raw=true)


## Running It Remotely
The HelloWorldService component has been installed on MSX, and we can make service requests. Next set the value of "MY_MSX_ENVIRONMENT" to match your MSX environment and run the curl command.
```shell
$ export MY_MSX_ENVIRONMENT=dev-plt-aio1.lab.ciscomsx.com
$ curl --insecure --request GET "https://$MY_MSX_ENVIRONMENT/helloworldservice/helloworld/api/v1/languages"
[
  {
    "id":"c486fe09-1b6f-4fae-8e1a-75da88e900a4",
    "name":"English",
    "description":"A West Germanic language that uses the Roman alphabet."
  }
]
```

We have now built and deployed an MSX component and made a request. If you see the following page when you make the request just wait for a few minutes and try again as the service is still deploying.

```html
<html>
<head><title>404 Not Found</title></head>
<body>
<center><h1>404 Not Found</h1></center>
<hr><center>nginx</center>
</body>
</html>
```


## The Missing Pieces
We have already built a useful framework and run code in MSX, but we still need to:
* implement the service layer
* persist domain specific data
* add role based access control
* how Swagger documentation


| [PREVIOUS](04-adding-the-service-delegate.md) | [NEXT](06-implementing-the-service-layer.md) | [HOME](../index.md#java-hello-world-service-example) |
|---|---|---|
