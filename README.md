[![Actions Status](https://github.com/zluuba/python-project-83/workflows/hexlet-check/badge.svg)](https://github.com/zluuba/python-project-83/actions) 
[![Project Check](https://github.com/zluuba/python-project-83/actions/workflows/project-check.yml/badge.svg)](https://github.com/zluuba/python-project-83/actions/workflows/project-check.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/bc7724c1971a7f520682/maintainability)](https://codeclimate.com/github/zluuba/python-project-83/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/bc7724c1971a7f520682/test_coverage)](https://codeclimate.com/github/zluuba/python-project-83/test_coverage)

https://python-project-83-production-6275.up.railway.app/

## Page Analyzer
Page Analyzer is a site that analyses specified pages for SEO-suitability (like [PageSpeed Insights](https://pagespeed.web.dev/)). <br>
**This is a training project**, so it will not be hosted, but you can use it by setting up a few things which will be described below.

### Requirements
- [python](https://www.python.org/), version 3.9 or higher
- [psycopg2](https://pypi.org/project/psycopg2/), version 2.9.5 or higher
- [gunicorn](https://pypi.org/project/gunicorn/), version 20.1.0 or higher
- [requests](https://pypi.org/project/requests/), version 2.28.2 or higher
- [flask](https://flask.palletsprojects.com/en/2.2.x/), version 2.2.3 or higher
- [jinja2](https://jinja.palletsprojects.com/en/3.1.x/), version 3.1.2 or higher
- [python-dotenv](https://pypi.org/project/python-dotenv/), version 0.21.1 or higher
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/), version 4.11.2 or higher
- [postgresql](https://www.postgresql.org/download/) - database

You can install all these libs with a single command.


### Installation

Clone this repo or download it with pip:
```ch
git clone https://github.com/zluuba/difference-generator.git
```
```ch
pip install --user git+https://github.com/zluuba/difference-generator.git
```

Use these command to install package:
```ch
make install
```

### Install Database (PostgreSQL)
For MacOS:
```ch
brew install postgresql
```
For Ubuntu, Windows:
```ch
sudo apt install postgresql
```

Create database:
```ch
createdb <name>
```

Set tables from package schema (database.sql):
```ch
psql <name> < database.sql
```


### How it works. Video

##### Step 1. Install package and set it up

--video--

##### Step 2. Go to the browser and use it

--video--
