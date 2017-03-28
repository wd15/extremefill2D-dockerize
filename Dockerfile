From ubuntu:16.10

MAINTAINER Daniel Wheeler <daniel.wheeler2@gmail.com>

ENV DEBIAN_FRONTEND noninteractive

USER root

RUN apt-get -y update
RUN apt-get install -y git sudo bzip2 g++ libgfortran3 liblapack3 wget
RUN apt-get clean
# RUN apt-get dist-upgrade -y

RUN useradd -m -s /bin/bash main

EXPOSE 8888

USER main

ENV HOME /home/main
ENV SHELL /bin/bash
ENV USER main
WORKDIR $HOME

USER root

RUN chown -R main:main /home/main

USER main

## Install FiPy Requirements

ENV ANACONDAPATH $HOME/anaconda
ENV PATH "$ANACONDAPATH/bin:${PATH}"

RUN wget https://repo.continuum.io/miniconda/Miniconda2-4.3.11-Linux-x86_64.sh
RUN bash Miniconda2-4.3.11-Linux-x86_64.sh -b -p $ANACONDAPATH
RUN conda update conda
RUN conda install libgfortran=1.0
RUN conda install --channel guyer scipy gmsh
RUN conda install --channel guyer pysparse openmpi mpi4py
RUN conda install --channel guyer trilinos
RUN pip install scikit-fmm

## Install FiPy

RUN git clone https://github.com/usnistgov/fipy
WORKDIR $HOME/fipy
RUN git checkout ecbe868f2aff6dbc43fb8ed532e581a03ebab5d5
RUN python setup.py develop

## Install Extremefill2D

WORKDIR $HOME
RUN git clone https://github.com/wd15/extremefill2D.git
WORKDIR $HOME/extremefill2D
RUN git checkout 7eb7ca8
RUN python setup.py develop
RUN pip install sumatra==0.7.4
RUN pip install configparser==3.5.0
RUN pip install gitpython==2.1.3
RUN pip install docopt==0.6.2
RUN pip install pandas==0.19.2
RUN pip install tables==3.3.0
RUN conda install jupyter=1.0.0
RUN conda install libgfortran=1.0

## Run Simulation

RUN git config --global user.name "Main"
RUN git config --global user.email "main@main.com"

WORKDIR $HOME/extremefill2D/scripts
RUN smt init smt-extremefill2D
RUN smt configure --executable=python --main=script.py
RUN smt configure -g uuid
RUN smt configure -c store-diff
RUN smt configure --addlabel=parameters

RUN smt run params_fig4.json totalSteps=20

ENV SHELL /bin/bash