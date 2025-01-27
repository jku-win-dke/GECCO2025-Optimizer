# HARMONIC-Optimizer-2


## Introduction
This project contains the API for the GECCO2025-Optimizer. <br>


## For local development
### Set up virtual environment and install requirements
```bash
pip install -r requirements.txt
```

### Activate the virtual environment
```bash
source .venv/bin/activate
```

### Run the live server
```bash
uvicorn app.main:app --reload
```


## Docker
### Build the image
```bash
docker build -t <IMAGE-NAME> .
```

### Run the container
```bash
docker run -d --name <CONTAINER-NAME> -p 8080:8000 <IMAGE-NAME>
```

Uvicorn server for the optimizer will be running on **http://localhost:8080**.
