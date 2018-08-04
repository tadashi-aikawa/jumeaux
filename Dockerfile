FROM python:3.6

RUN pip install jumeaux==0.57.1
WORKDIR tmp

ENTRYPOINT ["jumeaux", "run"]

