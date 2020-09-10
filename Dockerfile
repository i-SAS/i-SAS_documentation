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

# paraview
ENV PARAVIEW_VERSION v5.8.0
RUN git clone --recursive https://gitlab.kitware.com/paraview/paraview-superbuild.git && \
    cd paraview-superbuild && \
    git fetch origin && \
    git checkout $PARAVIEW_VERSION && \
    git submodule update
RUN mkdir paraview_build && \
    cd paraview_build && \
    cmake \
        -DPARAVIEW_CATALYST_EDITION=Essentials \
        -DPARAVIEW_CATALYST_PYTHON=ON \
        -DENABLE_osmesa=ON \
        -DENABLE_png=ON \
        -DUSE_SYSTEM_python3=ON \
        -DENABLE_python3=ON \
        -DENABLE_visitbridge=ON \
        ../paraview-superbuild \
    && \
    make && make install && \
    rm -rf ../paraview-superbuild

# for mcr
RUN apt-get update \
    && apt-get install -y \
      lxde \
    && apt-get clean \
    && rm -rf /var/cache/apt/archives/* \
    && rm -rf /var/lib/apt/lists/*

# if pyside2 == 5.13.2
RUN pip install -U pyside2

CMD ["bash"]
