FROM python:3.8
ENV DEBIAN_FRONTEND noninteractive

ENV WORKDIR /root/package_name
WORKDIR $WORKDIR

# poetry
COPY pyproject.toml poetry.toml poetry.lock $WORKDIR/
RUN mkdir $WORKDIR/package_name && touch $WORKDIR/package_name/__init__.py
RUN pip install poetry
RUN poetry install

# sphinx
RUN apt-get update && apt-get install -y \
    python3-sphinx \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

CMD ["bash"]
