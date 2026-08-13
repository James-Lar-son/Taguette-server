"""
Taguette server configuration.

Everything that varies between deployments is read from environment
variables, which are declared in render.yaml or set in the Render
dashboard. That means this file contains no passwords or keys and is
safe to keep in version control.

You will rarely need to edit this. To change behaviour, change the
environment variable in Render instead.
"""

import os


def _flag(name, default=False):
    """Read a true/false environment variable."""
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in ('1', 'true', 'yes', 'on')


# ---------------------------------------------------------------
#  Identity
# ---------------------------------------------------------------

# Shown in the browser tab and the page header.
NAME = os.environ.get('TAGUETTE_NAME', 'Qualitative Coding')

# Render automatically provides RENDER_EXTERNAL_HOSTNAME, so the public
# address is picked up on its own - no need to know the URL in advance.
# Taguette refuses to start on an empty DOMAIN, hence the final fallback.
DOMAIN = (
    os.environ.get('TAGUETTE_DOMAIN')
    or os.environ.get('RENDER_EXTERNAL_HOSTNAME')
    or 'localhost'
)


# ---------------------------------------------------------------
#  Networking
# ---------------------------------------------------------------

BIND_ADDRESS = '0.0.0.0'

# Render supplies PORT; the fallback is Taguette's own default so this
# config also works if you ever run it somewhere else.
PORT = int(os.environ.get('PORT', '7465'))

BASE_PATH = '/'

# Render terminates HTTPS in front of the app, so trust the
# X-Forwarded-For header it sets.
X_HEADERS = True


# ---------------------------------------------------------------
#  Secret key
# ---------------------------------------------------------------
# Signs your login cookie. render.yaml generates one automatically on
# first deploy and keeps it. Rotating it logs you out; it does not
# affect stored data.

SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    raise SystemExit(
        "SECRET_KEY is not set. In the Render dashboard open this service, "
        "go to Environment, and add a SECRET_KEY variable with any long "
        "random string as its value."
    )


# ---------------------------------------------------------------
#  Storage
# ---------------------------------------------------------------
# /data is the Render persistent disk, so documents, highlights and
# codebooks survive restarts, redeploys and instance changes.
# Note the four slashes - that is how SQLAlchemy spells an absolute path.

DATABASE = os.environ.get('DATABASE_URL', 'sqlite:////data/taguette.sqlite3')


# ---------------------------------------------------------------
#  Accounts
# ---------------------------------------------------------------

# Off by default, so nobody who finds the URL can create an account.
# Set REGISTRATION_ENABLED=true in Render to open it up temporarily
# when you want to add a collaborator.
REGISTRATION_ENABLED = _flag('REGISTRATION_ENABLED', False)

# Allows importing a project exported from any other Taguette,
# including the desktop app.
SQLITE3_IMPORT_ENABLED = True


# ---------------------------------------------------------------
#  Interface
# ---------------------------------------------------------------

TOS_FILE = None          # no terms-of-service page on a private instance
COOKIES_PROMPT = False   # no cookie banner
DEFAULT_LANGUAGE = os.environ.get('TAGUETTE_LANGUAGE', 'en_US')


# ---------------------------------------------------------------
#  Email
# ---------------------------------------------------------------
# No mail server is attached, so "forgot password" will not work.
# Keep your password in a password manager.

EMAIL = os.environ.get('TAGUETTE_EMAIL', 'Taguette <taguette@example.com>')
MAIL_SERVER = {
    'ssl': False,
    'host': 'localhost',
    'port': 25,
}


# ---------------------------------------------------------------
#  Document conversion timeouts, in seconds
# ---------------------------------------------------------------
# Raised from Taguette's 3-minute default so large PDFs and Word files
# have room to finish importing.

_convert_timeout = int(os.environ.get('CONVERT_TIMEOUT', '480'))
CONVERT_TO_HTML_TIMEOUT = _convert_timeout
CONVERT_FROM_HTML_TIMEOUT = _convert_timeout
