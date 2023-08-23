set -e

# ls /usr/src/app/
echo "Reset DB!!"

flask db drop
flask db create
flask db seed

echo "Run wsgi!!"

gunicorn --bind 0.0.0.0:${APP_PORT} wsgi:app