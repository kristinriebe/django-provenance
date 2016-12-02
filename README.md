# Provenance web application

This web application uses the Django framework to define models and serve provenance data. Different apps are used for different models:

* `prov_w3c`: implements the W3C PROV-DM model
* `prov_vo`: implements the IVOA ProvenanceDM model (under development)
* `prov_simdm`: reuses classes from the IVOA Simulation Data Model to define provenance for simulation data
 
The different parts of the web application are under heavy development and serve to test different possible implementations.

## Installation
Download everything and install the required python (2.7) packages:

django
django-braces -- for json views
djangorestframework -- rest
django-extensions -- e.g. for exporting model graphs
django-test-without-migrations -- for enabling tests of unmanaged models
pygments
markdown
BeautifulSoup -- xml parsing

## Starting the webapp
When everything is installed, start django's test server in the usual way:

python manage.py runserver

and point a web browser to localhost:8000. Note that you can also provide a different port as additional argument to manage.py, if the default port is already in use.

The webapp should be visible in the browser and it should even work offline, since all libraries are stored in the static directories, e.g. provenance/core/static.


