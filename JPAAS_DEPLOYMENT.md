# SpectraMatch — JPaaS Deployment Guide

> **Goal:** Stable, correct operation of heavy OpenCV/NumPy image processing
> on Jelastic PaaS (JPaaS) with the NGINX → Apache → mod_wsgi stack.
>
> **Traffic assumption:** ≤ 5 users per day. Stability over concurrency.

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Step 1 — Apache mod_wsgi Configuration](#2-step-1--apache-modwsgi-configuration)
3. [Step 2 — NGINX Reverse Proxy Timeouts](#3-step-2--nginx-reverse-proxy-timeouts)
4. [Step 3 — Deploy Application Code](#4-step-3--deploy-application-code)
5. [Step 4 — Environment Variables](#5-step-4--environment-variables)
6. [Step 5 — Verify & Test](#6-step-5--verify--test)
7. [Troubleshooting](#7-troubleshooting)
8. [Configuration Reference](#8-configuration-reference)

---

## 1. Architecture Overview

```
Browser
  │
  ▼
NGINX (JPaaS load-balancer node)
  │  proxy_read_timeout 660s
  ▼
Apache + mod_wsgi (JPaaS Python 3.11 node)
  │  WSGIDaemonProcess: 1 process, 1 thread
  │  WSGIApplicationGroup %{GLOBAL}
  │  response-timeout=600
  ▼
wsgi.py  →  app.py  →  modules/  (OpenCV, NumPy, scikit-image, …)
```

### Key design decisions

| Decision | Rationale |
|----------|-----------|
| **1 process, 1 thread** | Serialises requests — only ONE image analysis runs at a time, preventing memory exhaustion on limited cloudlets. |
| **`%{GLOBAL}` interpreter** | Eliminates the NumPy/OpenCV sub-interpreter crash (`"NumPy was imported from a Python sub-interpreter"`). |
| **600 s timeouts (both layers)** | Allows up to 10 minutes for very large images to be processed end-to-end. |
| **No background threads** | mod_wsgi can recycle daemon processes; cleanup is request-driven instead. |
| **Image dimension cap** | Prevents OOM on 1–2 GB cloudlets by downscaling images whose longest edge exceeds `MAX_IMAGE_DIMENSION`. |
| **Pre-import at WSGI startup** | Heavy C-extensions (cv2, numpy, matplotlib) are imported in `wsgi.py` during daemon init (covered by `startup-timeout=60`), so the first real request isn't penalised. |

---

## 2. Step 1 — Apache mod_wsgi Configuration

### Where to edit

1. Open the **Jelastic dashboard** → your **Python environment node** → **Config** (wrench icon).
2. Navigate to `/etc/httpd/conf.d/` or `/etc/httpd/conf/httpd.conf` — find the existing `WSGIDaemonProcess` / `WSGIScriptAlias` block.

### What to set

Replace the existing WSGI block with the contents of **`jpaas/httpd-wsgi.conf`** (included in this repository). The critical directives are:

```apache
# Force global interpreter — no sub-interpreters
WSGIApplicationGroup %{GLOBAL}

# Single process, single thread — serialise all requests
WSGIDaemonProcess spectramatch \
    processes=1 \
    threads=1 \
    python-home=/opt/jelastic-python311 \
    python-path=/var/www/webroot/ROOT \
    request-timeout=600 \
    response-timeout=600 \
    socket-timeout=600 \
    connect-timeout=30 \
    queue-timeout=600 \
    startup-timeout=60 \
    deadlock-timeout=660 \
    inactivity-timeout=0 \
    shutdown-timeout=10 \
    graceful-timeout=600 \
    maximum-requests=200 \
    display-name=spectramatch

WSGIProcessGroup spectramatch
WSGIScriptAlias / /var/www/webroot/ROOT/wsgi.py

<Directory /var/www/webroot/ROOT>
    Require all granted
</Directory>

# Apache core timeouts (must be >= mod_wsgi timeouts)
Timeout 600
ProxyTimeout 600
```

> **Note:** Adjust `python-home` to match your JPaaS Python installation path.
> Common values: `/opt/jelastic-python311`, `/opt/jelastic-python39`.
> You can find it by running `which python3` in the SSH terminal.

### Restart Apache

After saving, restart Apache from the Jelastic dashboard (or via SSH: `sudo systemctl restart httpd`).

---

## 3. Step 2 — NGINX Reverse Proxy Timeouts

### Where to edit

1. Open the **Jelastic dashboard** → your **NGINX load-balancer node** → **Config**.
2. Navigate to `/etc/nginx/nginx.conf` (or the relevant `server { }` / `location / { }` block).

### What to set

Add or modify these directives inside the `location / { }` block (see `jpaas/nginx-proxy.conf` for the full reference):

```nginx
proxy_read_timeout    660s;
proxy_connect_timeout 30s;
proxy_send_timeout    600s;
client_max_body_size  110m;
proxy_buffering       off;
```

### Why NGINX matters

If NGINX times out before Apache finishes, the user gets a **504 Gateway Timeout** even though Apache is still processing. NGINX timeouts must be **≥** Apache timeouts.

### Reload NGINX

After saving: `sudo nginx -s reload` (or restart from the dashboard).

---

## 4. Step 3 — Deploy Application Code

Upload the project to `/var/www/webroot/ROOT/` on the JPaaS Python node. The key files that changed:

| File | What changed |
|------|-------------|
| `wsgi.py` | Pre-imports heavy C-extensions at daemon startup; documents single-interpreter requirement. |
| `app.py` | Removed background cleanup thread → request-driven cleanup. Added `_cap_image_dimension()` for memory safety. Added `gc.collect()` after each analysis. |
| `.htaccess` | Request-read timeouts, deny access to `.py` files, compression. |
| `jpaas/httpd-wsgi.conf` | Reference Apache configuration (copy into server config). |
| `jpaas/nginx-proxy.conf` | Reference NGINX configuration (copy into NGINX config). |

---

## 5. Step 4 — Environment Variables

Set these in the Jelastic dashboard (**Environment → Variables**) or in the Apache config:

| Variable | Default | Description |
|----------|---------|-------------|
| `SPECTRAMATCH_MAX_DIM` | `6000` | Maximum image dimension (longest edge in px). Images larger than this are downscaled before analysis. Set to `0` to disable. |

### Choosing `SPECTRAMATCH_MAX_DIM`

| Cloudlet RAM | Recommended `MAX_DIM` | Peak memory estimate (2 images) |
|--------------|----------------------|--------------------------------|
| 1 GB | `4000` | ~600 MB |
| 2 GB | `6000` | ~1.2 GB |
| 4 GB | `8000` | ~2.0 GB |
| 8 GB+ | `0` (disabled) | Unbounded |

The estimate accounts for multiple intermediate copies (BGR, float64, LAB, gradient maps) that OpenCV and NumPy create during the analysis pipeline.

---

## 6. Step 5 — Verify & Test

### 1. Check Apache started correctly

SSH into the Python node and inspect the error log:

```bash
tail -50 /var/log/httpd/error_log
```

You should see:

```
AH00489: Apache/2.4.x … mod_wsgi/4.9.x Python/3.11 configured -- resuming normal operations
```

You should **NOT** see:

- ❌ `AH00161: server reached MaxRequestWorkers` — means config not applied
- ❌ `NumPy was imported from a Python sub-interpreter` — means `WSGIApplicationGroup %{GLOBAL}` is missing
- ❌ `AH10159: server is within MinSpareThreads of MaxRequestWorkers` — same as above

### 2. Test with a small image first

Upload a small image (e.g., 800×600 px) from the Ready-to-Test set and confirm the analysis completes without timeout.

### 3. Test with a large image

Upload a larger image (e.g., 4000×3000 px) and confirm:

- The analysis completes (may take 1–3 minutes).
- No timeout errors in `/var/log/httpd/error_log`.
- No 504 errors from NGINX.

### 4. Monitor memory

```bash
watch -n 2 'free -m && echo "---" && ps aux --sort=-%mem | head -5'
```

During analysis, the `spectramatch` process will spike in memory usage. It should drop back down after `gc.collect()` runs.

---

## 7. Troubleshooting

### "Timeout when reading response headers from daemon process"

**Cause:** `response-timeout` in `WSGIDaemonProcess` is too low (default 60 s).

**Fix:** Ensure `response-timeout=600` is set. Also check that NGINX `proxy_read_timeout` is at least 660 s.

### "Truncated or oversized response headers received from daemon process"

**Cause:** NumPy/OpenCV sub-interpreter memory corruption, or the daemon crashed mid-response.

**Fix:** Ensure `WSGIApplicationGroup %{GLOBAL}` is set. If the issue persists, the image may be too large — lower `SPECTRAMATCH_MAX_DIM`.

### "server reached MaxRequestWorkers"

**Cause:** All workers are blocked by long-running requests.

**Fix:** With `processes=1 threads=1`, this means a request is already being processed. The second request will wait in the queue (up to `queue-timeout=600` seconds). This is expected behaviour with serialised processing.

If you see this immediately after restart (with no requests in flight), the MPM config may be overriding the WSGI config. Check that `MaxRequestWorkers` in the MPM section is at least `2` (1 for the daemon + 1 for Apache itself).

### "client denied by server configuration: .well-known"

**Cause:** SSL certificate renewal probe from Jelastic infrastructure.

**Fix:** The `.htaccess` file includes a rewrite rule to allow `.well-known/` access. If using server config instead, add:

```apache
<Location "/.well-known">
    Require all granted
</Location>
```

### Process killed by OOM

**Cause:** Image too large for available cloudlet RAM.

**Fix:** Lower `SPECTRAMATCH_MAX_DIM` (e.g., `4000` for 1 GB cloudlets). Monitor with `dmesg | grep -i oom`.

---

## 8. Configuration Reference

### Timeout chain (all must be aligned)

```
NGINX proxy_read_timeout (660s)
  ≥ Apache Timeout (600s)
    ≥ mod_wsgi response-timeout (600s)
      ≥ mod_wsgi request-timeout (600s)
        ≥ actual processing time (~30–300s depending on image size)
```

### Files included in this repository

| File | Purpose |
|------|---------|
| `jpaas/httpd-wsgi.conf` | Complete Apache mod_wsgi config — copy into `/etc/httpd/conf.d/` |
| `jpaas/nginx-proxy.conf` | NGINX proxy timeout config — merge into NGINX server block |
| `.htaccess` | Per-directory Apache directives (request timeouts, security, compression) |
| `wsgi.py` | WSGI entry point with pre-imports and documentation |
| `app.py` | Application with request-driven cleanup, image capping, memory management |

### mod_wsgi directive quick reference

| Directive | Value | Purpose |
|-----------|-------|---------|
| `processes` | `1` | Single worker process |
| `threads` | `1` | Single thread per process |
| `response-timeout` | `600` | Max seconds to wait for response headers |
| `request-timeout` | `600` | Max seconds for complete request cycle |
| `startup-timeout` | `60` | Max seconds for daemon to initialise (heavy imports) |
| `deadlock-timeout` | `660` | Kill stuck daemon (> response-timeout) |
| `inactivity-timeout` | `0` | Never recycle idle daemon (avoids cold restarts) |
| `maximum-requests` | `200` | Recycle after N requests (memory leak recovery) |
| `WSGIApplicationGroup` | `%{GLOBAL}` | Single interpreter (NumPy/OpenCV safety) |
