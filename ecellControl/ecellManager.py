# Author Michele Mattioni
# Fri Jan 30 15:57:01 GMT 2009

import ecell.Session as Session
#import mySession as Session
import ecell.ecs
import ecell.config
import ecell.emc
import os
import numpy
from sumatra.external.NeuroTools import parameters

class EcellManager():
    """Control and instatiate the ecell simulator embedding it in an handy python object"""
    
    def __init__(self, filename=None):
        ecell.ecs.setDMSearchPath( os.pathsep.join( ecell.config.dm_path ) )
        self.sim = ecell.emc.Simulator()
        if ecell.config.version < '3.2.0':
            self.ses = Session.Session(self.sim, changeDirectory=False)
        else:
            self.ses = Session.Session(self.sim)
        
        # Load the model
        self.ses.loadModel(filename)
        self.molToTrack = ('ca',
                           'moles_bound_ca_per_moles_cam',
                           'Rbar',
                           'PP2Bbar', 
                           'CaMKIIbar', 
                           'PP1abar', # Active PP1/Total PP1
                           'AMPAR', # 
                           'AMPAR_P',
                           'D',
                           'totDp',
                           'Dpbar'
                           )
        # Tracking the calcium
        self.ca =  self.ses.createEntityStub( 'Variable:/Spine:ca' )
        self.CaMKIIbar = self.ses.createEntityStub( 'Variable:/Spine:CaMKIIbar' )
        self.ampar_P = self.ses.createEntityStub('Variable:/Spine:AMPAR_P')
        self.ca_in = self.ses.createEntityStub('Process:/Spine:ca_in')
        self.ca_leak = self.ses.createEntityStub('Process:/Spine:ca_leak')
        self.ca_pump = self.ses.createEntityStub('Process:/Spine:ca_pump')
        
    def createLoggers(self):
        """Create the logger to track the species"""
        loggers = {}
        #log = ecell.LoggerStub()
        
        for mol in self.molToTrack:
            
            loggers[mol]  = self.ses.createLoggerStub( "Variable:/Spine:" + mol 
                                                       + ":Value" )
            loggers[mol].create() # This creat the Logger Object in the backend
            if mol == 'ca':
                loggers['ca_conc']  = self.ses.createLoggerStub( "Variable:/Spine:" + mol 
                                                       + ":MolarConc" )
                loggers['ca_conc'].create() # This creat the Logger Object in the backend
        
        self.loggers = loggers
        
        
    def calcWeight(CaMKIIbar, PP2Bbar, alpha, beta, n=3, k=0.5):
        """Calc the weight of the synapses according to the CaMKII and Pospahtases
        PP2B and PP1"""
    
        # CaMKII term
        CaMKII_factor = math.pow(CaMKIIbar, n) / (math.pow(k, n) + 
                                                  math.pow(CaMKIIbar, n))
        Phosphatase_factor = math.pow(PP2Bbar, n) / (math.pow(k, n) + 
                                                     math.pow(PP2Bbar, n))
        scaled_CaMKII_factor = alpha * CaMKII_factor
        scaled_Phospatese_factor = beta * Phosphatase_factor 
        weight = 1 + scaled_CaMKII_factor - scaled_Phospatese_factor
        s = "Weight: %s CaMKII factor %s, Phosphatase factor %s" %(weight,
                                                                   scaled_CaMKII_factor,
                                                                   scaled_Phospatese_factor)
        return weight
        
    
    def calcium_peak(self, k_value, duration):
        """
        Mimic the calcium peak
        
        :Parameters
            k_value: the rate of calcium to enter
            duration: Duration of the spike
        """
        
        basal = self.ca_in['k']
        self.ca_in['k'] = k_value
        self.ses.run(duration)
        self.ca_in['k'] = basal
        
    def calciumTrain(self, spikes=30, interval=0.1):
        """Create a train of calcium with the specified number of spikes and interval
        
        :Parameter
            spikes: number of spikes
            interval: Interval between spikes
        """
        for i in range(spikes):
            self.calcium_peak(4.0e8, # Magic number from Lu
                         0.00001 #Really fast spike to avoid the overlap
                         )
            self.ses.run(interval)
        
    def converToTimeCourses(self):
        timeCourses = {}
        for key in self.loggers:
            timeCourses[key] = self.loggers[key].getData()
        
        self.timeCourses = timeCourses
        

        
##############################################
# Testing method

def testCalciumTrain(spikes_number, interval, filename):
    """Run a test simulation wit a train of calcium input"""
    
    print "Test the results of a train of calcium"""
    ecellManager = EcellManager(filename)
    ecellManager.createLoggers()
    #ecellManager.ca_in = ecellManager.ses.createEntityStub('Process:/Spine:ca_in')
    print "Model loaded, loggers created. Integration start."
    ecellManager.ses.run(300)
    print "Calcium Train"
    ecellManager.calciumTrain(spikes=spikes_number, interval=interval)
    ecellManager.ses.run(400)
    ecellManager.converToTimeCourses()
    print "CalciumTrain Test Concluded\n##################"
    return ecellManager
    




def testChangeCalciumValue(interval, caValue, filename="../biochemical_circuits/biomd183_noCalcium.eml"):
    """Run a test simulation changing the calcium value on the fly"""
    print "Show case of the possibilities to change the level of calcium on the fly"
    ecellManager = EcellManager(filename)
    ecellManager.createLoggers()
    print "Loggers created"
    print "Running with the updating interval of : %f" %interval
    
    tstop = 150
    while(ecellManager.ses.getCurrentTime() < tstop):
        ecellManager.ca['Value'] = caValue
        ecellManager.ses.run(interval)
        #ecellManager.ses.run(1)
        #print ecellManager.ses.getCurrentTime()
    
    print "immision of Calcium"
    print "Value of Calcium %f" %ecellManager.ca.getProperty('Value')
    spikes = 4
    for i in range(spikes):
        ecellManager.ca['Value'] = 7200
        ecellManager.ses.run(0.020)
        ecellManager.ca['Value'] = caValue
        ecellManager.ses.run(0.010)
    
    tstop = tstop+500
    while(ecellManager.ses.getCurrentTime() < tstop):
        ecellManager.ca['Value'] = caValue
        ecellManager.ses.run(interval)
        #ecellManager.ses.run(1)
        #print ecellManager.ses.getCurrentTime()
        
    ecellManager.converToTimeCourses()
    print "ChangeCalciumValue Test Concluded"
    return ecellManager
        
if __name__ == "__main__":
    
    import sys
    
    if len(sys.argv) != 2:
        print("No parameter file supplied. Abort.")
        usage = 'python ecellManager.py ecellControl.param'
        print usage
        sys.exit()
        
    parameter_file = sys.argv[1]
    param = parameters.ParameterSet(parameter_file)
    
    ## Setting the mat plotlib backend
    import matplotlib
    if param['interactive'] == False:
        matplotlib.use('Agg')
        print "Switching backend to Agg. Batch execution"
    import matplotlib.pyplot as plt
    from helpers.plotter import EcellPlotter
    import helpers
    loader = helpers.Loader()

#    ecellManager = testChangeCalciumValue(interval, caValue)
    if param['running_type'] == 'train':
        ecellManager = testCalciumTrain(param['num_spikes'],
                                        param['delay'],
                                        param['biochemical_filename'])
    

    ecp = EcellPlotter()
    if param['interactive'] == False:
        dir = loader.create_new_dir(prefix=os.getcwd())
        loader.save(ecellManager.timeCourses,  dir, "timeCourses")
        ecp.plot_timeCourses(ecellManager.timeCourses, save=True, dir=dir)
        ecp.plot_weight(ecellManager.timeCourses, dir=dir)
    else:
        ecp.plot_timeCourses(ecellManager.timeCourses)
        ecp.plot_weight(ecellManager.timeCourses)
        plt.show()
