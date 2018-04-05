
class Project(object):
    # data members:
    # activities dictionary  - {a:[b,c],b:[a]...}
    # critical path - [] \ {}
    # is cpm up to date
    # is valid  - searches for isolated nodes or circles in the graph
    def __init__(self,activities):
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
        if self.find_isolated_activity() is None and self.is_cyclic():
            return True

        return False

    def critical_path(self):
        # TODO  '''at - implement calculation of critical path'''
        self.is_cpm_updated = True
        raise NotImplementedError

    def add_activity(self,preceder,acivity):
        # TODO  '''at - implement add activity'''
        # is cpm update  = False
        # at each call
        self.is_cpm_updated = False

        raise NotImplementedError

    def remove_activity(self):
        # TODO  '''at - implement raise activity'''
        # is cpm update  = False
        # at each call
        self.is_cpm_updated = False
        raise NotImplementedError

    def find_isolated_activity(self):
        is_isolate = None
        for i in range(0, len(self.activities.keys())):
            if self.activities.keys()[i].precedors == []:
                for j in range(0, len(self.activities.values())):
                    if self.activities.keys()[i] not in self.activities.values()[j]:
                        is_isolate = self.activities.keys()[i]

        return is_isolate

    def is_cyclic(self):
        # TODO - AT fix is cyclic bug, currently shows True for non cyclic and flase for cyclic
        visited = set()
        path = set()

        def visit(node):
            if node in visited:
                return False
            visited.add(node)
            path.add(node)
            for n in self.activities.get(node, []):
                if n in path or visit(n):
                    return True
            path.remove(node)
            return False
        return any(visit(v) for v in self.activities)


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
    def __init__(self, name, duration,precedors):
        self.duration = duration
        self.name = name
        self.precedors = precedors

    def __str__(self):
        return "name: " + self.name + " , duration: " + str(self.duration) + " , precedors: " + str(self.precedors)

    def __repr__(self):
        return "name: " + self.name + " , duration: " + str(self.duration) + " , precedors: " + str(self.precedors)



