# This code is a derivation from the L1T TEA shifters code
# Last update: 02/01/2024

# Changed setup for Run3 Ntuples
# Using this ugly way of formatting strings instead of fstrings becuase python2.7 limitations

from CRABClient.UserUtilities import config
import datetime,sys,os

config = config()

# -----------------------------------------------
#				CONTROL PANEL
# -----------------------------------------------

cmssw_version	=	'13_2_0_pre3'
era			    =	'2023C' #'2022E' #'2018C' 
NJOBS			=	-1
workflow		=	'ZeroBias' #'FR'
runNumbers		=	[368685] #[367883] #[359684]	# CAN ONLY HANDLE 1 RUN AS OF NOW!!
StorageSite		=	'T3_CH_CERNBOX' 
# If providing data files, comment out runrange, inputDataset and inputBlocks
data_files		=	False #'Files/Files_Run_368685.txt'
#runSite        =       ['T2_FR_GRIF']
user            =   'rhashmi'

# -----------------------------------------------

all_files = []
if data_files:
	with open(data_files,'r') as f:
		for line in f:
			all_files.append(line.split()[0])

if workflow == 'ZeroBias':
	pSet = 'l1NtupleRAWEMU_2023_368685_RAW2DIGI.py'
	JOBID = 'ZeroBias'+str(era)+'-CMSSW-'+cmssw_version+'TEST'
	dataset	= 'ZeroBias'

if workflow == 'FR':
	pSet = 'l1NtupleRAWEMU_2022_test_684_RAW2DIGI.py'
	JOBID = 'FR'+str(era)+'-CMSSW-'+cmssw_version+'TEST'
	dataset	= 'FR'

print('Nutples will appear in subdiretory '+JOBID)

Nunits		= 1 # Units per job
#logbase		= "Run%s_ZeroBias_noRECO"%era
logbase		= "Run%s_DW2p5_noRECO"%era
splitting       = 'FileBased' #'LumiBased'
# IF splitting Automatic, comment out unitsPerJob
output		= '/store/user/%s/TP/'%user + JOBID
myJobs={}

for runNumber in runNumbers:
	myJobs["%d_%s_Run%s-v1"%(runNumber,dataset,era)] = ["/%s/Run%s-v1/RAW"%(dataset,era),Nunits,runNumber]
	#myJobs["%d_%s_Run%s-v1"%(runNumber,dataset,era)] = ["/ZeroBias/Run2018C-v1/RAW",Nunits,runNumber]

config.section_('General')
config.General.transferOutputs = True	# transfer output files to storage
config.General.transferLogs = True	# transfer job logs to storage
config.General.workArea = logbase + '_' + str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
#############
config.General.requestName = JOBID + "Zeroing_%d_%s_Run%s-v1"%(runNumbers[0],dataset,era)
#############
config.section_('JobType')
config.JobType.psetName = pSet
config.JobType.pluginName = 'Analysis'
config.JobType.maxMemoryMB = 2500
config.JobType.outputFiles = ['L1Ntuple.root']

config.section_('Data')
config.Data.ignoreLocality = False # allows jobs to run at any site
config.Data.inputDBS = 'global'
config.Data.splitting = splitting
config.Data.outLFNDirBase = output

#############
config.Data.inputDataset = "/ZeroBias/Run%s-v1/RAW"%era
#config.Data.inputDataset = "/SpecialHLTPhysics3/Run2022E-v1/RAW"
config.Data.inputBlocks = [
    '/ZeroBias/Run2023C-v1/RAW#40ae252b-bc6a-4584-b281-7b1d05d883f3',
    '/ZeroBias/Run2023C-v1/RAW#a16fbc68-3962-414e-9a13-0cd5a29afb39',
    '/ZeroBias/Run2023C-v1/RAW#d313aec0-b5b1-408c-9113-c00853a5bb6c',
    '/ZeroBias/Run2023C-v1/RAW#e4fef9b4-b718-4a78-84dc-c79027ea7f3b',
]
#config.Data.userInputFiles = all_files
config.Data.unitsPerJob = Nunits
config.Data.runRange = str(runNumbers[0])
config.Data.publication=False
#############

config.section_('Site')
#config.Site.whitelist = runSite
config.Site.storageSite =  StorageSite




