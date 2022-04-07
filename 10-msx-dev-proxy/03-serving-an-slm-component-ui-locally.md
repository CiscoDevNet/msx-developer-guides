# Serving an SLM Component UI Locally

* [Introduction](#introduction)
* [Goals](#goals)
* [Cleaning Up the Local Build](#cleaning-up-the-local-build)
* [Watching the Project on a Specific Path](#watching-the-project-on-a-specific-path)
* [Conclusion](#conclusion)


## Introduction
If you have completed the earlier steps in this guide [(help me)](01-installing-the-msx-dev-proxy.md) then you have
deployed an SLM component to an MSX instance and already know the path the component is being served from. In this guide
we will clean things up and start serving the UI locally on a specific path.


## Goals
* cleaning up the local build
* watching the project on a specific path


## Cleaning Up the Local Build
Earlier we build the `workflow-service-control-exmaple` with the command below:
```shell
$ npm run build

```

The project folder structure looks like this once it is done (the contents of node_modules is not shown for brevity).
```
├── Dockerfile
├── README.md
├── bin
│   ├── build-dev.sh
│   └── build.sh
├── build
│   ├── catalogMetadata.json
│   ├── manifest.yml
│   ├── services <<<< LOOK HERE
│   ├── tcui_package.zip
│   └── workflowexecutor_slm_deployable.tar.gz
├── config
│   ├── manifest.yml
│   └── nginx.conf
├── images
│   ├── import-workflow-1.jpg
│   ├── import-workflow-2.jpg
│   └── import-workflow-3.jpg
├── node_modules
├── package-lock.json
├── package.json
├── rollup.config.js
├── src
│   ├── metadata
│   └── ui
├── tsconfig.json
└── workflows
    └── 20210730_Hello World.json

```

We can see from this that the build output goes to `./build/services` but we want to serve the UI from 
`/workflowexecutorui`. So go ahead and delete the `./build` folder as we are about to rebuild the project and output it 
to match the version running in the MSX instance.


## Watching the Project on a Specific Path
We are now ready to start serving `workflow-service-control-example` locally. Do that run the command below:
```shell
$ env BUILD_PATH=build/workflowexecutorui rollup -c --watch
.
.
.
/Users/hagraham/Projects/workflow-service-control-example/build/workflowexecutorui/workflowexecutor.css 675 B
created build/workflowexecutorui in 6.1s

[2022-04-07 16:14:54] waiting for changes...
```

If you look at the folder structure again you will see that now we have `./build/workflowexecutorui`.
```
├── Dockerfile
├── README.md
├── bin
│   ├── build-dev.sh
│   └── build.sh
├── build
│   └── workflowexecutorui <<<< LOOK HERE!
├── config
│   ├── manifest.yml
│   └── nginx.conf
├── images
│   ├── import-workflow-1.jpg
│   ├── import-workflow-2.jpg
│   └── import-workflow-3.jpg
├── node_modules
├── package-lock.json
├── package.json
├── rollup.config.js
├── src
│   ├── metadata
│   └── ui
├── tsconfig.json
└── workflows
    └── 20210730_Hello World.json
```


## Conclusion
We are now serving the UI for our SLM component. The final step is to run msx-dev-proxy which we will cover in the 
next guide.


| [PREVIOUS](02-finding-an-slm-component-ui-path.md) | [NEXT](04-running-the-msx-dev-proxy.md) | [HOME](../index.md#msx-dev-proxy) |