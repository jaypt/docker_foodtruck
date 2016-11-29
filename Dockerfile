FROM python:2-onbuild

MAINTAINER jaypt

EXPOSE 5001

CMD ["python2.7", "./start_flask.py"]

