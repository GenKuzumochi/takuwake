import csv
import sys
from ortools.graph import pywrapgraph

if len(sys.argv) <= 1:
  print("python3 solve.py [卓1の枠] [卓2のPL枠] ...")
  sys.exit()

# read data.tsv
tsvFile = open("data.tsv")
tsv = csv.reader(tsvFile,delimiter = "\t")
tsv = [ x for x in tsv if x [1] != '']
count = len(tsv)

# start nodes
starts = sum(([x] * count for x in range(0,count+1)),[])
starts += (range(count+1,count+ 1 + count ))

# end nodes
ends = list(range(1,count+1))
ends += list(range(count+1,count+count+1)) * count
ends += [2*count+1]*count

# flow capacities
capacities  = [1] * len(starts)

# taku capacities
taku = [ int(x) for x in sys.argv[1:]]
taku_table = []
for i in range(len(taku)):
    taku_table += [i] * taku[i]

# flow costs
costs = [0] * count
for s in tsv:
    for i in range(0,len(taku)):
        costs += [-int(s[i+1]) ] * taku[i]
costs += [0] * count

print("PL Count" , count)
print("GM Capacity" , taku)

supplies = [count] + [0] * (count*2) + [-count]

# Instantiate a SimpleMinCostFlow solver.
min_cost_flow = pywrapgraph.SimpleMinCostFlow()

# Add each arc.
for i in range(0, len(starts)):
    min_cost_flow.AddArcWithCapacityAndUnitCost(starts[i], ends[i], capacities[i], costs[i])

# Add node supplies.

for i in range(0, len(supplies)):
    min_cost_flow.SetNodeSupply(i, supplies[i])
print(min_cost_flow.Solve())
if min_cost_flow.Solve() == min_cost_flow.OPTIMAL:
    print('Minimum cost:', min_cost_flow.OptimalCost())
    print('')
    print('  Arc    Flow / Capacity  Cost')
    for i in range(min_cost_flow.NumArcs()):
      cost = min_cost_flow.Flow(i) * min_cost_flow.UnitCost(i)
      if cost == 0:
        continue
      print('%2s %2s -> %2s   %3s  / %3s       %3s' % (
          min_cost_flow.Tail(i),
          tsv[min_cost_flow.Tail(i)-1][0],
          min_cost_flow.Head(i),
          min_cost_flow.Flow(i),
          min_cost_flow.Capacity(i),
          cost))
    for i in range(min_cost_flow.NumArcs()):
      cost = min_cost_flow.Flow(i) * min_cost_flow.UnitCost(i)
      if cost == 0:
        continue
      print('%s,%s' % (
          tsv[min_cost_flow.Tail(i)-1][0],
          taku_table[min_cost_flow.Head(i) - count - 1] + 1
      ))
else:
    print('There was an issue with the min cost flow input.')
