import numpy as np
import signal
import time

PROVIDER = -1
PEER = 0


class Timeout():
    """Timeout class using ALARM signal."""
    class Timeout(Exception):
        pass
 
    def __init__(self, sec):
        self.sec = sec
 
    def __enter__(self):
        signal.signal(signal.SIGALRM, self.raise_timeout)
        signal.setitimer(signal.ITIMER_REAL, self.sec)
 
    def __exit__(self, *args):
        signal.alarm(0)    # disable alarm
 
    def raise_timeout(self, *args):
        raise Timeout.Timeout()

class Cone:

    def __init__(self, AS, ASdata, othercones=None):
        if othercones == None:
            othercones = []
        self.othercones = othercones
        self.AS = AS
        self.ASdata = ASdata[:] #deep copy
        self.peers = []
        self.cones = []
        rows = np.where(self.ASdata[:,0] == AS)[0]
        rowminus = 0
        for rownum in rows:
            row = self.ASdata[rownum-rowminus]
            self.ASdata = np.delete( self.ASdata, rownum-rowminus, axis=0 )
            rowminus+=1

            if row[2] == PEER:
                self.add_peer(row[1])
            else:
                self.add_subcone( row[1] )

        del self.othercones
        del self.ASdata

    

    def add_subcone(self, AS):
        subcone = None
        for cone in self.othercones:
            subcone = cone.hasSubcone(AS)
            if subcone:
                break

        if subcone:
	    print("got one!")
            self.cones.append(subcone) 
        else:
            self.cones.append( Cone(AS, self.ASdata, self.othercones) )

    def add_peer(self, peer):
        self.peers.append(peer)
    

    def hasSubcone( self, AS ):
        for cone in self.cones:
            if cone.AS == AS:
                return cone
            else:
                resp = cone.hasSubcone( AS )
                if resp is None:
                    continue
                else:
                    return resp
    

    def __len__(self):

        length = len(self.cones)
        for cn in self.cones:
            
            length+=len(cn)

        return length

    def __repr__( self ):
        return "<cone of {} len={}>".format(self.AS, self.__len__())


def get_data_from_file(datfile="20170901.as-rel2.txt"):
    outarr = []
    with open(datfile) as datafd:
        for line in datafd:
            if not line.startswith("#"):
                outarr.append( [int(val) for val in line.split("|")[:-1] ] )

    return np.array( outarr )



def get_unique_providers(ASdata):
    providers = ASdata[np.where(ASdata[:,2] == -1)]
    
    return providers[np.unique(providers[:,0], return_index=True)[1]]



def get_all_cones(uprov_AS, ASdata, to=1, allcones=None):
    if allcones == None:
        allcones = []
    unproc =[]
    count = 0
    for AS in uprov_AS:
        try:
            with Timeout(to):
                allcones.append(Cone(AS, ASdata, allcones))
        except Timeout.Timeout:
            print "Could not process {} {}".format(count, AS)
            unproc.append(AS)
        count+=1

    unproc = np.array(unproc)
    
    return allcones, unproc
            

def get_slow_cones( AS, cones ):


    for cn in cones:
        if cn.AS == AS:
            return cn
        else:
            
            resp = get_slow_cones(AS, cn.cones)
            if resp is None:
                continue
            else:
                return resp

            
        




def main(  ):
    ASdata = get_data_from_file()
    

def test_to():
        try:
            with Timeout(0.1):
                time.sleep(1.0)
                print a

        except Timeout.Timeout:
            print "timeout"

