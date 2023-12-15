# Farmtool

Farmtool to help the farmer to automate and handle Cowsheds.

## Installation

Use the package manager to install poetry() to install all the needed dependencies for the project.

```bash
pip install poetry
```

Use poetry package to install all dependencies for the project.

```bash
poetry install
```

## Execute code and tests

***This step should be only executed after the installation is finished.***

* connect to the project environment.

```bash
poetry shell
```
and then you can run the code or test it using the following commands.

###  Run code


```bash
uvicorn farmtool.main:app --reload
```
After running the code, a session will be opened in the following [URL](http://127.0.0.1:8000)

#### - Recomendation: 

Use [docs](http://127.0.0.1:8000/docs) to load the swaggerUI to test endpoints seamlessly.

###  Test code

```bash
pytest
```


## Try it out:

A publicly deployed and running version of the farmtool is available on azure.

check it out: [farmtool](https://farmtool-aca-app.blackglacier-5fa52807.germanywestcentral.azurecontainerapps.io/)
