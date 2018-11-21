import sys


def build_mesh_graph(verts, edges, topo=True):
    mg = {}
    for v in verts:
        mg[v] = []

    for e in edges:
        distance = 1 if topo else e.calc_length()

        mg[e.verts[0]].append((e.verts[1], distance))
        mg[e.verts[1]].append((e.verts[0], distance))

    return mg


def get_shortest_path(bm, vstart, vend, topo=False, select=False):
    """
    author: "G Bantle, Bagration, MACHIN3",
    source: "https://blenderartists.org/forum/showthread.php?58564-Path-Select-script(Update-20060307-Ported-to-C-now-in-CVS",
    video: https://www.youtube.com/watch?v=_lHSawdgXpI
    """

    def dijkstra(mg, vstart, vend, topo=True):
        # for every vert, find the distance to every other vert
        d = dict.fromkeys(mg.keys(), sys.maxsize)

        predecessor = dict.fromkeys(mg.keys())

        # the distance of the start vert to itself is 0
        d[vstart] = 0

        # keep track of what verts are visited and add the the accumulated distances to those verts
        unknownverts = [(0, vstart)]

        # with topo you can exist as soon as you hit the vend, without topo you can't
        while (topo and vstart != vend) or (not topo and unknownverts):
            # unknownverts.sort()
            dist, u = unknownverts[0]  # Get the next vert that is closest to s
            others = mg[u]

            for vother, distance in others:  # v = neighbour vert, w = distance from u to this vert
                if d[vother] > d[u] + distance:
                    d[vother] = d[u] + distance
                    unknownverts.append((d[vother], vother))
                    predecessor[vother] = u

            unknownverts.pop(0)  # We just finished exploring this vert, so it can be removed
            vstart = u  # Set new start vert

        path = []
        endvert = vend

        while endvert is not None:  # Backtrace rom the end vertex using the "predecessor" dict
            path.append(endvert)
            endvert = predecessor[endvert]

        return reversed(path)

    def f7(seq):
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x))]

    verts = [v for v in bm.verts]
    edges = [e for e in bm.edges]

    mg = build_mesh_graph(verts, edges, topo)

    # [(shortest dist from s (start vert) to vert, vert)]
    path = dijkstra(mg, vstart, vend, topo)

    # remove duplicates, keeps order, see https://stackoverflow.com/a/480227
    path = f7(path)

    if select:
        for v in path:
            v.select = True

    return path
