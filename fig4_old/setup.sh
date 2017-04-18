WORKDIR=${PWD}
cd ${HOME}/extremefill2D
git fetch
git checkout 5319cc4d8df4
export PYTHONPATH=${PWD}
cd ${WORKDIR}

if ! [ -d ".smt" ]
        then
    smt init extremefill2D
    smt configure --executable=python --main=script.py
    smt configure -g uuid
    smt configure -c store-diff
    smt configure --addlabel=parameters
fi

smt run -t fig4test_old -m /home/main/work/fig4_old/script.py -r "test old version of code" /home/main/work/fig4_old/params.param totalSteps=10
