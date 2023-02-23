# Page Analyzer

[![Actions Status](https://github.com/zluuba/python-project-83/workflows/hexlet-check/badge.svg)](https://github.com/zluuba/python-project-83/actions) 
[![Project Check](https://github.com/zluuba/python-project-83/actions/workflows/project-check.yml/badge.svg)](https://github.com/zluuba/python-project-83/actions/workflows/project-check.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/bc7724c1971a7f520682/maintainability)](https://codeclimate.com/github/zluuba/python-project-83/maintainability)

[Link on Railway](https://python-project-83-production-6275.up.railway.app/)

Page Analyzer is a site that analyses specified pages for SEO-suitability (like [PageSpeed Insights](https://pagespeed.web.dev/)). <br>
**This is a study project**, so it will not be hosted, but you can use it by setting up a few things which will be described below.

### Requirements
Installed with one command.

- [postgresql](https://www.postgresql.org/download/)
- [python](https://www.python.org/), version 3.9 or higher
- [poetry](https://python-poetry.org/docs/#installation), version 1.0.0 or higher


### Installation

Clone this repo or download it with pip:
```ch
git clone https://github.com/zluuba/python-project-83.git
```
```ch
pip install --user git+https://github.com/zluuba/python-project-83.git
```

Use these commands to install package and dependencies:
```ch
cd python-project-83
make install
```

### Install Database (PostgreSQL)
Use these commands or download it from [the official website](https://www.postgresql.org/download/)
```ch
brew install postgresql             # MacOS
sudo apt install postgresql         # Ubuntu, Windows
```

Create database and set schema:
```ch
createdb mydb
psql mydb < database.sql
```

##### Now package ready to go.
Run WSGI HTTP server and follow the [link you will see](http://0.0.0.0:8000)
```ch
make start
```
Or run locally:
```ch
make dev
```


### How it works. Video

--video--
