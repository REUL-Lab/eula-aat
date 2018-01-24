# rest-listener

## Prerequisites

You will need the following things properly installed on your computer.

* [Git](https://git-scm.com/)
* [Conda 2.7](https://www.anaconda.com/download/)

## Installation

* `git clone https://github.com/EULA-Automated-Analysis/rest-listener.git` this repository
* `cd rest-listener`
* `conda env create -f environment.yml`
* Windows: `activate rest-listener` or MacOS/Linux `source activate rest-listener`


Next, you must install python-boilerpipe.  Be sure to do this in your home directory, not the project directory.
* Windows: `cd %userprofile%` MacOS/Linux `cd ~`
* `git clone https://github.com/misja/python-boilerpipe.git`
* `cd python-boilerpipe`
* `pip install -r requirements.txt`
* `python setup.py install`

Once the installation is done, you may delete the python-boilerpipe directory - it is no longer needed.
* Windows `rmdir /s %userprofile%\python-boilerpipe` MacOS/Linux `rm -rf ~/python-boilerpipe`