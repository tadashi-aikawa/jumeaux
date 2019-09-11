FROM python:3.7

RUN pip install jumeaux==2.2.0
WORKDIR tmp

ENTRYPOINT ["jumeaux", "run"]

