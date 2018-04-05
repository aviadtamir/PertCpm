
import PertProject

def is_valid_test(project_graph):
    return project_graph.is_valid()


def main():

    e = PertProject.Activity('e', 3, [])
    f = PertProject.Activity('f', 3, [])
    b = PertProject.Activity('b', 3, [e,])
    c = PertProject.Activity('c', 3, [e,])
    a = PertProject.Activity('a', 3, [b, c,])
    #e = PertProject.Activity('e', 3, [a,])

    g = PertProject.Activity('g', 3, [e,])

    d = {a: a.successors, b: b.successors, c: c.successors, e: e.successors}# ,f: c.successors}
    p = PertProject.Project(d)
    isolated = (p.find_isolated_activity())
    p.add_activity(g,[a])

    p.remove_activity(g)
    print(p.is_cyclic())
    #print(p.is_valid())





main()