# Sticky Notes

A small Django application for creating and managing sticky notes. It uses
Django templates and custom CSS, with create, read, update, and delete flows.

- **Repository:** <https://github.com/joshakrm/sticky-notes-django>
- **Documentation:** open [`docs/_build/html/index.html`](docs/_build/html/index.html)
  in a browser after cloning (generated with Sphinx).

## Project layout

```text
sticky-notes-django/
├── Dockerfile            # Container image definition
├── requirements.txt      # Python dependencies
├── .env.example          # Template for your local settings/secrets
├── docs/                 # Sphinx sources and generated HTML (docs/_build/html)
├── diagrams/             # Use case, sequence and class diagrams
└── sticky_notes/         # Django project (contains manage.py)
    ├── notes/            # The notes app: models, views, forms, templates, tests
    └── sticky_notes/     # Project settings and URL configuration
```

## Requirements

- Python 3.12 or newer (for running with venv), **or**
- Docker (for running in a container)

## Get the code

```bash
git clone https://github.com/joshakrm/sticky-notes-django.git
cd sticky-notes-django
```

## Secrets and configuration

No secrets are stored in this repository. The application reads its
configuration from environment variables:

| Variable | Purpose | Default |
| --- | --- | --- |
| `DJANGO_SECRET_KEY` | Django's secret key used for cryptographic signing | An insecure development-only key |
| `DJANGO_DEBUG` | `True` for development, `False` for production | `True` |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated host names the site is served from | `localhost,127.0.0.1` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Comma-separated origins trusted for form posts behind an HTTPS proxy | *(empty)* |

The app runs locally without setting anything, but you should use your own
secret key for anything other than a quick local test:

1. Generate a key (after installing the requirements, see below):

   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

2. Copy `.env.example` to `.env` and paste the key in as the value of
   `DJANGO_SECRET_KEY`. The `.env` file is listed in `.gitignore`, so it is
   never committed.

3. Make the values available to the app:
   - **Docker:** pass the file with `--env-file .env` (shown below).
   - **venv:** set the variable in your terminal before starting the server,
     for example `export DJANGO_SECRET_KEY="your-key"` (macOS/Linux) or
     `$env:DJANGO_SECRET_KEY = "your-key"` (Windows PowerShell).

## Run with venv

Run these commands from the repository root.

**Windows (PowerShell)**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python sticky_notes\manage.py migrate
python sticky_notes\manage.py runserver
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python sticky_notes/manage.py migrate
python sticky_notes/manage.py runserver
```

Open <http://127.0.0.1:8000/>. The root URL redirects to the notes list at
`/notes/`.

To use the admin site at `/admin/`, first create an account with
`python sticky_notes/manage.py createsuperuser`.

## Run with Docker

Build the image from the repository root:

```bash
docker build -t sticky-notes .
```

Start a container:

```bash
docker run --rm -p 8000:8000 sticky-notes
```

Or, to use your own settings from a `.env` file:

```bash
docker run --rm -p 8000:8000 --env-file .env sticky-notes
```

Open <http://localhost:8000/>. The container applies the database migrations
automatically and then starts the server on port 8000. Press `Ctrl+C` to stop
it. Notes are stored inside the container, so they are removed when the
container is deleted.

### Docker playground

On [Play with Docker](https://labs.play-with-docker.com/), clone the
repository, build the image as above, then start it with the playground's
address as a trusted origin so that forms can be submitted over HTTPS:

```bash
docker run --rm -p 8000:8000 -e DJANGO_CSRF_TRUSTED_ORIGINS=https://*.play-with-docker.com sticky-notes
```

Then click the **8000** port badge at the top of the page.

## Tests

Run the notes app test suite from the repository root:

```bash
python sticky_notes/manage.py test notes
```

The suite covers note model behaviour, list/detail/create/update/delete
views, form validation, URL patterns, and the home redirect.

## Documentation

The code is documented with docstrings and published with Sphinx. The
generated pages are committed in `docs/_build/html`. To rebuild them after
changing the code (with the virtual environment active):

```bash
cd docs
make html
```

On Windows use `.\make.bat html` instead.

## Design diagrams

- [Use case diagram](diagrams/Use%20Case%20Diagram.png)
- [Sequence diagram](diagrams/Sequence%20Diagram.png)
- [Class diagram](diagrams/Class%20Diagram.png)
