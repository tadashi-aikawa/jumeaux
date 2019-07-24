FROM python:3.6

RUN pip install jumeaux==1.2.2
WORKDIR tmp

ENTRYPOINT ["jumeaux", "run"]

