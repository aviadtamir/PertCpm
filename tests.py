import unittest
from PertProject import *


class ProjectTests(unittest.TestCase):

    def test_early_times_calculation_with_valid_activities(self):
        activities = {Activity('a', 10): ['b', 'c'],
                      Activity('b', 15): ['d', 'e'],
                      Activity('c', 25): ['e'],
                      Activity('d', 5): [],
                      Activity('e', 15): [],
                      }
        expected_activities_with_early_timings = {'a': {'early_start': 0, 'early_finish': 10},
                                                  'b': {'early_start': 10, 'early_finish': 25},
                                                  'c': {'early_start': 10, 'early_finish': 35},
                                                  'd': {'early_start': 25, 'early_finish': 30},
                                                  'e': {'early_start': 35, 'early_finish': 50},
                                                  }

        pert_project = Project(activities)
        pert_project.__calculate_early_times__()

        for current_activity in pert_project.activities:
            expected_times = expected_activities_with_early_timings[current_activity.name]

            self.assertEqual(current_activity.early_start, expected_times['early_start'],
                             r"Error, activity '{0}' early start is not as expected (expected: {1}, "
                             r"actual: {2})".format(current_activity.name,
                                                    expected_times['early_start'],
                                                    current_activity.early_start))

            self.assertEqual(current_activity.early_finish, expected_times['early_finish'],
                             r"Error, activity '{0}' early finish is not as expected (expected: {1}, "
                             r"actual: {2})".format(current_activity.name,
                                                    expected_times['early_finish'],
                                                    current_activity.early_finish))

    def test_late_times_calculation_with_valid_activities(self):
        activities = {Activity('a', 10, 0, 10): ['b', 'c'],
                      Activity('b', 15, 10, 25): ['d', 'e'],
                      Activity('c', 25, 10, 35): ['e'],
                      Activity('d', 5, 25, 30): [],
                      Activity('e', 15, 35, 50): [],
                      }
        expected_activities_with_late_times = {'a': {'late_start': 0, 'late_finish': 10},
                                               'b': {'late_start': 20, 'late_finish': 35},
                                               'c': {'late_start': 10, 'late_finish': 35},
                                               'd': {'late_start': 45, 'late_finish': 50},
                                               'e': {'late_start': 35, 'late_finish': 50},
                                               }

        pert_project = Project(activities)
        pert_project.__calculate_late_times__()

        for current_activity in pert_project.activities:
            expected_times = expected_activities_with_late_times[current_activity.name]

            self.assertEqual(current_activity.late_start, expected_times['late_start'],
                             r"Error, activity '{0}' late start is not as expected (expected: {1}, "
                             r"actual: {2})".format(current_activity.name,
                                                    expected_times['late_start'],
                                                    current_activity.late_start))

            self.assertEqual(current_activity.late_finish, expected_times['late_finish'],
                             r"Error, activity '{0}' late finish is not as expected (expected: {1}, "
                             r"actual: {2})".format(current_activity.name,
                                                    expected_times['late_finish'],
                                                    current_activity.late_finish))

    def test_slack_calculation_with_valid_activities(self):
        activities = {Activity('a', 10, 0, 10): ['b', 'c'],
                      Activity('b', 15, 10, 25): ['d', 'e'],
                      Activity('c', 25, 10, 35): ['e'],
                      Activity('d', 5, 25, 30): [],
                      Activity('e', 15, 35, 50): [],
                      }

        expected_activities_with_slack = {'a': {'slack': 0},
                                          'b': {'slack': 10},
                                          'c': {'slack': 0},
                                          'd': {'slack': 20},
                                          'e': {'slack': 0},
                                          }

        pert_project = Project(activities)
        pert_project.calculate_slack()

        for current_activity in pert_project.activities:
            expected_slack = expected_activities_with_slack[current_activity.name]

            self.assertEqual(current_activity.slack, expected_slack['slack'],
                             r"Error, activity '{0}' slack is not as expected (expected: {1}, "
                             r"actual: {2})".format(current_activity.name,
                                                    expected_slack['slack'],
                                                    current_activity.slack))

    def test_critical_path_calculation_with_valid_activities(self):
        activities = {Activity('a', 10, 0, 10): ['b', 'c'],
                      Activity('b', 15, 10, 25): ['d', 'e'],
                      Activity('c', 25, 10, 35): ['e'],
                      Activity('d', 5, 25, 30): [],
                      Activity('e', 15, 35, 50): [],
                      }

        expected_critical_paths = [['a', 'c', 'e']]

        pert_project = Project(activities)
        critical_paths_in_project = pert_project.get_all_critical_paths()

        self.assertCountEqual(expected_critical_paths, critical_paths_in_project,
                              r"Error, The number of critical paths is not as expected, expected: '{0}' actual: {1}, ".
                              format(len(expected_critical_paths), len(critical_paths_in_project)))

        self.assertListEqual(expected_critical_paths, critical_paths_in_project,
                             r"Error, The critical paths is not as expected, expected: '{0}' actual: {1}, ".
                             format(expected_critical_paths, critical_paths_in_project))

    def test_critical_path_calculation_with_valid_activities_with_multiple_critical_paths(self):
        activities = {Activity('a1', 10, 0, 10): ['b', 'c'],
                      Activity('a2', 10, 0, 10): ['b', 'c'],
                      Activity('b', 15, 10, 25): ['d', 'e'],
                      Activity('c', 25, 10, 35): ['e', 'f'],
                      Activity('d', 5, 25, 30): [],
                      Activity('e', 15, 35, 50): [],
                      Activity('f', 15, 35, 50): [],
                      }

        expected_critical_paths = [['a1', 'c', 'e'], ['a1', 'c', 'f'], ['a2', 'c', 'e'], ['a2', 'c', 'f']]

        pert_project = Project(activities)
        critical_paths_in_project = pert_project.get_all_critical_paths()

        self.assertCountEqual(expected_critical_paths, critical_paths_in_project,
                              r"Error, The number of critical paths is not as expected, expected: '{0}' actual: {1}, ".
                              format(len(expected_critical_paths), len(critical_paths_in_project)))

        self.assertListEqual(expected_critical_paths, critical_paths_in_project,
                             r"Error, The critical paths is not as expected, expected: '{0}' actual: {1}, ".
                             format(expected_critical_paths, critical_paths_in_project))


if __name__ == '__main__':
    unittest.main()
