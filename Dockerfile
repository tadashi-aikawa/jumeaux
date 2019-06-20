FROM python:3.6

RUN pip install jumeaux==1.2.1
WORKDIR tmp

ENTRYPOINT ["jumeaux", "run"]

