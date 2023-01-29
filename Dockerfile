FROM python:3.8-slim
WORKDIR /app
COPY . .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir


CMD ["gunicorn", "antalia_project.wsgi:application", "--bind", "0:8000"]

LABEL author='antalya dom development team' version=1.0.0 app_name=antalia_project