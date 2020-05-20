FROM python

ADD uwsgi.ini requirements.txt /

RUN pip install uwsgi && pip install -r requirements.txt
