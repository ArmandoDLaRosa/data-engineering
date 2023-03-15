# Data Engineering - Python

## [Backend Module](https://github.com/ArmandoDLaRosa/data-engineering/tree/main/backend)

This module creates a backend server in 

### Setup

From root (backend/) in cmd, run:

```sh
$ pipenv install
```

```sh
$ pipenv shell
```

#### How to add new libraries?

```
$ pipenv install <library>
```

### Start the Data API

if you have run  `pipenv shell` and `export FLASK_APP=api`, then from (backend/), run:

```sh
$ flask run
```

### Initialize the tables in the database

Remember to change in  api/____init____.py  the database string, then run:

```sh
$ python3.8 database.py
```


## [Data Science Module](https://github.com/ArmandoDLaRosa/data-engineering/tree/main/data_scienc)

### Setup

From root (data_science/) in cmd, run:

```sh
$ pipenv install
```

```sh
$ pipenv shell
```

#### How to add new libraries?

```
$ pipenv install <library>
```

## [SQL Module](https://github.com/ArmandoDLaRosa/data-engineering/tree/main/sql)

### Setup

From root (sql/) in cmd, run:

```sh
$ pipenv install
```

```sh
$ pipenv shell
```

#### How to add new libraries?

```
$ pipenv install <library>
```
