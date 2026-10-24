"""Where this server runs: a hosted platform, or a local checkout.

#2151 (Arch 10-23): lifted from ``web/api/routes/setup.py``'s ``_IN_DOCKER`` (#2089)
so surfaces outside the setup wizard decide "hosted" by the SAME deployment signal,
never by probing for a ``.git`` tree (a probe fails open: an image that happened to
contain a tree would read as "local" and serve the host's repository to users).
"""

import os


def is_hosted_deployment() -> bool:
    """True when the platform runs the services: Docker, Fly, or a declared
    production environment. Evaluated at call time."""
    return (
        os.path.exists("/.dockerenv")
        or bool(os.getenv("FLY_APP_NAME"))
        or (os.getenv("PIPER_ENVIRONMENT") or "").lower() == "production"
    )
