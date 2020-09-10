FROM python:3.8
ENV DEBIAN_FRONTEND noninteractive

ENV WORKDIR /root/documentation
WORKDIR $WORKDIR

# poetry
COPY pyproject.toml poetry.toml poetry.lock $WORKDIR/
RUN mkdir $WORKDIR/documentation && touch $WORKDIR/documentation/__init__.py
RUN pip install poetry
RUN poetry install

# sphinx
RUN apt-get update && apt-get install -y \
    python3-sphinx \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Qt
ENV QT_VERSION 5.12
RUN apt-get update && apt-get install -y --no-install-recommends \
        cmake \
        git \
        gcc \
        libclang-dev \
        libdbus-1-dev \
        libgl-dev \
        libxkbcommon-dev \
        libxkbcommon-x11-dev \
    && \
    apt-get clean  && \
    rm -rf /var/lib/apt/lists/*
RUN git clone git://code.qt.io/qt/qt5.git && \
    cd qt5 && \
    git checkout $QT_VERSION && \
    perl init-repository

CMD ["bash"]
