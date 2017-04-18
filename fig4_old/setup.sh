WORKDIR=${PWD}
cd ${HOME}/extremefill2D
git checkout 71e554bd8a2a
export PYTHONPATH=${PWD}
cd ${WORKDIR}
cp ${HOME}/extremefill2D/annular.py ./fig4_old/script.py
cp ${HOME}/extremefill2D/annular.param ./fig4_old/params.param

if ! [ -d ".smt" ]
        then
    smt init extremefill2D
    smt configure --executable=python --main=script.py
    smt configure -g uuid
    smt configure -c store-diff
    smt configure --addlabel=parameters
fi

smt run -t fig4test_old -m /home/main/work/fig4_old/script.py -r "test old version of code" /home/main/work/fig4_old/params.param totalSteps=10
