# Service Containerization and Packaging
* [Introduction](#introduction)
* [Goals](#goals)
* [Prerequisites](#prerequisites)
* [Containerizing a Service](#containerizing-a-service)
* [Containerizing a Binary Service](#containerizing-a-binary-service)
* [Containerizing a Java Service](#containerizing-a-java-service)
* [Containerizing a React Application](#containerizing-a-react-application)
* [Saving Your Container](#saving-your-container)
* [Putting it All Together](#putting-it-all-together)
* [References](#references)

## Introduction
Once you have written your service or application it must be containerized before it can be loaded into MSX. In this guide will outline how to containerize your service or application, and package it with the manifest.


## Goals
* learn how to containerize services 
* assemble a manifest and container into a component


## Prerequisites
* your service/application container
* your component manifest
* [Docker Desktop](https://www.docker.com/products/docker-desktop)


## Containerizing a Service
There are no hard and fast rules on how to containerize a service. Docker outline a number of helpful
best practices that you should review if you are new to building Docker containers [(help me)](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/).

It is also important that developers keep security and reliability in mind. Here are some key questions to ask yourself when building a container for your application:
1. Is this as compact as I can make it?
    * Did I add anything I did not need 
    * Conversely, have I striped out anything unnecessary?
    * Have I minimized the number of layers in my final container?
    * Could I have saved space by using a multi-stage build and only including final artifacts in my container?
    * Did I choose a small FROM image?  Most apps do not need full-featured OS images such as Ubuntu or CentOS, could I use a minimized Debian image, Alpine or even from scratch? 
2. Did I start with a minimal trusted base image?  
    * Do I know where the image in my FROM command comes from and do I trust the source?  It is best to start with root OS container images rather than chaining on top of other third party images.
    * Did I limit the packages installed in the container to just those required by my application? You should not need to include cli operator tools like vim for example.
    * Are the packages in my container up to date?  It is critical for security that your base image not include known exploits where patches are available.
3. Is my app running as a non-root user?  
    * While it might be tempting to let the container run as root it is far more secure to create a user for your app to limit privileges to just those needed.
4. Am I storing any credentials in my container?  
    * Of course, you would never do that.
5. Am I only running one thing in my container?  
    * Restrict your container to a single function to make it easier to manage and scale. If your service requires more than one app, make another container and resist the urge to package them into the same container.

See the Dockerfiles below for simple examples that illustrate these ideas:


## Containerizing a Binary Service 
Binary services are those written in languages like Rust and Go that much be cross compiled to run on different platforms. This is in contrast to Java which is compiled to bytecode that can be run on any machine with a JVM, or Python which is an interpreted scripting language. This example shows the use of a multi-stage build to compile the source code while constructing a minimal final image. Whilst the example uses Go the same principals can be ported to other compiled languages. 
```dockerfile
# Select a base image to use as builder.  
# This container will be used to compile source but will not be included in the final image.
FROM --platform=linux/amd64 golang:alpine as builder

# Add any additional packages required for the build or for populating the final image. 
# In this case we are pulling ca-certificates and upx (to compact the binary for truely minimal size)
RUN apk update && apk add ca-certificates upx

# Copy in the application source code to an expected location.  
# This Dockerfile lives along side the source code and uses relative paths for the source copy
# This could be omitted if you would prefer to include code checkouts in the build step.
COPY cmd/ /go/src/cto-github.cisco.com/NFV-BU/msx-agent/cmd/
COPY internal/ /go/src/cto-github.cisco.com/NFV-BU/msx-agent/internal/

# Define the working directory for the build
WORKDIR /go/src/cto-github.cisco.com/NFV-BU/msx-agent

# Run the build.  You could include a code checkout here in case you are not including your source along with your Dockerfile
# Note the chaining of commands into a single RUN step. This minimizes the number of layers. 
# While not really required in a build container, it is worth pointing out.
RUN pwd && ls -l \
  && go build -ldflags="-s -w" -o agent cmd/main.go \
  && upx agent
  
# Create the user for the application.  We are doing this in the build container so that the resulting passwd and groups
# file can be copied into the final target thus supporting a scratch container.
ENV USER=agentuser
ENV UID=10001
# See https://stackoverflow.com/a/55757473/12429735RUN
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    "${USER}"
    
# The below commands are being run in the build container to support the use of a scratch target.
# If the target is a full OS these could be run in the final target instead.
COPY testdata/ca.pem testdata/agent.pem testdata/agent-key.pem /certs/
COPY testdata/url testdata/token /conf/
RUN chown -R agentuser:agentuser /certs/
RUN chown -R agentuser:agentuser /conf/

# Define the final container for your application.
# This example shows a scratch container as such it does not contain anything that has not been added. 
# Finaly containers can just as easily be based on an OS such as Alpine or Debian.
# If using a target OS its a good idea to version pin and not use latest for stability. 
FROM --platform=linux/amd64 scratch

# Copy in the final compiled binary from the build container
COPY --from=builder /go/src/cto-github.cisco.com/NFV-BU/msx-agent/agent /agent

# Copy in any required supporting files. Since this is a scratch container we are copying in a number of files
# This is due to the fact that there is no base OS so we must lay down everything we need.
COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /etc/group /etc/group
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /certs/ /certs/
COPY --from=builder /conf/ /conf/

# Note the inclusion of ld-musl to support the use of a dynamicaly linked binary.
# This can be avoided by building statically link binaries. 
# If statically linking, pay careful attention to licensing requirements of any included libs (glibc is GPL for example).
COPY --from=builder /lib/ld-musl-x86_64.so.1 /lib/ld-musl-x86_64.so.1

# Set the user for the application to the one you added earlier.  This will be the default user used to launch the app.
USER agentuser:agentuser

# Define the entrypoint and / or command for your application to ensure Docker will know how to start it.
ENTRYPOINT ["/agent"]
```


## Containerizing a Java Service
This example shows how to create a containerized Java service. Most of the steps below  will also apply to interpreted languages such as Python and Ruby. In this example we are using a single build step which assumes the JAR has been compiled in a prior step, either manually or via automation. 
```dockerfile
# Since this is a single step container we are selecting a minimized Debian image as our base 
# Details of how its put together can be found here: https://github.com/bitnami/minideb 
# Note that we are version pinning to buster to ensure consistency 
FROM --platform=linux/amd64 bitnami/minideb:buster

# Here we are defining the name of application jar as a build arg that can be overwritten by a pipeline job
ARG APP_JAR="myservice.jar"

# First we prep the container by installing the minimal set of packages required to run our Java App
# We will also run a standard package update to ensure the base OS is up to date and includes all available fixes
# Finally we will clean up any cache to ensure this layer is as small as possible.
# Note the chaining of commands here to ensure we do as much work in this single layer as possible
RUN apt-get update &&\
    apt-get dist-upgrade -y --no-install-recommends &&\
    echo deb http://ftp.debian.org/debian buster-backports main >> /etc/apt/sources.list &&\
    apt-get update &&\
    apt -t buster-backports install openjdk-11-jre-headless gosu dumb-init -y --no-install-recommends &&\
    rm -r /var/lib/apt/lists /var/cache/apt/archives &&\
    rm "$rootfsDir/var/cache/ldconfig/aux-cache" &&\
    find "$rootfsDir/usr/share/doc" -mindepth 1 -not -name copyright -not -type d -delete &&\
    find "$rootfsDir/usr/share/doc" -mindepth 1 -type d -empty -delete

# Next, we add in our application jar and launch script 
# Our launch script is a dumb-init script that will use gosu to start our application as a non-root user 
# with the appropriate JVM flags.  Dumb-init is a simple supervisor that will ensure the application handles signals
# correctly and can be cleanly terminated without leaving zombies behind.
COPY $APP_JAR /service/
COPY dockerlaunch.sh /service/

# Next we will setup our user and ensure permissions are correctly set on our application
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "999" \
    "myappuser" &&\
    chmod 0755 /service/dockerlaunch.sh &&\
    chown -R myappuser:myappuser /service/

# Finally, we define the port our app uses and a good ENTRYPOINT
EXPOSE 8080
ENTRYPOINT ["/service/dockerlaunch.sh"]
```


## Containerizing a React Application
This example shows how to containerize a React application. In this example we assume that "npm run build" has been run manually or via automation. 
```Dockerfile
FROM --platform=linux/amd64 nginx:latest
COPY ./build/ /usr/share/nginx/html/reactSsoAppAuthDemo
COPY ./slm/nginx.conf /etc/nginx/conf.d/default.conf
```


## Saving Your Container
Once your Dockerfile is complete you can build it with the following command. Be sure to substitute your project name and tag.
```bash
docker build -t [MY_PROJECT_NAME]:[MY_DOCKER_TAG] .
```

Assuming there are no errors in the build a local copy of your container will be created.

Now that you have built a container for your application you have to save it as an external artifact for uploading into SLM.
This can be accomplished with the following simple command: 

```bash
docker save [MY_PROJECT_NAME]:[MY_DOCKER_TAG] | gzip > ./slm/[MY_PROJECT_NAME]-[MY_DOCKER_TAG].tar.gz
```


## Putting it All Together
You now have all the files in the folder "[MY_PROJECT_FOLDER]/slm" to make the component. 
* a containerized service or application
* an Component Manifest
* any additional config files you want to mount.  

The final step is to package the container(s) and manifest into a tarball using the following command.

```shell
$ tar -czvf [MY_PROJECT_NAME]-[MY_DOCKER_TAG]-component.tar.gz  -C ./slm manifest.yml [MY_PROJECT_NAME]-[MY_DOCKER_TAG].tar.gz config.file
```


## References
[Docker Desktop](https://www.docker.com/products/docker-desktop)


| [PREVIOUS](02-configuring-the-component-manifest.md) | [NEXT](04-onboarding-and-deploying-components.md) | [HOME](../index.md#msx-component-manager) |
