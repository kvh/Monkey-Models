filename = 'data/summary_total_numbers.csv'
f = open(filename)
o = open('data/clean_summary.csv', 'w')
for l in f.readlines():
    l =l.replace('\r', '\n')
    print l
    o.write(l)
o.close()

    