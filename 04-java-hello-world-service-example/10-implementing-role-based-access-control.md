# Implementing Role Based Access Control

* [Introduction](#introduction)
* [Goals](#goals)
* [Prerequisites](#prerequisites)
* [Configuring the Project](#configuring-the-project)
    * [pom.xml](#pomxml)
    * [application.yml](#applicationxml)
    * [manifest.xml](#manifestxml)
    * [LanguageService.java](#languageservicejava)
* [Building and Deploying the Service](#building-and-deploying-the-service)
* [Making a Secure Request](#making-a-secure-request)
* [The Missing Pieces](#the-missing-pieces)


## Introduction
All the Hello World Service requests we have made so were insecure because we have not passed an access token in the header. In this guide we will add that security, and show how to validate the access token and get the list of permissions associated with it.  


## Goals
* secure the API requests
* validate the access token
* fetch list of associated permissions


## Prerequisites
* Java Hello World Service 5 [(help me)](https://github.com/CiscoDevNet/msx-examples/main/java-hello-world-service-5)
* access to an MSX environment [(help me)](../01-msx-developer-program-basics/02-getting-access-to-an-msx-environment.md)
* [Docker Desktop](https://www.docker.com/products/docker-desktop)


## Configuring the Project
Adding security to the Hello World Service is an exercise in configuration. We describe the required changes for each file below.

### pom.xml
A good rule of thumb is not to role your own encryption or security protocols. Those problems have already been solved and tested, so we take advantage of that by including the following dependencies.
```xml
.
.
.
        <!-- MSX Security -->
        <dependency>
            <groupId>com.github.ciscodevnet</groupId>
            <artifactId>java-msx-security</artifactId>
            <version>v1.0.0</version>
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

## application.xml
In the previous guide we added a security rule to enable Swagger, now we update `application.xml` to include a rule for the Hello World Service. The consequence being that all Hello World Service requests will need to include an access token in the authorization header.

For the security integration to work we must also provide a reference to the confidential security client we created earlier [(help me)](../04-java-hello-world-service-example/08-creating-the-security-clients.md). This security client will be used when the access token is validated. 
```yaml
.
.
.
security:
  resources:
    rules:
      -
        # "/v2/api-docs" required for Swagger documentation.
        # "/helloworld/**" required for Hello World Service.
        patterns: "/v2/api-docs, /helloworld/**"
        expr: "hasRole('ROLE_CLIENT') and hasAuthority('SCOPE_read') and hasAuthority('SCOPE_write')"

integration:
  security:
    # The private client identifier for the service.
    clientId: hello-world-service-private-client
    # The private client secret for the service
    clientSecret: make-up-a-private-client-secret-and-keep-it-safe
.
.
.
```

<br>

### manifest.xml
When we created the security clients [(help me)](../04-java-hello-world-service-example/08-creating-the-security-clients.md) we talked about configuring the confidential security client. We added the public security client identifier in the last guide, now update `manifest.yml` to include details of the confidential security client. Note that in a future release SLM will create and configure the confidential security client automatically, but today it is a manual task. 
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
  - Name: "integration.security.clientId" 
    Value: "hello-world-service-private-client"


# [Optional] Configuration section for sensitive values such as passwords.  The name:value pairs specified in the Secrets section
# will be inserted into secure configuration Vault and will be accessible to your application at startup and runtime.
# The service configurations are in a sandbox with restricted access.  Multiple name:value pairs can be specified.
Secrets:
  - Name: "integration.security.clientSecret"
    Value: "make-up-a-private-client-secret-and-keep-it-safe"
.
.
.
```

<br>

### LanguageService.java
The Hello World Service API is now more secure, in that it requires a valid MSX access token for requests to succeed, however any token will do. We may want some users to be able to `read` resources but not `write` them. We implement this Role Based Access Control (RBAC) by creating resource `permissions` and assigning them to "roles" [(help me)](../01-msx-developer-program-basics/90-understanding-roles-and-permissions.md). We can then enforce rules in our API based on which `roles`, and hence `permissions`, the caller has. 

The security code we added includes a `SecurityContextDetailsAccessor` bean that we can inject into our service to get the security context. Open `LanguagesService.java` and wire the bean in as shown.
```javascript
package com.example.helloworldservice.service;

import com.cisco.msx.security.SecurityContextBasedRBACUtils;
import com.example.helloworldservice.cockroach.model.LanguageRow;
import com.example.helloworldservice.cockroach.repository.LanguagesRepository;
import com.example.helloworldservice.model.Language;

import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;


@RequiredArgsConstructor
public class LanguagesService {
    @Autowired
    private SecurityContextBasedRBACUtils securityContextBasedRBACUtils;
.
.
.
```

<br>

Next we can update on or more of our requests to consume it. The class `SecurityContextDetails` is already in the project, so you can view it in IntelliJ. If you have already created `roles` and `permissions` for the service then you can now check if the access token has them by looking at the corresponding fields in the security context.
```javascript
.
.
.
    public List<Language> getAllLanguages() {
        SecurityContextDetails securityContextDetails = securityContextBasedRBACUtils.getSecurityContextDetails();
        // TODO - Do something with the security context.
.
.
.
```

<br>

Here is an example security context that shows example `roles` and `permissions` that can be checked. Implementing RBAC rules is left as an exercise for the reader.
```json
{
    "iss":"http://localhost:9103/idm",
    "sub":"superuser",
    "aud":"hello-world-service-private-client",
    "exp":1607121952,
    "iat":1607112952,
    "jti":"d97fbdd8-0b54-491c-ac55-86925f5f1e80",
    "authTime":1607112849,
    "givenName":"Super",
    "familyName":"User",
    "email":"noreply@cisco.com",
    "locale":"en_US",
    "active":true,
    "scope":[
        "address",
        "email",
        "openid",
        "phone",
        "profile",
        "read",
        "write"
    ],
    "clientId":"hello-world-service-public-client",
    "username":"jeff",
    "userId":"30976d60-359d-11eb-95fd-e5bc02165d45",
    "accountType":"user",
    "currency":"USD",
    "tenantId":"306a9100-359d-11eb-95fd-e5bc02165d45",
    "tenantName":"vms-tenant",
    "providerId":"fe3ad89c-449f-42f2-b4f8-b10ab7bc0266",
    "providerName":"CiscoSystems",
    "providerEmail":"noreply@cisco.com",
    "assignedTenants":[
      "306a9100-359d-11eb-95fd-e5bc02165d45"
    ],
    "roles":[
      "HELLOWORLD_ADMIN"
    ],
    "permissions":[
        .
        .
        .
        "READ_HELLOWORLD_LANGUAGE",
        "WRITE_HELLOWORLD_LANGUAGE",
        "READ_HELLOWORLD_ITEM",
        "WRITE_HELLOWORLD_ITEM",
        .
        .
        .
    ]
}
```


## Building and Deploying the Service
Run the command below from a terminal window in the same folder as `pom.xml` then deploy the resulting tarball into MSX using the Cisco MSX Portal.
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


## Making a Secure Request
Once Hello World Service has been deployed open a terminal window and try making a request to get a list of languages, remembering to use your MSX hostname. Looking at the response you can see that the server responded with `HTTP 401 Unauthorized` because we did not provide an access token. Note that the `--insecure` switch here just allows us to use a self-signed SSL certificate for our development MSX environment.

```shell
$ export MY_MSX_ENVIRONMENT=dev-plt-aio1.lab.ciscomsx.com
$ curl -i "https://$MY_MSX_ENVIRONMENT/helloworldservice/helloworld/api/v1/languages" \
--header "Content-Type: application/json" \
--insecure 

HTTP/1.1 401 
Server: nginx
Date: Fri, 04 Dec 2020 19:24:14 GMT
Content-Length: 0
Vary: Origin
Vary: Access-Control-Request-Method
Vary: Access-Control-Request-Headers
WWW-Authenticate: Bearer
X-XSS-Protection: 1; mode=block
Cache-Control: no-cache, no-store, max-age=0, must-revalidate
Pragma: no-cache
Expires: 0
Content-Security-Policy: base-uri 'self'; default-src 'self'; script-src 'self' blob: 'unsafe-inline' 'unsafe-eval' https://maps.googleapis.com https://maps.gstatic.com http://maps.googleapis.com http://maps.gstatic.com https://dev-plt-aio1.lab.ciscomsx.com;  font-src 'self' data: https://fonts.googleapis.com http://fonts.googleapis.com https://fonts.gstatic.com http://fonts.gstatic.com https://dev-plt-aio1.lab.ciscomsx.com;  connect-src 'self' https://dev-plt-aio1.lab.ciscomsx.com:9443  https://dev-plt-aio1.lab.ciscomsx.com:8765 https://dev-plt-aio1.lab.ciscomsx.com;  img-src 'self' data: https://maps.googleapis.com https://maps.gstatic.com http://maps.googleapis.com http://maps.gstatic.com  https://dev-plt-aio1.lab.ciscomsx.com;  style-src 'self' data: 'unsafe-inline' http://maps.googleapis.com https://maps.gstatic.com https://fonts.googleapis.com http://fonts.googleapis.com https://dev-plt-aio1.lab.ciscomsx.com;  frame-ancestors 'self';  block-all-mixed-content;  report-uri /_/csp-reports
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
X-Frame-Options: SAMEORIGIN
Referrer-Policy: no-referrer
Feature-Policy: accelerometer 'none'; camera 'none'; geolocation 'none'; gyroscope 'none'; magnetometer 'none'; microphone 'none'; payment 'none'; usb 'none';
Expect-CT: max-age=86400, enforce;
Strict-Transport-Security: max-age=15768000
```

We need to get an access token before we can fix the **curl** request we just made. There are two ways to do this:
* complete password grant guide with the Hello World Service confidential security client [(help me)](../02-msx-platform-sdk/02-using-java-to-get-an-access-token-with-the-password-grant.md)
* use the Hello World Service Swagger documentation [(help me)](../04-java-hello-world-service-example/09-adding-swagger-support.md#finding-the-swagger-documentation)

Swagger is faster, so we will use that. The added bonus being that you can create some Language resources if you have no already done so. Start by logging into the Cisco MSX Portal and navigating to the Hello World Service Swagger documentation. Once there click on **GET /helloworldservice/helloworld/api/v1/languages**, then **Try it out**, then **Execute**. If everything worked as expected you should see something similar to this: 

![](images/using-swagger-1.png?raw=true)

<br>

Copy the generated `curl` request and add the `--insecure` switch before running it in a terminal window. The chunk of text after "Authorization: Bearer" is the access token.
```shell
$ curl --insecure -X GET "https://dev-plt-aio1.lab.ciscomsx.com/helloworldservice/helloworld/api/v1/languages" -H  "accept: application/json" -H  "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImFuZDBMV3ByYzBGQThtOCJ9.eyJzdWIiOiJzdXBlcnVzZXIiLCJsYXN0TmFtZSI6IlVzZXIiLCJ1c2VyX25hbWUiOiJzdXBlcnVzZXIiLCJyb2xlcyI6WyJTVVBFUlVTRVIiXSwiaXNzIjoiaHR0cHM6Ly9kZXYtcGx0LWFpbzEubGFiLmNpc2NvbXN4LmNvbTo0NDMvaWRtIiwiYXV0aG9yaXRpZXMiOlsiUk9MRV9DTElFTlQiXSwiY2xpZW50X2lkIjoiaGVsbG8td29ybGQtc2VydmljZS1wdWJsaWMtY2xpZW50IiwiZmlyc3ROYW1lIjoiU3VwZXIiLCJzY29wZSI6WyJhZGRyZXNzIiwiZW1haWwiLCJvcGVuaWQiLCJwaG9uZSIsInByb2ZpbGUiLCJyZWFkIiwid3JpdGUiXSwidGVuYW50SWQiOiJlMGUwZTI4MC0zMGY0LTExZWItYjA4MS02Mzg5MTJjZTUxYmIiLCJleHAiOjE2MDcxMTk4NzMsImlhdCI6MTYwNzExMDg3MywianRpIjoiMjAxYmY0YzUtZmVkNy00MjI3LThhOGItNzg5YzVhNGE2NmNhIiwiZW1haWwiOiJub3JlcGx5QGNpc2NvLmNvbSJ9.Cnrr7LL1s8Roy1K4axX8_0apzfTwvFWe9PZmNa0eT-Hd_kr3rVPwxWMDWTBaDNHmWIsUf4ikiuIOgL9XY2wlYfnX0gZbkFiB9hFODg6zKh1PFiF9ALRCO7E7TeoVJItpUVZWhAdj1q4m1vRg5KkTmDmwMHucBIY0AvCsoqbgIEur_6CPBAu2GT45ja36y24Ithx0gzWX3URYaIqIaUfsUWF-FrfXdNRbPS_ENppmRUT4mo4ncO9-MHIeqRk8qWf8vxp8WVwSQot5yzj6LOqlRHGqc4nlZVc9vxSHdOkcynvYl3o_S_ZrJYhdSZqkxW9Pq1VmwObTtjnvRsaW85K7k2_5tIaLrSSCCn5tQsHUliwRKHgNvG3_JNA38CKyKwuieYhfaYowZ3_5jv74wRPH9pl9nibi44DpRaQu4lcgJzObXfZhvmXERGdyrGYD2Jw2Vt3ofcBrGfZhs_fNXCcY8BkcUDWdcwrTuIa_hoM7rWdGwDAe4SLx5PDVTsHdwzsJSytSgesLrmM_Mn4KjJf-mYuMSpEEPog4_Nm9OCzXKL4U3eYrNOmTATlx-ExXjbuEY-BmMOYwkNeDFzPwDPR1zHSVZE36pFREjhUBeSDhIVU_krZiaE9xUPkH1KgFVyi5eXWxJl8vmIPLqA-3648h-EnpmYKFhYFMG2OqfCXTpwE"

[
  {
    "id": "10b9eab1-0199-4945-b660-c915468af2e6",
    "name": "English",
    "description": "A West Germanic language that uses the Roman alphabet."
  },
  {
    "id": "a46e528f-63b6-448c-8a46-d9a49c74806b",
    "name": "Spanish",
    "description": "A Romance language used to write the first modern novel Don Quixote."
  }
] 
```


## The Missing Pieces
Congratulations you have reached the end of the Java guides for MSX service development. If you worked through them all you will now have a service based on an OpenAPI specification, that persists domain specific data, supports Swagger Documentation, and can enforce RBAC rules. Future guides will cover the subjects below so check back if they interest you:
* monitoring service health
* storing and retrieving secrets
* working with notifications
* accessing event and audit logs
* migrating a service to a new version
