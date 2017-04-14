if ! [ -d ".smt" ]
        then
    smt init extremefill2D
    smt configure --executable=python --main=script.py
    smt configure -g uuid
    smt configure -c store-diff
    smt configure --addlabel=parameters
fi
smt run -t testrun params.json totalSteps=10
