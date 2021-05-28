# SKA Notes: Generic ESAP Gateway Deployment with Docker

## Context

Rather than this being specific to any SKA deployment, these auxiliary files are added to facilitate generic deployment of the ESAP Gateway (hereafter simply ESAP) stack, i.e. front and back ends, either as a local development version, or in production environments, using Docker.

This was identified as a potential gap in the existing repository, since there were a number of different means of deploying for different purposes (local dev vs. CI machine vs. production instance), when in practice it is often desirable for all such use cases to use the same container architecture so the development environments mirror the production environments.

These instructions are intended as a guide for a new ESAP developer to be able to get up and running with a development ESAP instance, to start testing against.

## Prerequisites

- Docker
- npm
- Source code: assumed to have default repo names, nested within in a single root folder (`$ESAP_ROOT`), i.e.:
    - `$ESAP_ROOT/esap-api-gateway`
    - `$ESAP_ROOT/esap-gui`

## Deployment

### Auxiliary file summary

These auxiliary files sit within the esap-api-gateway code repository, and contain:
- docker-compose.yml: docker-compose specification for launching both ESAP API Gateway (back end) and ESAP GUI (front end)
- Dockerfile: the container image file for the front end, using an NGINX web server to serve the content
- nginx.conf: Configuration file for the NGINX container, enabling the traffic between the services

### Setting the API host

A single change to the front end source code is necessary to set the API host location. This is in the `$ESAP_ROOT/esap-gui/src/contexts/GlobalContext.js:20` file, which specifies:
```js
  const api_host =
    process.env.NODE_ENV === "development"
      ? "http://localhost:5555/esap-api/"
      : "https://sdc-dev.astron.nl:5555/esap-api/";
```

Since the built front end code we will serve in this guide will always consider `NODE_ENV="production"`, the second of these URLs is the one that should be changed.

- For a local deployment, accessed from clients co-located with the running server, or if using SSH port-forwarding to access a remote machine, this should be set to: `"http://localhost:8080/esap-api/"`.

- If running on an externally accessible cloud machine without an external proxy, this should be set to `"http://<host_machine_IP>:<port>/esap-api/"`.

- If running on a cloud machine accessed through a proxy machine (e.g. a separate machine on the same network as the host which uses a web server to direct external traffic to the ESAP instance), then the public floating IP of the proxy machine should be used: `"http://<proxy_machine_external_IP>:<port>/esap-api/"`.

### Deployment step-by-step

1) Set the $ESAP_ROOT environment variable:
    ```bash
    $ export ESAP_ROOT=/path/to/root/directory
    ```
2) Modify the API host in `$ESAP_ROOT/esap-gui/src/contexts/GlobalContext.js` as detailed above
3) Build the front end with npm
    ```bash
    $ cd $ESAP_ROOT/esap-gui
    $ npm run build
    ```
4) Build and run the ESAP service
    ```bash
    $ docker-compose -f $ESAP_ROOT/esap-api-gateway/esap/docker/ska/docker-compose.yml up --build -d
    ```
5) Verify the deployment by navigating to the specified API host from a browser. In the case of a local deployment with no other changes to the Docker (compose) files, this will be: `http://localhost:8080/`

## Future work

In future, it would be good to automate the assignment of the API host in the GUI source code, though as environment variables are not respected after transpilation (building the web content), this will require some careful thought.

Similarly, live code changes will not be reflected in this documentation's current form. This can be done using features provided by the various IDEs of choice and will vary from system to system. The other documentation in this repo and on the Wiki (https://git.astron.nl/astron-sdc/esap-api-gateway/-/wikis/running-in-local-development) should help with this.