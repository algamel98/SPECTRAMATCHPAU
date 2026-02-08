"""WSGI entry point for SpectraMatch on JPaaS (Apache + mod_wsgi).

Key measures for stability with heavy OpenCV / NumPy processing:
  1. Force single-interpreter mode (avoid NumPy sub-interpreter bugs).
  2. Pre-import heavy C-extension libraries at module level so the first
     real request doesn't pay the full cold-start penalty.
  3. Keep the WSGI callable simple — just expose the Flask app.

The matching Apache configuration is in jpaas/httpd-wsgi.conf.
"""
import sys
import os

# ---------------------------------------------------------------------------
# 1. Project root on sys.path
# ---------------------------------------------------------------------------
_project_root = os.path.dirname(os.path.abspath(__file__))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

# ---------------------------------------------------------------------------
# 2. Pre-import heavy C-extension libraries at WSGI startup
# ---------------------------------------------------------------------------
# These imports take 5–15 s on cold start.  Doing them here (during daemon
# process initialisation) avoids the "Timeout when reading response headers"
# error that occurs when they happen inside the first request handler.
#
# Requires startup-timeout >= 60 in the WSGIDaemonProcess directive
# (see jpaas/httpd-wsgi.conf).
try:
    import numpy          # noqa: F401  — ~2 s
    import cv2            # noqa: F401  — ~5 s (loads numpy internally)
    import matplotlib     # noqa: F401  — ~3 s
    matplotlib.use("Agg")  # headless backend, must be set before pyplot
    import reportlab      # noqa: F401
except ImportError:
    pass  # graceful — the request handler will raise a clear error later

# ---------------------------------------------------------------------------
# 3. Import the Flask application
# ---------------------------------------------------------------------------
from app import app as application
