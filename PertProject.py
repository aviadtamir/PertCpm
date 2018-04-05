
class Project(object):
    # data members:
    # activities dictionary  - {a:[b,c],b:[a]...}
    # critical path - [] \ {}
    # is cpm up to date
    # is valid  - searches for isolated nodes or circles in the graph
    def __init__(self, activities):
        if activities is None:
            self.activities = {}
            self.is_cpm_updated = False
            self.graph_valid = False
        else:
            self.activities = activities
            self.is_cpm_updated = False
            self.graph_valid = self.is_valid()

    def is_valid(self):
        # calls find circles
        # calls find isolates()
        if self.find_isolated_activity() is None and not self.is_cyclic():
            return True

        return False

    def critical_path(self):
        # TODO  '''at - implement calculation of critical path'''
        self.is_cpm_updated = True
        raise NotImplementedError

    def add_activity(self, activity, precedors=None):
        # is cpm update  = False
        # at each call
        self.activities[activity] = activity.successors
        if precedors is not None:
            for ac in precedors:
                ac.successors.append(activity)

        self.is_cpm_updated = False

    def remove_activity(self, activity):
        # is cpm update  = False
        # at each call
        self.activities.pop(activity, None)
        for v in self.activities.values():
            if activity in v:
                v.remove(activity)
        self.is_cpm_updated = False

    def find_isolated_activity(self):
        is_isolate = None
        for key in self.activities.keys():
            if key.successors is []:
                for v in self.activities.values():
                    if not any(key in v for v in self.activities.values()):
                        is_isolate = key
        return is_isolate

    '''def find_isolated_activity(self):
        is_isolate = None
        for i in range(0, len(self.activities.keys())):
            if self.activities.keys()[i].successors == []:
                for j in range(0, len(self.activities.values())):
                    if not any(self.activities.keys()[i] in v for v in self.activities.values()):
                        is_isolate = self.activities.keys()[i]
        return is_isolate'''

    def is_cyclic(self):
        # TODO - AT fix is cyclic bug, currently shows True for non cyclic and False for cyclic
        visited = set()
        path = set()

        def visit(node):
            if node in visited:
                return False
            visited.add(node.name)
            path.add(node.name)
            for successor in self.activities.get(node, []):
                if successor.name in path or visit(successor) is True:
                    return True
            path.remove(node.name)
            return False

        return any(visit(activity) for activity in self.activities)

    def show_activities_slack(self):
        # TODO  '''at - show_activities_slack - slack should be calculated in each activity at
        # creation(contructor) or in a different method and should be added as a
        # data member in runtime '''
        raise NotImplementedError

    def __str__(self):
        project = "Project activities:  \n"
        for activity in self.activities.keys():
            project += str(activity) +"\n"
        if self.is_cpm_updated is True:
            project += "Critical Path: " + self.critical_path + "\n"
        return project


class Activity(object):

    def __init__(self, name, duration, successors):
        self.duration = duration
        self.name = name
        self.successors = successors

    def __str__(self):
        return "name: " + self.name + " , duration: " + str(self.duration) + " , successors: " + str(self.successors)

    def __repr__(self):
        return "name: " + self.name + " , duration: " + str(self.duration) + " , successors: " + str(self.successors)



