"""TestShortestPathGraph to check shortest path calculation of GeneralGraph"""

from unittest import TestCase
import copy
import multiprocessing as mp
from grape.general_graph import GeneralGraph
from grape.parallel_general_graph import ParallelGeneralGraph
from grape.fault_diagnosis import FaultDiagnosis


class TestShortestPathGraph(TestCase):
    """
	Class TestShortestPathGraph to check shortest path calculation
    of GeneralGraph
	"""

    @classmethod
    def setUpClass(cls):
        """
		Shortest paths for the toy graph:
		- 'initial': shortest paths before any perturbation
		- 'final_element_perturbation': shortest paths after
        element perturbation
		- 'final_area_perturbation': shortest paths after area perturbation
		"""
        cls.initial = {
            '1': {
				'1': ['1'],
				'2': ['1', '2'],
				'3': ['1', '3'],
				'4': ['1', '2', '4'],
				'5': ['1', '3', '5'],
				'6': ['1', '2', '4', '6'],
				'11': ['1', '3', '5', '11'],
				'7': ['1', '2', '4', '6', '7'],
				'8': ['1', '2', '4', '6', '8'],
				'19': ['1', '3', '5', '11', '19'],
				'9': ['1', '2', '4', '6', '8', '9'],
				'12': ['1', '3', '5', '11', '19', '12'],
				'14': ['1', '3', '5', '11', '19', '14'],
				'16': ['1', '2', '4', '6', '8', '9', '16'],
				'13': ['1', '3', '5', '11', '19', '12', '13'],
				'18': ['1', '3', '5', '11', '19', '14', '18'],
				'17': ['1', '2', '4', '6', '8', '9', '16', '17'],
				'10': ['1', '2', '4', '6', '8', '9', '16', '17', '10']
            },
            '2': {
				'2': ['2'],
				'4': ['2', '4'],
				'6': ['2', '4', '6'],
				'7': ['2', '4', '6', '7'],
				'8': ['2', '4', '6', '8'],
				'9': ['2', '4', '6', '8', '9'],
				'16': ['2', '4', '6', '8', '9', '16'],
				'17': ['2', '4', '6', '8', '9', '16', '17'],
				'10': ['2', '4', '6', '8', '9', '16', '17', '10'],
				'11': ['2', '4', '6', '8', '9', '16', '17', '10', '11'],
				'19': ['2', '4', '6', '8', '9', '16', '17', '10', '11', '19'],
				'12': ['2', '4', '6', '8', '9', '16', '17', '10', '11', '19', '12'],
				'14': ['2', '4', '6', '8', '9', '16', '17', '10', '11', '19', '14'],
				'13': ['2', '4', '6', '8', '9', '16', '17', '10', '11', '19', '12', '13'],
				'18': ['2', '4', '6', '8', '9', '16', '17', '10', '11', '19', '14', '18']
            },
            '3': {
				'3': ['3'],
				'5': ['3', '5'],
				'11': ['3', '5', '11'],
				'19': ['3', '5', '11', '19'],
				'12': ['3', '5', '11', '19', '12'],
				'14': ['3', '5', '11', '19', '14'],
				'13': ['3', '5', '11', '19', '12', '13'],
				'18': ['3', '5', '11', '19', '14', '18']
            },
            '4': {
				'4': ['4'],
				'6': ['4', '6'],
				'7': ['4', '6', '7'],
				'8': ['4', '6', '8'],
				'9': ['4', '6', '8', '9'],
				'16': ['4', '6', '8', '9', '16'],
				'17': ['4', '6', '8', '9', '16', '17'],
				'10': ['4', '6', '8', '9', '16', '17', '10'],
				'11': ['4', '6', '8', '9', '16', '17', '10', '11'],
				'19': ['4', '6', '8', '9', '16', '17', '10', '11', '19'],
				'12': ['4', '6', '8', '9', '16', '17', '10', '11', '19', '12'],
				'14': ['4', '6', '8', '9', '16', '17', '10', '11', '19', '14'],
				'13': ['4', '6', '8', '9', '16', '17', '10', '11', '19', '12', '13'],
				'18': ['4', '6', '8', '9', '16', '17', '10', '11', '19', '14', '18']
            },
            '5': {
				'5': ['5'],
				'11': ['5', '11'],
				'19': ['5', '11', '19'],
				'12': ['5', '11', '19', '12'],
				'14': ['5', '11', '19', '14'],
				'13': ['5', '11', '19', '12', '13'],
				'18': ['5', '11', '19', '14', '18']
            },
            '6': {
				'6': ['6'],
				'7': ['6', '7'],
				'8': ['6', '8'],
				'9': ['6', '8', '9'],
				'16': ['6', '8', '9', '16'],
				'17': ['6', '8', '9', '16', '17'],
				'10': ['6', '8', '9', '16', '17', '10'],
				'11': ['6', '8', '9', '16', '17', '10', '11'],
				'19': ['6', '8', '9', '16', '17', '10', '11', '19'],
				'12': ['6', '8', '9', '16', '17', '10', '11', '19', '12'],
				'14': ['6', '8', '9', '16', '17', '10', '11', '19', '14'],
				'13': ['6', '8', '9', '16', '17', '10', '11', '19', '12', '13'],
				'18': ['6', '8', '9', '16', '17', '10', '11', '19', '14', '18']
			},
            '7': {
				'7': ['7'],
				'6': ['7', '6'],
				'8': ['7', '6', '8'],
				'9': ['7', '6', '8', '9'],
				'16': ['7', '6', '8', '9', '16'],
				'17': ['7', '6', '8', '9', '16', '17'],
				'10': ['7', '6', '8', '9', '16', '17', '10'],
				'11': ['7', '6', '8', '9', '16', '17', '10', '11'],
				'19': ['7', '6', '8', '9', '16', '17', '10', '11', '19'],
				'12': ['7', '6', '8', '9', '16', '17', '10', '11', '19', '12'],
				'14': ['7', '6', '8', '9', '16', '17', '10', '11', '19', '14'],
				'13': ['7', '6', '8', '9', '16', '17', '10', '11', '19', '12', '13'],
				'18': ['7', '6', '8', '9', '16', '17', '10', '11', '19', '14', '18']
            },
            '8': {
				'8': ['8'],
				'6': ['8', '6'],
				'9': ['8', '9'],
				'7': ['8', '6', '7'],
				'16': ['8', '9', '16'],
				'17': ['8', '9', '16', '17'],
				'10': ['8', '9', '16', '17', '10'],
				'11': ['8', '9', '16', '17', '10', '11'],
				'19': ['8', '9', '16', '17', '10', '11', '19'],
				'12': ['8', '9', '16', '17', '10', '11', '19', '12'],
				'14': ['8', '9', '16', '17', '10', '11', '19', '14'],
				'13': ['8', '9', '16', '17', '10', '11', '19', '12', '13'],
				'18': ['8', '9', '16', '17', '10', '11', '19', '14', '18']
			},
            '9': {
				'9': ['9'],
				'16': ['9', '16'],
				'17': ['9', '16', '17'],
				'10': ['9', '16', '17', '10'],
				'11': ['9', '16', '17', '10', '11'],
				'19': ['9', '16', '17', '10', '11', '19'],
				'12': ['9', '16', '17', '10', '11', '19', '12'],
				'14': ['9', '16', '17', '10', '11', '19', '14'],
				'13': ['9', '16', '17', '10', '11', '19', '12', '13'],
				'18': ['9', '16', '17', '10', '11', '19', '14', '18']
			},
            '10': {
				'10': ['10'],
				'11': ['10', '11'],
				'19': ['10', '11', '19'],
				'12': ['10', '11', '19', '12'],
				'14': ['10', '11', '19', '14'],
				'13': ['10', '11', '19', '12', '13'],
				'18': ['10', '11', '19', '14', '18']
            },
            '11': {
				'11': ['11'],
				'19': ['11', '19'],
				'12': ['11', '19', '12'],
				'14': ['11', '19', '14'],
				'13': ['11', '19', '12', '13'],
				'18': ['11', '19', '14', '18']
            },
            '12': {
				'12': ['12'],
				'19': ['12', '19'],
				'13': ['12', '13'],
				'14': ['12', '19', '14'],
				'18': ['12', '19', '14', '18']
            },
            '13': {
				'13': ['13'],
				'12': ['13', '12'],
				'14': ['13', '14'],
				'19': ['13', '12', '19'],
				'18': ['13', '14', '18']
            },
            '14': {
				'14': ['14'],
				'19': ['14', '19'],
				'13': ['14', '13'],
				'18': ['14', '18'],
				'12': ['14', '19', '12']
            },
            '15': {
				'15': ['15'],
				'9': ['15', '9'],
				'16': ['15', '9', '16'],
				'17': ['15', '9', '16', '17'],
				'10': ['15', '9', '16', '17', '10'],
				'11': ['15', '9', '16', '17', '10', '11'],
				'19': ['15', '9', '16', '17', '10', '11', '19'],
				'12': ['15', '9', '16', '17', '10', '11', '19', '12'],
				'14': ['15', '9', '16', '17', '10', '11', '19', '14'],
				'13': ['15', '9', '16', '17', '10', '11', '19', '12', '13'],
				'18': ['15', '9', '16', '17', '10', '11', '19', '14', '18']
            },
            '16': {
				'16': ['16'],
				'17': ['16', '17'],
				'10': ['16', '17', '10'],
				'11': ['16', '17', '10', '11'],
				'19': ['16', '17', '10', '11', '19'],
				'12': ['16', '17', '10', '11', '19', '12'],
				'14': ['16', '17', '10', '11', '19', '14'],
				'13': ['16', '17', '10', '11', '19', '12', '13'],
				'18': ['16', '17', '10', '11', '19', '14', '18']
            },
            '17': {
				'17': ['17'],
				'16': ['17', '16'],
				'10': ['17', '10'],
				'11': ['17', '10', '11'],
				'19': ['17', '10', '11', '19'],
				'12': ['17', '10', '11', '19', '12'],
				'14': ['17', '10', '11', '19', '14'],
				'13': ['17', '10', '11', '19', '12', '13'],
				'18': ['17', '10', '11', '19', '14', '18']
            },
            '18': {
                '18': ['18']
            },
            '19': {
				'19': ['19'],
				'12': ['19', '12'],
				'14': ['19', '14'],
				'13': ['19', '12', '13'],
				'18': ['19', '14', '18']
            }
        }

        cls.final_element_perturbation = copy.deepcopy(cls.initial)
        cls.final_element_perturbation.pop('1')

        cls.final_multi_area_perturbation = {
            '2': {
                '2': ['2'],
                '4': ['2', '4'],
                '6': ['2', '4', '6'],
                '7': ['2', '4', '6', '7'],
                '8': ['2', '4', '6', '8']
            },
            '3': {
                '3': ['3'],
                '5': ['3', '5']
            },
            '4': {
                '4': ['4'],
                '6': ['4', '6'],
                '7': ['4', '6', '7'],
                '8': ['4', '6', '8']
            },
            '5': {
                '5': ['5']
            },
            '6': {
                '6': ['6'],
                '7': ['6', '7'],
                '8': ['6', '8']
            },
            '7': {
                '7': ['7'],
                '6': ['7', '6'],
                '8': ['7', '6', '8']
            },
            '8': {
                '8': ['8'],
                '6': ['8', '6'],
                '7': ['8', '6', '7'],
            }
        }

    @classmethod
    def check_shortest_paths(cls, test, true_path, shpath, shpath_len):
        """
		For every path, source and target must match with the true ones.
		The length of the shortest path beteween source
		and target must also match.
		The shortest path is not necessarily unique:
		the entire source-target path does not necessarily coincide.
		"""
        for source, all_paths in true_path.items():
            for target, path in all_paths.items():
                test.assertEqual(
                    path[0], shpath[source][target][0],
                    msg="Wrong SOURCE in path from " + str(source) + " to " +
                    str(target))

                test.assertEqual(
                    path[-1], shpath[source][target][-1],
                    msg="Wrong TARGET in path from " + str(source) + " to " +
                    str(target))

                if source != target:
                    test.assertEqual(
                        len(path)-1, shpath_len[source][target],
                        msg="Wrong LENGTH of path from " + str(source) +
                        " to " + str(target))
                else:
                    test.assertEqual(
                        0.0, shpath_len[source][target],
                        msg="Wrong LENGTH of path from " + str(source) +
                        " to " + str(target))

    def test_Dijkstra_parallel(self):
        """
		The following test checks the parallel SSSP algorithm based
		on Dijkstra's method.
		"""
        g = ParallelGeneralGraph()
        g.load("tests/TOY_graph.csv")
        g.num = mp.cpu_count()
        shpath, shpath_len = g.dijkstra_single_source_shortest_path()

        self.check_shortest_paths(self, self.initial, shpath, shpath_len)

    def test_floyd_warshall_parallel(self):
        """
		The following test checks the parallel Floyd Warshall's APSP algorithm.
		"""
        g = ParallelGeneralGraph()
        g.load("tests/TOY_graph.csv")
        g.num = mp.cpu_count()
        shpath, shpath_len = g.floyd_warshall_predecessor_and_distance()

        self.check_shortest_paths(self, self.initial, shpath, shpath_len)

    def test_Dijkstra_serial(self):
        """
		The following test checks the serial SSSP algorithm based
		on Dijkstra's method.
		"""
        g = GeneralGraph()
        g.load("tests/TOY_graph.csv")
        shpath, shpath_len = g.dijkstra_single_source_shortest_path()

        self.check_shortest_paths(self, self.initial, shpath, shpath_len)

    def test_floyd_warshall_serial(self):
        """
		The following test checks the serial Floyd Warshall's APSP algorithm.
		"""
        g = GeneralGraph()
        g.load("tests/TOY_graph.csv")
        shpath, shpath_len = g.floyd_warshall_predecessor_and_distance()

        self.check_shortest_paths(self, self.initial, shpath, shpath_len)

    def test_element_perturbation(self):
        """
		The following test checks the topology of the graph after
        a perturbation. The perturbation here considered is the
        perturbation of element '1'.
		"""
        F = FaultDiagnosis("tests/TOY_graph.csv")
        F.simulate_element_perturbation(["1"])

        self.check_shortest_paths(self, self.final_element_perturbation,
            F.G.shortest_path, F.G.shortest_path_length)
