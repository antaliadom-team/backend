FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN python -m pip install --upgrade pip
RUN pip install -r req-prod.txt --no-cache-dir


CMD ["gunicorn", "antalia_project.wsgi:application", "--bind", "0:8000"]
CMD celery -A antalia_project worker -l info -B

LABEL author='antalya dom development team' version=1.0.0 app_name=antalia_project
