FROM python:3.7

RUN pip install jumeaux==5.0.4
WORKDIR tmp

ENTRYPOINT ["jumeaux", "run"]

