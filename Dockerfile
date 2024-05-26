FROM python:3.12

RUN pip install jumeaux==5.0.1
WORKDIR tmp

ENTRYPOINT ["jumeaux"]

