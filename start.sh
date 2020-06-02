. venv/bin/activate
redis-server &
celery -A src.resources.Tasks.celery worker --loglevel=DEBUG &
python3 run.py