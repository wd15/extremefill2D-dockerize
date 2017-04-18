#!/usr/bin/env python

__docformat__ = 'restructuredtext'

import tables
import fipy as fp
from fipy import numerix
import numpy as np
import imp
import sys
import os
import tempfile
from tools import write_data
from fipy.variables.surfactantVariable import _InterfaceSurfactantVariable
import shutil
from tools import get_nonuniform_dx
from tools import DistanceVariableNonUniform as DVNU

filename = sys.argv[1]
filenamec = filename + 'c'
params = imp.load_source('params', filename)
if os.path.exists(filenamec):
    os.remove(filenamec)

totalSteps = params.totalSteps
sweeps = params.sweeps
tol = params.tol
appliedPotential = params.appliedPotential
deltaRef = params.deltaRef
featureDepth = params.featureDepth
Nx = params.Nx
CFL = params.CFL
dataFile = os.path.join(tempfile.gettempdir(), 'data.h5')
kPlus = params.kPlus
kMinus = params.kMinus
featureDepth = params.featureDepth
bulkSuppressor = params.bulkSuppressor
rinner = params.rinner
router = params.router
rboundary = params.rboundary
dtMax = params.dtMax
levelset_update_ncell = params.levelset_update_ncell
totalTime = params.totalTime
spacing_ratio = params.spacing_ratio
data_frequency = params.data_frequency
delete_islands = params.delete_islands
shutdown_deposition_rate = params.shutdown_deposition_rate
write_potential = params.write_potential

dtMin = .5e-7
dt = 0.01
delta = 150e-6
i1 = -40.
i0 = 40.
diffusionCupric = 2.65e-10
faradaysConstant = 9.6485e4
gasConstant = 8.314
temperature = 298.
alpha = 0.4
charge = 2
bulkCupric = 1000.
diffusionSuppressor = 9.2e-11
kappa = 15.26
omega = 7.1e-6
gamma = 2.5e-7
capacitance = 0.3
NxBase = 1000
solver_tol = 1e-10

Fbar = faradaysConstant / gasConstant / temperature



dy = featureDepth / Nx
dx = dy
distanceBelowTrench = 10 * dx
padding = 3 * dx

dx_nonuniform = get_nonuniform_dx(dx, rinner, router, rboundary, padding, spacing_ratio)
dy_nonuniform = get_nonuniform_dx(dy, distanceBelowTrench,
                                  distanceBelowTrench + featureDepth,
                                  distanceBelowTrench + featureDepth + delta, padding, spacing_ratio)

mesh = fp.CylindricalGrid2D(dx=dx_nonuniform, dy=dy_nonuniform) - [[-dx / 100.], [distanceBelowTrench + featureDepth]]
print 'number of cells:',mesh.numberOfCells
dt = fp.Variable(dt)

potential = fp.CellVariable(mesh=mesh, hasOld=True, name=r'$\psi$')
potential[:] = -appliedPotential

cupric = fp.CellVariable(mesh=mesh, hasOld=True, name=r'$c_{cu}$')
cupric[:] = bulkCupric
cupric.constrain(bulkCupric, mesh.facesTop)

suppressor = fp.CellVariable(mesh=mesh, hasOld=True, name=r'$c_{\theta}$')
suppressor[:] = bulkSuppressor
suppressor.constrain(bulkSuppressor, mesh.facesTop)

distance = DVNU(mesh=mesh, value=1.)
distance.setValue(-1., where=mesh.y < -featureDepth)
distance.setValue(-1., where=(mesh.y < 0) & (mesh.x < rinner))        
distance.setValue(-1., where=(mesh.y < 0) & (mesh.x > router))


distance.calcDistanceFunction(order=1)

# fp.Viewer(distance).plot()
# raw_input('stopped')

extension = fp.CellVariable(mesh=mesh)

class _InterfaceVar(_InterfaceSurfactantVariable):
    def _calcValue(self):
        return np.minimum(1, super(_InterfaceVar, self)._calcValue())

theta = fp.SurfactantVariable(distanceVar=distance, hasOld=True, name=r'$\theta$', value=0.)
interfaceTheta = _InterfaceVar(theta)

I0 = (i0 + i1 * interfaceTheta)
baseCurrent = I0 * (numerix.exp(alpha * Fbar * potential) \
                        - numerix.exp(-(2 - alpha) * Fbar * potential))
cbar =  cupric / bulkCupric
current = cbar * baseCurrent
currentDerivative = cbar * I0 * (alpha * Fbar *  numerix.exp(alpha * Fbar * potential) \
                                     + (2 - alpha) * Fbar * numerix.exp(-(2 - alpha) * Fbar * potential))

upper = fp.CellVariable(mesh=mesh)
ID = mesh._getNearestCellID(mesh.faceCenters[:,mesh.facesTop.value])

upper[ID] = kappa / mesh.dy[-1] / (deltaRef - delta + mesh.dy[-1])

surface = distance.cellInterfaceAreas / distance.mesh.cellVolumes
area = 1.
harmonic = (distance >= 0).harmonicFaceValue

potentialEq = fp.TransientTerm(capacitance * surface + (distance < 0)) == \
  fp.DiffusionTerm(kappa * area * harmonic) \
  - surface * (current - potential * currentDerivative) \
  - fp.ImplicitSourceTerm(surface * currentDerivative) \
  - upper * appliedPotential - fp.ImplicitSourceTerm(upper) 
    
cupricEq = fp.TransientTerm(area) == fp.DiffusionTerm(diffusionCupric * area * harmonic) \
  - fp.ImplicitSourceTerm(baseCurrent * surface / (bulkCupric * charge * faradaysConstant))

suppressorEq = fp.TransientTerm(area) == fp.DiffusionTerm(diffusionSuppressor * area * harmonic) \
  - fp.ImplicitSourceTerm(gamma * kPlus * (1 - interfaceTheta) * surface)

depositionRate = current * omega / charge / faradaysConstant
adsorptionCoeff = dt * suppressor * kPlus
thetaEq = fp.TransientTerm() == fp.ExplicitUpwindConvectionTerm(fp.SurfactantConvectionVariable(distance)) \
          + adsorptionCoeff * surface \
          - fp.ImplicitSourceTerm(adsorptionCoeff * distance._cellInterfaceFlag) \
          - fp.ImplicitSourceTerm(kMinus * depositionRate * dt)

advectionEq = fp.TransientTerm() + fp.AdvectionTerm(extension)

elapsedTime = 0.
step = 0

potentialBar = -potential / appliedPotential
potentialBar.name = r'$\bar{\eta}$'
cbar.name = r'$\bar{c_{cu}}$'
suppressorBar = suppressor / bulkSuppressor
suppressorBar.name = r'$\bar{c_{\theta}}$'

potentialSolver = fp.LinearPCGSolver(tolerance=solver_tol)
cupricSolver = fp.LinearPCGSolver(tolerance=solver_tol)
suppressorSolver = fp.LinearPCGSolver(tolerance=solver_tol)
thetaSolver = fp.LinearPCGSolver(tolerance=solver_tol)

extensionGlobalValue = max(extension.globalValue)

def extend(depositionRate, extend, distance):
    extension[:] = depositionRate
    distance.extendVariable(extension)
    return max(extension.globalValue)

redo_timestep = False

while (step < totalSteps) and (elapsedTime < totalTime):
    
    potential.updateOld()
    cupric.updateOld()
    suppressor.updateOld()
    theta.updateOld()
    distanceOld = numerix.array(distance).copy()

    if (dataFile is not None) and (step % data_frequency == 0) and (not redo_timestep):
#        write_data(dataFile, elapsedTime, distance, step, potential, cupric, suppressor, interfaceTheta)
        kwargs = dict()
        if write_potential:
            kwargs['potential'] = potential
        write_data(dataFile, elapsedTime, distance, step, extensionGlobalValue=extensionGlobalValue, **kwargs)
        if step > 0 and extensionGlobalValue < shutdown_deposition_rate:
            break

    if (step % int(levelset_update_ncell / CFL) == 0):
        if delete_islands:
            distance.deleteIslands()
        distance.calcDistanceFunction(order=1)

    extensionGlobalValue = extend(depositionRate, extend, distance)

    dt.setValue(min(float(CFL * dx / extensionGlobalValue), float(dt) * 1.1))
    dt.setValue(min((float(dt), dtMax)))
    dt.setValue(max((float(dt), dtMin)))

    advectionEq.solve(distance, dt=dt)

    for sweep in range(sweeps):
        potentialRes = potentialEq.sweep(potential, dt=dt, solver=potentialSolver)
        cupricRes = cupricEq.sweep(cupric, dt=dt, solver=cupricSolver)
        suppressorRes = suppressorEq.sweep(suppressor, dt=dt, solver=suppressorSolver)
        thetaRes = thetaEq.sweep(theta, dt=1., solver=thetaSolver)
        res = numerix.array((potentialRes, cupricRes, suppressorRes, thetaRes))
        print 'sweep: {0}, res: {1}'.format(sweep, res)

    extensionGlobalValue = extend(depositionRate, extend, distance)
    if float(dt) > (CFL * dx / extensionGlobalValue * 1.1):
        dt.setValue(float(dt) * 0.1)
        print 'redo time step'
        print 'new dt',float(dt)
        potential[:] = potential.old
        cupric[:] = cupric.old
        suppressor[:] = suppressor.old
        theta[:] = theta.old
        distance[:] = distanceOld
        redo_timestep = True
    else:
        elapsedTime += float(dt)
        step += 1
        redo_timestep = False
    
    print 'dt',dt
    print 'elapsed time',elapsedTime
    print 'step',step
    import datetime
    print 'time: ',datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    print
        
if not hasattr(params, 'sumatra_label'):
    params.sumatra_label = '.'

finaldir = os.path.join('Data', params.sumatra_label)

shutil.move(dataFile, finaldir)

