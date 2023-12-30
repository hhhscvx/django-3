1. `docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management`
2. `celery -A myshop worker -l info`
3. `docker run -it --rm --name redis -p 6379:6379 redis`
4. `stripe login`
5. `stripe listen --forward-to localhost:8000/payment/webhook/`
6. `python manage.py runserver`
