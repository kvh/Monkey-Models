from monkey import Monkey
import datetime
#import matplotlib.pyplot as plt
#import networkx as nx
import os,time
import cPickle as pickle
#import pylab
from collections import defaultdict

def load_from_grooming_csv(filename):
    csv = open(filename)
    names = csv.readline().strip().split(',')[1:]
    #g = nx.DiGraph()
    #g.add_nodes_from(names)
    tot = 0
    recip = defaultdict(int)
    for line in csv.readlines():
        s = line.strip().split(',')
        name = s[0]
        counts = s[1:]
        for n, c in zip(names, counts):
			c = int(c)
			
			if c > 0:     
			    tot += 1
			    recip[','.join(list(set([n, name])))]   += 1
				#g.add_edge(name, n, weight=c)
    #print "avg deg", tot/float(len(names))
    rr = 0
    if tot:
        rr = sum([r > 1 for r in recip.values()])/float(tot)
    print "recip", rr
    d = tot/float(len(names) * (len(names) - 1))
    #print "density", d
    #return g
    return rr
        

def make_grooming_gif(graphs):
    
    pylab.ion()
    gs = graphs.items()
    gs.sort()
    i=0
    for d, g in gs:
        i+=1
        print d        
        nx.draw_circular(g)
        pylab.suptitle(d.date())
        pylab.draw()
        pylab.savefig("troop_%02d.png"%i)
        #time.sleep(.5)
        pylab.clf()
    
    for g in graphs.values():
        print sum([g.degree(n) for n in g.nodes()])/float(g.order())
        

    
        
if __name__ == '__main__':
    dir_name = 'data/Grooming_adult_females_95-99/'
    graphs = {}
    fs = os.listdir(dir_name)
    n = 0
    dd = 0
    for fname in fs:
        try:
            dt = datetime.datetime.strptime(fname, 'Grooming_adult_females_%Y_%m.csv')
        except ValueError:
            continue
        n += 1
        dd += load_from_grooming_csv(dir_name + fname)
    print "avg dens", dd/ float(n)
    pickle.dump(graphs, open("groom_graphs.pkl", "w"))

    
    
    
