FROM python:3.6

RUN pip install jumeaux==0.27.3
WORKDIR tmp

ENTRYPOINT ["jumeaux"]
