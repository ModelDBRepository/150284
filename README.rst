Note from the ModelDB Administrator
===================================
This is a July 15th, 2013 copy of the repository at:
https://github.com/mattions/TimeScales
where you can find the most recent copy.

************************
The TimeScales framework
************************

This is the README of the TimeScales framework, which is used to 
run a Multiscale Model of the Medium Spiny Neuron of the Neostriatum, 
integrating electrical signalling with biochemical pathways.

The main script to launch the simulation is spinesIntegration.py, which 
accepts a certain amount of parameters (described in the source code).

The code is licensed under BSD.

********
Citation
********

::

    Mattioni M, Le Novère N (2013) Integration of Biochemical and Electrical 
    Signaling-Multiscale Model of the Medium Spiny Neuron of the Striatum. 
    PLoS ONE 8(7): e66811. doi:10.1371/journal.pone.0066811
    
The paper is online at http://www.plosone.org/article/info%3Adoi%2F10.1371%2Fjournal.pone.0066811
    

*****************
Package structure
*****************

These are the directories of the package:

- *biochemical_circuits* contains all the biochemical network which have been used at different stage 
  of the development of the model.
- *branch_dist* contains the code to calculate the spine distribution as explained in the paper 
  and in the thesis
- *ecellControl* is the module with the ecellManager class, which controls the E-Cell simulator 
  and it's used ae entry-point in the main synchronization script (`spineIntegration.py`)
- *helpers* is a directory where there are some utilities script used to plot and explore the data
- *hoc* contains the hoc file to instantiate the MSN without any spines based on the model of 
- *mod* contains the NMODL file which needs to be compiled and than can be loaded into section in the 
  Neuron model. 
- *neuroControl* is the module with the NeuronManager class, which is used to control NEURON. In this module
  there are also the class to create the hybrid spine, which has both electrical and biochemical nature.
- *param* contains the parameters file used to run the simulations.
- *spineIntegration.py* is the main script which runs the multiscale model.
- *extref.py* contains the class to extend Neuronvisio storage format to accept the biochemical results 
  on top of the electrical one. 
- *visioStart.py* instantiate the model and loads it in the Neuronvisio software.

****************************************
How to launch simulation on the EBI cluster
****************************************

==========
TimeScales
==========

Launching the simulations
=========================

This is the README to launch TimeScales with the Hybrid model on the EBI cluster


Storing here for future references::

    bsub -M 20000 -R "rusage[mem=20000]" smt run param/allspines.param -r "Testing the new synchro mechanism." -t "test, all"


Small memory, for testing
-------------------------

    bsub -M 4000 -R "rusage[mem=4000]" smt run param/default.param -r "Testing the new synchro mechanism." -t "test, twospines"
    
    bsub -M 4000 -R "rusage[mem=4000]" -q research-rh6 smt run param/short_tstop_double_stim.param -r "Double stims applied for short tstop." -t "test, twospines"
    
    bsub -M 10000 -R "rusage[mem=10000]" -q research-rh6 smt run param/short_tstop_onebranch_several_stimulation.param -r "Short tstop for testing. One branch populated with spines. Using 10 Gb" -t "onebranch"


K flux investigation
--------------------

    bsub -M 4000 -R "rusage[mem=4000]" smt run param/short_tstop_k_flux_investigation.param -r "Testing different calcium sampling" -t "k_flux"

Long tStop test
---------------

    bsub -M 4000 -R "rusage[mem=4000]" -q research-rh6 smt run param/long_tstop.param -r "Running a long simulation." -t "test, twospines"

    bsub -M 10000 -R "rusage[mem=6000]" -q research-rh6 smt run param/long_tstop_double_stim_two_spines.param -r "Running a double excitation with two spines." -t "twospines"
    
    bsub -M 60000 -R "rusage[mem=20000]" -q research-rh6 smt run param/long_tstop_double_stim_all_spines.param -r "Running a double excitation with two spines." -t "all"
    
    bsub -M 10000 -R "rusage[mem=6000]" -q research-rh6 smt run param/long_tstop_one_pulse.param -r "Running one pulse event in one spine." -t "twospines"

One branch stim
---------------

    bsub -M 10000 -R "rusage[mem=6000]" -q research-rh6 smt run param/long_tstop_onebranch_several_stimulation.param -r "Several stims across one branch populated with spines. Using 10 Gb" -t "onebranch"
    
    bsub -M 10000 -R "rusage[mem=6000]" -q research-rh6 smt run param/long_tstop_onebranch_1_spine_1Hz.param -r "One branch: One spine double stim. 1Hz. Using 10 Gb" -t "onebranch"
    
    bsub -M 10000 -R "rusage[mem=6000]" -q research-rh6 smt run param/long_tstop_onebranch_1_spine_4Hz.param -r "One branch: One spine double stim. 4Hz. Using 10 Gb" -t "onebranch"
    
    bsub -M 10000 -R "rusage[mem=6000]" -q research-rh6 smt run param/long_tstop_onebranch_1_spine_8Hz.param -r "One branch: One spine double stim. 8Hz. Using 10 Gb" -t "onebranch"
    
    bsub -M 10000 -R "rusage[mem=6000]" -q research-rh6 smt run param/long_tstop_onebranch_1_spine_20Hz.param -r "One branch: One spine double stim. 20Hz. Using 10 Gb" -t "onebranch"
    
    bsub -M 10000 -R "rusage[mem=6000]" -q research-rh6 smt run param/long_tstop_onebranch_1_spine_50Hz.param -r "One branch: One spine double stim. 50Hz. Using 10 Gb" -t "onebranch"
    
    bsub -M 10000 -R "rusage[mem=6000]" -q research-rh6 smt run param/long_tstop_onebranch_1_spine_100Hz.param -r "One branch: One spine double stim. 100Hz. Using 10 Gb" -t "onebranch"

    
All Branches - Double stim one spine    
------------------------------------

    bsub -M 60000 -R "rusage[mem=20000]" -q research-rh6 smt run param/long_tstop_allspines_1_spine_1Hz.param -r "All spines: One spine double stim. 1Hz. Using 10 Gb" -t "all"
    
    bsub -M 60000 -R "rusage[mem=20000]" -q research-rh6 smt run param/long_tstop_allspines_1_spine_4Hz.param -r "All spines: One spine double stim. 4Hz. Using 10 Gb" -t "all"
    
    bsub -M 60000 -R "rusage[mem=20000]" -q research-rh6 smt run param/long_tstop_allspines_1_spine_8Hz.param -r "All spines: One spine double stim. 8Hz. Using 10 Gb" -t "all"
    
    bsub -M 60000 -R "rusage[mem=20000]" -q research-rh6 smt run param/long_tstop_allspines_1_spine_20Hz.param -r "All spines: One spine double stim. 20Hz. Using 10 Gb" -t "all"
    
    bsub -M 60000 -R "rusage[mem=20000]" -q research-rh6 smt run param/long_tstop_allspines_1_spine_50Hz.param -r "All spines: One spine double stim. 50Hz. Using 10 Gb" -t "all"
    
    bsub -M 60000 -R "rusage[mem=20000]" -q research-rh6 smt run param/long_tstop_allspines_1_spine_100Hz.param -r "All spines: One spine double stim. 100Hz. Using 10 Gb" -t "all"

All branches - CPM
------------------

    bsub -M 10000 -R "rusage[mem=6000]" -q research-rh6 smt run param/long_tstop_onebranch_clustered_plasticity_model.param -r "One branch: Clustered Plasticity Model. 9 spines stimulated. 20 Hz. Using 10 Gb" -t "onebranch"
    
    bsub -M 60000 -R "rusage[mem=20000]" -q research-rh6 smt run param/long_tstop_allbranch_cpm_two_branches_stims_8_Hz.param -r "CPM 2 branches, all spine 8 Hz. Using 60 Gb of RAM" -t "all"
    
    bsub -M 60000 -R "rusage[mem=20000]" -q research-rh6 smt run param/long_tstop_allbranch_cpm_two_branches_stims_20_Hz.param -r "CPM 2 branches, all spine 20 Hz. Using 60 Gb of RAM (5seg med)" -t "all"
    
    bsub -M 60000 -R "rusage[mem=20000]" -q research-rh6 smt run param/long_tstop_allbranch_cpm_two_branches_stims_40_Hz.param -r "CPM 2 branches, all spine 40 Hz. Using 60 Gb of RAM (5seg med)" -t "all"
    
    bsub -M 60000 -R "rusage[mem=20000]" -q research-rh6 smt run param/long_tstop_allbranch_cpm_two_branches_stims_50_Hz.param -r "CPM 2 branches, all spine 50 Hz. Using 60 Gb of RAM (5seg med)" -t "all"
    
    bsub -M 60000 -R "rusage[mem=20000]" -q research-rh6 smt run param/long_tstop_allbranch_cpm_two_branches_stims_40_Hz_long_train.param -r "CPM 2 branches, all spine 40 Hz long stimulation. Using 60 Gb of RAM (5seg med)" -t "all"   


Kir_investigation
-----------------

    bsub -M 60000 -R "rusage[mem=20000]" -q research-rh6 smt run param/long_tstop_allbranch_cpm_two_branches_stims_20_Hz.param -r "Kir Investigation kir_gkbar=0.00014" -t "all" kir_gkbar=0.00014

    bsub -M 60000 -R "rusage[mem=20000]" -q research-rh6 smt run param/long_tstop_allbranch_cpm_two_branches_stims_20_Hz.param -r "Kir Investigation kir_gkbar=0.00018" -t "all" kir_gkbar=0.00018

    bsub -M 60000 -R "rusage[mem=20000]" -q research-rh6 smt run param/long_tstop_allbranch_cpm_two_branches_stims_20_Hz.param -r "Kir Investigation kir_gkbar=0.00012" -t "all" kir_gkbar=0.00012

    bsub -M 60000 -R "rusage[mem=20000]" -q research-rh6 smt run param/long_tstop_allbranch_cpm_two_branches_stims_20_Hz.param -r "Kir Investigation kir_gkbar=0.00020" -t "all" kir_gkbar=0.00020

Neighbours psine investigation
------------------------------

    bsub -M 60000 -R "rusage[mem=20000]" -q research-rh6 smt run param/neighbouring_spine_20Hz.param -r "Neighboring spine with bio on" -t "all, neighbouring"

Reading simulations' results
============================

Reload the storage.h5 file with neuronvisio

    run nrnvisio path/to/Sim/storage.h5
 
 
============
EcellManager
============

Used to launch the biochemical alone for testing.

Launching the simulations
========================

This is for the weight checking::

    bsub -M 4000 -R "rusage[mem=4000]" smt run -m ecellControl/ecellManager.py ecellControl/ecellControl.param -r "Testing AMPA weight"

Reading simulations' results
============================

Open an ipython and run

    run helpers/plotter path/to/TimeCourses

