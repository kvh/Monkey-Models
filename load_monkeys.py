from monkey import Monkey
import datetime

NA_STR = '\N'

field_map = dict(       sname='name',
                        sex='sex',
                        birth='birthdate',
                        statdate=None,
                        mom='mother',
                        dad='father',
                        birthyear=None)
                        
transform_map = dict(   sname=lambda x:x,
                        sex=lambda x:x.lower(),
                        birth=lambda x:datetime.datetime.strptime(x, '%m/%d/%y'),
                        statdate=lambda x:None,
                        mom=lambda x: None if x==NA_STR else x,
                        dad=lambda x: None if x==NA_STR else x,
                        birthyear=lambda x: None)

def load_from_biography_csv(filename):
    csv = open(filename)
    orig_fields = csv.readline().strip().split(',')
    #print orig_fields
    #fields = [field_map[of] for of in orig_fields]
    monkeys = []
    for line in csv.readlines():
        attrs = line.strip().split(',')
        args = dict([(field_map[f], transform_map[f](a)) for f, a in zip(orig_fields, attrs) if field_map[f] is not None])
        print args
        new_monkey = Monkey(**args)
        monkeys.append(new_monkey)
        
if __name__ == '__main__':
    load_from_biography_csv('data/clean_biography.csv')
