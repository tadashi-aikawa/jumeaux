FROM python:3.7

RUN pip install jumeaux==4.1.0
WORKDIR tmp

ENTRYPOINT ["jumeaux", "run"]

