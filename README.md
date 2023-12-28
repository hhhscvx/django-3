docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management
celery -A myshop worker -l info
stripe login
stripe listen --forward-to localhost:8000/payment/webhook/
python manage.py runserver
