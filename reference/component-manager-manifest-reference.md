# Component Manager Manifest Reference
* [Introduction](#introduction)
* [Manifest Format](#manifest-format)
* [Field Definitions](#field-definitions)
* [Manifest Tips and Tricks](#manifest-tips-and-tricks)
  * [The Minimal Manifest](#the-minimal-manifest)
  * [Executing Special Commands](#executing-special-commands)
  * [Extra Configuration Files](#extra-configuration-files)
  * [Defining Custom Secrets](#defining-custom-secrets)
  * [Defining Custom Consul Configurations](#defining-custom-consul-configurations)
  * [Configuring Cassandra](#configuring-cassandra)
  * [Configuring CockraochDB](#configuring-cockroachdb)
* [References](#references)


## Introduction
One of the inputs to deploying a service is the input manifest.  Each service deployment tar.gz file must contain exactly one input manifest file named manifest.yml.  This file defines environment dependencies for the service such as hardware resource requirements and infrastructure dependencies such as database needs.  


## Manifest Format
```yaml
---
# Metadata for the service to be deployed consisting of name, description, version, and type of service.
Name: "servicename" # Please do not use names with dashes in them as that creates problems with Consul/Vault name resolutions which automatically remove the dashes.
                    # The value of the Name attribute is suggested to consist of lower-case letters and digits and start with a lower-case letter.
                    # The value is a part of Consul and Vault configuration paths: 
                    # e.g. secret/thirdpartyservices/servicename for Vault configuration path, kv/thirdpartyservices/servicename for Consul configuration path.
                    # Please make sure the Name value matches the Consul/Vault configuration paths that the service uses. 
                    # Otherwise, it can cause permission issues when accessing the unmatched paths.
Description: "Service function description"
Version: "v1.0.3" # version of the service
Type: Internal #or External

# Wrapper for containers making up the service to be deployed.  Each service must have at least one container section
# which describes the Docker image to be used for the service.
Containers:
  - Name: "Container-Name-as-identified-after-docker-import"
    Uid: "Optional unique identifier.  Required for pre-populate containers!"
    Version: "Container Version"
    Artifact: "Filename of the container tar.gz. The filename must match a name of <service>.tar.gz packaged inside the wrapping service tar.gz.  The container file must be at the same level as the manifest file, no subdirectories."
    Port: 80 #Service listening Port
    ContextPath: /serviceContextPath # Context path to configure the application routing with

    # [Optional] Collection of tags which will be inserted into Consul.  These tags can be used to query and offer specific functionality
    # to the service.  Certain (required) tags are automatically appended by the deployment process.  Others are highly
    # recommended and required if services need to show inside the MSX UI.  Here are some of the tags that you should consider
    # including:
    #      - "managedMicroservice"
    #      - "buildNumber=1.0.19"
    #      - "contextPath=/test"
    #      - "instanceUuid=45b40541-35c2-4c47-9f14-5ec511b7c365"
    #      - "buildDateTime=2020-10-10T17:51:34.965122Z"
    #      - "componentAttributes=serviceName:testservice~context:test~name:Test Service~description:Test Service~parent:platform~type:platform"
    #      - "swaggerPath=/swagger/"
    #      - "name=Test Service"
    #      - "version=1.0.19"
    Tags:
      - "some"
      - "set"
      - "of"
      - "tags"

    # [Optional] Health check configurations.  Each container can have 1 health endpoint configured.  If a service has a specific
    # health endpoint implemented, please use the Http configuration along with the common health check section.  Otherwise,
    # for services that don't have a dedicated health endpoint implemented please configure the Tcp block and the host
    # will be pinged by tcp health checks instead - useful for DB or other services which need a socket connection check.
    # Note: If no explicit health check is specified, the default of Http check will be used resolving to the application's context-path.
    Check:
      #Should only include one of the below check types.
      Http:
        Scheme: "http" #or https
        Host: "service.example.com" #FQDN or IP of service host if internal can be 127.0.0.1
        Path: "/service/admin/health"
      Tcp:
        Host: "service.example.com" #FQDN or IP of service host if internal can be 127.0.0.1
      IntervalSec: 30 # how often (in seconds) should the system check if your service is up
      InitialDelaySec: 5 # initialization delay - how many seconds should the system wait after application is started before firing off the first health check request
      TimeoutSec: 30 # number of seconds before health check is considered to be timed-out/unhealthy
      Port: 80 # port to use for health checks if different from application's default listening port

    # [Optional] In this section you need to specify the hardware requirements for your application.
    Limits:
      Memory: "512Mi"  # amount of memory/RAM that the application needs.  In this case the example asks for 512MB of RAM.  You should specify what your application needs based on your profiling findings.
      CPU: "1"  # number of virtual CPUs that the application needs

    # [Optional] Environment variables to be populated during deployment which will then be available to the application at startup.
    Env:
      - Name: "EnvVar1"
        Value: "Value1"
      - Name: "EnvVar2"
        Value: "Value2"

    # [Optional] Command to use to start the application.
    Command:
      - "/bin/bash"
      - "-c"
      - "startmycoolservice.sh -c /config/path/config.yml"

    # [Optional] The endpoints sections is used for documenting the endpoints that your application supports.  Some functionality
    # can uses these endpoints to enable/disable features based on these values.
    Endpoints:
      - "/swagger"
      - "/other"

# [Optional] In this section you can configure external configuration files that may be included within your service tar.gz package
# that you are uploading.  These configuration files will be mounted and visible to your application.
ConfigFiles:
  - Name: "conf.yml"  # Name of the configuration file.  The file must be present within the uploaded package in the directory adjacent to your manifest file.
    # Mount configuration section which causes the specified configuration file to be mounted to the specified container
    # from your list above.  The configuration file will only be mounted/visible in the specified container.
    MountTo:
      Container: "registry.service.consul:5000/helloworld"  # container to associate (mount and make visible) the configuration file to
      Path: "/conf.yml" # path of the configuration file to mount


# [Optional] Configuration section for sensitive values such as passwords.  The name:value pairs specified in the Secrets section
# will be inserted into secure configuration Vault and will be accessible to your application at startup and runtime.
# The service configurations are in a sandbox with restricted access.  Multiple name:value pairs can be specified.
Secrets:
  - Name: "<secretsName>" # pathed secret name to be injected at /thirdpartyservices/<service name>/
    Value: "<secretsValue>" # Arbitrary data to be injected into the secret configuration vault corresponding to the above key/name

# [Optional] General configuration section for your application for values to be stored in Consul and be available to your application
# during startup and runtime.  The service configurations are in a sandbox with restricted access. Multiple name:value
# pairs can be specified.
ConsulKeys:
  - Name: "<consulKeyName>" # pathed key name to be injected at /thirdpartyservices/<service name>/
    Value: "<consulKeyValue>" # Arbitrary data to be injected into the Consul configurations corresponding to the above key/name

# [Optional] Customer will be allowed to trigger a pre-populate container to run as a job prior to their deployment
# This container can be used to init DB, Warm cache, Consume platform APIs, etc ...
PrePopulate:
  Uid: "<Uid of Container Manifest to run all pre-populate tasks>"

# [Optional] Configuration section for infrastructure needs such as database for your application.
# List of required infra services required all are optional
# Consul and Vault access granted by default restricted to /<servicename> path in KV
# Population of Env defaults (e.g. cassandra address) will be done by onboarding service
Infrastructure:
  # Database configuration section.  The details for the account that was created for your service can be retrieved from Consul.
  # If your application needs Cassandra, the following configurations can be retrieved from Consul at startup/runtime:
  # - db.cassandra.username
  # - db.cassandra.keyspaceName
  #
  # and the following attribute can be retrieved from Vault at startup time:
  # - db.cassandra.password
  #
  # If your application needs CockroachDB, the following configurations can be retrieved from Consul at startup/runtime:
  # - db.cockroach.username
  # - db.cockroach.databaseName
  #
  # and the following attribute can be retrieved from Vault at startup time:
  # - db.cockroach.password
  Database:
    Type: Cassandra # or Cockroach
    Name: "Expected DB name"

  # !!! Bus functionality is currently not supported.
  Bus:
    Type: Kafka #Maybe NATS in future
    Topics: [ "list of required topics" ]

  # !!! Caching functionality is currently not supported.
  Caching:
    # Assumption is on boarded services run in isolated Redis
    Type: Redis
```

## Field Definitions

| Field                            | Required | Description   |
|----------------------------------|----------|---------------|
| Name                             | Y        | Service name. |
| Type                             | Y        | Manifest type: Internal or External. Currently only support internal.|
| Version                          | Y        | Service version. |
| Description                      | N        | Description of the service. |
| Containers                       | Y        | List of containers within the embedded tar.gz image. For each container we need a Container section describing the container and its needs. |
| Containers.Name                  | Y        | Unique name of the container to be deployed in Docker. Can include target repository or group information. The image will be retagged if the target repository information within the name is incorrect. The retagging will try to remove prefix if host:port format is used. Otherwise, the retagging will just prepend the name with the configured target repository and host like: target_repository_host:port/<original_name>. |
| Containers.Uid                   | N        | Unique identifier for container within manifest. Required only for containers that are pre-populate containers. Optional for non pre-populate containers. |
| Containers.Version               | Y        | Unique version for the container. |
| Containers.Artifact              | Y        | Name of the tar.gz file containing the image for this container within the included in the tar.gz. Example: "helloworld4b.tar.gz" |
| Containers.Port                  | Y        | Unique port to use for the container. |
| Containers.ContextPath           | Y        | Context path for the service/container. |
| Containers.Tags                  | N        | List of custom tags to include in the container deployment within Consul registration. |
| Containers.Command               | N        | List of commands and arguments for the container to run within the deployed Pod. Can be empty list. |
| Containers.Limits                | N        | Resource limits for the container. |
| Containers.Limits.CPU            | N        | Kubernetes CPU limit configuration. Maximum number of vCPU/Core(s) to allocate. |
| Containers.Limits.Memory         | N        | Kubernetes memory limit configuration. Should use Kubernetes "Mi" formatting. |
| Containers.Check                 | N        | If health check is configured, need 1 of either Tcp or Http health check blocks. Defaults to http. |
| Containers.Check.Http.Scheme     | N        | Http or Https. Defaults to slm.k8s.healthcheck.httpCheckScheme=http. |
| Containers.Check.Http.Host       | N        | Host to health check. In most cases the value should be: "127.0.0.0".  Defaults to slm.k8s.healthcheck.defaultHost=127.0.0.1. |
| Containers.Check.Http.Path       | N        | Path to use for health check. Defaults to container's context path. |
| Containers.Check.Tcp.Host        | N        | Host to use for health check. |
| Containers.Check.IntervalSec     | N        | Number of seconds between polling health check endpoint. Defaults to slm.k8s.healthcheck.periodSeconds=30. |
| Containers.Check.InitialDelaySec | N        | Number of seconds to wait before first starting to poll the pod for health. Defaults to slm.k8s.healthcheck.initDelaySeconds=60. |
| Containers.Check.TimeoutSec      | N        | Number of seconds to wait before considering the health check unhealthy due to timeout. Defaults to slm.k8s.healthcheck.timeoutSec=30. |
| Containers.Env                   | N        | List of key:value pairs containing environmental variables/arguments to define for the container deployment. |
| Containers.Endpoints             | N        | List of advertised endpoints that the service handles. |
| ConfigFiles                      | N        | List of configuration files included within the service deployment tar.gz |
| ConfigFiles.Name                 | Y        | Name of the file container within the service tar.gz. The name must match a filename included in the tar.gz |
| ConfigFiles.MountTo              | Y        | Configuration linking to the the container that the file should be associated with. |
| ConfigFiles.MountTo.Container    | Y        | Name of the container to associate with. This value must match the container name field. |
| ConfigFiles.MountToPath          | Y        | Path to mount the file to within the container. The container must expect that file at that location. |
| Secrets                          | N        | List of key:value pairs that should be considered secret/sensitive configurations and should be stored in Vault. |
| Secrets.Name                     | Y        | Name/key of a secret to store in Vault and make available to container(s) within service deployment. If Vault is enabled for the service deployment, the Vault token is provided to all containers within the deployment and they have access to the secrets. Other service deployments do NOT have access to these values - Vault configurations are sandboxed and thus service/deployment specific. |
| Secrets.Value                    | Y        | Value of secret to store in Vault. |
| ConsulKeys                       | N        | List of key:value pairs that should be considered configurations that should be stored in Consul.
| ConsulKeys.Name                  | Y        | Name/key of configuration to store in Consul and make available to container(s) within service deployment. Configurations are sandboxed and thus service/deployment specific. |
| ConsulKeys.Value                 | Y        | Value of configuration to store in Consul. |
| PrePopulate                      | N        | Container that is needed to be deployed prior to the service container in order to pre-populate/initialize the environment for the service. |
| PrePopulate.Uid                  | Y        | Unique identifier of container defined within Container section. |
| Infrastructure                   | N        | Infrastructure related configurations for the service to be deployed. This section contains information such as database and caching dependency definitions. |
| Infrastructure.Database          | N        | Configurations for database connection requirements. |
| Infrastructure.Database.Name     | Y        | Name of database to create for the service. |
| Infrastructure.Database.Type     | Y        | Type of database to use [Cassandra &#124; CockroachDB]. |
| Infrastructure.Bus               | N        | UNSUPPORTED - Configurations for Kafka requirements. |
| Infrastructure.Bus.Topics        | Y        | UNSUPPORTED |
| Infrastructure.Bus.Type          | Y        | UNSUPPORTED |
| Infrastructure.Caching           | N        | UNSUPPORTED - Configurations for Caching/Redis requirements.  |
| Infrastructure.Caching.Type      | Y        | UNSUPPORTED |


## Manifest Tips and Tricks


### The Minimal Manifest
Create a new, empty file called manifest.yml within your directory where you have your service image container tar.gz file.
Take the bare minimum manifest content and paste it into the new manifest.yml that you created.  Use it as a starting point and customize it according to your service needs.  
```yaml
#This is a basic manifest that represents the minimal information required to launch helloworld
Name: "helloworld"
Type: Internal
Containers:
  - Name: "Container Name as identified after docker import"
    Version: "v0.1"
    Artifact: "myServiceImage.tar.gz"
    Port: 8080
    ContextPath: /serviceContextPath
```

### Specifying Custom Hardware Allocations
By default, the deployment mechanism will allocate 128MB and 0.2 virtual CPU cycles to the application.  If you application requires
 more in terms of resources, please include the `Limits` section within your manifest and specify the resource overrides
 that your application requires based on your profiling.
```yaml
Containers:
  - Name: "registry.service.consul:5000/helloworld"
    Version: "v0.1"
    Artifact: "helloworld.tar.gz"
    Port: 8080
    ContextPath: /test
    Limits:
      Memory: "128Mi"
      CPU: "1"
```  

### Using Custom Health Checks
By default, health checks will be performed automatically against the deployed context path and port expecting response of 200.  So,
 if your service `myserviceA` was deployed on port `8080`, automatic health checks would be performed by Consul against
 `http://<host>:8080/myserviceA` expecting a 200 response.  If your service requires health checks against a different context path,
 you will need to include a `Check` section with `Http` block:
```yaml
Containers:
  - Name: "registry.service.consul:5000/helloworld"
    Version: "v0.1"
    Artifact: "helloworld.tar.gz"
    Port: 8080
    ContextPath: /test
    Check:
      Http:
        Scheme: "http"      # or "https"
        Host: "127.0.0.1"   #FQDN or IP of service host if internal can be 127.0.0.1
        Path: "/serviceA/admin/health"
      IntervalSec: 30       # how often (in seconds) should the system check if your service is up
      InitialDelaySec: 20   # initialization delay - how many seconds should the system wait after application is started before firing off the first health check request
      TimeoutSec: 45        # number of seconds before health check is considered to be timed-out/unhealthy
      Port: 8081            # port to use for health checks if different from application's default listening port
``` 

If your service requires a socket connection to determine service health, you'll need to configure a `Tcp` health check instead:
```yaml
Containers:
  - Name: "registry.service.consul:5000/helloworld"
    Version: "v0.1"
    Artifact: "helloworld.tar.gz"
    Port: 8080
    ContextPath: /test
    Check:
      Tcp:
        Host: "127.0.0.1" #FQDN or IP of service host if internal can be 127.0.0.1
      IntervalSec: 30 # how often (in seconds) should the system check if your service is up
      InitialDelaySec: 15 # initialization delay - how many seconds should the system wait after application is started before firing off the first health check request
      TimeoutSec: 30 # number of seconds before health check is considered to be timed-out/unhealthy
      Port: 80 # port to use for health checks if different from application's default listening port
```
 
### Including Custom Tags

If the service needs to be displayed inside MSX UI's list of services supporting Swagger, the following tags section should be specified:
```yaml
Containers:
  - Name: "registry.service.consul:5000/helloworld"
    Version: "v0.1"
    Artifact: "helloworld.tar.gz"
    Port: 8080
    ContextPath: /test
    Tags:
      - "3.10.0"
      - "4.0.0"
      - "managedMicroservice"
      - "buildNumber=1.0.0"
      - "instanceUuid=45b40541-35c2-4c47-9f14-5ec511b7c365"
      - "buildDateTime=2021-01-26T17:51:34.965122Z"
      - "componentAttributes=serviceName:myservice~context:myservice~name:My Test Service~description:Test Service~parent:platform~type:platform"
      - "swaggerPath=/swagger/"
      - "name=My Custom Service"
      - "version=1.0.0"
```

### Executing Special Commands
If your service container needs any special commands to be executed, please add a Command block to your container section within the manifest.yml with the appropriate list of commands.  
```yaml
Containers:
  - Name: "myServiceContainer"
    ContextPath: "/serviceContextPath"
    ...
    Command:
      - "/usr/bin/myservice"
      - --profile
      - production
```


### Extra Configuration Files
If you have any configuration files, add each configuration file to the directory where you have the service image and add a ConfigFile block for each configuration file that the application needs. In each case, the name of the file must match the filename, the container must reference the defined container above, and the path must match the location where your service expects to find the file within the mounted runtime. 
```yaml
Name: "servicename"
Type: Internal
Containers:
  ...
ConfigFiles:
  - Name: "conf1.yml"
    MountTo:
      Container: "myServiceContainer"
      Path: "/conf1.yml"
  - Name: "conf2.yml"
    MountTo:
      Container: "myServiceContainer"
      Path: "/conf2.yml"
```


### Defining Custom Secrets
If you have any custom secrets (secure configurations) that must be inserted into Vault, please add a Secrets block for each property key:value pair.
```yaml  
Name: "servicename"
Type: Internal
Containers:
  ...
Secrets:
  - Name: config1
    Value: value1
  - Name: config2
    Value: value2
```


### Defining Custom Consul Configurations
If you have any custom configurations that must be inserted into Consul, please add a ConsulKeys block for each property key:value pair.  
```yaml
Name: "servicename"
Type: Internal
Containers:
  ...
ConsulKeys:
  - Name: config1
    Value: value1
  - Name: config2
    Value: value2
```


### Configuring Cassandra 
If your service requires a Cassandra database, please add a Infrastructure.Database block to your manifest.yml. A Cassandra DB will be created for your application with the specified name.  A user will also be created for your service. The SLM service generates a unique account for your application. To retrieve the username that your application needs to use to connect to the generated Cassandra DB please retrieve the value under key db.cassandra.username from Consul and value under key db.cassandra.password from Vault to get the auto generated password. The database name(keyspace name) is stored by the key db.cassandra.keyspaceName in Consul.
```yaml
Name: "servicename"
Type: Internal
Containers:
  ...
Infrastructure:
  Database:
    Type: "Cassandra"
    Name: "myServiceDB"
```


### Configuring CockroachDB
If your service requires a Cockroach database, please add a Infrastructure.Database block to your manifest.yml. A Cockroach DB will be created for your application with the specified name.  A user will also be created for your service. The SLM service generates a unique account for your application. To retrieve the username that your application needs to use to connect to the generated Cockroach DB please retrieve the value under key db.cockroach.username from Consul and value under key db.cockroach.password from Vault to get the auto generated password. The database name is stored by the key db.cockroach.databaseName in Consul. The sslrootcert connection parameter must be set to /etc/ssl/certs/ca-bundle.crt.
```yaml
Name: "servicename"
Type: Internal
Containers:
  ...
Infrastructure:
  Database:
    Type: "Cockroach"
    Name: "myServiceDB"
```


## References
[Docker Desktop](https://www.docker.com)

[Kubernetes Managing Resources For Containers](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)
