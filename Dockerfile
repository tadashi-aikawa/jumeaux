FROM python:3.6

RUN pip install jumeaux==2.5.0
WORKDIR tmp

ENTRYPOINT ["jumeaux", "run"]

