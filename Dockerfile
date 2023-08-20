
FROM python:3.7
ENV PYTHONUNBUFFERED 1
ENV DEBUG False
COPY requirements.txt /code/requirements.txt
WORKDIR /code
RUN pip install -r requirements.txt
RUN apt update
RUN apt install gettext -y
ADD . .
# RUN python manage.py collectstatic --noinput
CMD [ "gunicorn", "--bind", "0.0.0.0", "-p", "8000",  "homemart.wsgi" ]