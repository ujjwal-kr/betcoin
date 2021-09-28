FROM python:3.9
LABEL maintainer='0xbirdie@gmail.com'

ADD . .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt


# ┌────────────────────────┐
# │       WARNING!         │
# │ Do NOT forget to expose│
# │ ports when running!    │
# └────────────────────────┘
CMD [ "flask", "run" ]