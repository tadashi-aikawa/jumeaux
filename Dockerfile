FROM python:3.6

RUN pip install jumeaux==0.28.0
WORKDIR tmp

ENTRYPOINT ["jumeaux"]
