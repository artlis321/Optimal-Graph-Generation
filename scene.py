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

    def update_values(self,runtime):
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

        return Transform(self.pointgroup,pointgroup,run_time=runtime),Transform(self.linegroup,linegroup,run_time=runtime)

    def move_nodes(self,t,mult,soft):
        forces = [P.force(t,mult,soft) for P in self.nodes]
        for i in range(len(forces)):
            self.nodes[i].moveBy(forces[i])
        size = sum([P.selfSize() for P in self.nodes])
        delay = sum([P.selfDelay() for P in self.nodes])
        print(size,"|",delay)

class Test(Scene):
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

        network = NetworkTest(nodes,np.array([-3,-3,0]),6)

        self.add(network.pointgroup)
        self.add(network.linegroup)

        for i in range(100):
            network.move_nodes(0,0.02,0.01)
        anims = network.update_values(1)

        self.play( anims[0] , anims[1] )

        for t in np.linspace(0.7,0.8,100):
            for j in range(100):
                network.move_nodes(t,0.001,0.001)
            anims = network.update_values(3/60)
            self.play( anims[0] , anims[1] )