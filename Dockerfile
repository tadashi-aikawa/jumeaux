FROM python:3.6

RUN pip install jumeaux==3.0.1
WORKDIR tmp

ENTRYPOINT ["jumeaux", "run"]

