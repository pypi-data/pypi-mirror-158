# Refraction

## Overview

This program is a [flask](https://palletsprojects.com/p/flask/) WSGI app
for serving views of spreadsheets to individuals whose usernames
(authenticated via a Central Authentication Service a.k.a. CAS) appear in
a particular column of the spreadsheet. For example, you could allow each
user to view their row in a gradesheet. It supports integration with
Google Sheets as well as storing manually uploaded CSV or TSV files.


## Dependencies:

- Python version 2.7 or 3.6+
- `flask`, `flask_cas`, `jinja2`, and `markupsafe` for server support
- `redis` which is used for data storage. You will need to separately
  install the `redis` executable and make sure it's launchable by your
  web server (or you can launch `redis` manually).
- `google` and `googleapiclient` are used for Google Sheets integration,
  but can be ignored if you're not using that.
- `flask_talisman` is highly recommended; without it the server won't
  force HTTPS and will be much less secure; and `flask_seasurf` is also
  recommended to help prevent Cross-Site Request Forgery (CSRF).
- `OpenSSL` is necessary if you want to run in debug mode using HTTPs.
- `pytest` for testing, install with `[test]` option to get it automatically.


## Installing

Run `pip install refraction` which will install the `refraction` module.

You can then run `python -m exploration.tests` to run tests.

NOTE: Right now, tests are broken and will not pass in one phase, and
will leave a running redis server...


## Getting Started:

To set up the server, you'll need to create a directory for running it
from that has certain files (this can be anywhere on your system). The
`rundir` directory in the installed module has an example of what you'll
need, complete with configuration files you can edit.

The main files you will need to change are `rf_config.py` and
`refraction-admin.json`: the former has things like the CAS setup in it,
while the latter needs to list app-wide administrators who will be able
to access *everyone*'s data (or you can leave the admins list empty).

Once these files have been edited, if you want to use Google Sheets,
you'll also have to set up a service account via a Google Cloud project
(you won't need to pay for anything). You'll need a credentials file to
authenticate as the service account (TODO: Detailed steps for that!) and
that must be in your run directory.

When your run directory is set up and you've edited your configuration
files, run:

```py
python -m refraction.app
```

This will start the server locally, and you can test things out. Note
that in some cases a redis instance may remain after you're done testing;
you can kill that process manually.

TODO: Redis cleanup on local server shutdown?


To run the server for real, make sure that you have CAS set up in the
configuration file (you'll need access to a CAS server, which you might
have via a company or academic institution). You should also make sure to
install `flask_talisman` and `flask_seasurf`.

Whatever web server you're running should supply a WSGI layer (e.g.,
Apache has `mod_wsgi`). Use this to actually get the server running; the
`refraction.wsgi` file in the run directory can be the target. For
example, using Apache `mod_wsgi` your configuration file might look like
this:

```cfg
# =================================================
# Refraction App for spreadsheet sharing row-by-row

# the following is now necessary in Apache 2.4; the default seems to be to deny.
# TODO: Does this make these files served up?
<Directory "/home/refraction/rundir">
    Require all granted
</Directory>

WSGIDaemonProcess refraction user=refraction processes=5 display-name=httpd-refraction home=/home/refraction/rundir python-home=/home/refraction/refraction-python python-path=/home/refraction/rundir
WSGIScriptAlias /refraction /home/refraction/rundir/refraction.wsgi process-group=refraction
```

This example configuration assumes that you've created a user named
`refraction`, and put your run directory `rundir` in the home directory
of that user.


## Plans

- All-user views to support things like Q&A.


## Changelog

- v0.1 Initial pre-alpha upload.

