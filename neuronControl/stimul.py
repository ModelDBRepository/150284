# Author Michele Mattioni   
# Tue Oct  6 08:01:52 BST 2009

class Stimul(object):
    """Store the inputs we are going to deliver to the different synapses"""
    def __init__(self, time, number, interval, chan_type, noise=0):
        """
        Initialize the stimul class
        
        Params:
        time: first time the input is deployed, in seconds
        number: numbers of repetition of the pulses
        interval: Interval between the pulses. In seconds
        chan_type: the type (AMPA or NMDA)
        """
        
        self.time = time * 1e3 
        self.number = number
        self.chan_type = chan_type
        self.noise = noise
        self.interval = interval * 1e3
        
#        self.spine = None #Used for logging
    def get_stims_time(self):
        """
        Calculate the list of all the stims time.
        
        Return the list of all the stimul applied in this stimuli.
        """
        stims_time = []
        for i in range(self.number):
            if not stims_time: 
                stims_time.append(self.time + self.interval)
            else: #List contains at least one el. Adding from there.
                stims_time.append(stims_time[-1] + self.interval)
        return stims_time
            
    
    def to_log(self):
        s = "spine %s, time %s [ms], number %s\n" %(self.spine, self.time, self.number)
        return s 