# Using Go To Get an Access Token With the Password Grant
* [Introduction](#introduction)
* [Goals](#goals)
* [Prerequisites](#prerequisites)
* [Creating the Project](#creating-the-project)
* [Creating the OAuth2 Confidential Security Client](#creating-the-oauth2-confidential-security-client)
* [Adding the MSX Platform Dependency](#adding-the-msx-platform-dependency)
* [Writing the Code](#writing-the-code)
* [Running the Application](#running-the-application)


## Introduction
In this guide we will write a Go application that uses the MSX Platform SDK to get an access token using an OAuth2 password grant. We recommend that you use SSO in production, but the password grant is a quick way to programmatically kick the tires.


## Goals
* get an access token using the password grant


## Prerequisites
* access to an MSX environment [(help me)](../01-msx-developer-program-basics/02-getting-access-to-an-msx-environment.md)
* a confidential security client for your application [(help me)](../01-msx-developer-program-basics/80-configuring-security-clients.md) 
* the example source code [(help me)](https://github.com/CiscoDevNet/msx-examples/tree/main/go-password-grant-demo)
* a Go IDE like IntelliJ GoLand [(help me)](https://www.jetbrains.com/goland/)

## Creating the OAuth2 Confidential Security Client
Before we can create the Go application and write the code we need to create a confidential security client [(help me)](../01-msx-developer-program-basics/80-configuring-security-clients.md). Use this payload to create the security client on your MSX environment using Swagger:
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


## Creating the Project
If you want to jump straight to the final solution you can download the example source code  [(help me)](https://github.com/CiscoDevNet/msx-examples/tree/examples/go-password-grant-demo). However, this guide provides step-by-step instructions if you want to work through the example.

Create a new folder then create a project with the following terminal commands:
```shell
$ mkdir go-password-grant-demo
$ cd go-password-grant-demo
$ go mod init go-password-grant-demo
```


## Adding the MSX Platform Dependency
The MSX Platform SDK client provides an easy way to make requests. To add this dependency run "go get" like this:
```shell
$ export GO111MODULE=on
$ go get -u github.com/CiscoDevNet/go-msx-sdk
go: github.com/CiscoDevNet/go-msx-sdk upgrade => v1.0.1
go: github.com/golang/protobuf upgrade => v1.4.3
go: google.golang.org/appengine upgrade => v1.6.7
go: google.golang.org/protobuf upgrade => v1.25.0
go: golang.org/x/oauth2 upgrade => v0.0.0-20210311163135-5366d9dc1934
go: golang.org/x/net upgrade => v0.0.0-20210226172049-e18ecbb05110
```


## Writing the Code
Now that the security client has been created, and the project has been configured, we can write "main.go". Make sure you update the constants in main() to match your MSX environment. 
```go
package main

import (
	"context"
	"crypto/tls"
	"encoding/base64"
	"fmt"
	"net/http"
	"os"

	msxsdk "github.com/CiscoDevNet/go-msx-sdk"
	"github.com/google/uuid"
)

func main() {
	// TODO - Replace these with values from your test MSX environment.
	const (
		myHostName     = "dev-alt-aio1.ciscomsx.com"
		myClientId     = "go-test-private-client"
		myClientSecret = "make-up-a-private-client-secret-and-keep-it-safe"
		myUsername     = "Jeff"
		myPassword     = "Password@1"
	)

	var (
		config             = msxsdk.NewConfiguration()
		ctx                = context.Background()
		client             = msxsdk.NewAPIClient(config)
		basicToken         = fmt.Sprintf("%s:%s", myClientId, myClientSecret)
		basicAuthorization = fmt.Sprintf("Basic %s", base64.StdEncoding.EncodeToString([]byte(basicToken)))
	)

	// <DANGER> Do not defeat the SSL certificate in production.
	customTransport = http.DefaultTransport.(*http.Transport).Clone()
	customTransport.TLSClientConfig = &tls.Config{InsecureSkipVerify: true}
	// </DANGER>

	// Create the MSX SDK client.
	config.Scheme = "https"
	config.Host = myHostName
	config.HTTPClient = &http.Client{Transport: customTransport}

	// Make the authorization token to pass to MSX.

	// Call GetAccessToken with a username and credentials.
	accessToken, _, _ := client.SecurityApi.
		GetAccessToken(ctx).
		Authorization(basicAuthorization).
		GrantType("password").
		Username(myUsername).
		Password(myPassword).
		Execute()

	// Add Access Token Header in the Request
	if token := accessToken.GetAccessToken(); token != "" {
		bearer := fmt.Sprintf("Bearer %s", token)
		config.AddDefaultHeader("Authorization", bearer)
		fmt.Printf("Access Token: %s\n\n", token)
	}

	// Create a new Tenant
	tenantCreate := *msxsdk.NewTenantCreate("GoSDKTestTenant_" + uuid.New().String())

	createResp, _, _ := client.TenantsApi.
		CreateTenant(ctx).
		TenantCreate(tenantCreate).
		Execute()

	// Get list of tenant pages
	pageResp, _, err := client.TenantsApi.
		GetTenantsPage(ctx).
		Page(0).
		PageSize(100).
		Execute()

	if err != nil {
		fmt.Printf("Something went wrong.\n%s\n", err.Error())
		os.Exit(1)
	}

	fmt.Println("Create tenant:")
	fmt.Printf("\tId : %s \n", *createResp.Id)
	fmt.Printf("\tName : %s\n\n", createResp.Name)

	fmt.Println("List of tenants:")
	for _, v := range pageResp.GetContents() {
		fmt.Printf("\tId : %s\n", *v.Id)
		fmt.Printf("\tName : %s\n\n", v.Name)
	}

	// Delete previously created tenant
	client.TenantsApi.
		DeleteTenant(ctx, *createResp.Id).
		Execute()

	fmt.Println("Delete tenant:")
	fmt.Printf("\tId : %s \n", *createResp.Id)
	fmt.Printf("\tName : %s\n\n", createResp.Name)

}
```


## Running the Application
If you are running against a test environment you will need to uncomment the code that defeats the SSL certificate as they are self-signed. We included this code for convenience but recommend that you do not include it in a real project.
```go
.
.
.
    // <DANGER> Do not defeat the SSL certificate in production.
    customTransport := http.DefaultTransport.(*http.Transport).Clone()
    customTransport.TLSClientConfig = &tls.Config{InsecureSkipVerify: true}
    // </DANGER>
.
.
.
```


Now we can run the app from a terminal window.
```shell
$ go run main.go
Access Token:
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImFuZDBMV3ByYzBUckVSWSJ9.eyJzdWIiOiJqZWZmIiwibGFzdE5hbWUiOiJQb3AiLCJ1c2VyX25hbWUiOiJqZWZmIiwicm9sZXMiOlsiT1BFUkFUT1IiLCJIRUxMT1dPUkxEX0NPTlNVTUVSIl0sImlzcyI6Imh0dHBzOi8vZGV2LXBsdC1haW8xLmxhYi5jaXNjb21zeC5jb206NDQzL2lkbSIsImF1dGhvcml0aWVzIjpbIlJPTEVfQ0xJRU5UIl0sImNsaWVudF9pZCI6Im15LXRlc3QtcHJpdmF0ZS1jbGllbnQiLCJmaXJzdE5hbWUiOiJKZWZmIiwic2NvcGUiOlsiYWRkcmVzcyIsImVtYWlsIiwib3BlbmlkIiwicGhvbmUiLCJwcm9maWxlIiwicmVhZCIsInRlbmFudF9oaWVyYXJjaHkiLCJ0b2tlbl9kZXRhaWxzIiwid3JpdGUiXSwidGVuYW50SWQiOiJkNjZlNGEzMC0zOGNmLTExZWItOTg0My0wOTE2ZTdmMzY5ZTAiLCJleHAiOjE2MDgzMjIzNDksImlhdCI6MTYwODMxMzM0OSwianRpIjoiOWM1NDk3ZmQtNGQ1ZS00ZjllLWIxMTUtNmMwOTk3OWQ0MzQxIiwiZW1haWwiOiJub2JvZHlAZXhhbXBsZS5jb20ifQ.ojnB817ptzry0HfQTaTZVnZZZ0E6R_iTQ6iKsIy8c1YP4_JVXIoIEeHxHjiJxV2-GWXfMkiW5sHL0EFl37J5jJnzpRJRhY-wvmWOWUpWmRunacnylbnqqTSnOm-QGxsDFGd3qds8uQrBkkoZbSQKi4EZeVtYCNoGxh9KsySpeMc42JwGB4JItrdhIxgUEISerEYYmEEsXSYnqxQM1ApWcx7dqRnbz-w3GR-pVuEPYgypjOMIToHkS2-yoBPdQNV73tz5STtYU-g8yBzth0sqCVjChq-xUxBQC8EWWWAIsrqkAeun7_N-XW2Rh16tgkdBH0E9AUHh7wiLsZdlDiJ_9Nx46nYBH-MyzulrohlTiOXLiG7MsemMmiTCgQZR_7HgwFw7koZv1-YAvsC5CjqtkKbSitCQTmrKlhtXQwU5Q-QNJ83_rS_Y7EH6DDdR04mzXs5ZAAWKbff0IKDpFARIFgM1xWdaYHDzdgJD4c5ohr_ZUqByQe0HDjxUKM6H8izaJqvhMwYfkYA_9aHAQGOvN_-iOK-k3bfXCsFV4QmrkhoYOaMighJP2Ne89FJnmPCPtSZ4KwvvaBq7YTe4Iz42qk0h9-_iIhrMBl-UmvExN3X3AgTMK1OjqAWkUS2eyjVO9uoOzZ51B55D_th5s7AvsiV3EFJd06eqOJMCytbcwJI

Create tenant:
	Id : ce8c2072-b12c-4453-a59a-b380cc62be9c
	Name : GoSDKTestTenant_acdefcf2-17a1-4fde-b53f-ceab1b137b3d

List of tenants:
	Id : 16697b5f-e2c5-44d6-9c28-c8ab74b70d73
	Name : Pepsi

	Id : 1de5c310-2244-4da7-a0f0-1bbf9a740b20
	Name : Fritolays

	Id : 2e4a7c3b-0484-4c14-a68c-53f6c2e838ef
	Name : Coca-Cola

	Id : ce8c2072-b12c-4453-a59a-b380cc62be9c
	Name : GoSDKTestTenant_acdefcf2-17a1-4fde-b53f-ceab1b137b3d

Delete tenant:
	Id : ce8c2072-b12c-4453-a59a-b380cc62be9c
	Name : GoSDKTestTenant_acdefcf2-17a1-4fde-b53f-ceab1b137b3d
```

<br>

If you are having trouble running the application make sure you:
* created the security client on your MSX environment
* updated the constants in main() to point to your environment
* uncommented the code to defeat the SSL certificate


| [PREVIOUS](02-using-java-to-get-an-access-token-with-the-password-grant.md) | [NEXT](04-using-python-to-get-an-access-token-with-the-password-grant.md) | [HOME](../index.md#msx-platform-sdk) |
