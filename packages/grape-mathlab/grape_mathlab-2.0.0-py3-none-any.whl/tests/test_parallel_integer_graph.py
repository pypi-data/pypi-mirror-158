"""TestOutputGraph to check output of GeneralGraph"""

import numpy as np
from grape.parallel_general_graph import ParallelGeneralGraph


def test_nodal_efficiency():
    """
	The following test checks nodal efficiency before any perturbation.
	"""
    g = ParallelGeneralGraph()
    g.load("tests/TOY_graph.csv")

    nodal_eff_before = {
        '1': 0.3213624338624339,
        '2': 0.19689554272887605,
        '3': 0.15185185185185185,
        '4': 0.20222663139329808,
        '5': 0.14814814814814814,
        '6': 0.22583774250440916,
        '7': 0.17444885361552032,
        '8': 0.2492063492063492,
        '9': 0.16124338624338624,
        '10': 0.14814814814814814,
        '11': 0.14814814814814814,
        '12': 0.15740740740740738,
        '13': 0.16666666666666666,
        '14': 0.19444444444444445,
        '15': 0.16587301587301587,
        '16': 0.15648148148148147,
        '17': 0.20740740740740743,
        '18': 0.0,
        '19': 0.16666666666666666
    }

    np.testing.assert_array_almost_equal(
        np.asarray(sorted(nodal_eff_before.values())),
        np.asarray(sorted(g.nodal_efficiency.values())),
        err_msg="ORIGINAL NODAL EFFICIENCY failure (PARALLEL)")

def test_global_efficiency():
    """
	The following test checks global efficiency before any perturbation.
	"""
    g = ParallelGeneralGraph()
    g.load("tests/TOY_graph.csv")

    np.testing.assert_almost_equal(g.global_efficiency, 0.1759191750419821,
        err_msg="ORIGINAL GLOBAL EFFICIENCY failure")

def test_local_efficiency():
    """
	The following test checks local efficiency before any perturbation.
	"""
    g = ParallelGeneralGraph()
    g.load("tests/TOY_graph.csv")

    local_eff_before = {
        '1': 0.17437369729036395,
        '2': 0.20222663139329808,
        '3': 0.14814814814814814,
        '4': 0.22583774250440916,
        '5': 0.14814814814814814,
        '6': 0.21182760141093476,
        '7': 0.22583774250440916,
        '8': 0.19354056437389772,
        '9': 0.15648148148148147,
        '10': 0.14814814814814814,
        '11': 0.16666666666666666,
        '12': 0.16666666666666666,
        '13': 0.17592592592592593,
        '14': 0.1111111111111111,
        '15': 0.16124338624338624,
        '16': 0.20740740740740743,
        '17': 0.1523148148148148,
        '18': 0.0,
        '19': 0.17592592592592593
    }

    np.testing.assert_array_almost_equal(
        np.asarray(sorted(local_eff_before.values())),
        np.asarray(sorted(g.local_efficiency.values())),
        err_msg="ORIGINAL LOCAL EFFICIENCY failure (PARALLEL)")

def test_closeness_centrality():
    """
	The following test checks closeness centrality before any perturbation.
	"""
    g = ParallelGeneralGraph()
    g.load("tests/TOY_graph.csv")

    closeness_centrality = {
        '1': 0.0,
        '2': 0.05555555555555555,
        '3': 0.05555555555555555,
        '4': 0.07407407407407407,
        '5': 0.07407407407407407,
        '6': 0.1736111111111111,
        '7': 0.11574074074074076,
        '8': 0.11574074074074076,
        '9': 0.14327485380116958,
        '10': 0.12077294685990338,
        '11': 0.17386831275720163,
        '12': 0.1866925064599483,
        '13': 0.16055555555555556,
        '14': 0.1866925064599483,
        '15': 0.0,
        '16': 0.16071428571428573,
        '17': 0.125,
        '18': 0.17307692307692307,
        '19': 0.22299382716049382
    }

    np.testing.assert_array_almost_equal(
        np.asarray(sorted(closeness_centrality.values())),
        np.asarray(sorted(g.closeness_centrality.values())),
        err_msg="CLOSENESS CENTRALITY failure (PARALLEL)")

def test_betweenness_centrality():
    """
	The following test checks betweenness centrality before any perturbation.
	"""
    g = ParallelGeneralGraph()
    g.load("tests/TOY_graph.csv")

    betweenness_centrality = {
        '1': 0.0,
        '2': 0.05161290322580645,
        '3': 0.04516129032258064,
        '4': 0.12903225806451613,
        '5': 0.07741935483870968,
        '6': 0.2709677419354839,
        '7': 0.0,
        '8': 0.2838709677419355,
        '9': 0.36774193548387096,
        '10': 0.34838709677419355,
        '11': 0.41935483870967744,
        '12': 0.1032258064516129,
        '13': 0.0,
        '14': 0.10967741935483871,
        '15': 0.0,
        '16': 0.3741935483870968,
        '17': 0.36774193548387096,
        '18': 0.0,
        '19': 0.38064516129032255
    }

    np.testing.assert_array_almost_equal(
        np.asarray(sorted(betweenness_centrality.values())),
        np.asarray(sorted(g.betweenness_centrality.values())),
        err_msg="BETWENNESS CENTRALITY failure (PARALLEL)")

def test_indegree_centrality():
    """
	The following test checks indegree centrality before any perturbation.
	"""
    g = ParallelGeneralGraph()
    g.load("tests/TOY_graph.csv")

    indegree_centrality = {
        '1': 0.0,
        '2': 0.05555555555555555,
        '3': 0.05555555555555555,
        '4': 0.05555555555555555,
        '5': 0.05555555555555555,
        '6': 0.16666666666666666,
        '7': 0.05555555555555555,
        '8': 0.05555555555555555,
        '9': 0.1111111111111111,
        '10': 0.05555555555555555,
        '11': 0.1111111111111111,
        '12': 0.1111111111111111,
        '13': 0.1111111111111111,
        '14': 0.1111111111111111,
        '15': 0.0,
        '16': 0.1111111111111111,
        '17': 0.05555555555555555,
        '18': 0.05555555555555555,
        '19': 0.16666666666666666
    }

    np.testing.assert_array_almost_equal(
        np.asarray(sorted(indegree_centrality.values())),
        np.asarray(sorted(g.indegree_centrality.values())),
        err_msg="INDEGREE CENTRALITY failure (PARALLEL)")

def test_outdegree_centrality():
    """
	The following test checks outdegree centrality before any perturbation.
	"""
    g = ParallelGeneralGraph()
    g.load("tests/TOY_graph.csv")

    outdegree_centrality = {
        '1': 0.1111111111111111,
        '2': 0.05555555555555555,
        '3': 0.05555555555555555,
        '4': 0.05555555555555555,
        '5': 0.05555555555555555,
        '6': 0.1111111111111111,
        '7': 0.05555555555555555,
        '8': 0.1111111111111111,
        '9': 0.05555555555555555,
        '10': 0.05555555555555555,
        '11': 0.05555555555555555,
        '12': 0.1111111111111111,
        '13': 0.1111111111111111,
        '14': 0.16666666666666666,
        '15': 0.05555555555555555,
        '16': 0.05555555555555555,
        '17': 0.1111111111111111,
        '18': 0.0,
        '19': 0.1111111111111111
    }

    np.testing.assert_array_almost_equal(
        np.asarray(sorted(outdegree_centrality.values())),
        np.asarray(sorted(g.outdegree_centrality.values())),
        err_msg="OUTDEGREE CENTRALITY failure (PARALLEL)")

def test_degree_centrality():
    """
	The following test checks degree centrality before any perturbation.
	"""
    g = ParallelGeneralGraph()
    g.load("tests/TOY_graph.csv")

    degree_centrality = {
        '1': 0.1111111111111111,
        '2': 0.1111111111111111,
        '3': 0.1111111111111111,
        '4': 0.1111111111111111,
        '5': 0.1111111111111111,
        '6': 0.2777777777777778,
        '7': 0.1111111111111111,
        '8': 0.16666666666666666,
        '9': 0.16666666666666666,
        '10': 0.1111111111111111,
        '11': 0.16666666666666666,
        '12': 0.2222222222222222,
        '13': 0.2222222222222222,
        '14': 0.2777777777777778,
        '15': 0.05555555555555555,
        '16': 0.16666666666666666,
        '17': 0.16666666666666666,
        '18': 0.05555555555555555,
        '19': 0.2777777777777778
    }

    np.testing.assert_array_almost_equal(
        np.asarray(sorted(degree_centrality.values())),
        np.asarray(sorted(g.degree_centrality.values())),
        err_msg="DEGREE CENTRALITY failure (PARALLEL)")
