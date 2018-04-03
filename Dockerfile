FROM python:3.6

RUN pip install jumeaux==0.46.0
WORKDIR tmp

ENTRYPOINT ["jumeaux", "run"]

