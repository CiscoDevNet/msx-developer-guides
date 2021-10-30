# Using Java To Get an Access Token With the Password Grant
* [Introduction](#introduction)
* [Goals](#goals)
* [Prerequisites](#prerequisites)
* [Creating the OAuth2 Confidential Security Client](#creating-the-oauth2-confidential-security-client)
* [Importing the Example](#importing-the-example)
* [Configuring the Example](#configuring-the-example)
* [Running the Example](#running-the-example)
* [Explaining the Example](#explaining-the-example)
* [References](#references)


## Introduction
This guide will help you get an access token using the password grant and make your first MSK SDK client request. We recommend that you use SSO in production, but the password grant is a quick way to programmatically kick the tires.


## Goals
* get an access token using the password grant
* get a page of tenants using the MSX SDK client


## Prerequisites
* access to an MSX environment [(help me)](../01-msx-developer-program-basics/02-getting-access-to-an-msx-environment.md)
* a confidential security client for your application [(help me)](../01-msx-developer-program-basics/80-configuring-security-clients.md) 
* the example source code [(help me)](https://github.com/CiscoDevNet/msx-examples/tree/main/java-password-grant-demo)
* a Java IDE like IntelliJ IDEA [(help me)](https://www.jetbrains.com/idea/)


## Creating the OAuth2 Confidential Security Client
Before we can create the Java application and write the code we need to create a confidential security client [(help me)](../01-msx-developer-program-basics/80-configuring-security-clients.md). Use this payload to create the security client on your MSX environment using Swagger:
```json
{
    "clientId": "my-test-private-client",
    "clientSecret": "make-up-a-private-client-secret-and-keep-it-safe",
    "grantTypes": [
        "password", 
        "urn:cisco:nfv:oauth:grant-type:switch-tenant", 
        "urn:cisco:nfv:oauth:grant-type:switch-user"
    ],
    "maxTokensPerUser": -1,
    "useSessionTimeout": false,
    "resourceIds": [],
    "scopes": [
        "address",
        "read",
        "phone",
        "openid",
        "profile",
        "write",
        "email",
        "tenant_hierarchy", 
        "token_details"
    ],
    "autoApproveScopes": [
        "address",
        "read",
        "phone",
        "openid",
        "profile",
        "write",
        "email",
        "tenant_hierarchy", 
        "token_details"
    ],
    "authorities": [
        "ROLE_USER"
    ],
    "accessTokenValiditySeconds": 9000,
    "refreshTokenValiditySeconds": 18000,
    "additionalInformation": {
    }
}
```


## Importing the Example
Download the example source then open IntelliJ and import the project. Then open the pom.xml file. You can see that the project has a single dependency on MSX Platform SDK.

![](images/password-grant-demo-1.png?raw=true)

<br>


## Configuring the Example
Before you can build and run the example you have to update the highlighted variables.
* your MSX environment URL [(help me)](../01-msx-developer-program-basics/02-getting-access-to-an-msx-environment.md)
* your confidential security client ID [(help me)](../01-msx-developer-program-basics/80-configuring-security-clients.md)
* a username and password [(help me)](../01-msx-developer-program-basics/03-navigating-the-msx-user-interface.md)
* some imaginary tenants [(help me)](../01-msx-developer-program-basics/03-navigating-the-msx-user-interface.md)

![](images/password-grant-demo-2.png?raw=true)

<br>


## Running the Example
We will break the code down line by line in a minute, but for now run ahead and run the application. You will see a list of tenants names displayed in the console window.
![](images/password-grant-demo-3.png?raw=true)

<br>


## Explaining the Example

### Imports
Most of the imports come from `com.cisco.msx.platform` and we will explain each one as we use it.
```javascript
package com.cisco.msx.passwordgrantdemo;

import com.cisco.msx.platform.ApiClient;
import com.cisco.msx.platform.ApiException;
import com.cisco.msx.platform.client.SecurityApi;
import com.cisco.msx.platform.client.TenantsApi;
import com.cisco.msx.platform.model.TenantsPage;
import java.util.Base64;
```

### Configuring the Application
We discussed the configuration earlier, so we could run the application as soon as possible. We include them again here for completeness but remember you will have to update them to match your environment.
```javascript
public static final String MY_SERVER_URL = "https://dev-plt-aio1.lab.ciscomsx.com";
public static final String MY_CLIENT_ID = "my-private-client";
public static final String MY_CLIENT_SECRET = "there-are-no-secrets-that-time-does-not-reveal";
public static final String MY_USERNAME = "jeff";
public static final String MY_PASSWORD = "Password@1";
```

### Creating the SDK Client
Behind the scenes the MSX SDK client is an HTTP client with a funny hat on. It will take care of sending requests and processing responses. 
```javascript
// Create an MSX SDK client.
ApiClient client = new ApiClient().setBasePath(MY_SERVER_URL);
client.setVerifyingSsl(false);
````

> **GOTCHA**
>
> Do not defeat the SSL certificate in production code!

### Getting an Access Token
We use a SecurityApi object to make the password grant request to get an access token. Before we can make the request we have to construct the "Basic Authentication Token". To make this concatenate the client identifier and client secret separated by a colon, then base64 encode the result. The server will decode this string to get the information it needs to complete the request.
```javascript
// Get an access token using the password grant.
SecurityApi securityApi = new SecurityApi(client);
String basicToken = MY_CLIENT_ID + ":" + MY_CLIENT_SECRET;
String basicAuthorization = "Basic " + Base64.getEncoder().encodeToString(basicToken.getBytes());
String accessToken = securityApi.getAccessToken(basicAuthorization, 
    "password", MY_USERNAME, MY_PASSWORD,
     null, null, null, null, null, null)
    .getAccessToken();
```

### Adding the Access Token Header
Now that we have an access token we need to add a default authorisation header to the SDK client so that the server can authenticate and authorize our requests.
```javascript
// Add the access token header to the client.
client.addDefaultHeader("Authorization", "Bearer " + accessToken);
``` 

### Displaying a Page of Tenants
The final step is to make an MSX SDK client request to get the tenants and display the result. Note that we are handed a page of tenant objects. We do not have to parse a JSON or define a model for the response, the SDK takes care of all that. 
```javascript
// Get a page of tenants and display the names.
TenantsApi tenantsApi = new TenantsApi(client);
TenantsPage tenantsPage = tenantsApi.getTenantsPage(0,10, null, false, null, null);
tenantsPage.getContents().forEach(x -> System.out.println(x.getName()));
```

### Catching and Handling Exceptions
The example has a single catch for all the exceptions. All it does is write an  error message to the console. In a real application you should catch and handle exceptions in a more useful way.
```javascript
catch (ApiException e) {
    System.err.println(e.toString());
}
   ```
## References
[IntelliJ IDEA](https://www.jetbrains.com/idea/)


| [PREVIOUS](01-introducing-the-msx-platform-sdk.md) | [NEXT](03-using-go-to-get-an-access-token-with-the-password-grant.md) | [HOME](../index.md#msx-platform-sdk) |


