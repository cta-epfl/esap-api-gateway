# Astron Data Explorer (ADEX) - API (prototype)

Prototype for a small information portal to the different ASTRON datasources (WSRT, Apertif, LOFAR, VO).

This backend API can be used to serve information about several datasources in `json` format through a `REST API`, 
which can be accessed by a (ReactJS) frontend application.

## Initial Setup
A Django project was created by following the instructions on the Django website.
* https://docs.djangoproject.com/en/2.2/intro/tutorial01/

## Data Model

A very simple data model was defined as the core of a `Django` application.

```
class DataSource(models.Model):

    name = models.CharField(max_length=40, default="unknown")
    instrument = models.CharField(max_length=30, default="unknown") # WSRT, Apertif, LOFAR
    description = models.CharField(max_length=1000, default="unknown")
    thumbnail = models.CharField(max_length=200, default="https://alta.astron.nl/alta-static/unknown.jpg")

```

This datamodel was 'migrated' to a database and 'serialized' as a REST API.

## Database
`adex.sqlite3` is a simple "SQlite" database. This is a file based database mechanism which comes out-of-the-box with 
Django and does not require a separate database engine or database server to be installed.

## Deployment
A prototype is deployed in a `Docker` container on a dedicated Docker machine that was setup specifically as a 
test environment.

* http://dop457.astron.nl/adex/

## Admin
Django comes with an Admin application, which can be accessed here. (user: `admin`, password: `admin`)
* http://dop457.astron.nl/adex/admin/

You can log in to the REST API with the same credentials.
