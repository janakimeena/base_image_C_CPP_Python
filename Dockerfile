FROM ubuntu:latest
MAINTAINER Kumar Shubham "kumar.shubham2015@vit.ac.in"

RUN apt-get update -y
RUN apt-get install -y python3 python3-pip python3-dev build-essential

RUN ["adduser",  "--home",  "/usr/src/app", "--system", "sandboxuser"]
RUN ["chown", "-R", "sandboxuser", "/usr/src/app"]
RUN ["chmod", "-R", "u+rwx", "/usr/src/app"]

COPY . /usr/src/app
WORKDIR /usr/src/app

RUN chmod 755 /usr/src/app/runcode.sh

RUN pip3 install -r requirements.txt

RUN rm /bin/ls
RUN rm /usr/bin/apt
RUN rm /bin/mv
RUN rm /bin/dd
RUN rm /bin/uname
RUN rm /sbin/mkf*
RUN rm /bin/mkdir
RUN rm /bin/rm


ENTRYPOINT ["python3"]
CMD ["app.py"]
