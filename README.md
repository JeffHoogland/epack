![icon](https://github.com/wfx/epack/blob/master/data/epack_64.png) epack
=====

epack is a tiny file extractor

![Screenshot](https://github.com/wfx/epack/blob/master/data/screenshot.jpg)


## Requirements ##

* Python 2.7 or higher
* python modules: efl, magic


## Installation ##

* For system-wide installation (needs administrator privileges):

 `(sudo) python setup.py install --record files.txt`

* Install in a custom location:

 `python setup.py install --prefix=/MY_PREFIX`

## Uninstall ##

* For system.wide deinstallation (need administrator privileges):

 `(sudo) cat files.txt | xargs rm -rf
