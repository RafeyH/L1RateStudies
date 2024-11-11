# L1RateStudies
Repository to maintain utility code and instructions to produce and plot L1 rates for customized CMS runs

# Instructions for L1Ntuple production
## Set-up CMSSW version
Set-up instructions for L1Ntuple production can be found here [twiki: L1 Trigger Emulator Stage 2 Upgrade Instructions](https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideL1TStage2Instructions#Environment_Setup_with_Integrati). The instructions are updated regularly. Following is are the instructions I followed for the set-up; might no longer be applicable.
```sh
cmsrel CMSSW_13_2_0_pre3
cd CMSSW_13_2_0_pre3/src
cmsenv
git cms-init
git remote add cms-l1t-offline git@github.com:cms-l1t-offline/cmssw.git
git fetch cms-l1t-offline l1t-integration-CMSSW_13_2_0_pre3
git cms-merge-topic -u cms-l1t-offline:l1t-integration-v164-CMSSW_13_2_0_pre3
git clone https://github.com/cms-l1t-offline/L1Trigger-L1TCalorimeter.git L1Trigger/L1TCalorimeter/data

git cms-checkdeps -A -a

scram b -j 8
```
## Set-up L1Ntuple python script
Produce python config file for the re-emulation by using the appropriate GTAG ,customizations and input file. 
```sh
cmsDriver.py l1NtupleRAWEMU_2022 \
	-s RAW2DIGI \
	--era=Run3 \
	--customise=L1Trigger/Configuration/customiseReEmul.L1TReEmulFromRAWsimEcalTP \
	--customise=L1Trigger/L1TNtuples/customiseL1Ntuple.L1NtupleRAWEMU \
	--conditions=124X_dataRun3_Prompt_v4 \
	-n 200 --data --no_exec --no_output \
	--filein=/store/data/Run2022E/SpecialHLTPhysics10/RAW/v1/000/359/664/00000/0d7a5cab-ccd1-4eda-9744-b12c8e8ded92.root
```

## Produce L1Ntuples
- Customize and test run the produced l1NtupleRAWEMU\_2022\_RAW2DIGI.py locally by:
```sh
voms-proxy-init -voms cms
cmsRun l1NtupleRAWEMU_2022_RAW2DIGI.py &> testRun.log &
```
This will ofc not run if the input file is not available on disk. In which case, follow the next step and directly submit a crab job a single input file for TAPERECALL

- Run over a full run / provided data files by submitting crab job using crabNtuple.py. The run number/input files/output dataset location/input dataset/era/etc need to be configured before submitting the job. The python script has a control center for easy access to variables most used, but it is recommended that user goes over the script atleast once before submitting.
```sh
crab submit -c crabNtuple.py
``` 
  
# Instructions for rate-estimation
## Set-up L1MenuTools
Set-up instructions for L1MenuTools can be found here: [twiki: L1 Trigger Menu development for Phase-I (Run3)](https://twiki.cern.ch/twiki/bin/viewauth/CMS/HowToL1TriggerMenu#4_Run_3_settings). Instructions are updated and maintained regularly. I'm using earlier version of instructions where the CMSSW version is compatible with the CMSSW version I've used to produce Ntuples.
**NOTE** : exit out of lxplus and log back in to the src dir. Do not cmsenv
**NOTE** : Using L1Menu\_Collisions2022\_v1\_1\_3\_0 because thats the menu for Run 359664, 359684
```sh
git clone --depth 1 https://github.com/cms-l1-dpg/L1MenuTools.git
cd L1MenuTools/rate-estimation
wget https://raw.githubusercontent.com/cms-l1-dpg/L1MenuRun3/master/development/L1Menu_Collisions2022_v1_3_0/L1Menu_Collisions2022_v1_3_0.xml
bash configure.sh  L1Menu_Collisions2022_v1_3_0.xml
cmsenv
mkdir -p objs/include
make -j 8
```
Every time the menu is modified/changed:
```sh
bash configure.sh L1Menu_NEW.xml
cmsenv
mkdir -p objs/include
make -j 8
```


## Steps for L1 rate estimation
Following steps will all take place in the direcotry
> $CMSSW\_BASE/L1MenuTools/rate-estimation/

### Ntuple List
Produce a file in dir ntuples with list of paths to produced Ntuples. eg:
```
root://eoscms.cern.ch//eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/elfontan/condor/2022EphZB_run362439_126X/1.root
root://eoscms.cern.ch//eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/elfontan/condor/2022EphZB_run362439_126X/10.root
root://eoscms.cern.ch//eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/elfontan/condor/2022EphZB_run362439_126X/100.root
```
Or if the files are stored on CERNBOX
```
/eos/user/r/rhashmi/TP/FR2022E-CMSSW-13_2_0_pre3TEST/SpecialHLTPhysics0/crab_FR2022E-CMSSW-13_2_0_pre3TEST_Special0Zeroing_359663_FR_Run2022E-v1/240806_120509/L1Ntuple_359663_Zeroing_fgb1_Special0.root
/eos/user/r/rhashmi/TP/FR2022E-CMSSW-13_2_0_pre3TEST/SpecialHLTPhysics1/crab_FR2022E-CMSSW-13_2_0_pre3TEST_Special1Zeroing_359663_FR_Run2022E-v1/240809_112900/L1Ntuple_359663_Zeroing_fgb1_Special1.root
/eos/user/r/rhashmi/TP/FR2022E-CMSSW-13_2_0_pre3TEST/SpecialHLTPhysics3/crab_FR2022E-CMSSW-13_2_0_pre3TEST_Special3Zeroing_359663_FR_Run2022E-v1/240809_113012/L1Ntuple_359663_Zeroing_fgb1_Special3.root
```
### Lumisection Info
Follow up-to-date instructions on the twiki 

### Prescale Table
Follow up-to-date instructions on the twiki

### Rate Estimation
To produce L1 rates using the Ntuples for the selected L1Menu:
```sh
./testMenu2016 \
    -u menu/run_lumi.csv \
    -m menu/Prescale_2022_v0_1_2.csv \
    -l ntuple/Run3_359684_2022FR_Zeroing.list \
    -o fgbit1_Zeroing_359684 \
    --doPlotRate --doPlotEff --doPrintPU --SelectCol 2E+34 \
    -b 2400 &> zeroingFinal/fgbit1_Zeroing_359684.log &
```
Add --UseUnpackTree to the above if you wish to find unpacked rates(L1 rates without the customization). General form of the script:
```sh
./testMenu2016 \
    -u <lumisection table> \
    -m <prescale table> \
    -l <your_ntuple.list> \
    -o <name_of_output_files> \
    -b 2400 --doPlotRate [--UseUnpackTree] \
    --doPlotLS --SelectRun <your_run_number> \
    --SelectLS '[start_LS,end_LS]' \
    --maxEvent value \
    --SelectCol <chosen column in the PS table> \
    --lowerPUbound value \
    --upperPUbound value --doPrintPU
```

## Produce L1Rate plots
To produce L1Rate plots, one requires the output .csv files produced by the rate-estimation tool from L1MenuTools. The python script top\_ten\_rates.py expects 2 files as input in order:
1. Unpacked rates .csv file
2. Customized rates .csv file
   
The program will output a list of L1Seed names (that pass selection criteria: prescale = 1 and L1Rate > cutoff) in order of how much it has been affected by customization. One can choose to select the L1Seeds of interest from this list and save it in a file like example file L1SeedsOrdered. This will be an imput to the rate\_plotter.py script. 

rate\_plotter.py has a control center for most required functionality. It expects a file with a list of L1Seeds to plot, in ansense of which, it'll plot from a pre-provided list of L1Bits. The script requires an installation of matplotlib and requires python3.6 or above. To use the scipt:
```sh
python3 rate_plotter.py
```


