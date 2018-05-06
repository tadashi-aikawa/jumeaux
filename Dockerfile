FROM python:3.6

RUN pip install jumeaux==0.49.0
WORKDIR tmp

ENTRYPOINT ["jumeaux", "run"]

