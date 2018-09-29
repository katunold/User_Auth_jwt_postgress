web: gunicorn --workers=1 run:app

release: psql -U postgres -f heroku_db.sql