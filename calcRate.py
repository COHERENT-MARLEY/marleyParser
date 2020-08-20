#Given a parsed marley output, computes the event rate given the detector and source
#details provided in the json file. Assumes parsed root file has a hist titled
#"excitationEnergyHist"
import sys
import ROOT
import math
import json

#############
#Check usage#
#############
if len(sys.argv) != 2:
  print("\nError! No json file specified!")
  print("Usage: python calcRate.py <json file>\n")
  sys.exit()

################
#Load JSON file#
################
jsonFile = open(sys.argv[1],"r")
data = json.load(jsonFile)

###################
#Load source type"#
###################
if not "sourceType" in data:
  print("No source type, exiting!")
  sys.exit()
if data["sourceType"]=="SNS":
  sourceType="SNS"
elif data["sourceType"]=="SN":
  sourceType="SN"
else:
  print("No valid source type found, use 'SNS' or 'SN', exiting")
  sys.exit()
  
###########################
#Check for JSON parameters#
###########################
headings=["inpFile","sourceType","target_settings","source_settings"]
#Make subheadings to check
subHeadings=[[],[],["mass_kg","atoms_per_kg"]]
if sourceType=="SNS":
  subHeadings.append(["SNS_years","SNS_HoursPerYear","power","beam_energy","distance_from_source_cm","neutrinos_Per_Proton","type"])
elif sourceType=="SN":
  subHeadings.append(["distance","mass"])

#Check and make sure appropriate headings are there
for i,heading in enumerate(headings):
  if not heading in data:
    print("No "+heading+" parameter found in json file, exiting")
    sys.exit()
  for subHeading in subHeadings[i]:
    if not subHeading in data[heading]:
      print("No "+subHeading+" parameter found in parameter "+heading+",exiting")
      sys.exit()
     
#################
#Load input file#
#################
inpFile = ROOT.TFile(data["inpFile"],"READ")
hist = inpFile.Get("normalizedExcitationEnergyHist")

######################
#Load target settings#
######################
nAtoms_per_kg = data["target_settings"]["atoms_per_kg"] #4.431 * math.pow(10,24)
mass = data["target_settings"]["mass_kg"]
nAtoms = mass*nAtoms_per_kg

######################
#Load source dettings#
######################
if sourceType=="SNS":
  snsYears = data["source_settings"]["SNS_years"]
  SNS_HoursPerYear = data["source_settings"]["SNS_HoursPerYear"]
  power = data["source_settings"]["power"]
  beam_energy = data["source_settings"]["beam_energy"]
  distance_from_source_cm = data["source_settings"]["distance_from_source_cm"]
  neutrinos_Per_Proton = data["source_settings"]["neutrinos_Per_Proton"]
  type = data["source_settings"]["type"]


  MWHrs = snsYears*SNS_HoursPerYear*power
  MWHr_to_MeV = 2.247*math.pow(10,22)
  MeV = MWHr_to_MeV*MWHrs
  nProtons = MeV/beam_energy
  nNeutrinos = neutrinos_Per_Proton*nProtons
  if type=="CC":
    nNeutrinos = nNeutrinos/3.
  nNeutrinos_perCm_atDistance = nNeutrinos/(4*3.141592*math.pow(distance_from_source_cm,2))

  scaleFactor = nNeutrinos_perCm_atDistance*nAtoms*math.pow(10,-40)
  
elif sourceType=="SN":
  #Calculate scale factor, i.e. number of neutrinos * math.pow(10,-40)
  print("To do")

totalInteractions = hist.Integral()*scaleFactor
print("Expect " +str(totalInteractions)+" interactions")
