FROM python:3.8.5
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
WORKDIR /src/

ADD ./requirement.txt /src/
#RUN pip install -r /src/requirement.txt -i https://mirrors.aliyun.com/pypi/simple/
#RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ uwsgi celery
#RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ vine==1.3.0 mysqlclient

RUN pip install -r /src/requirement.txt
ADD . /src/
RUN python manage.py makemigrations
RUN python manage.py migrate
#CMD gunicorn -w 2 -k gevent -b 0.0.0.0:8080 wallet.wsgi:application
RUN python manage.py runserver
