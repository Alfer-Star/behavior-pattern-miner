import unittest
import subprocess
from os import makedirs
from genericpath import exists

from src.subgraph_mining import createSubdueInputFile
from src.subgraph_mining import getSubGraphs

# Testfall aus Beispiel in Diamantini et al 2016

ig1Nodes = {'M3RR', 'M1WD', 'M2WD',  'M5RD', 'M4WC'}
ig1Edges = {('M3RR', 'M1WD'),
            ('M3RR', 'M2WD'), ('M2WD', 'M5RD'), ('M1WD', 'M5RD'), ('M5RD', 'M4WC')}
ig1 = (ig1Nodes, ig1Edges, dict())

ig2Nodes = {'M3RR', 'M1WD', 'M2WD',  'M3RD', 'M6WC'}
ig2Edges = {('M3RR', 'M1WD'),
            ('M3RR', 'M2WD'), ('M2WD', 'M3RD'), ('M1WD', 'M3RD'), ('M3RD', 'M6WC')}
ig2 = (ig2Nodes, ig2Edges, dict())

ig3Nodes = {'M6RR', 'M3WD', 'M5RD', 'M4WC'}
ig3Edges = {('M6RR', 'M3WD'),
            ('M3WD', 'M5RD'), ('M5RD', 'M4WC')}
ig3 = (ig3Nodes, ig3Edges, dict())

bp1 = ({'M3RR', 'M1WD', 'M2WD'}, {('M3RR', 'M1WD'),
                                  ('M3RR', 'M2WD'), ('M2WD', 'M3RD')}, dict())
bp2 = ({'M5RD', 'M4WC'}, {('M5RD', 'M4WC')}, dict())
bp3 = ({'M3RD', 'BP1'}, {('M3RD', 'BP1')}, dict())
bp4 = ({'BP1', 'BP2'}, {('BP1', 'BP2')}, dict())
expectedBPs = [bp1, bp2, bp3, bp4]

pathToSubdue = '/home/adrian/Schreibtisch/behavior-pattern-miner/subdue-5.2.2/bin/subdue'


class TestInstanceGraphRepairNew(unittest.TestCase):
    def test_BP_with_Dot_Formatter(self):
        self.fail('test with graphviz transformation not finished')
        igs = [ig1, ig2, ig3]
        outputFilePath = 'output/test/subdueGraphs.g'
        inputFilePath = '/home/adrian/Schreibtisch/behavior-pattern-miner/output/test/subdueGraphs.g'
        # TODO: GraphViz Input Files!
        # TODO: Transform Graphviz Files to Subdue Format with Subdue Functions
        self.failIf(not exists(pathToSubdue),
                    'test_BP_with_own_formatter: cannot run. Did not find Subdue install Subdue, see ReadMe or check if pathToSubdue is correct (probably not).')
        subprocess.check_output(
            [
                pathToSubdue,
                '-beam', '4',
                '-compress',
                '-eval', '1',
                '-iterations', '0',
                '-output', '4',
                '-threshold', '0.9',
                '-out', outputFilePath,
                inputFilePath
            ])
        BPs = list()
        self.assertEqual(BPs, expectedBPs)

    def test_BP_with_own_formatter(self):
        igs = [ig1, ig2, ig3]
        igDict = {'variant'+i: igs[i] for i in range(2)}
        outputFilePath = 'output/test/subdueGraphs.g'
        inputFilePath = '/home/adrian/Schreibtisch/behavior-pattern-miner/output/test/subdueGraphs.g'
        createSubdueInputFile(igDict, outputFilePath)
        self.failIf(not exists(pathToSubdue),
                    'test_BP_with_own_formatter: cannot run. Did not find Subdue install Subdue, see ReadMe or check if pathToSubdue is correct (probably not).')
        subprocess.check_output(
            [
                pathToSubdue,
                '-beam', '4',
                '-compress',
                '-eval', '1',
                '-iterations', '0',
                '-output', '4',
                '-threshold', '0.9',
                '-out', outputFilePath,
                inputFilePath
            ])
        BPs = list()
        self.assertEqual(BPs, expectedBPs)


if __name__ == '__main__':
    unittest.main()
