FROM python:3.6

RUN pip install jumeaux==0.56.0
WORKDIR tmp

ENTRYPOINT ["jumeaux", "run"]

