#%%
import os
import numpy as np
import matplotlib.pyplot as plt
import cst_python_api as cpa

scriptDir = os.path.dirname(os.path.abspath(__file__))
projectName = "Patch_Antenna_2p4GHz_optimized_v3.cst"

# Create the CST project
myCST = cpa.CST_MicrowaveStudio(scriptDir, projectName)

# Set the default units for the project (CST default is mm)
myCST.Project.setUnits()

######################
#
# DEFINITION OF THE GEOMETRY PARAMETERS (all values in mm)
#
######################
# Optimized and confirmed parameters
patchWidth = 38.35
patchLength = 29.42
feedPoint = 8.60
feedLineWidth = 2.95
feedingGap = 1.0
substrateWidth = 76.71
substrateLength = 59.57
condThickness = 0.035
substrateThickness = 1.5

######################
#
# MATERIALS
#
######################
# Add FR-4 material to the project (must be defined before use)
# eps_r = 4.3, mu_r = 1.0, tanD = 0.025
myCST.Build.Material.addNormalMaterial(
    "FR-4", 4.3, 1.0, colour=[0.94, 0.82, 0.76], tanD = 0.025)

######################
#
# GEOMETRY (create from bottom up: Groundplane -> Substrate -> Patch)
#
######################
# Create ground plane (copper is default material in CST)
myCST.Build.Shape.addBrick(
    xMin = -0.5*substrateWidth, xMax = 0.5*substrateWidth,
    yMin = -0.5*substrateLength, yMax = 0.5*substrateLength,
    zMin = 0.0, zMax = condThickness,
    name = "Groundplane", component = "component1", material="Copper (annealed)"
)

# Create substrate using FR-4
myCST.Build.Shape.addBrick(
    xMin = -0.5*substrateWidth, xMax = 0.5*substrateWidth,
    yMin = -0.5*substrateLength, yMax = 0.5*substrateLength,
    zMin = condThickness, zMax = condThickness + substrateThickness, 
    name = "Substrate", component = "component1", material="FR-4"
)

# Create patch (copper)
myCST.Build.Shape.addBrick(
    xMin = -0.5*patchWidth, xMax = 0.5*patchWidth,
    yMin = -0.5*patchLength, yMax = 0.5*patchLength,
    zMin = condThickness + substrateThickness,
    zMax = 2*condThickness + substrateThickness,
    name = "Patch", component = "component1", material="Copper (annealed)"
)

# Create feeding gap (vacuum) to inset the feed into the patch
myCST.Build.Shape.addBrick(
    xMin = -(0.5*feedLineWidth + feedingGap),
    xMax = (0.5*feedLineWidth + feedingGap),
    yMin = -0.5*patchLength, yMax = -0.5*patchLength + feedPoint,
    zMin = condThickness + substrateThickness,
    zMax = 2*condThickness + substrateThickness,
    name = "Feeding_gap", component = "component1", material="Vacuum"
)

# Subtract the feeding gap from the patch
myCST.Build.Boolean.subtract("component1:Patch", "component1:Feeding_gap")

# Create feed line (copper)
myCST.Build.Shape.addBrick(
    xMin = -0.5*feedLineWidth, xMax = 0.5*feedLineWidth,
    yMin = -0.5*substrateLength, yMax = -0.5*patchLength + feedPoint,
    zMin = condThickness + substrateThickness,
    zMax = 2*condThickness + substrateThickness,
    name = "Feed_line", component = "component1", material="Copper (annealed)"
)

# Join the feed line and the patch
myCST.Build.Boolean.add("component1:Patch", "component1:Feed_line")

###########################
#
# PORTS
#
###########################
# Set the frequency range for the solver
myCST.Solver.setFrequencyRange(2.0, 3.0)

# Waveguide port definition at the bottom edge (to excite the microstrip feed)
k = 5  # extension factor for the port volume
myCST.Solver.Port.addWaveguidePort(
    xMin=-(feedLineWidth/2 + k*substrateThickness), xMax=(feedLineWidth/2 + k*substrateThickness),
    yMin=-substrateLength/2, yMax=-substrateLength/2,
    zMin=condThickness, zMax=substrateThickness + k*substrateThickness,
    orientation="ymin", nModes=1
)

###########################
#
# SOLVER & FIELD MONITORS
#
###########################
# Field monitors at the operating frequency
myCST.Solver.addFieldMonitor("Efield", 2.4)
myCST.Solver.addFieldMonitor("Hfield", 2.4)
myCST.Solver.addFieldMonitor("Farfield", 2.4)

# Use Time Domain solver
myCST.Solver.changeSolverType("HF Time Domain")

##############################################
#
# RUN THE SIMULATION
#
##############################################
# Launch the simulation
myCST.Solver.runSimulation()

#%%
# Retrieve S-Parameters results and save to file
freq, S11 = myCST.Results.getSParameters(1, 1)
# Do not change name of output file
np.savetxt("S11_results.csv", np.column_stack((np.real(freq), 20.0 * np.log10(np.abs(S11)))), delimiter=",", header="Frequency(S) [GHz], S11(dB)", comments="")