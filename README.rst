MiniSentry. Cheap Sentry replacement for development
====================================================

Sentry is too resource heavy for tiny tasks. If all you need is just to receive
limited amount of exceptions and have basic aggregation, you can try this.

This is hardly more than my weekend project. You can use it in development,
or (if you're brave enough) even in you pet projects. But for sure not on
any kind of serious production.

Tested only with Python apps.

Features:
---------

- You can kep your `raven` setup. Just replace Sentry server with this.
- Aggregates exceptions by some basic rules and displays them in the browser.
- Send emails when new exception group is created.
- Works with SQLite, PostgreSQL or MySQL as database backends.

That's it, if you need more, why don't you use real Sentry instead? It's free.


Requirements:
-------------

- Python 3.6
- Free time (because I haven't tested it much yet).


Deployment:
-----------

1. Create virtualenv and install this app

```
pip install minisentry
```

2. Create `.env`-config file, or use defaults (see configuration).
To pick up `.env`-file you need to export path to it

3. Run migrations

```manage.py migrate```

4. Create superuser

```manage.py createsuperuser```

5. Run it.

```minisentry```

Embedded uwsgi server will be started and you can access interface at (e.g.):

```http://localhost:9000```

Daemonization is up to you. I prefer `systemd`. `supervisord` will also work.

6. Go to admin interface and add some projects. You will get project DSN string
in admin. Getting it in browser is not implemented yet.

```http://localhost:9000/admin/```


Upgrading:
----------

```
pip install -U minisentry
manage.py migrate
service minisentry restart (in case of systemd)
```


Configuration:
--------------

Everything is configured in envvars. You can either use `.env` file to store
them, or manage environment yourself.

If you want to use `.env`-file, just place values in plain text file and export
path to it in `MINISENTRY_ENV_PATH`. E.g.:

```export MINISENTRY_ENV_PATH=~/minisentry.env```

Here are list of variables:

- SECRET_KEY: django secret key
- DEBUG: run in debug mode
- ALLOWED_HOSTS: put here your domain name where you hosting this server. Comma separated list
- DB_ENGINE: either sqlite/postgresql/mysql
- DB_NAME: in case of `sqlite` - path to the file, else - database name
- DB_USER/DB_PASSWORD/DB_HOST/DB_PORT: you know what to do. For sqlite not needed
- TIME_ZONE: Your time zone. Mine is "Europe/Amsterdam"
- LOGGING_CONSOLE_FORMATTER: "simple" or "verbose"

Email settings:
- DEFAULT_FROM_EMAIL: `From` field for mails from minisentry
- EMAIL_HOST/EMAIL_PORT/EMAIL_HOST_USER/EMAIL_HOST_PASSWORD/EMAIL_USE_SSL: Smtp server settings

Server settings:
- MINISENTRY_WEB_HOST/MINISENTRY_WEB_PORT: E.g. "0.0.0.0" and 9000
- MINISENTRY_WEB_STATS_ENABLE: Will enable uwsgi stats server, accessible by telnet
- MINISENTRY_WEB_STATS_HOST/MINISENTRY_WEB_STATS_PORT: address for that stats server
- MINISENTRY_WEB_SERVE_STATIC: Will serve static through uwsgi (default option)
- MINISENTRY_WEB_MULE_COUNT: Number of processed for offloaded tasks

More stuff:
- MINISENTRY_URL_PREFIX: Full address of your server: E.g. https://minisentry.com:9000
- KEEP_DATA_FOR_DAYS: How long to keep not updated events


User management and emails:
---------------------------

You can create as many accounts as you want. Everyone, who has email
in his account details will receive emails. No configuration on that yet.
DSN and admin access will be only for accounts with `is_staff=True`

Docker:
-------

It is TODO. Send me a PR maybe?



