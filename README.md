# Provenance web application

This web application uses the Django framework to define models and serve provenance data, using metadata from CosmoSim as an example. Different apps are used for different models:

* `prov_w3c`: implements the W3C PROV-DM model
* `prov_vo`: implements the IVOA ProvenanceDM model (under development)
* `prov_simdm`: reuses classes from the IVOA Simulation Data Model to define provenance for simulation data

The different parts of the web application are under heavy development and serve to test different possible implementations.

## Disclaimer
This webapp is under development. There can be major changes at any time and it's likely that some things are broken.

## Installation
Clone the git repository:
```
git clone https://github.com/kristinriebe/provenance-cosmosim.git
```

Create a virtual environment and install the required python (2.7) packages:

```
virtualenv -p /usr/bin/python2.7 env
source env/bin/activate

cd provenance-cosmosim
pip install -r requirements.txt
```

The following packages are needed:

django  -- version 1.11  
django-braces -- for json views  
djangorestframework -- rest  
django-extensions -- e.g. for exporting model graphs  
django-test-without-migrations -- for enabling tests of unmanaged models  
pygments  
markdown  
shall be deployed  
BeautifulSoup -- xml parsing  
logger -- write proper log and error messages  
pyyaml -- for loading data (fixtures) from yaml representation  
lxml  -- used for pretty-printing of xml (Votable, VOSI tables renderer), VOSI tables etc.  

Additionally, you will need `mod_wsgi` when deploying the webapp on an apache server (see below).


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

For the `prov_simdm` and `core` app, I wrote a data fixture. If necessary, first clean up all simdm-related data and then reingest using `manage.py loaddata`:

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


## Deploying the webapp on an apache server with `mod_wsgi`.
* Create the directory on a server

    ```
    cd /srv/
    mkdir provenance-cosmosim
    cd provenance-cosmosim
    ```

* Clone the git repository to this directory:

    ```
    git clone https://github.com/kristinriebe/provenance-cosmosim.git
    ```

* If `mod_wsgi` is not yet installed, install it with 
    ```
    sudo apt-get install libapache2-mod-wsgi
    ```
    and enable the module with:
    ```
    sudo a2enmod wsgi
    ```

* Create a virtual environment and install the requirements:

    ```
    virtualenv -p /usr/bin/python2.7 env
    source env/bin/activate

    cd provenance-cosmosim
    pip install -r requirements.txt
    ```

* Collect static files:
    - `cd provenance-cosmosim`
    - `python manage.py collectstatic`
    - You may be asked, if you want to overwrite existing files - check the given paths and type 'yes' to confirm.
    - Adjust file permissions, if needed (see next step)

* Make sure that the webserver-user has read (maybe also write) access to this directory. On Debian systems you can achieve this using:
    - `sudo chown -R apache:apache /srv/provenance-cosmosim`
    - on Ubuntu, the user is called `www-data`.
  - you may need to repeat this each time you do `collectstatic`

* Add a virtual host or an alias to your server configuration. Here's an example for a configuration on Debian using an alias (provenance-cosmosim), which you need to add to the config file at `/etc/httpd/conf.d/vhosts.conf`:

    ```
    <VirtualHost *:80>
    [...]

        # provenance test webapp
        Alias "/provenance-cosmosim/static" "/srv/provenance-cosmosim/provenance-cosmosim/static/"
        <Directory "/srv/provenance-cosmosim/provenance-cosmosim/static/">
            Require all granted
        </Directory>

        WSGIDaemonProcess provenance-cosmosim-app python-home=/srv/provenance-cosmosim/env
        WSGIProcessGroup provenance-cosmosim-app
        WSGIScriptAlias /provenance-cosmosim /srv/provenance-cosmosim/provenance-cosmosim/provenance/wsgi.py process-group=provenance-cosmosim-app
        <Directory "/srv/provenance-cosmosim/provenance-cosmosim/provenance">
            <Files wsgi.py>
                Require all granted
            </Files>
        </Directory>

    </VirtualHost>
    ```
    This uses a separate process group for the wsgi demon, so that multiple django instances can be installed on the same server.

* If you use a new port instead of an alias, do not forget to add `Listen 8111` (replace with your own port no.) to your webserver configuration (e.g. ports.conf)

* Enter your hostname to ALLOWED_HOSTS in `provenance/settings.py`,if it's not yet there already. E.g. for the localhost:
    - `ALLOWED_HOSTS = [u'127.0.0.1', u'localhost']`

* If using an alias (WSGIScriptAlias), do not forget to add it to the STATIC_URL in settings.py:
  `STATIC_URL = '/provenance-cosmosim/static/'`

* Reload the webserver, e.g. on Debian: `service httpd reload`

* Now open your web browser at the server specific address (e.g. http://localhost:8111/ or http://localhost/provenance-cosmosim/) and try the web application!