# Choosing Between Java and Go
* [Introduction](#introduction)
* [Goals](#goals)
* [Prerequisites](#prerequisites)
* [Java](#java)
* [Go](#go)
* [References](#references)


## Introduction
Choosing a language for your project depends on several factors. Even if you have an existing Java team do not rule out Go until you have reviewed your requirements. This guide will touch on the pros and cons of Java and Go.


## Goals
* highlight the advantages of different languages


# Prerequisites
* general programming knowledge
* details of available team experience


## Java
Java is class-based, object-oriented programming language originally developed by Sun Microsystems but now owned by Oracle. Java applications are typically compiled to bytecode and can be run on any computer with a Java Virtual Machine (JVM).

The Java slogan "Write Once, Run Anywhere" from the mid 1990s promised a cross platform solution for the masses. In reality, it fell short of that goal but did find purpose as the enterprise programming language of a generation. The upside of this adoption is that Java programmers are not hard to find, and third party libraries are abundant and well supported. Consequently, it is possible to put a team together and build a prototype quickly. However even with optimisation, Java services tend to be on the heavy side, and the garbage collector can be a performance anchor. Java is a good choice for smaller projects when you do not anticipate high loads and performance is not a key metric. 


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
[Java](https://www.java.com/en/)

[Go](https://golang.org)


| [PREVIOUS](05-service-offers-and-subscriptions.md) | [NEXT](07-working-with-openapi-specifications.md) | [HOME](../index.md#msx-component-manager) |
