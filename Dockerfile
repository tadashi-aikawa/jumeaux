FROM python:3.7

RUN pip install jumeaux==6.0.0
WORKDIR tmp

ENTRYPOINT ["jumeaux", "run"]

