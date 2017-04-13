From wd15/extremefill2d_base:latest

MAINTAINER Daniel Wheeler <daniel.wheeler2@gmail.com>

RUN git checkout 7eb7ca8
RUN python setup.py develop
WORKDIR $HOME/extremefill2D/scripts
ADD view.ipynb view.ipynb

WORKDIR $HOME/data

CMD bash $HOME/run.sh $HOME/data
