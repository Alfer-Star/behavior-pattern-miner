import unittest
from pm4py.objects.log.obj import Trace

from src.instance_graph_repair_new import repairDeletionEvent as repairDeletionEventNew
from src.instance_graph_repair_new import repairInsertedEvent as repairInsertedEventNew

from src.instance_graph_new import genInstanceGraph as genInstanceGraphNew

# Testfall aus Diamantini


def generateLifecyleTrace(nodes):
    def f(eventname, index): return [{'concept:name': eventname, 'time:timestamp': index,
                                      'lifecycle:transition': 'start'}, {'concept:name': eventname, 'time:timestamp': index + 0.5,
                                                                         'lifecycle:transition': 'complete'}]
    return Trace([event for index, eventname in enumerate(
        nodes) for event in f(eventname, index)])


class TestInstanceGraphRepairNew(unittest.TestCase):
    def test_deletion_repair(self):
        deletion = [('M3WR', 'M4RR'), ('M4RR', 'M1WD'),
                    ('M4RR1', 'M2WD'), ('M4WC', 'M1TC')]
        nodesDel = ['M3WR', 'M4RR1', 'M4RR2', 'M1WD', 'M2WD', 'M4WC', 'M1TC']
        cr = [('M3WR', 'M4RR', 0), ('M4RR', 'M1WD', 0), ('M4RR', 'M2WD', 0),
              ('M1WD', 'M5RD', 0), ('M2WD', 'M5RD', 0), ('M5RD', 'M4WC', 0), ('M4WC', 'M1TC', 0)]
        # Should
        shouldEdgesDel = {('M3WR', 'M4RR'), ('M4RR', 'M1WD'),
                          ('M4RR1', 'M2WD'), ('M2WD', 'M4WC'), ('M1WD', 'M4WC'), ('M4WC', 'M1TC')}
        self.assertEqual(repairDeletionEventNew(
            set(nodesDel), set(deletion), 'M5RD', cr, 1), shouldEdgesDel)

    def test_insertion_repair(self):
        insertion = [('M3WR', 'M4RR1'), ('M3WR', 'M4RR2'), ('M4RR1', 'M1WD'), ('M4RR1', 'M2WD'),
                     ('M1WD', 'M5RD'), ('M2WD', 'M5RD'), ('M5RD', 'M4WC'), ('M4WC', 'M1TC')]
        nodesIns = ['M3WR', 'M4RR1', 'M1WD',
                    'M2WD', 'M4RR2', 'M5RD', 'M4WC', 'M1TC']
        traceIns = Trace([{'concept:name': eventname, 'time:timestamp': index,
                           'lifecycle:transition': 'complete'} for index, eventname in enumerate(nodesIns)])
        # Should
        shouldEdgesIns = {('M3WR', 'M4RR1'), ('M4RR1', 'M1WD'), ('M4RR1', 'M2WD'),
                          ('M1WD', 'M4RR2'), ('M2WD', 'M4RR2'), ('M4RR2', 'M5RD'), ('M5RD', 'M4WC'), ('M4WC', 'M1TC')}

        self.assertEqual(repairInsertedEventNew(
            set(insertion), 'M4RR2', traceIns, 4), shouldEdgesIns)

    def test_insertion_repair_lifecycles(self):
        insertion = [('M3WR', 'M4RR1'), ('M3WR', 'M4RR2'), ('M4RR1', 'M1WD'), ('M4RR1', 'M2WD'),
                     ('M1WD', 'M5RD'), ('M2WD', 'M5RD'), ('M5RD', 'M4WC'), ('M4WC', 'M1TC')]
        nodesIns = ['M3WR', 'M4RR1', 'M1WD',
                    'M2WD', 'M4RR2', 'M5RD', 'M4WC', 'M1TC']

        traceIns = generateLifecyleTrace(nodesIns)
        # Should
        shouldEdgesIns = {('M3WR', 'M4RR1'), ('M4RR1', 'M1WD'), ('M4RR1', 'M2WD'),
                          ('M1WD', 'M4RR2'), ('M2WD', 'M4RR2'), ('M4RR2', 'M5RD'), ('M5RD', 'M4WC'), ('M4WC', 'M1TC')}

        self.assertEqual(repairInsertedEventNew(
            set(insertion), 'M4RR2', traceIns, 8), shouldEdgesIns)


class TestInstanceGraphNewGen(unittest.TestCase):
    def test_insertion_IG_gen(self):
        activities = ['WR', 'RR', 'WD', 'WD', 'RR', 'RD', 'WC', 'TC']
        oragUnits = ['M3', 'M4', 'M1', 'M2', 'M4', 'M5', 'M4', 'M1']
        orgaDict = {oragUnit: oragUnit for oragUnit in oragUnits}
        trace = Trace([{'concept:name': activities[i], 'time:timestamp': i, 'org:resource':oragUnits[i],
                        'lifecycle:transition': 'start'} for i in range(len(activities))])
        cr = set([('WR', 'RR', 0), ('RR', 'WD', 0), ('RR', 'WD', 0),
                  ('WD', 'RD', 0), ('WD', 'RD', 0), ('RD', 'WC', 0), ('WC', 'TC', 0)])

        # should
        # ignore Case if two appearence, First Appearence has also an index appendix
        nodes = set(['M3WR', 'M4RR', 'M1WD', 'M2WD',
                     'M4RR2', 'M5RD', 'M4WC', 'M1TC'])
        edges = set([('M3WR', 'M4RR'), ('M3WR', 'M4RR2'), ('M4RR', 'M1WD'), ('M4RR', 'M2WD'),
                    ('M1WD', 'M5RD'), ('M2WD', 'M5RD'), ('M5RD', 'M4WC'), ('M4WC', 'M1TC')])

        #nodeEventDict = {nodes[i]: trace[i] for i in range(len(trace))}
        igraph = genInstanceGraphNew(
            trace, cr, orgaDict)
        self.assertEqual(igraph[0], nodes)
        self.assertEqual(igraph[1], edges)

    def test_deletion_IG_gen(self):
        #'M3WR', 'M4RR1', 'M1WD', 'M2WD', 'M4WC', 'M1TC'
        activities = ['WR', 'RR', 'WD', 'WD', 'WC', 'TC']
        oragUnits = ['M3', 'M4', 'M1', 'M2', 'M4', 'M1']
        orgaDict = {oragUnit: oragUnit for oragUnit in oragUnits}
        trace = Trace([{'concept:name': activities[i], 'time:timestamp': i, 'org:resource':oragUnits[i],
                        'lifecycle:transition': 'start'} for i in range(len(activities))])
        cr = set([('WR', 'RR', 0), ('RR', 'WD', 0), ('RR', 'WD', 0),
                  ('WD', 'RD', 0), ('WD', 'RD', 0), ('RD', 'WC', 0), ('WC', 'TC', 0)])

        # should
        nodes = set(['M3WR', 'M4RR', 'M1WD', 'M2WD', 'M4WC', 'M1TC'])
        edges = set([('M3WR', 'M4RR'), ('M4RR', 'M1WD'),
                    ('M4RR', 'M2WD'), ('M4WC', 'M1TC')])
        #nodeEventDict = {nodes[i]: trace[i] for i in range(len(trace))}
        igraph = genInstanceGraphNew(
            trace, cr, orgaDict)
        self.assertEqual(igraph[0], nodes)
        self.assertEqual(igraph[1], edges)


if __name__ == '__main__':
    unittest.main()
