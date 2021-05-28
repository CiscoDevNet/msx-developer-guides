# Configuring a Component Manifest
* [Introduction](#introduction)
* [Goals](#goals)
* [Areas of Configuration](#areas-of-configuration)
* [Simple Example Manifest](#simple-manifest-example)
    * [Component Metadata](#component-metadata)
    * [Security Client Configuration](#security-client-configuration)
    * [Container Array](#container-array)
    * [Container Metadata](#container-metadata)
    * [Container Health Check Configuration](#container-health-check-configuration)
    * [Container Hardware Resource Limits](#container-hardware-resource-limits)
* [References](#references)


## Introduction
The Component Manifest is a configuration file that contains all the information required to onboard and deploy a service. It is combined with one or more containerized services to produce an installable component.  


## Goals
* explain the function of the Component Manifest
* illustrate the explanation with an example


## Areas of Configuration
Full details of the manifest contents can be found in the reference documentation [(help me)](/docs/reference/component-manager-manifest). The view from 30,000 feet looks like this:
* service metadata 
* container details
    * container metadata
    * consul tags
    * security client configuration
    * health check configuration
    * hardware resource limits
    * environment variables 
    * start commands
    * endpoint paths
* ancillary configuration files
* system secrets
* consul configuration
* infrastructure details
     

## Simple Manifest Example
Consider this simple manifest that configures a basic service without a user interface. 
```yaml
Name: "Service Name"
Type: Internal
ConsulKeys:
  - Name: "public.security.clientId"
    Value: "my-public-client-id"
  - Name: "integration.security.clientId"
    Value: "my-confidential-client-id"
Secrets:
  - Name: "integration.security.clientSecret"
    Value: "there-are-no-secrets-that-time-does-not-reveal"
Containers:
  - Name: "Container Name as identified after docker import"
    Version: "v0.1"
    Artifact: "myServiceImage.tar.gz"
    Port: 8080
    ContextPath: "/serviceContextPath"
    Check:
      Http:
        Scheme: "http"
        Host: "127.0.0.1"
        Path: "/service/admin/health"
      IntervalSec: 30
      InitialDelaySec: 5
      TimeoutSec: 30
    Limits:
      Memory: "128Mi"
      CPU: "1"
```


### Component Metadata
At the top manifest we include service metadata like name and description.
```yaml
Name: "Service Name"
Type: Internal
```
The only supported "Type" is "Internal", but the options are:
* Internal - A service that is deployed into Kubernetes inside MSX and is registered via its Consul sidecar.
* External (UNSUPPORTED) - A consumable service that exists outside the MSX cluster.


### Security Client Configuration
You must create public and confidential security clients for your service manually using MSX before you can install it [(help me)](../01-msx-developer-program-basics/80-configuring-security-clients.md). The public client will be used for the Single Sign On (SSO) flow used by Swagger and your user interface. The confidential client will be used to retrieve the user security context, thus enabling RBAC control for your API requests.
```yaml
ConsulKeys:
  - Name: "public.security.clientId"
    Value: "my-public-client-id"
  - Name: "integration.security.clientId"
    Value: "my-confidential-client-id"
Secrets:
  - Name: "integration.security.clientSecret"
    Value: "there-are-no-secrets-that-time-does-not-reveal"
```


### Container Array
The manifest can configure multiple containers, but one is sufficient for many purposes, and multiple services can be put in the same container. Consequently, you can host your service primitives and service applications in a single container. Note in some cases it makes sense to host service initialization and migration processes in their own containers. 


### Container Metadata
Like the service each container has some associated metadata. The final step of packaging a service is to put the manifest and containers in a tarball. Here the "Artifact" is the name of the container in that tarball. The "Port" and "ContextPath" are used by Component Manager to configure Consul in order generate dynamic routes in nginx.
```yaml
Containers:
  - Name: "Container Name as identified after docker import"
    Version: "v0.1"
    Artifact: "myServiceImage.tar.gz"
    Port: 8080
    ContextPath: "/serviceContextPath"
```


### Container Health Check Configuration
These values define the health check endpoint for your application. Component Manager allows for either a TCP health check, or an HTTP health check. A working health check is mandatory for all applications as only healthy applications will be added to the Nginx ingress.
The example below contains good default settings for the assorted timers, but they must be adjusted to suit the individual
needs of each application.
```yaml
    Check:
      Http:
        Scheme: "http"
        Host: "127.0.0.1"
        Path: "/service/admin/health"
      IntervalSec: 30
      InitialDelaySec: 5
      TimeoutSec: 30
```


### Container Hardware Resource Limits
These values set the resource limits that Kubernetes will apply to the container. 

You must ensure that the limits set here align with the full memory requirements of your application's heap and stack.
For example, if a Java application's "Max Heap" is larger than the defined limit, then the application will get reaped before it can start.
 
```yaml
    Limits:
      Memory: "128Mi"
      CPU: "1"
```


## References
[Component Manager Manifest Reference](/docs/reference/component-manager-manifest)
