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

## Starting the webapp locally
When everything is installed, start django's test server in the usual way:

python manage.py runserver

and point a web browser to localhost:8000. Note that you can also provide a different port as additional argument to manage.py, if the default port is already in use.

The webapp should be visible in the browser and it should even work offline, since all libraries are stored in the static directories, e.g. provenance/core/static.


## Deploying the webapp on a server
* Copy everything to your destination, e.g. /srv/
    - `sudo cp -r provenance /srv/`
    - Make sure that the webserver-user read (maybe also write) access to this directory. On Ubuntu you can achieve this using:
        + `sudo chown -R www-data:www-data /srv/provenance`
        + on Debian, the user is called `apache2`.

* Add a virtual host (or an alias) to your server configuration.
    - e.g. for an apache server on Ubuntu, you can use something similar to this:

    ```
    <VirtualHost *:8111>
       DocumentRoot "/srv/provenance/"
       ServerName Django.local

       # This should be omitted in the production environment
       SetEnv APPLICATION_ENV development

       <Directory "/srv/provenance/provenance">
           Options Indexes MultiViews FollowSymLinks
           AllowOverride All
           Require all granted
       </Directory>

        Alias /static "/srv/provenance/static/"
        <Directory "/srv/provenance/static/">
            Require all granted
        </Directory>

        WSGIScriptAlias / /srv/provenance/provenance/wsgi.py
        <Directory "/srv/provenance/provenance">
            <Files wsgi.py>
            Require all granted
            </Files>
        </Directory>

    </VirtualHost>
    ```

    - in Ubuntu, the virtual host configuration files lie at: /etc/apache2/sites-available; and still need to be enabled using 
        `sudo a2ensite <name of vhost-configuration-file>`

* Reload the webserver, e.g. on Ubuntu: `service apache2 reload`

* Collect static files:
    - `cd provenance`
    - `python manage.py collectstatic`
    - You may be asked, if you want to overwrite existing files - check the given paths and type 'yes' to confirm.

* Now open your web browser at the provided port and try the web application!