FROM python:3.6

RUN pip install jumeaux==2.1.0
WORKDIR tmp

ENTRYPOINT ["jumeaux", "run"]

