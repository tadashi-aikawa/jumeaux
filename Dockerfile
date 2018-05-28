FROM python:3.6

RUN pip install jumeaux==0.52.0
WORKDIR tmp

ENTRYPOINT ["jumeaux", "run"]

