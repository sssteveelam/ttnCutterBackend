
## Installing dependencies locally

If you are running the project outside of Docker you need to install the Python
dependencies listed in `requirements.txt`.

```bash
# (optional) create and activate a virtual environment first
python -m venv .venv
source .venv/bin/activate

# upgrade pip so binary wheels such as `curl_cffi` install cleanly
python -m pip install --upgrade pip

# install the packages declared in requirements.txt
python -m pip install -r requirements.txt
```

After installing the dependencies you can start the API with `uvicorn
app.main:app --reload` for local development.

## Deploying to Render

1. Create a new **Web Service** on Render and connect this repository.
2. Set the **Build Command** to `pip install -r requirements.txt`.
3. Set the **Start Command** to `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
4. Add a `DATABASE_URL` environment variable. For SQLite you can leave it empty (the
   application falls back to `sqlite:///./logs.db`), but when using a Render PostgreSQL
   instance paste the connection string provided by Render.
5. (Optional) Add a **Persistent Disk** if you plan on keeping the generated
   `temp_videos` or SQLite database file between deployments.

The application automatically creates the `temp_videos` directory on startup so the
static files route works in the Render container filesystem.

### Throttling yt-dlp to avoid rate limits

Some providers (such as YouTube) can temporarily block repeated downloads from the
same IP address. Configure the following optional environment variables on Render
to slow down requests when you notice HTTP 429 or "Too Many Requests" errors:

| Variable | Default | Description |
| --- | --- | --- |
| `YT_DLP_SLEEP_INTERVAL` | `0` | Minimum seconds to sleep between yt-dlp HTTP requests. |
| `YT_DLP_MAX_SLEEP_INTERVAL` | `YT_DLP_SLEEP_INTERVAL` | Maximum seconds to sleep (enables random jitter when greater than the minimum). |
| `YT_DLP_LIMIT_RATE` | _unset_ | Limit download bandwidth (e.g. `1M` for 1 MiB/s). |
| `YT_DLP_MAX_ATTEMPTS` | `3` | Maximum attempts for yt-dlp commands when rate limits are detected. |
| `YT_DLP_BACKOFF_INITIAL` | `2` | Initial backoff delay in seconds before retrying. |
| `YT_DLP_BACKOFF_MULTIPLIER` | `2` | Multiplier applied to the delay after each retry. |
| `YT_DLP_BACKOFF_JITTER` | `1` | Random jitter (+/- seconds) added to each delay to avoid bursts. |
| `YT_DLP_IMPERSONATE` | _unset_ | When set, adds `--impersonate <value>` to every yt-dlp command (e.g. `chrome:windows-10`) so providers see traffic as a browser. |

Set only the variables you need—leaving them unset keeps the existing fast
behaviour for development.

> **Note:** yt-dlp's impersonation feature relies on the optional
> [curl_cffi](https://github.com/yifeikong/curl_cffi) dependency. This project
> ships with curl_cffi so setting `YT_DLP_IMPERSONATE` immediately enables the
> more browser-like TLS fingerprint.

### Overriding impersonation per request

Front-end clients can override the impersonation setting for a single download by
including `impersonate_client` in the POST body sent to `/api/download`. When the
field is present (for example the UI defaults to `"chrome"`), the backend adds
`--impersonate <value>` to the yt-dlp commands for that request even if the
`YT_DLP_IMPERSONATE` environment variable is not configured. If neither the
request body nor the environment variable specifies an impersonation target, the
commands run without the flag just like before.
