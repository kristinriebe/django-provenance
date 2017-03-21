# Provenance web application

This web application uses the Django framework to define models and serve provenance data, using metadata from CosmoSim as an example. Different apps are used for different models:

* `prov_w3c`: implements the W3C PROV-DM model
* `prov_vo`: implements the IVOA ProvenanceDM model (under development)
* `prov_simdm`: reuses classes from the IVOA Simulation Data Model to define provenance for simulation data
 
The different parts of the web application are under heavy development and serve to test different possible implementations.

## Installation
Download everything and install the required python (2.7) packages, e.g. using `pip install`:

django  -- version 1.10
django-braces -- for json views  
djangorestframework -- rest  
django-extensions -- e.g. for exporting model graphs  
django-test-without-migrations -- for enabling tests of unmanaged models  
pygments  
markdown  
mod_wsgi -- wsgi-module for apache2, needed on the server on which the webapp shall be deployed 
BeautifulSoup -- xml parsing  
logger -- write proper log and error messages
pyyaml -- for loading data (fixtures) from yaml representation


## Testing
Tests can be run as usual:

```
python manage.py test
```

This executes all tests in the subdirectories as well. Currently, there are only a few tests available, but this will hopefully improve in the future.

## Loading data
There are different possibilities to load data into a Django web application.
For the apps `prov_vo` and `prov_w3c`, the data is loaded directly into the SQlite database with `INSERT` statements from the corresponding files in the `data/` directory. These can be executed using:

```bash
cat data/insert_data_w3c.sql | sqlite3 db.sqlite3
cat data/insert_data_vo.sql | sqlite3 db.sqlite3
```

For the `prov_simdm` app, I wrote a data fixture. If necessary, first clean up all simdm-related data and then reingest using `manage.py loaddata`:

```bash
cat data/delete_data_simdm.sql | sqlite3 db.sqlite3 
python manage.py loaddata prov_simdm/fixtures/simdm_data.yaml
```

## Starting the webapp locally
When everything is installed, start django's test server in the usual way:

```
python manage.py runserver
```

and point a web browser to localhost:8000. Note that you can also provide a different port as additional argument to manage.py, if the default port is already in use.

The webapp should be visible in the browser and it should even work offline, since all libraries are stored in the static directories, e.g. provenance/core/static.


## Deploying the webapp on a server
* Copy everything to your destination, e.g. /srv/
    - `sudo cp -r provenance-cosmosim /srv/`
    - Make sure that the webserver-user has read (maybe also write) access to this directory. On Ubuntu you can achieve this using:
        + `sudo chown -R www-data:www-data /srv/provenance-cosmosim`
        + on Debian, the user is called `apache2`.

* Add a virtual host (or an alias) to your server configuration.
    - e.g. for an apache server on Ubuntu, you can use something similar to this:

    ```
    <VirtualHost *:8111>
       DocumentRoot "/srv/provenance-cosmosim/"
       ServerName Django.local

       # This should be omitted in the production environment
       SetEnv APPLICATION_ENV development

       <Directory "/srv/provenance-cosmosim/provenance">
           Options Indexes MultiViews FollowSymLinks
           AllowOverride All
           Require all granted
       </Directory>

        Alias /static "/srv/provenance-cosmosim/static/"
        <Directory "/srv/provenance-cosmosim/static/">
            Require all granted
        </Directory>

        WSGIScriptAlias / /srv/provenance-cosmosim/provenance/wsgi.py
        <Directory "/srv/provenance-cosmosim/provenance">
            <Files wsgi.py>
            Require all granted
            </Files>
        </Directory>

    </VirtualHost>
    ```

    - in Ubuntu, the virtual host configuration files lie at: `/etc/apache2/sites-available`; and still need to be enabled using 
        `sudo a2ensite <name of vhost>`
    - If you use a new port, do not forget to add `Listen 8111` (replace with your own port no.) to your webserver configuration (e.g. ports.conf)

* Reload the webserver, e.g. on Ubuntu: `service apache2 reload`

* Collect static files:
    - `cd provenance`
    - `python manage.py collectstatic`
    - You may be asked, if you want to overwrite existing files - check the given paths and type 'yes' to confirm.

* Enter your hostname to ALLOWED_HOSTS in `provenance/settings.py`,if it's not yet there already. E.g. for the localhost:
    - `ALLOWED_HOSTS = [u'127.0.0.1', u'localhost']`

* Now open your web browser at the provided port (e.g. http://localhost:8111/) and try the web application!