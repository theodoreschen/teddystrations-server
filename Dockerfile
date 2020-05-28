FROM python

RUN adduser --disabled-password game-manager &&\
    pip install --no-cache-dir flask flask-cors jsonschema redis pymongo uwsgi

USER game-manager
WORKDIR /home/game-manager

ADD game-server.ini main.py /home/game-manager/
ADD static/* static/
ADD teddystrations/* teddystrations/ 

# CMD ["tail", "-f", "/dev/null"]
CMD ["uwsgi", "--ini", "game-server.ini"]