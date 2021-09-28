FROM python:3.9
LABEL maintainer='0xbirdie@gmail.com'

ADD . .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

CMD [ "flask", "run" ]