import sys
import ROOT
import math

inpFile = ROOT.TFile(sys.argv[1],"READ")
hist = inpFile.Get("normalizedEmEnergyHist")

nAtoms = 4.431 * math.pow(10,24)
snsHours = 5000
power = 1.4 #MW

MWHrs = snsHours*power
MWHr_to_MeV = 2.247*math.pow(10,22)
MeV = MWHr_to_MeV*MWHrs

beamEnergy=1010
nProtons = MeV/beamEnergy
nNeutrinos = 0.09*nProtons
nVeNeutrinos = nNeutrinos/3.

veNeutrinos_percm_at20m = nVeNeutrinos/(4*3.141592*math.pow(2000,2))

scaleFactor = veNeutrinos_percm_at20m*nAtoms*math.pow(10,-40)

totalInteractions = hist.Integral()*scaleFactor
 
print(totalInteractions)
