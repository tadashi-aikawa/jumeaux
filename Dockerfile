FROM python:3.6

RUN pip install jumeaux==0.24.2
WORKDIR tmp

ENTRYPOINT ["jumeaux"]
