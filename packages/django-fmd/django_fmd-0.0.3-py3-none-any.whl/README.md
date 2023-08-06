# Django Find My Device

![django-fmd @ PyPi](https://img.shields.io/pypi/v/django-fmd?label=django-fmd%20%40%20PyPi)
![Python Versions](https://img.shields.io/pypi/pyversions/django-fmd)
![License GPL V3+](https://img.shields.io/pypi/l/django-fmd)

Find My Device Server implemented in Python using Django.
Usable for the Andorid App [**FindMyDevice**](https://gitlab.com/Nulide/findmydevice/) by [Nnulide](https://nulide.de/):

[<img src="https://fdroid.gitlab.io/artwork/badge/get-it-on.png" alt="Get FindMyDevice on F-Droid" height="80">](https://f-droid.org/packages/de.nulide.findmydevice/)

# Django "Find My Device" server for YunoHost

[![Integration level](https://dash.yunohost.org/integration/django-fmd.svg)](https://dash.yunohost.org/appci/app/django-fmd) ![Working status](https://ci-apps.yunohost.org/ci/badges/django-fmd.status.svg) ![Maintenance status](https://ci-apps.yunohost.org/ci/badges/django-fmd.maintain.svg)  
[![Install django-fmd with YunoHost](https://install-app.yunohost.org/install-with-yunohost.svg)](https://install-app.yunohost.org/?app=django-fmd)

## State

It's in early developing stage and not really usable ;)

What worked (a little bit) with Django's development server:

* App can register the device
* App can send a new location
* App can delete all server data from the device
* The Web page can fetch the location of a device

TODOs:

* Paginate between locations in Web page
* Commands/Push/Pictures
* Write tests, setup CI, deploy python package etc.


## Start hacking:

```bash
~$ git clone https://gitlab.com/jedie/django-find-my-device.git
~$ cd django-find-my-device
~/django-find-my-device$ ./devshell.py
...
(findmydevice) run_testserver
```

## credits

The *FindMyDevice* concept and the App/Web pages credits goes to [Nnulide](https://nulide.de/) the creator of the app FindMyDevice.

Currently, we store a copy of html/js/css etc. files from [findmydeviceserver/web/](https://gitlab.com/Nulide/findmydeviceserver/-/tree/master/web) ([GNU GPLv3](https://gitlab.com/Nulide/findmydeviceserver/-/blob/master/LICENSE))
into our project repository here: [django-find-my-device/findmydevice/web/](https://gitlab.com/jedie/django-find-my-device/-/tree/main/findmydevice/web)
with the [update_fmdserver_files.sh](https://gitlab.com/jedie/django-find-my-device/-/blob/main/update_fmdserver_files.sh) script.

## versions

* [*dev*](https://gitlab.com/jedie/django-find-my-device/-/compare/v0.0.3...main)
  * TBC
* [v0.0.3 - 11.07.2022](https://gitlab.com/jedie/django-find-my-device/-/compare/v0.0.2...v0.0.3)
  * Bugfix store location because of too large `raw_date` field value
* [v0.0.2 - 11.07.2022](https://gitlab.com/jedie/django-find-my-device/-/compare/v0.0.1...v0.0.2)
  * Support Python 3.7 (for current YunoHost version)
  * Setup Gitlab CI pipeline
  * Update README
* [v0.0.1 - 05.07.2022](https://gitlab.com/jedie/django-find-my-device/-/compare/11d09ecb...v0.0.1)
  * init project
  * App can register the device
  * App can send a new location
  * App can delete all server data from the device
  * The Web page can fetch the location of a devi

