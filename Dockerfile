FROM python:3.7

RUN pip install jumeaux==4.0.1
WORKDIR tmp

ENTRYPOINT ["jumeaux", "run"]

