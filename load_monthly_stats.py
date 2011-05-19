from monkey import Monkey
import datetime
import cPickle as pickle
                        
transform_map = [   lambda x:datetime.datetime.strptime(x, '%Y_%m'), 
                    lambda x: int(x),
                    lambda x: int(x),
                    lambda x: int(x),
                    lambda x: int(x),
                    lambda x: int(x),
                    lambda x: float(x),
                    lambda x: None,
                    lambda x: None
                ]

def load_from_csv(filename):
    csv = open(filename)
    orig_fields = csv.readline().strip().split(',')
    print orig_fields
    #fields = [field_map[of] for of in orig_fields]
    monthly = {}
    for line in csv.readlines():
        vals = line.strip().split(',')
        vs = [tm(v) for tm, v in zip(transform_map, vals)]
        print vs
        monthly[vs[0]] = vs
    return monthly
        
if __name__ == '__main__':
    m = load_from_csv('data/clean_summary.csv')
    pickle.dump(m, open("monthly.pkl", "w"))
