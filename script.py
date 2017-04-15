#!/usr/bin/env python
"""
Usage: script.py [<jsonfile>]

"""

__docformat__ = 'restructuredtext'


import shutil
from collections import namedtuple
import json
import os
import tempfile


from docopt import docopt
from extremefill2D.systems import ExtremeFillSystem
# from extremefill2D.systems import ConstantCurrentSystem
from extremefill2D.tools import DataWriter, WriteCupricData




if __name__ == '__main__':
    arguments = docopt(__doc__, version='Run script.py')
    jsonfile = arguments['<jsonfile>']
    with open(jsonfile, 'rb') as ff:
        params_dict = json.load(ff)
    params = namedtuple('ParamClass', params_dict.keys())(*params_dict.values())


    with tempfile.NamedTemporaryFile(suffix='.h5', delete=False) as f:
        print f.name
        datafile = f.name

    dataWriter = WriteCupricData(datafile)

    system = ExtremeFillSystem(params, dataWriter)
    # system = ConstantCurrentSystem(params, dataWriter)
    system.run()

    if not hasattr(params, 'sumatra_label'):
        sumatra_label = '.'
    else:
        sumatra_label = params.sumatra_label

    finaldir = os.path.join('Data', sumatra_label)
    finalpath = os.path.join(finaldir, 'data.h5')
    shutil.move(datafile, finalpath)
