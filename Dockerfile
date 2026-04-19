FROM python:3.7

RUN pip install jumeaux==6.1.2
WORKDIR tmp

ENTRYPOINT ["jumeaux", "run"]

