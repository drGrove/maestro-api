ARG PYTHON_VERSION=3.8-buster@sha256:1d24b4656d4df536d8fa690be572774aa84b56c0418266b73886dc8138f047e6

FROM python:${PYTHON_VERSION} as base
ADD **/*.py /srv/app/
ADD migrations /srv/app/
ADD requirements.txt /srv/app/

FROM base as dev
COPY --from=base /srv/app /srv/app
ADD requirements-dev.txt /srv/app/
WORKDIR /srv/app
RUN pip install -r requirements-dev.txt
CMD ["flask", "run"]

FROM base as prod
COPY --from=base /srv/app /srv/app
WORKDIR /srv/app
RUN pip install -r requirements.txt
CMD ["python3", "wsgi.py"]
