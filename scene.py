from manim import *
from matplotlib.pyplot import fill
import numpy as np
from Node import Node

class NetworkTest(object):
    def __init__(self,nodes,origin,scale):
        self.origin = origin
        self.scale = scale

        self.nodes = nodes

        self.points = []
        for i in range(len(self.nodes)):
            pos = self.nodes[i].pos*self.scale+self.origin
            fill_color = WHITE if self.nodes[i].static else BLACK
            self.points.append( Circle(radius=0.08,color=WHITE,arc_center=pos,fill_opacity=1,fill_color=fill_color) )

        self.lines = []
        for i in range(len(self.points)-1):
            for j in range(i+1,len(self.points)):
                if self.nodes[j].name in self.nodes[i].bound:
                    self.lines.append( Line(start=self.points[i].get_center(),end=self.points[j].get_center(),color=WHITE) )

        self.linegroup = VGroup()
        self.linegroup.add(*self.lines)

        self.pointgroup = VGroup()
        self.pointgroup.add(*self.points)

        self.previous_forces = np.ones((len(self.points),3))

    def update_values(self,runtime_type,runtime_num=1):
        if runtime_type == 'given':
            runtime = runtime_num
        if runtime_type == 'relative_distance':
            distance = np.sum([ np.linalg.norm(self.points[i].get_center()-(self.nodes[i].pos*self.scale+self.origin)) for i in range(len(self.nodes)) ])
            runtime = distance / runtime_num
        print(np.sum([ np.linalg.norm(self.points[i].get_center()-(self.nodes[i].pos*self.scale+self.origin)) for i in range(len(self.nodes)) ]))
        points = []
        for i in range(len(self.nodes)):
            pos = self.nodes[i].pos*self.scale+self.origin
            fill_color = WHITE if self.nodes[i].static else BLACK
            points.append( Circle(radius=0.08,color=WHITE,arc_center=pos,fill_opacity=1,fill_color=fill_color) )

        lines = []
        for i in range(len(points)-1):
            for j in range(i+1,len(points)):
                if self.nodes[j].name in self.nodes[i].bound:
                    lines.append( Line(start=points[i].get_center(),end=points[j].get_center(),color=WHITE) )

        pointgroup = VGroup()
        pointgroup.add(*points)

        linegroup = VGroup()
        linegroup.add(*lines)

        return (Transform(self.pointgroup,pointgroup,run_time=runtime),Transform(self.linegroup,linegroup,run_time=runtime)),runtime

    def move_nodes(self,t,mult,soft):
        forces = np.array([P.force(t,mult,soft) for P in self.nodes])
        consistency = np.sum(forces * self.previous_forces) / np.linalg.norm(forces) / np.linalg.norm(self.previous_forces)
        self.previous_forces = forces
        for i in range(len(forces)):
            self.nodes[i].moveBy(forces[i])
        size = sum([P.selfSize() for P in self.nodes])
        delay = sum([P.selfDelay() for P in self.nodes])
        return size,delay,consistency

    def move_until_static(self,t,mult,soft,min_run,max_run):
        sizes = []
        delays = []
        size,delay,consistency = self.move_nodes(t,mult,soft)
        sizes.append(size)
        delays.append(delay)
        consitency = 1
        while (consistency > -0.2 or len(sizes)<min_run) and len(sizes)<max_run:
            size,delay,consistency = self.move_nodes(t,mult,soft)
            sizes.append(size)
            delays.append(delay)
        return sizes,delays,len(sizes)

    def getDelay(self):
        total = 0
        for point in self.nodes:
            total += point.selfDelay()
        return total

    def getSize(self):
        total = 0
        for point in self.nodes:
            total += point.selfSize()
        return total

class SquareHex(Scene):
    def construct(self):
        A = Node('A',np.array([0,0,0]),True)
        B = Node('B',np.array([1,0,0]),True)
        C = Node('C',np.array([1,1,0]),True)
        D = Node('D',np.array([0,1,0]),True)

        O1 = Node('O1',np.array([0.3,0.3,0]),False)
        O2 = Node('O2',np.array([0.5,0.4,0]),False)
        O3 = Node('O3',np.array([0.7,0.3,0]),False)

        P1 = Node('P1',np.array([0.3,0.7,0]),False)
        P2 = Node('P2',np.array([0.5,0.6,0]),False)
        P3 = Node('P3',np.array([0.7,0.7,0]),False)

        A.bindTo(O1,3)
        B.bindTo(O3,3)
        O1.bindTo(O2,2)
        O1.bindTo(O3,1)
        O3.bindTo(O2,2)
        O2.bindTo(P2,4)
        P2.bindTo(P1,2)
        P1.bindTo(P3,1)
        P2.bindTo(P3,2)
        P1.bindTo(D,3)
        P3.bindTo(C,3)

        nodes = [A,B,C,D,O1,O2,O3,P1,P2,P3]

        network = NetworkTest(nodes,np.array([-6.5,-3,0]),6)

        self.add(network.pointgroup)
        self.add(network.linegroup)
        
        sizes,delays,count = network.move_until_static(0,0.002,0.001,10,200)
        anims,runtime = network.update_values('relative_distance',1)

        self.play( *anims )

        for t in np.linspace(0.7,0.9,100):
            sizes,delays,count = network.move_until_static(t,0.002,0.001,10,200)
            anims,runtime = network.update_values('relative_distance',1)
            self.play( *anims )

class SquareOct(Scene):
    def construct(self):
        A = Node('A',np.array([0,0,0]),True)
        B = Node('B',np.array([1,0,0]),True)
        C = Node('C',np.array([1,1,0]),True)
        D = Node('D',np.array([0,1,0]),True)

        A1 = Node('A1',np.array([0.3,0.3,0]),False)
        B1 = Node('B1',np.array([0.7,0.3,0]),False)

        A2 = Node('A2',np.array([0.4,0.4,0]),False)
        B2 = Node('B2',np.array([0.6,0.4,0]),False)

        C2 = Node('C2',np.array([0.6,0.6,0]),False)
        D2 = Node('D2',np.array([0.4,0.6,0]),False)

        C1 = Node('C1',np.array([0.7,0.7,0]),False)
        D1 = Node('D1',np.array([0.3,0.7,0]),False)

        A1.bindTo(A,3)
        B1.bindTo(B,3)
        A1.bindTo(B1,1)

        A1.bindTo(A2,2)
        B1.bindTo(B2,2)

        A2.bindTo(C2,1)
        A2.bindTo(D2,1)
        B2.bindTo(C2,1)
        B2.bindTo(D2,1)

        C1.bindTo(C,3)
        D1.bindTo(D,3)
        C1.bindTo(D1,1)

        C1.bindTo(C2,2)
        D1.bindTo(D2,2)

        nodes = [A,B,C,D,A1,A2,B1,B2,C1,C2,D1,D2]

        network = NetworkTest(nodes,np.array([-3,-3,0]),6)

        self.add(network.pointgroup)
        self.add(network.linegroup)

        
        sizes,delays,count = network.move_until_static(0,0.002,0.001,10,200)
        anims = network.update_values('relative_distance',1)

        self.play( anims[0] , anims[1] )

        for t in np.linspace(0.7,0.9,100):
            sizes,delays,count = network.move_until_static(t,0.002,0.001,10,200)
            anims = network.update_values('relative_distance',1)
            self.play( anims[0] , anims[1] )