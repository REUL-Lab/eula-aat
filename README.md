# EULA Automated Analysis Tool

The EULA Automated Analysis Tool is a web application that retrieves, parses, and analyzes EULA documents.  These documents can either be uploaded or retrieved from a publicly accessible URL.  The tool evaluates EULAs on a set of heuristics defined within the project.

### Quickstart for Deploy

If deploying to a debian/Ubuntu server environment, you may follow the [quickstart guide](QUICKSTART.md) to quickly install and initialize the program.

## Prerequisites

You will need the following things properly installed on your computer.

* A Unix or Linux based operating system
* [Git](https://git-scm.com/)
* [Conda 2.7](https://www.anaconda.com/download/) for development or [Native Pip](https://pip.pypa.io/en/stable/installing/) if deploying.
* [Node.js](https://nodejs.org/) (with NPM)
* [Java 8](https://java.com/en/download/)
* [nginx](https://www.nginx.com/resources/wiki/start/topics/tutorials/install/)
* [uwsgi](http://uwsgi-docs.readthedocs.io/en/latest/Install.html)
* [mongodb-dameon](https://docs.mongodb.com/manual/installation/)
* [Google Chrome](https://google.com/chrome)
* [The Google chromedriver for your system](https://sites.google.com/a/chromium.org/chromedriver/downloads), and available in your path.
* The C++ compiler for your system.  For MacOS, this is included in XCode via `xcode-select --install`.  For Linux systems, the package is `g++` for Debian systems and `gcc-c++` for Fedora systems.

## Installation

### Part 1 (Back-end)
* `git clone https://github.com/REUL-Lab/eula-aat.git` this repository
* `cd eula-aat`
* If developing, initialize and acgivate the environment with conda using
    - `conda env create -f environment.yml`
    - `source activate eula-aat`
* If running for deploy (on debian distributions only), run the quick configure script and skip to Part 2
    - `sudo chmod +x setup.sh && sudo ./setup.sh`
* For other deploys, install the python environment and continue following
    - `pip install -r requirements.txt` 

Install the punkt package for nltk
* `python -c 'import nltk; nltk.download("punkt")'`

Next, you must install python-boilerpipe.  Be sure to do this in your home directory, not the project directory.
* `cd /tmp`
* `git clone https://github.com/misja/python-boilerpipe.git`
* `cd python-boilerpipe`
* `pip install -r requirements.txt`
* `python setup.py install`

Once the installation is done, you may delete the python-boilerpipe directory - it is no longer needed.
* `rm -rf /tmp/python-boilerpipe`

### Pt 2 (Front-end)
* `cd app`
* `npm install`
    - Note that by default, node.js will attempt to allocate 4GB of memory.  If you machine has less memory, use the command `node --max-old-space-size=XXX /usr/bin/npm install` where `XXX` is memory in MB.

### Pt 3 (nginx and uwsgi)

Finally, run the nginx and uwsgi config script by typing `./configure.sh` while in the project directory.  This will append two lines to your .bashrc file to set the `analyze_max_threads` and `google_api_key` environment variables.

Note: Choosing the "test" option will just proxy requests from nginx onto your flask and ember debug systems.  They must still be running for the request to serve properly.  Choosing deploy will cause nginx to serve the requests itself.

If you wish to run the project immediately, run `source ~/.bashrc` to export the new environment variables set in the configuration script.

## Running for Further Development

Run the flask service by activating the `eula-aat` environment as described above then running
* `python api/app.py` from the root directory
* `nginx`
    - If you specified a different configuration name during configure.sh, choose it by adding `-c yourconfig.conf`.
    - When done, stop the nginx daemon by running `nginx -s stop`
* `mongod --fork` to start mongodb as a daemon
    - When done, stop the mongodb daemon by runnning `mongod --shutdown`

Run the ember service by navigating to the `/app` directory then running
* `ember serve`

A guide to adding heuristics can be found in [DEVGUIDE.md](DEVGUIDE.MD).

## Running as a Public Web Service (Linux Only)

After installing the application and running the `./configure.sh` script for deploy, set your webserver firewall to accept requests on port 80.

Create a build of the Ember application for nginx to serve by running `./node_modules/ember-cli/bin/ember build`

Run the following command to initialize nginx as a service so it will start with your server:
    - `sudo systemctl enable nginx`
   
Configure mongodb as a service:
    - `sudo systemctl enable mongod`

Configure uwsgi as a service:
    - `sudo systemctl enable uwsgi`

Your server should now be ready to serve requests.