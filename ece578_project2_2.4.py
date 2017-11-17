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
        count = 0
        for rownum in rows:
            row = self.ASdata[rownum-rowminus]
            self.ASdata = np.delete( self.ASdata, rownum-rowminus, axis=0 )
            rowminus+=1

            if row[2] == PEER:
                self.add_peer(row[1])
            else:
                self.add_subcone( row[1] )
            count+=1
        del self.othercones
        del self.ASdata

    

    def add_subcone(self, AS):
        print "{} is looking for {}".format( self.AS, AS),

        if self.hasSubcone(AS):
            return None
        
        subcone = None
        for cone in self.othercones:
            
            subcone = cone.hasSubcone(AS)

            if subcone is not None:
                print " found it",
                break


        if subcone is not None:
            self.cones.append(subcone)
            print " We already built it"

        else:
            print " Building it"
            self.cones.append( Cone(AS, self.ASdata, self.othercones) )

    def add_peer(self, peer):
        self.peers.append(peer)
    

    def hasSubcone( self, AS ):
        if AS == self.AS:
            return self
        for cone in self.cones:
            if cone.AS == AS:
                return cone
            else:
                resp = cone.hasSubcone( AS )
                if resp is None:
                    continue
                else:
                    return resp

    def hasPeer(self, AS):
        if AS == self.AS:
            return self

        for peer in self.peers:
            if peer.AS == AS:
                return peer
            else:
                resp = peer.hasPeer( AS )
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


def hasCone(AS, allcones):
    subcn = None
    for cn in allcones:
        subcn = cn.hasSubcone(AS)

        if subcn:
            break
    return subcn

def get_unprocessed(uprov, allcones):

    unproc = []
    sorted_uprov = uprov[uprov[:,1].argsort()][:,0]
    allcones_AS = [cn.AS for cn in allcones]
    for AS in sorted_uprov:
        if AS not in allcones_AS:
            unproc.append(AS)


    return np.array(unproc)


def get_all_cones(uprov_AS, ASdata, to=1, allcones=None):
    if allcones == None:
        allcones = []
    unproc =[]
    count = 0
    now = time.time()
    for AS in uprov_AS:
        try:
            with Timeout(to):
                allcones.append(Cone(AS, ASdata, allcones))
                print "processed {} number {} at time {}".format(AS, count, (time.time()-now)/60.0)
        except Timeout.Timeout:
            print "Could not process {} {} {}".format(count, AS, (time.time()-now)/60.0)
            
        count+=1

        unproc = np.array(unproc)
    
        yield allcones 
            
def get_unproc_degrank(unproc, data):
    deg = np.zeros( (unproc.shape[0],2), dtype=int )
    row = 0
    for AS in unproc:
        deg[row, 0] = AS
        deg[row, 1]=data[ np.where(data[:,0] == AS) ].shape[0]
        row+=1
    deg = deg[deg[:,1].argsort()]
    return deg


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

            
        


def reduce_data( data, allcones ):
    ASdata = data[:]
    count = 0
    for cone in allcones:
        rownum = 0
        remove = False
        for row in ASdata:
            if cone.hasSubcone( row[0] ):
                remove = True
                AS=row[0]
                break
            rownum+=1
        if remove:
            print 100*float(count)/len(allcones), ASdata.shape, np.where(ASdata[:,0] == AS)[0].shape
            ASdata = np.delete( ASdata, np.where(ASdata[:,0] == AS), axis=0 )
        count+=1


    return ASdata



def main(  ):
    ASdata = get_data_from_file()
    

def test_to():
        try:
            with Timeout(0.1):
                time.sleep(1.0)
                print a

        except Timeout.Timeout:
            print "timeout"

