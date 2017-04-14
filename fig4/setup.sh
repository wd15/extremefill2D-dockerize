WORKDIR=${PWD}
cd ${HOME}/extremefill2D
git checkout 3ad19bd930d7
python setup.py develop
cd ${WORKDIR}

if ! [ -d ".smt" ]
        then
    smt init extremefill2D
    smt configure --executable=python --main=script.py
    smt configure -g uuid
    smt configure -c store-diff
    smt configure --addlabel=parameters
fi

smt run -t fig4test fig4/params.json totalSteps=10
