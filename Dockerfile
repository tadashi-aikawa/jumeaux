FROM python:3.6

RUN pip install jumeaux
WORKDIR tmp

ENTRYPOINT ["jumeaux"]
