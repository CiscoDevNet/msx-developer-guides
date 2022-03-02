# Common Vault and Consul Configurations

* [Introduction](#introduction)
* [Goals](#goals)
* [Prerequisites](#prerequisites)
* [Prefix Required] (#prefex-required)
* [Inspecting the Log](#inspecting-the-log)
* [Generating the Log](#generating-the-log)
* [Conclusion](#conclusion)

## Introduction

Services and applications need to be passed configuration to control integrations and behaviours. In this section, we will discuss common Consul and Vault configurations used to bootstrap service components.

<br>

## Goals

* understanding Consul and Vault configurations

<br>

## Prerequisites

* access to an MSX environment [(help me)](../01-msx-developer-program-basics/02-getting-access-to-an-msx-environment.md)

<br>

## Prefix Required

Depending on the version of MSX you are using, you would be required to use a different prefix.

| MSX Version | Prefix               |
|-------------|----------------------|
| <= 4.0.0    | thirdpartyservices   |
| >= 4.1.0    | thirdpartycomponents |

<br>

## Generating the Log

The Hello World Service we deployed is written in Go, all it does to write a log entry is call `log.Printf`.

```go
func (s *LanguagesApiService) GetLanguages(ctx context.Context) (ImplResponse, error) {
 log.Printf(`Hello World - Get Languages`)
 list := []Language{StubLanguage}
 return Response(http.StatusOK, list), nil
}
```

Make a `curl` command to get a list of languages from your MSX enviorment then check the log again.

```bash
$ export MY_MSX_ENVIRONMENT=dev-plt-aio1.lab.ciscomsx.com
$ curl --insecure --request GET `https://$MY_MSX_ENVIRONMENT/helloworld/api/v1/languages`
[
  {
    `id`:`20f329ac-123f-48f0-917d-a70497cfd22a`,
    `name`:`Esperanto`,
    `description`:`Esperanto is a constructed auxiliary language. Its creator was L. L. Zamenhof, a Polish eye doctor.`
  }
]
```

Switch back to Kibana and set the time window to `Minute` and narrow in on the log entry we just created.

![](images/using-kibana-7.png)

<br>

## Conclusion

If your service works as expected locally, but has some strange behaviours when deployed to MSX, then using logging and Kibana to work out what is going on.

| [PREVIOUS](09-troubleshooting-services.md) | [HOME](../index.md#msx-component-manager) |
