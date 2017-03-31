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
RUN conda install matplotlib
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
RUN pip install ipy_table==1.12
RUN pip install brewer2mpl==1.4.1


## Run Simulation

RUN git config --global user.name "Main"
RUN git config --global user.email "main@main.com"

WORKDIR $HOME/extremefill2D/scripts

ADD view.ipynb view.ipynb

EXPOSE 8888

ENV SHELL /bin/bash

# Force update from this point
ENV FAKE_ENV_VAR "Thu Mar 30 17:47:29 EDT 2017"

RUN mkdir /data
RUN mkdir /data/Data
WORKDIR /data
VOLUME /data

CMD \rm -rf * && \
    cp $HOME/extremefill2D/scripts/script.py /data && \
    cp $HOME/extremefill2D/scripts/params_fig4.json /data && \
    cp $HOME/extremefill2D/scripts/view.ipynb /data && \
    git init && \
    git add script.py params_fig4.json && \
    git commit -m "initial commit" && \
    smt init smt-extremefill2D && \
    smt configure --executable=python --main=script.py && \
    smt configure -g uuid && \
    smt configure -c store-diff && \
    smt configure --addlabel=parameters && \
    smt run -t testrun params_fig4.json totalSteps=10

# jupyter notebook --ip 0.0.0.0 --no-browser
