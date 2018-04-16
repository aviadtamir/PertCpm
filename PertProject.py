import copy

DEFAULT_TIME_VALUE = -1


class Project(object):

    def __init__(self, activities):
        self.early_times_calculated = False
        self.late_times_calculated = False
        self.slack_calculated = False
        self.activities = dict() if activities is None else activities

    def validate_graph(self):
        # TODO  '''at - implement validation of the project graph'''
        return True

    def calculate_slack(self):
        if not self.early_times_calculated:
            self.__calculate_early_times__()
        if not self.late_times_calculated:
            self.__calculate_late_times__()

        for current_activity in self.activities:
            current_activity.slack = current_activity.late_finish - current_activity.early_finish

        self.slack_calculated = True

    def get_all_critical_paths(self):
        if not self.validate_graph():
            raise RuntimeError("Error, cannot calculate critical path on invalid graph!")
        if not self.slack_calculated:
            self.calculate_slack()

        # There might be more than one critical path, and we want to support it
        starting_activities_in_critical_path = [starting_activity for starting_activity in
                                                self.__get_starting_activities__() if starting_activity.slack is 0]
        last_activities = self.__get_last_activities__()

        critical_paths = []
        for current_starting_activity in starting_activities_in_critical_path:
            critical_paths += self.__calculate_critical_paths__(
                current_starting_activity,
                [],
                last_activities,
                self.__get_activities_names_map__())

        return critical_paths

    def __calculate_critical_paths__(
            self,
            current_activity_in_critical_path_chain,
            critical_path__chain_so_far,
            ending_activities,
            activities_names_map):
        critical_path__chain_so_far.append(current_activity_in_critical_path_chain.name)

        if current_activity_in_critical_path_chain in ending_activities:
            return [critical_path__chain_so_far]

        next_activities_in_critical_paths = [next_activity for next_activity in
                                             [activities_names_map[next_activity_name] for next_activity_name
                                              in self.activities[current_activity_in_critical_path_chain]]
                                             if next_activity.slack is 0]

        critical_paths = []
        for current_next_activity in next_activities_in_critical_paths:
            critical_paths += self.__calculate_critical_paths__(
                current_next_activity,
                copy.deepcopy(critical_path__chain_so_far),
                ending_activities,
                activities_names_map)

        return critical_paths

    def __calculate_times_for_chain__(
            self,
            current_activity_in_chain,
            activities_graph,
            times_update_function,
            current_calculated_time,
            activities_names_map):

        current_calculated_time = times_update_function(current_activity_in_chain, current_calculated_time)

        for next_activity_name in activities_graph[current_activity_in_chain]:
            next_activity = activities_names_map[next_activity_name]
            self.__calculate_times_for_chain__(
                next_activity,
                activities_graph,
                times_update_function,
                current_calculated_time,
                self.__get_activities_names_map__())

    @staticmethod
    def __calculate_early_times_for_activity__(activity, total_time_since_start):
        if activity.early_start is DEFAULT_TIME_VALUE or activity.early_start < total_time_since_start:
            activity.early_start = total_time_since_start
            activity.early_finish = total_time_since_start + activity.duration
        return activity.early_finish

    def __calculate_early_times__(self):
        starting_time = 0
        starting_activities = self.__get_starting_activities__()

        for current_starting_activity in starting_activities:
            self.__calculate_times_for_chain__(
                current_starting_activity,
                self.activities,
                Project.__calculate_early_times_for_activity__,
                starting_time,
                self.__get_activities_names_map__())

        self.early_times_calculated = True

    def __get_starting_activities__(self):
        activities_with_dependencies = set()
        for current_activity_dependencies in self.activities.values():
            [activities_with_dependencies.add(activity_with_dependency)
                for activity_with_dependency in current_activity_dependencies]

        # The activities without dependencies are the starting activities
        activities_without_dependencies = [current_activity for current_activity in self.activities
                                           if current_activity.name not in activities_with_dependencies]

        return activities_without_dependencies

    @staticmethod
    def __calculate_late_times_for_activity__(activity, time_since_start):
        if activity.late_finish is DEFAULT_TIME_VALUE or activity.late_finish > time_since_start:
            activity.late_finish = time_since_start
            activity.late_start = time_since_start - activity.duration
        return activity.late_start

    def __calculate_late_times__(self):
        last_activities = self.__get_last_activities__()
        reverse_graph = self.__get_reverse_graph__()

        late_finish_time = 0
        for current_last_activity in last_activities:
            if current_last_activity.early_finish > late_finish_time:
                late_finish_time = current_last_activity.early_finish

        for current_last_activity in last_activities:
            self.__calculate_times_for_chain__(
                current_last_activity,
                reverse_graph,
                Project.__calculate_late_times_for_activity__,
                late_finish_time,
                self.__get_activities_names_map__())

        self.late_times_calculated = True

    def __get_last_activities__(self):
        return set(filter(lambda current_activity: not self.activities[current_activity], self.activities))

    def __get_reverse_graph__(self):
        activities_names_map = self.__get_activities_names_map__()

        reverse_graph = {current_activity: list() for current_activity in self.activities}

        for current_activity in self.activities:
            for next_activity_name in self.activities[current_activity]:
                next_activity = activities_names_map[next_activity_name]
                reverse_graph[next_activity].append(current_activity.name)

        return reverse_graph

    def __get_activities_names_map__(self):
        return {current_activity.name: current_activity for current_activity in self.activities}

    def add_activity(self):
        # TODO  '''at - implement add activity'''
        raise NotImplementedError

    def remove_activity(self):
        # TODO  '''at - implement raise activity'''
        raise NotImplementedError

    def find_isolated_activity(self):
        # TODO  '''at - implement find isolated'''
        raise NotImplementedError

    def show_activities_slack(self):
        # TODO  '''at - show_activities_slack - slack should be calculated in each activity at
        # creation(contructor) or in a different method and should be added as a
        # data member in runtime '''
        raise NotImplementedError

    def __str__(self):
        # TODO at - override __str__
        raise NotImplementedError


class Activity(object):

    # TODO at - maybe change c'tor and add more
    # data members like es, fs, preceding and seceding activities
    def __init__(self,
                 name,
                 duration,
                 early_start=DEFAULT_TIME_VALUE,
                 early_finish=DEFAULT_TIME_VALUE,
                 late_start=DEFAULT_TIME_VALUE,
                 late_finish=DEFAULT_TIME_VALUE, ):
        self.duration = duration
        self.name = name
        self.early_start = early_start
        self.early_finish = early_finish
        self.late_start = late_start
        self.late_finish = late_finish
        self.slack = DEFAULT_TIME_VALUE

    def __str__(self):
        # TODO at - override __str__
        raise NotImplementedError
