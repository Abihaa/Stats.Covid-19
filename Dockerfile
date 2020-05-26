FROM python:slim-buster
COPY . /app
WORKDIR /app
#RUN apt-get update && apt-get upgrade
#RUN apt-get install default-libmysqlclient-dev python-dev
RUN pip3 install -r requirements.txt 
EXPOSE 5001 
ENTRYPOINT [ "python" ] 
CMD [ "init.py" ] 

