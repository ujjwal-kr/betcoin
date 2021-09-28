FROM python:3.9
LABEL maintainer='0xbirdie@gmail.com'

ADD . .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt


# ┌─────────────┬──────────┬───────────────┐
# │             │ WARNING!!│               │
# │             └──────────┘               │
# │ Do NOT forget to expose ports when     │
# │ deploying to production!               │
# │                                        │
# │ Always use this command when deploying │
# │ using Dockerfile via docker build      │
# │ command:                               │
# ├────────────────────────────────────────┤
# │ -$ docker run betcoin -p 5000:5000 --rm│
# │    --name betcoin                      │
# ├────────────────────────────────────────┤
# │                                        │
# └────────────────────────────────────────┘
CMD [ "flask", "run" ]