# Installing the MSX Development Proxy

* [Introduction](#introduction)
* [Goals](goals)
* [Installation](#installation)
    * [Homebrew](#homebrew)
    * [coreutils](#coreutils)
    * [node](#node)
    * [msx-dev-proxy](m#sx-dev-proxy)
* [Conclusion](#conclusion)


## Introduction
If you have written a Service Pack or Service Control that was deployed into MSX as an SLM component, then you will 
already have experienced the slow debug cycle. This guide explains how to use the `msx-dev-proxy` to serve the UI for
the component locally against a remote MSX instance.


## Goals
* install homebrew
* install coreutils
* install node
* install msx-dev-proxy


## Installation
Run the terminal commands below to install the software require to run the `msx-dev-proxy` on an Intel Mac.

### Homebrew
```shell
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### coreutils
```shell
$ brew install coreutils
.
.
.
Commands also provided by macOS and the commands dir, dircolors, vdir have been installed with the prefix "g".
If you need to use these commands with their normal names, you can add a "gnubin" directory to your PATH with:
  PATH="/usr/local/opt/coreutils/libexec/gnubin:$PATH"
```

### node
```shell
$ brew install node@14
.
.
.
If you need to have node@14 first in your PATH, run:
  echo 'export PATH="/usr/local/opt/node@14/bin:$PATH"' >> ~/.profile

For compilers to find node@14 you may need to set:
  export LDFLAGS="-L/usr/local/opt/node@14/lib"
  export CPPFLAGS="-I/usr/local/opt/node@14/include"
```

### msx-dev-proxy
```shell
$ npm install --save-dev @cisco-msx/dev-proxy
.
.
.
```


## Conclusion 
You now have all the software required to serve an SLM component UI locally against a remote MSX instance.


| [NEXT](02-finding-an-slm-component-ui-path.md) | [HOME](../index.md#msx-dev-proxy) |
