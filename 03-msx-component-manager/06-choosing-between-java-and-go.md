# Choosing Between Java and Go
* [Introduction](#introduction)
* [Goals](#goals)
* [Prerequisites](#prerequisites)
* [Go](#go)
* [References](#references)


## Introduction
Choosing a language for your project depends on several factors. Even if you have an existing Java team do not rule out Go until you have reviewed your requirements. This guide will touch on the pros and cons of Java and Go.


## Goals
* highlight the advantages of different languages


# Prerequisites
* general programming knowledge
* details of available team experience


## Go
Go, also known as Golang, is an open source, compiled, and statically typed programming language developed by Google. 

Go is a general-purpose programming language with a simple syntax, backed by a robust standard library. Go programs are assembled using packages for efficient management of dependencies. The language shines in the creation of highly available and scalable web services. It can also be used to create command-line, desktop, and mobile applications. Other benefits include:

* Goroutines have growable segmented stacks. That means they will use more memory only when needed.
* Goroutines have a faster startup time than threads.
* Goroutines come with built-in primitives to communicate safely between themselves (channels).
* Goroutines allow you to avoid having to resort to mutex locking when sharing data structures.
* Goroutines and OS threads do not have 1:1 mapping. A single goroutine can run on multiple threads.
* Goroutines are multiplexed into small number of OS threads.


## References
[Go](https://golang.org)


| [PREVIOUS](05-service-offers-and-subscriptions.md) | [NEXT](07-working-with-openapi-specifications.md) | [HOME](../index.md#msx-component-manager) |
