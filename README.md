# EULA Automated Analysis Tool

## Prerequisites

You will need the following things properly installed on your computer.

* A Unix or Linux based operating system
* [Git](https://git-scm.com/)
* [Conda 2.7](https://www.anaconda.com/download/)
* [Node.js](https://nodejs.org/) (with NPM)
* [Ember CLI](https://ember-cli.com/)
* [Java 8](https://java.com/en/download/)
* [nginx](https://www.nginx.com/resources/wiki/start/topics/tutorials/install/)
* [Google Chrome](https://google.com/chrome)
* [The google chromedriver for your system](https://sites.google.com/a/chromium.org/chromedriver/downloads), and available in your path.
* The C++ compiler for your system.  For MacOS, this is included in XCode via `xcode-select --install`.  For Linux systems, the package is `g++` for Debian systems and `gcc-c++` for Fedora systems.

## Installation

### Part 1 (Back-end)
* `git clone https://github.com/EULA-Automated-Analysis/rest-listener.git` this repository
* `cd rest-listener`
* `conda env create -f environment.yml`
* `source activate eula-aat`

Install the punkt package for nltk
* `python -c 'import nltk; nltk.download("punkt")'`

Next, you must install python-boilerpipe.  Be sure to do this in your home directory, not the project directory.
* `cd ~`
* `git clone https://github.com/misja/python-boilerpipe.git`
* `cd python-boilerpipe`
* `pip install -r requirements.txt`
* `python setup.py install`

Once the installation is done, you may delete the python-boilerpipe directory - it is no longer needed.
* `rm -rf ~/python-boilerpipe`


### Pt 2 (Front-end)
* `cd app`
* `npm install`

### Pt 3 (nginx and uwsgi)

Finally, run the nginx and uwsgi config script by typing `./setup.sh` while in the project directory.

Note: Choosing the "test" option will just proxy requests from nginx onto your flask or ember debug systems.  They must still be running for the request to serve properly.  Choosing deploy will cause nginx to serve the requests itself.

## Running for Debug

Run the flask service by activating the `eula-aat` environment as described above then running
* `python api/app.py` from the root directory
* `nginx`
    - If you specified a different configuration name during setup.sh, choose it by adding `-c yourconfig.conf`.
    - Ensure you stop the nginx service at the end of your development by running `nginx -s stop`

Run the ember service by navigating to the `/app` directory then running
* ember serve

## Running for Deploy

After installing the application, set your webserver firewall to accept requests on port 80.

Run one of the following commands to initialize nginx as a service so it will start with your server:
* For MacOS systems:
    - `sudo cp /usr/local/opt/nginx/*.plist /Library/LaunchDaemons`
    - `sudo launchctl load -w /Library/LaunchDaemons/homebrew.mxcl.nginx.plist`
* For Linux systems:
    - `sudo systemctl enable nginx`
