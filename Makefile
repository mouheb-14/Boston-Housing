# Makefile pour orchestrer le pipeline MLOps du projet Boston Housing

.PHONY: setup train register serve test pipeline

# Utilisation du Python du venv pour assurer l'isolation
PYTHON = .\backend\venv_64\Scripts\python.exe
PIP = .\backend\venv_64\Scripts\pip.exe
UVICORN = .\backend\venv_64\Scripts\uvicorn.exe

setup:
	$(PIP) install -r backend/requirements.txt
	$(PIP) install evidently scipy

train:
	$(PYTHON) backend/train.py

register:
	$(PYTHON) backend/register_best_model.py

serve:
	cd backend && ..\venv_64\Scripts\uvicorn.exe app:app --host 127.0.0.1 --port 8000 --reload

test:
	$(PYTHON) backend/test_api.py

pipeline: train register test
	@echo [MLOps] Pipeline complet execute avec succes !
