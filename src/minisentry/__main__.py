"""
Configure and run uwsgi server with MiniSentry and also serve static from it.
"""

# Mostly taken from:
# https://github.com/getsentry/sentry/blob/master/src/sentry/services/http.py


import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "minisentry.settings")


def convert_options_to_env(options):
    for k, v in options.items():
        if v is None:
            continue
        key = "UWSGI_" + k.upper().replace("-", "_")
        if isinstance(v, str):
            value = v
        elif v is True:
            value = "true"
        elif v is False:
            value = "false"
        elif isinstance(v, int):
            value = str(v)
        else:
            raise TypeError("Unknown option type: %r (%s)" % (k, type(v)))
        yield key, value


def prepare_environment(options, env=None):
    if env is None:
        env = os.environ

    # Move all of the options into UWSGI_ env vars
    for k, v in convert_options_to_env(options):
        env.setdefault(k, v)

    # Signal that we"re running within uwsgi
    env["MINISENTRY_RUNNING_UWSGI"] = "1"

    # Look up the bin directory where `minisentry` exists, which should be
    # sys.argv[0], then inject that to the front of our PATH so we can reliably
    # find the `uwsgi` that's installed when inside virtualenv.
    # This is so the virtualenv doesn't need to be sourced in, which effectively
    # does exactly this.
    virtualenv_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    current_path = env.get("PATH", "")
    if virtualenv_path not in current_path:
        env["PATH"] = "%s:%s" % (virtualenv_path, current_path)


def main():
    from django.conf import settings

    host = settings.MINISENTRY_WEB_HOST
    port = settings.MINISENTRY_WEB_PORT

    options = {}
    options.setdefault("module", "minisentry.wsgi:application")
    options.setdefault("protocol", "http")
    options.setdefault("auto-procname", True)
    options.setdefault("procname-prefix-spaced", "[MiniSentry]")
    options.setdefault("workers", 3)
    options.setdefault("threads", 4)
    options.setdefault("http-timeout", 30)
    options.setdefault("vacuum", True)
    options.setdefault("thunder-lock", True)
    options.setdefault("log-x-forwarded-for", False)
    # Not sure about this
    # options.setdefault("buffer-size", 32768)
    options.setdefault("post-buffering", 65536)
    options.setdefault("limit-post", 1048576)  # I think 20971520 way too large
    options.setdefault("need-app", True)
    options.setdefault("disable-logging", False)
    options.setdefault("memory-report", True)
    options.setdefault("reload-on-rss", 600)
    options.setdefault("ignore-sigpipe", True)
    options.setdefault("ignore-write-errors", True)
    options.setdefault("disable-write-exception", True)
    options.setdefault("virtualenv", sys.prefix)
    options.setdefault("die-on-term", True)
    options.setdefault(
        'log-format',
        '%(addr) - %(user) [%(ltime)] "%(method) %(uri) %(proto)" '
        '%(status) %(size) "%(referer)" "%(uagent)"'
    )
    options.setdefault("%s-socket" % options["protocol"], "%s:%s" % (host, port))

    # We only need to set uid/gid when stepping down from root, but if
    # we are trying to run as root, then ignore it entirely.
    uid = os.getuid()
    if uid > 0:
        options.setdefault("uid", uid)
    gid = os.getgid()
    if gid > 0:
        options.setdefault("gid", gid)

    # Required arguments that should not be overridden
    options["master"] = True
    options["enable-threads"] = True
    options["lazy-apps"] = False  # Otherwise signals will be delivered to all workers
    options["single-interpreter"] = True
    
    # Enable or not stats server
    if settings.MINISENTRY_WEB_STATS_ENABLE:
        options["stats"] = \
            f"{settings.MINISENTRY_WEB_STATS_HOST}:{settings.MINISENTRY_WEB_STATS_PORT}"

    args = ("uwsgi", )

    # Serve static or not
    if settings.MINISENTRY_WEB_SERVE_STATIC:
        args += (
            "--static-map", f"/static/minisentry={settings.STATIC_DIR_MINISENTRY}",
            "--static-map", f"/static/admin={settings.STATIC_DIR_ADMIN}",
        )

    args += (f"--mule={settings.MULE_SCRIPT_PATH}", ) * settings.MINISENTRY_WEB_MULE_COUNT

    prepare_environment(options)
    os.execvp("uwsgi", args)


if __name__ == "__main__":
    main()
