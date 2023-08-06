from .common import *

def traversalTree(
    tree:   "Dictionary, returns the children of given nodeID, tuple if in order, list otherwise, \
                {\
                    nodeID1: (child1, child2, ...), \
                    nodeID2: (child1, child2, ...), \
                    nodeWithNoChild: None, \
                    ... \
                }" = None, 
    oID:    "1) String/Integer, nodeID of the root or, \
             2) None, (default) the first nodeID in `tree`" = None,
    algo:   "1) String, (default) 'DepthFirst' or, \
             2) String, 'BreadthFirst'" = 'DepthFirst'
    ) -> "Return a sequence of node ids that traverses the tree":

    # Solve by different algorithms ===========================================
    res = None
    if (algo == 'DepthFirst'):
        res = _traversalTreeDepthFirst(tree, oID)

    return res

def _traversalTreeDepthFirst(tree, oID):
    visited = []

    # Visit children recursively ==============================================
    def visitNode(nodeID):
        visited.append(nodeID)
        children = tree[nodeID]
        if (children != None and children not in visited):
            if (type(children) == int or type(children) == str):
                visitNode(children)
            else:
                for child in children:
                    visitNode(child)

    # Start search from root ==================================================
    # FIXME! Incorrect for dictionary that root is not the first element
    if (oID == None):
        oID = list(tree.keys())[0]
    visitNode(oID)

    return {
        'seq': visited
    }

def traversalGraph(
    arcs:   "1) A list of 3-tuple (nodeID1, nodeID2, weight) or, \
             2) A list of 2-tuple (nodeID1, nodeID2)",
    oID:    "1) String/Integer, nodeID of the root or, \
             2) None, (default) the first nodeID in `tree`" = None,
    algo:   "1) String, (default) 'DepthFirst' or, \
             2) String, 'BreadthFirst'" = 'DepthFirst'
    ) -> "Return a sequence of node ids that traverses the tree":

    # Convert arcs into adjList ===============================================
    neighbors = arcs2AdjList(arcs)

    # Solve by different algorithms ===========================================
    res = None
    if (algo == 'DepthFirst'):
        res = _traversalGraphDepthFirst(neighbors, oID)

    return res

def _traversalGraphDepthFirst(neighbors, oID):
    visited = []

    # Visit neighbors that has not been visited ===============================
    def visitNode(nodeID):
        visited.append(nodeID)
        neis = neighbors[nodeID]
        for nei in neis:
            if (nei not in visited):
                visitNode(nei)

    # Start search from root ==================================================
    if (oID == None):
        oID = list(neighbors.keys())[0]
    visitNode(oID)

    return {
        'seq': visited,
        'oID': oID
    }
