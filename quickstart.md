# Quickstart for Deploy

An automatic setup and configuration script has been provided for use on Debian/Ubuntu systems.  Other systems that do not use systemctl and the aptitude package manager are not supported.

The script requires execution privileges, enable them by running `sudo chmod +x setup.sh`.
Run the script as root `sudo ./setup.sh` and wait for it to complete.

The eula-aat directory must be in a location accessible by your service workers.  A recommended location is `/usr/share`.

After ensuring that your directory is accessible, run the configuration script as root `sudo ./configure.sh` and choose the following options:

* Environment type (test/deploy): `deploy`
* nginx configuration location: `/etc/nginx`
* name for nginx config file: `nginx.conf`
* directory for www directory: `/var/www` 
* uwsgi configuration location: `/etc/uwsgi/apps-enabled`
* uid of service user: `www-data`
* gid of service usergroup: `www-data`
* directory of project accessible by your service worker: The location of your repository clone, the recommended path is `/usr/share/eula-aat`
* number of nginx worker processes: `16`
* number of processing threads for a request: `4`
* key for google APIs: your-api-key
* Set nginx to run on start? [y/N]? `y`
* Set uwsgi to run on start [y/N]? `y`
* Set mongod to run on start? [y/N]? `y`

Build the front-end by navigating to the `app` directory and running the following, in order:
* `node --max-old-space-size=512 /usr/bin/npm --unsafe-perm install`
* `./node_modules/ember-cli/bin/ember build`

Reboot the system, and the program should be ready to serve requests on port 80.