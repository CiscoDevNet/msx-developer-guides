# Working with Self-Signed SSL Certificates

* [Introduction](#introduction)
* [Goals](#goals)
* [macOS Safari](#macos-safari)
* [macOS Chrome](#macos-chrome)
* [References](#references)


## Introduction
It is never appropriate to use self-signed SSL certificates in production environments, however sometimes it is convenient during development. Most browsers will let you accept self-signed SSL certificates on a case by case basis which will be the focus of this guide. Users familiar with key chain utilities on their operating system can use them to add certificates.


## Goals
This guide will help you work with self-signed SSL certificates during development.


## macOS Safari
When Safari sees a self-signed certificate it shows a page stating "This Page Is Not Private". To proceed to the site anyway click on the "Show Details" button then click "visit this website" and follow the instructions.

![](images/self-signed-certificate-macos-safari.png?raw=true)


## macOS Chrome
When Chrome sees a self-signed certificate it shows a page stating "Your connection is not private". To proceed to the site anyway click on the "Show advanced" button then click "Proceed to xxx.xxx.xxx.xxx (unsafe)" and follow the instructions.

![](images/self-signed-certificate-macos-chrome.png?raw=true)


## References
https://en.wikipedia.org/wiki/Self-signed_certificate


| [PREVIOUS](01-choosing-a-user-interface-framework.md) | [NEXT](03-writing-an-application-with-react.md) | [HOME](../index.md#react-user-interface-example) |
|---|---|---|