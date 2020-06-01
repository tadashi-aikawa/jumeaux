FROM python:3.6

RUN pip install jumeaux==2.4.1
WORKDIR tmp

ENTRYPOINT ["jumeaux", "run"]

