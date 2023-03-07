# Page Analyzer

[![Actions Status](https://github.com/zluuba/python-project-83/workflows/hexlet-check/badge.svg)](https://github.com/zluuba/python-project-83/actions) 
[![Project Check](https://github.com/zluuba/python-project-83/actions/workflows/project-check.yml/badge.svg)](https://github.com/zluuba/python-project-83/actions/workflows/project-check.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/bc7724c1971a7f520682/maintainability)](https://codeclimate.com/github/zluuba/python-project-83/maintainability)

Page Analyzer is a site that analyses specified pages for SEO-suitability (like [PageSpeed Insights](https://pagespeed.web.dev/)). <br>
**This is a study project**, so it's not hosted, but you can use it by setting up a few things which will be described below.

### Requirements

- [python](https://www.python.org/), version 3.9 or higher
- [poetry](https://python-poetry.org/docs/#installation), version 1.0.0 or higher


### Installation

Clone this repo or download it with pip:
```ch
git clone https://github.com/zluuba/page-analyzer.git
```
```ch
pip install --user git+https://github.com/zluuba/page-analyzer.git
```

Install dependencies:
```ch
cd page-analyzer                    # don't forget cd to downloaded package dir
make install
```

### Install Database (PostgreSQL)
Use these commands or download DB from [official website](https://www.postgresql.org/download/):
```ch
brew install postgresql             # MacOS
sudo apt install postgresql         # Linux, Windows
```

Create database and set schema:
```ch
createdb mydb
psql mydb < database.sql
```

### Create .env file
```ch
nano .env
```
And write down the following environment variables (paste your data):
```ch
DATABASE_URL = 'postgres://<username>:<password>@<localhost>:<port>/mydb'
SECRET_KEY = 'SecretKey'
```

### Now package ready to go
Run WSGI HTTP server and follow the [link you will see](http://0.0.0.0:8000):
```ch
make start
```
Or run locally with flask:
```ch
make dev
```


### Demos

#### Package setup

https://user-images.githubusercontent.com/87614163/220867550-2d8e1f02-fc26-41b0-9406-3787a6632780.mp4


#### Usage

https://user-images.githubusercontent.com/87614163/220869914-21c3617d-ef11-40eb-8cb3-842d5c057114.mp4

