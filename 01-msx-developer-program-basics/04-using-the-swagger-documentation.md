# Accessing the Swagger Documentation
* [Introduction](#introduction)
* [Goals](#goals)
* [Prerequisites](#prerequisites)
* [Finding the Swagger Documentation](#finding-the-swagger-documentation)
* [Making User Management Requests](#making-user-management-requests)
* [Executing Requests in a Terminal Window](#executing-requests-in-a-terminal-window)
* [References](#references)


## Introduction
The Swagger documentation in MSX describes the available service requests, and provides a way to try them out.  

## Goals
* find the Swagger documentation
* make some basic requests


## Prerequisites
* access to an MSX environment [(help me)](../01-msx-developer-program-basics/02-getting-access-to-an-msx-environment.md)


## Finding the Swagger Documentation
To access the MSX Swagger documentation sign into MSX [(help me)](../01-msx-developer-program-basics/03-navigating-the-msx-user-interface.md), click on the username in the top right-hand corner, the select "Account Settings".

![](images/navigating-the-msx-user-interface-7.png)

<br>

Scroll to the bottom of the setting and click "Swagger UI". 

![](images/navigating-the-msx-user-interface-8.png)

<br>

A list of all microservices will be shown, including those from supported third parties.   

![](images/navigating-the-msx-user-interface-9.png)

<br>

## Making User Management Requests
Click on "IDM Microservice" to show the User Management Swagger documentation,

![](images/user-management-1.png)

<br>

Scroll down until you see "Tenants" and click it to expand the list of available requests.

![](images/user-management-2.png)

<br>

Scroll again to find "GET /idm/api/v8/tenants getTenantsPage" and click it. You can now see the inputs and outputs for the request to get a page of tenants. 

![](images/user-management-3.png)

<br>

The power of Swagger documentation is that we can make requests right from the page. To do that select "Try it out", enter values for the "page" and "pageSize" parameters, then click "Execute".

![](images/user-management-4.png)

<br>

Without writing any code we are able to explore the available APIs, or if we have written our service we can use Swagger to do some basic tests. In future guides we will use Swagger to set up resources like roles, permissions, and users to support testing.


## Executing Requests in a Terminal Window
It is also worth mentioning the "curl" command shown in the Swagger response above. Sometimes it is convenient to copy that and run it from a terminal window like this:
```shell
$ curl -X GET "https://dev-plt-aio1.lab.ciscomsx.com/idm/api/v8/tenants?page=0&pageSize=10&showImage=false" -H  "accept: application/json" -H  "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImFuZDBMV3ByYzlXX054YyJ9.eyJzdWIiOiJzdXBlcnVzZXIiLCJsYXN0TmFtZSI6IlVzZXIiLCJ1c2VyX25hbWUiOiJzdXBlcnVzZXIiLCJyb2xlcyI6WyJTVVBFUlVTRVIiXSwiaXNzIjoiaHR0cHM6Ly9kZXYtcGx0LWFpbzEubGFiLmNpc2NvbXN4LmNvbTo0NDMvaWRtIiwiYXV0aG9yaXRpZXMiOlsiUk9MRV9DTElFTlQiXSwiY2xpZW50X2lkIjoibmZ2LWNsaWVudCIsImZpcnN0TmFtZSI6IlN1cGVyIiwic2NvcGUiOlsiYWRkcmVzcyIsImVtYWlsIiwib3BlbmlkIiwicGhvbmUiLCJwcm9maWxlIiwicmVhZCIsIndyaXRlIl0sInRlbmFudElkIjoiNjdkNmMyMDAtNjMzYi0xMWViLWI5MTAtMWQxYWU3NGZjNTUyIiwiZXhwIjoxNjEyMzc5NDE5LCJpYXQiOjE2MTIzNjE0MTksImp0aSI6ImVjOGYyMWMwLWQ4YTktNDgwOS04ZTU5LTI4ZjEzYzZmYjUyNiIsImVtYWlsIjoibm9yZXBseUBjaXNjby5jb20ifQ.GgknMysFLbzKfkf61ko7-Epe9EeW9lpIQNWLVK7IQwe-3GkTxuWbNJsbZO1A_-uYNXLphH2aj1660oaMgOL1r_lLtUJnE5o7HoOG3nGmF0k3PuIqbjWQEAVmH33D7qLatIrijBYhLYdqF4bUOtQ73dfW6MXeS1a-JEWDu_ydTfg0uNtRoKNc9dHlqxc0uH1NCvB98nKAhWKTkUgJ4KIImuMKOXXPWeRnstOaOQzkekk3Kj1TI0h-RKyDP-QKUBlU4ZpPsHQsw8OSOgHGfxqZ44a8T2WVuCf618lv9QtCfjOC_fsjfmf8GBUK_U9_EVBZkXQrbrPA5fjdDKHelhbQRjKJG6VGJt-wc3AD4awFHvjUdFef3ERHwasbKQwULm_rKfvTq11wsiE6tl-8hQcXHpKAvDsyfgT4HEUTYc1eorM_x2bjJh5uwyDPg702PVcnSx1hIV56QVPmX0BErqyKJZfykE4p4pfybUI49TnjxNtjCRzxLXx6MUXs4clbCWfcX2gQ0i7DbwojuQp9nc2faeugndd8ytaFChdolq495SgcK7MjEQda55FRKqgl8GNx5jAKI7oRVvdei0v8WXuz86J8YLKTxa0wjjfdK17G5CWrf-Gr0JcgBXblgZMo6aY1M9v-MKp9_awSVX_Vl8TAG5O1Xs4-U680HB_NkZFAgaQ" --insecure

{
  "page": 0,
  "pageSize": 10,
  "totalItems": null,
  "hasNext": false,
  "hasPrevious": false,
  "sortBy": null,
  "sortOrder": null,
  "contents": [
    {
      "id": "1050ee29-3d5e-46fe-aa9d-5bbdd4e829b5",
      "createdOn": "2021-02-02T20:42:28.515Z",
      "modifiedOn": "2021-02-02T20:42:28.515Z",
      "suspended": false,
      "name": "Fanta",
      "description": "",
      "url": "",
      "image": null,
      "parentId": null,
      "numberOfChildren": 0
    },
    {
      "id": "eed2cffb-ff66-48f7-a331-260e618452ac",
      "createdOn": "2021-02-02T20:42:10.095Z",
      "modifiedOn": "2021-02-02T20:42:10.095Z",
      "suspended": false,
      "name": "Coke",
      "description": "",
      "url": "",
      "image": null,
      "parentId": null,
      "numberOfChildren": 0
    },
    {
      "id": "b7125a9e-c3d9-49e7-a5a9-23f46b85e300",
      "createdOn": "2021-02-02T20:42:16.118Z",
      "modifiedOn": "2021-02-02T20:42:16.118Z",
      "suspended": false,
      "name": "Pepsi",
      "description": "",
      "url": "",
      "image": null,
      "parentId": null,
      "numberOfChildren": 0
    },
    {
      "id": "0ddcbf6b-ea4a-442d-95f0-2ee062e01005",
      "createdOn": "2021-02-01T15:00:42.313Z",
      "modifiedOn": "2021-02-01T15:00:42.313Z",
      "suspended": false,
      "name": "Test Tenant",
      "description": "",
      "url": "",
      "image": null,
      "parentId": null,
      "numberOfChildren": 0
    }
  ]
}
```

There are two important things to note about the request we made:
1. we added the switch "--insecue" because the SSL certificate in our environment is not signed
2. the access token in the header will be different each time you sign in 
   
You will need a valid access token each time you want to make requests like this. You can get that token from Swagger, at which point it maybe just as easy to make your request there. In later guides we show how to get an access token using the password grant in [Java](../02-msx-platform-sdk/02-using-java-to-get-an-access-token-with-the-password-grant.md) and [Go](../02-msx-platform-sdk/02-using-go-to-get-an-access-token-with-the-password-grant.md) which you can then use to make SDK client requests.


## References
[curl - transfer a URL](https://www.mit.edu/afs.new/sipb/user/ssen/src/curl-7.11.1/docs/curl.html)

[Swagger - API Development for Everyone](https://swagger.io)


| [PREVIOUS](03-navigating-the-msx-user-interface.md) | [NEXT](80-configuring-security-clients.md) | [HOME](../index.md#msx-developer-program-basics) |


