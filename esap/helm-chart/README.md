# Installation

## Add helm repository

```bash
$ helm repo add ctaepfl https://cta-epfl.github.io
$ helm repo update
$ helm search repo esap 
```

## Add values

in `values.yaml`:

```yaml
ingress:
  enabled: true
  className: ""
  annotations: #{}
    traefik.ingress.kubernetes.io/router.entrypoints: websecure
    traefik.ingress.kubernetes.io/router.tls: "true"
    ingress.kubernetes.io/proxy-body-size: 50m
  hosts:
  # all of the hosts
  - host: esap.obsuks1.unige.ch
    paths:
    - path: /
      pathType: ImplementationSpecific
  tls:
  - secretName: esap.tls-secret
    # just the hosts for which TLS is needed
    # this will require some standard certmanager on the kubernetes cluster, see e.g. https://getbetterdevops.io/k8s-ingress-with-letsencrypt/    
    # for a service with public IP, letsencrypt certmanager is very straightforward
    hosts: 
    - esap.obsuks1.unige.ch
```

in `values-secret.yaml` (beware to keep secret, do not store in git):

```yaml
django_secret_key: YOUR_OWN_SECRET_KEY

oidc:
    # this is an example for gitlab, which is open for any user. 
    # INDIGO IAM might be preferrable for scientific activities
    OIDC_OP_AUTHORIZATION_ENDPOINT: "https://gitlab.com/oauth/authorize"
    OIDC_OP_TOKEN_ENDPOINT: "https://gitlab.com/oauth/token"
    OIDC_OP_USER_ENDPOINT: "https://gitlab.com/oauth/userinfo"
    OIDC_OP_JWKS_ENDPOINT: "https://gitlab.com/oauth/discovery/keys"    
    OIDC_AUTHENTICATION_CALLBACK_URL: "oidc_authentication_callback"
    #  these secret values
    OIDC_RP_CLIENT_ID: "YOUR_OWN_SECRET_CLIENT_ID"
    OIDC_RP_CLIENT_SECRET: "YOUR_OWN_SECRET_CLIENT_SECRET"
```

## Install the app

```bash
helm install esap ctaepfl/esap -f values.yaml -f values-secret.yaml
```

# Development: TODO

Image versions

App version

TODO: helpers to ingest docker image versions

Helm chart version