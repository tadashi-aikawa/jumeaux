FROM python:3.6

RUN pip install jumeaux==0.36.2
WORKDIR tmp

ENTRYPOINT ["jumeaux"]

