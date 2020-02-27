# ESAP-gateway

ESAP-gateway is the backend for the Escape WP5 ESAP application. Currently only used for data discovery.

It contains a small Sqlite database to store information about dataset, catalogs and services. 
And a REST API for access, either directly, or through a GUI. (see the ESAP-GUI)

The ESAP gateway also contains the 'business logic' to query several external services.

The goal is to have a top level generic query interface accessable through the REST API, which is then translated into 
the specific query parameters and functionality for the underlying services.
The parameter translations are stored in the database per catalog. 

Ideally, the underlying services follow a commom access patterna and behaviour, so that the 'service adaptor' classes can be shared. 
This is the case for standard VO services like the 'ivoa.obscore' service.

But in many cases this might not be possible, and then specific 'service connector' classes can be added.


## Documentation 
* backend (API): https://git.astron.nl/vermaas/esap-gateway/wikis/ESAP-gateway

See also:
* frontend (GUI): https://git.astron.nl/vermaas/adex-gui/wikis/ADEX-GUI