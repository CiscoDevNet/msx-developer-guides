# Subscribing to Your Application
* [Introduction](#introduction)
* [Goals](#goals)
* [Prerequisites](#prerequisites)
* [Publishing the Application](#publishing-the-application)
* [Creating an Offer](#creating-an-offer)
* [Subscribing to the Application](#subscribing-to-the-application)
* [Using the Application](#using-the-application)
* [Unsubscribing from an Application](#unsubscribing-from-the-application) 


## Introduction
Deploying an application into MSX is the first step in making it available. A tenant cannot subscribe to the application until it has been published, and an offer created. In this guide we walk through the steps in the Cisco MSX Portal to achieve these goals. Note that if you see an unexpected behaviour you may have to hit refresh on the browser.


## Goals
* publish an MSX Application
* create an MSX Application Offer
* subscribe to an MSX Application Offer


## Prerequisites
* everything from previous guide [(help me)](../06-react-user-interface-example/04-building-the-component.md)
* an MSX Component tarball 


## Publishing the Application
Open the Cisco MSX Portal and navigate to "Settings->Component Manager", then click on the ellipsis and select "Publish Application".

![](images/publishing-1.png?raw=true)

<br>

Fill in the "Label" field and click "Save". The "Advanced Settings" are not covered in the document.

![](images/publishing-2.png?raw=true)

<br>

Follow the prompts until the application is published, and you see the success screen.

![](images/publishing-3.png?raw=true)

<br>


## Creating an Offer
Next we need to create an offer that sets details like price and the terms and conditions. Click the ellipsis on the application this time (instead of the component), and select "Offers".

> **GOTCHA**
>
>To create offers your user must have role SUPERUSER or ADMIN.

![](images/offering-1.png?raw=true)

<br>

As this is a new application there are no offers yet.

![](images/offering-2.png?raw=true)

<br>

Click "Create Offer" and fill in the mandatory fields, then click "Save".

![](images/offering-3.png?raw=true)

<br>

The offer will be created and appear in the list. You can create as many offers as you want. Offers can also be restricted by Tenant, but that process is not covered here.

![](images/offering-4.png?raw=true)

<br>


## Subscribing to the Application
To subscribe to the application choose a tenant, click on "Offer Catalog", and select "My React Demo".

![](images/subscribing-1.png?raw=true)

<br>


Follow the prompts until the success dialog is shown. 

![](images/subscribing-2.png?raw=true)

<br>

## Using the Application
Once you have successfully subscribed to the application it will appear in the dashboard for that tenant.

![](images/using-1.png?raw=true)

<br>

The application does implement SSO but for demonstration purposes we do not start the flow until the "Sign In" button is pressed. Go ahead and press the that button, as you are already signed in you will not be prompted to do so again. Instead, the application will show the current user information.

![](images/using-2.png?raw=true)

<br>

To demonstrate the MS SDK client click on the "Tenants" in the application title bar. That will request a page of tenants from MSX and show the response. As an exercise you could display that result in a table, rather than our blunt JSON dump. 

![](images/using-3.png?raw=true)

<br>

Let us take a moment to step back and acknowledge what we have achieved. We have written an MSX user interface, packaged it, onboarded it, deployed it, published it, offered it, subscribed to it, and used it.


## Unsubscribing from the Application
You cannot remove a component that has subscriptions. To unsubscribe from an application click on the cross in the top right-hand corner of the application.

![](images/unsubscribing-1.png?raw=true)

<br>

The application will no longer be visible in the dashboard once the process has completed.

![](images/unsubscribing-2.png?raw=true)

<br>


| [PREVIOUS](04-building-the-component.md) |  [HOME](../index.md#react-user-interface-example) | 
|---|---|