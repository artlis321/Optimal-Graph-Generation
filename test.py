from Node import Node
import numpy as np

A = Node('A',np.array([0,0]),True)
B = Node('B',np.array([1,0]),True)
C = Node('C',np.array([1,1]),True)
D = Node('D',np.array([0,1]),True)

O1 = Node('O1',np.array([0.3,0.3]),False)
O2 = Node('O2',np.array([0.5,0.4]),False)
O3 = Node('O3',np.array([0.7,0.3]),False)

P1 = Node('P1',np.array([0.3,0.7]),False)
P2 = Node('P2',np.array([0.5,0.6]),False)
P3 = Node('P3',np.array([0.7,0.7]),False)

A.bindTo(O1,3)
B.bindTo(O3,3)
O1.bindTo(O2,2)
O1.bindTo(O3,1)
O3.bindTo(O2,2)
O2.bindTo(P2,4)
P2.bindTo(P1,2)
P1.bindTo(P3,1)
P2.bindTo(P3,2)
P1.bindTo(C,3)
P3.bindTo(D,3)

points = [A,B,C,D,O1,O2,O3,P1,P2,P3]

mult = 1/500
soft = 1/200
t = 0.8

for i in range(0,3000):
    forces = [P.force(t,mult,soft) for P in points]
    for i in range(len(forces)):
        points[i].moveBy(forces[i])
    size = sum([P.selfSize() for P in points])
    delay = sum([P.selfDelay() for P in points])
    print(size,"|",delay)