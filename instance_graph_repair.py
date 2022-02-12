import unittest
from pm4py.objects.log.obj import Trace

from src.instance_graph_repair import repairDeletionEvent
from src.instance_graph_repair import repairInsertedEvent

# Testfall aus Diamantini
insertion = [('M3WR', 'M4RR1'), ('M3WR', 'M4RR2'), ('M4RR1', 'M1WD'), ('M4RR1', 'M2WD'),
             ('M1WD', 'M5RD'), ('M2WD', 'M5RD'), ('M5RD', 'M4WC'), ('M4WC', 'M1TC')]
deletion = [('M3WR', 'M4RR'), ('M4RR', 'M1WD'),
            ('M4RR1', 'M2WD'), ('M4WC', 'M1TC')]

nodesIns = ['M3WR', 'M4RR1', 'M1WD', 'M2WD', 'M4RR2', 'M5RD', 'M4WC', 'M1TC']
nodesDel = ['M3WR', 'M4RR1', 'M4RR2', 'M1WD', 'M2WD', 'M4WC', 'M1TC']

cr = [('M3WR', 'M4RR', 0), ('M4RR', 'M1WD', 0), ('M4RR', 'M2WD', 0),
      ('M1WD', 'M5RD', 0), ('M2WD', 'M5RD', 0), ('M5RD', 'M4WC', 0), ('M4WC', 'M1TC', 0)]

traceIns = Trace([{'concept:name': eventname, 'time:timestamp': index,
                 'lifecycle:transition': 'complete'} for index, eventname in enumerate(nodesIns)])
traceDel = Trace([{'concept:name': eventname, 'time:timestamp': index,
                 'lifecycle:transition': 'complete'} for index, eventname in enumerate(nodesDel)])
# Should

shouldEdgesIns = {('M3WR', 'M4RR1'), ('M4RR1', 'M1WD'), ('M4RR1', 'M2WD'),
                  ('M1WD', 'M4RR2'), ('M2WD', 'M4RR2'), ('M4RR2', 'M5RD'), ('M5RD', 'M4WC'), ('M4WC', 'M1TC')}
shouldEdgesDel = {('M3WR', 'M4RR'), ('M4RR', 'M1WD'),
                  ('M4RR1', 'M2WD'), ('M2WD', 'M4WC'), ('M1WD', 'M4WC'), ('M4WC', 'M1TC')}


class TestInstanceGraphRepair(unittest.TestCase):
    def test_deletion_repair(self):
        deletion = [('M3WR', 'M4RR'), ('M4RR', 'M1WD'),
                    ('M4RR1', 'M2WD'), ('M4WC', 'M1TC')]
        nodesDel = ['M3WR', 'M4RR1', 'M4RR2', 'M1WD', 'M2WD', 'M4WC', 'M1TC']
        cr = [('M3WR', 'M4RR', 0), ('M4RR', 'M1WD', 0), ('M4RR', 'M2WD', 0),
              ('M1WD', 'M5RD', 0), ('M2WD', 'M5RD', 0), ('M5RD', 'M4WC', 0), ('M4WC', 'M1TC', 0)]
        # Should
        shouldEdgesDel = {('M3WR', 'M4RR'), ('M4RR', 'M1WD'),
                          ('M4RR1', 'M2WD'), ('M2WD', 'M4WC'), ('M1WD', 'M4WC'), ('M4WC', 'M1TC')}
        self.assertEqual(repairDeletionEvent(
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

        self.assertEqual(repairInsertedEvent(
            set(insertion), 'M4RR2', traceIns, 4), shouldEdgesIns)

    def test_insertion_repair_lifecycles(self):
        insertion = [('M3WR', 'M4RR1'), ('M3WR', 'M4RR2'), ('M4RR1', 'M1WD'), ('M4RR1', 'M2WD'),
                     ('M1WD', 'M5RD'), ('M2WD', 'M5RD'), ('M5RD', 'M4WC'), ('M4WC', 'M1TC')]
        nodesIns = ['M3WR', 'M4RR1', 'M1WD',
                    'M2WD', 'M4RR2', 'M5RD', 'M4WC', 'M1TC']

        def f(eventname, index): return [{'concept:name': eventname, 'time:timestamp': index,
                                          'lifecycle:transition': 'start'}, {'concept:name': eventname, 'time:timestamp': index + 0.5,
                                                                             'lifecycle:transition': 'complete'}]
        traceIns = Trace([event for index, eventname in enumerate(
            nodesIns) for event in f(eventname, index)])
        # Should
        shouldEdgesIns = {('M3WR', 'M4RR1'), ('M4RR1', 'M1WD'), ('M4RR1', 'M2WD'),
                          ('M1WD', 'M4RR2'), ('M2WD', 'M4RR2'), ('M4RR2', 'M5RD'), ('M5RD', 'M4WC'), ('M4WC', 'M1TC')}

        self.assertEqual(repairInsertedEvent(
            set(insertion), 'M4RR2', traceIns, 8), shouldEdgesIns)


if __name__ == '__main__':
    unittest.main()
