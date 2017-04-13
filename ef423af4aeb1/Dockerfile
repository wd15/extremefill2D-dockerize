From wd15/extremefill2d_base:latest

MAINTAINER Daniel Wheeler <daniel.wheeler2@gmail.com>

RUN git checkout 3ad19bd930d7
RUN python setup.py develop
WORKDIR $HOME/extremefill2D/scripts
ADD view.ipynb view.ipynb
ADD run.sh run.sh
ADD params.json params.json

WORKDIR $HOME/data

CMD bash $HOME/extremefill2D/scripts/run.sh $HOME/data
