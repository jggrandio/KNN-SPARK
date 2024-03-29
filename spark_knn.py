#Fastest way until now
from pyspark import SparkContext, SparkConf
import time
import sys

start = time.time()

def distances (dt):
    idts = dt[1]
    l = len (dt[0])-1
    ts = list(map(float, dt[0][0:l]))
    cltr = int(dt[0][l])
    
    
    x = [(float('inf'),0)]*k.value
    
    for i in tr:
        if not idts == i[1]:
            dist = sum((p-q)*(p-q) for p, q in zip(i[0][0:l], ts))
            if dist < x[len(x)-1][0]:
                for j in range(len(x)):
                    if dist < x[j][0]:
                        x.insert(j,(dist,i[0][l]))
                        x.pop()
                        break
                
    return (cltr,x)
def guess_class(dt):
    rclass = dt[0]
    freq = 0
    predict = 0
    for i in range(len(dt[1])):
        tfreq = 1
        tpredict = dt[1][i][1]
        for j in range(i+1,len(dt[1])):
            if tpredict == dt[1][j][1]:
                tfreq +=1
        if tfreq > freq:
            predict = tpredict
            freq = tfreq
    return (rclass,predict)

def correct(dt):
    if dt[0]==dt[1]:
        return 1
    else:
        return 0

dataset = sys.argv[1]
partitions = int(sys.argv[3])

sc = SparkContext.getOrCreate()
ts = sc.textFile(dataset,partitions).zipWithUniqueId()\
    .map(lambda line: (line[0].split(','), line[1]))\
    .map(lambda line: (list(map(float, line[0])),line[1]))


tr = ts.collect()
k = sc.broadcast(int(sys.argv[2]))


k_vals = ts.map(distances)
guess_class = k_vals.map(guess_class)
correct = guess_class.map(correct)
accuracy = correct.mean()
end = time.time()
print('The time to run is:', end - start)
print(accuracy)
