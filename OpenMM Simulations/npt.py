##!/bin/env python
from simtk.openmm.app import *
from simtk.openmm import *
from simtk.unit import *
from sys import stdout, exit, stderr
import numpy as np
import sys


xlength = 68.7301608/10
ylength = 59.2345525/10
zlength = 53.9341051/10

psf = CharmmPsfFile('../../3-neutralization/light_sol_ion.psf')
psf.setBox(xlength,ylength,zlength)
cor = CharmmCrdFile('light_heated.cor')
params = CharmmParameterSet('/users/mayarm/scratch/Light/ff/top_all27_prot_na.rtf','/users/mayarm/scratch/Light/ff/fmn-alltop-06302008.top','/users/mayarm/scratch/Light/ff/fmc-alltop-06302008.top','/users/mayarm/scratch/Light/ff/par_all27_prot_na.prm','/users/mayarm/scratch/Light/ff/fmc-allpar-05302008.par')

system = psf.createSystem(params, nonbondedMethod=PME,
        nonbondedCutoff=1.2*nanometers,
        constraints=HBonds,
        rigidWater=True, ewaldErrorTolerance=0.0005)

system.addForce(MonteCarloBarostat(1*bar, 300*kelvin, 100))
integrator = LangevinIntegrator(300*kelvin, 1.0/picoseconds, 2.0*femtoseconds)
integrator.setConstraintTolerance(0.00001)
platform = Platform.getPlatformByName('CUDA')
properties = {'CudaPrecision': 'single'}

tstep=5000000
simulation = Simulation(psf.topology, system, integrator, platform, properties)
simulation.context.setPositions(cor.positions)
simulation.minimizeEnergy()
simulation.context.setVelocitiesToTemperature(300*kelvin)

simulation.reporters.append(DCDReporter(sys.argv[1]+'-'+sys.argv[2]+'.dcd', 50000))
simulation.reporters.append(StateDataReporter(sys.argv[1]+'-'+sys.argv[2]+'.log', 50000, step=True, potentialEnergy=True, temperature=True, volume=True, progress=True, remainingTime=True, speed=True, totalSteps=tstep))
simulation.reporters.append(CheckpointReporter(sys.argv[1]+'-'+sys.argv[2]+'.chk', 50000))
simulation.step(tstep)
