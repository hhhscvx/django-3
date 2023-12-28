1. `docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management`
2. `celery -A myshop worker -l info`
3. `stripe login`
3. `stripe listen --forward-to localhost:8000/payment/webhook/`
4. `python manage.py runserver`
