FROM python:3.6

RUN pip install jumeaux==1.1.0
WORKDIR tmp

ENTRYPOINT ["jumeaux", "run"]

