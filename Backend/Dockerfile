FROM ubuntu

RUN apt-get update
RUN apt-get install -y python3 python3-pip && \
    mdkir Backend

WORKDIR /Backend

COPY . ./

RUN pip3 install -r requirements.txt

CMD ["python3 manage.py runserver"]