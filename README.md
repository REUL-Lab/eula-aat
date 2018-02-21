# EULA Automated Analysis Tool

## Prerequisites

You will need the following things properly installed on your computer.

* [Git](https://git-scm.com/)
* [Conda 2.7](https://www.anaconda.com/download/)
* [Java 8](https://java.com/en/download/)
* [nginx](https://www.nginx.com/resources/wiki/start/topics/tutorials/install/)
* [Google Chrome](https://google.com/chrome)
* [The google chromedriver for your system](https://sites.google.com/a/chromium.org/chromedriver/downloads), and available in your path.
* The C++ compiler for your system.  For MacOS, this is included in XCode via `xcode-select --install`.  For Linux systems, the package is `g++` for Debian systems and `gcc-c++` for Fedora systems.

## Installation

* `git clone https://github.com/EULA-Automated-Analysis/rest-listener.git` this repository
* `cd rest-listener`
* `conda env create -f environment.yml`
* Windows: `activate eula-aat` or MacOS/Linux `source activate eula-aat`

Install the punkt package for nltk
* `python -c 'import nltk; nltk.download("punkt")'`


Next, you must install python-boilerpipe.  Be sure to do this in your home directory, not the project directory.
* Windows: `cd %userprofile%` MacOS/Linux `cd ~`
* `git clone https://github.com/misja/python-boilerpipe.git`
* `cd python-boilerpipe`
* `pip install -r requirements.txt`
* `python setup.py install`

Once the installation is done, you may delete the python-boilerpipe directory - it is no longer needed.
* Windows `rmdir /s %userprofile%\python-boilerpipe` MacOS/Linux `rm -rf ~/python-boilerpipe`

Finally, run the nginx and uwsgi config script by typing `./setup.sh` while in the project directory.

Note: Choosing the "test" option will just proxy requests from nginx onto your flask or ember debug systems.  They must still be running for the request to serve properly.  Choosing deploy will cause nginx to serve the requests itself.

## Running for Debug

Run the flask service by activating the `eula-aat` environment as described above then running
* `python api/app.py`
* `nginx`
    - If you specified a different configuration name during setup.sh, choose it by adding `-c yourconfig.conf`.

Run the ember service by navigating to the `/app` directory then running
* ember serve

## Running for Deploy

TODO
