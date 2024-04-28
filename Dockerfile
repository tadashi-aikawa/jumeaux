FROM python:3.12

RUN pip install jumeaux==4.1.0
WORKDIR tmp

ENTRYPOINT ["jumeaux", "run"]

