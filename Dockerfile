FROM python:3.7

RUN pip install jumeaux==3.1.1
WORKDIR tmp

ENTRYPOINT ["jumeaux", "run"]

