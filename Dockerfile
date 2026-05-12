FROM python:3.7

RUN pip install jumeaux==6.1.4
WORKDIR tmp

ENTRYPOINT ["jumeaux", "run"]

