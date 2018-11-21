import bpy
import bmesh
import os
import sys
import platform
import subprocess


def clear():
    os.system("clear")


def get_active():
    return bpy.context.active_object


def make_active(obj):
    bpy.context.view_layer.objects.active = obj
    return obj


def selected_objects():
    return bpy.context.selected_objects


def select_all(string):
    if string == "MESH":
        bpy.ops.mesh.select_all(action='SELECT')
    elif string == "OBJECT":
        bpy.ops.object.select_all(action='SELECT')


def unselect_all(string):
    if string == "MESH":
        bpy.ops.mesh.select_all(action='DESELECT')
    elif string == "OBJECT":
        bpy.ops.object.select_all(action='DESELECT')


def select(objlist):
    for obj in objlist:
        obj.select = True


def hide_all(string):
    if string == "OBJECT":
        select_all(string)
        bpy.ops.object.hide_view_set(unselected=False)
    elif string == "MESH":
        select_all(string)
        bpy.ops.mesh.hide(unselected=False)


def unhide_all(string="OBJECT"):
    if string == "OBJECT":
        for obj in bpy.data.objects:
            obj.hide = False
    elif string == "MESH":
        bpy.ops.mesh.reveal()


def get_mode():
    mode = bpy.context.mode

    if mode == "OBJECT":
        return "OBJECT"
    elif mode == "EDIT_MESH":
        return get_mesh_select_mode()


def get_mesh_select_mode():
    mode = tuple(bpy.context.scene.tool_settings.mesh_select_mode)
    if mode == (True, False, False):
        return "VERT"
    elif mode == (False, True, False):
        return "EDGE"
    elif mode == (False, False, True):
        return "FACE"
    else:
        return None


def set_mode(string, extend=False, expand=False):
    if string == "EDIT":
        bpy.ops.object.mode_set(mode='EDIT')
    elif string == "OBJECT":
        bpy.ops.object.mode_set(mode='OBJECT')
    elif string in ["VERT", "EDGE", "FACE"]:
        bpy.ops.mesh.select_mode(use_extend=extend, use_expand=expand, type=string)



def change_context(string):
    area = bpy.context.area

    print("area:", area)

    old_type = area.type

    print("old type before:", old_type)

    area.type = string

    print("old type after:", old_type)

    return old_type


def change_pivot(string):
    space_data = bpy.context.space_data
    old_type = space_data.pivot_point
    space_data.pivot_point = string
    return old_type


def DM_check():
    return addon_check("DECALmachine")


def MM_check():
    return addon_check("MESHmachine")


def RM_check():
    return addon_check("RIGmachine")


def HOps_check():
    return addon_check("HOps")


def BC_check():
    return addon_check("BoxCutter")


def AM_check():
    return addon_check("asset_management", precise=False)


def GP_check():
    return addon_check("GroupPro")


def addon_check(string, precise=True):
    for addon in bpy.context.user_preferences.addons.keys():
        if precise:
            if string == addon:
                return True
        else:
            if string.lower() in addon.lower():
                return True
    return False


def move_to_cursor(obj, scene):
    obj.select = True
    make_active(obj)
    obj.location = bpy.context.scene.cursor_location


def lock(obj, location=True, rotation=True, scale=True):
    if location:
        for idx, _ in enumerate(obj.lock_location):
            obj.lock_location[idx] = True

    if rotation:
        for idx, _ in enumerate(obj.lock_rotation):
            obj.lock_rotation[idx] = True

    if scale:
        for idx, _ in enumerate(obj.lock_scale):
            obj.lock_scale[idx] = True


def open_folder(pathstring):

    if platform.system() == "Windows":
        os.startfile(pathstring)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", pathstring])
    else:
        # subprocess.Popen(["xdg-open", pathstring])
        os.system('xdg-open "%s" %s &' % (pathstring, "> /dev/null 2> /dev/null"))  # > sends stdout,  2> sends stderr


def makedir(pathstring):
    if not os.path.exists(pathstring):
        os.makedirs(pathstring)
    return pathstring


def addon_prefs(addonstring):
    return bpy.context.user_preferences.addons[addonstring].preferences


def DM_prefs():
    return bpy.context.user_preferences.addons["DECALmachine"].preferences


def MM_prefs():
    return bpy.context.user_preferences.addons["MESHmachine"].preferences


def RM_prefs():
    return bpy.context.user_preferences.addons["RIGmachine"].preferences


def M3_prefs():
    return bpy.context.user_preferences.addons["MACHIN3tools"].preferences


def make_selection(string, idlist):
    mesh = bpy.context.object.data
    set_mode("OBJECT")
    if string == "VERT":
        for v in idlist:
            mesh.vertices[v].select = True
    elif string == "EDGE":
        for e in idlist:
            mesh.edges[e].select = True
    elif string == "FACE":
        for p in idlist:
            mesh.polygons[p].select = True
    set_mode("EDIT")


def get_selection(string):
    active = bpy.context.active_object
    active.update_from_editmode()

    if string == "VERT":
        return [v.index for v in active.data.vertices if v.select]
    if string == "EDGE":
        return [e.index for e in active.data.edges if e.select]
    if string == "FACE":
        return [f.index for f in active.data.polygons if f.select]


def get_selection_history():
    mesh = bpy.context.object.data
    bm = bmesh.from_edit_mesh(mesh)
    vertlist = [elem.index for elem in bm.select_history if isinstance(elem, bmesh.types.BMVert)]
    return vertlist


def get_scene_scale():
    return bpy.context.scene.unit_settings.scale_length


def lerp(value1, value2, amount):
    if 0 <= amount <= 1:
        return (amount * value2) + ((1 - amount) * value1)


def select_shortest_path_topo(obj):
    """
    "author": "G Bantle, Bagration, MACHIN3",
    "source": "https://blenderartists.org/forum/showthread.php?58564-Path-Select-script(Update-20060307-Ported-to-C-now-in-CVS",
    """

    def build_mesh_graph(verts, edges):
        mg = {}
        for v in verts:
            mg[v] = []

        for e in edges:
            mg[e.verts[0]].append((e.verts[1], 1))
            mg[e.verts[1]].append((e.verts[0], 1))

        return mg

    def dijkstra(mg, vstart, vend):
        d = dict.fromkeys(mg.keys(), sys.maxsize)
        predecessor = dict.fromkeys(mg.keys())

        # The distance of the start vert to itself is 0
        d[vstart] = 0

        unknownverts = []
        unknownverts.append((0, vstart))

        while vstart != vend:
            # unknownverts.sort()
            dist, u = unknownverts[0]  # Get the next vert that is closest to s
            edges = mg[u]

            for vlinked, distance in edges:  # v = neighbour vert, w = distance from u to this vert
                if d[vlinked] > d[u] + distance:
                    d[vlinked] = d[u] + distance
                    unknownverts.append((d[vlinked], vlinked))
                    predecessor[vlinked] = u

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

    import time

    start = time.time()


    # create bmesh
    bm = bmesh.from_edit_mesh(obj.data)
    bm.normal_update()
    bm.verts.ensure_lookup_table()

    verts = [v for v in bm.verts]
    edges = [e for e in bm.edges]

    mg = build_mesh_graph(verts, edges)

    selection = [v for v in verts if v.select]

    # [(shortest dist from s (start vert) to vert, vert)]
    path = dijkstra(mg, selection[0], selection[1])

    # remove duplicates, keeps order, see https://stackoverflow.com/a/480227
    path = f7(path)


    for v in path:
        v.select = True


    bmesh.update_edit_mesh(obj.data)



    end = time.time()

    print(end - start)


def select_shortest_path_len(obj):
    """
    "author": "G Bantle, Bagration, MACHIN3",
    "source": "https://blenderartists.org/forum/showthread.php?58564-Path-Select-script(Update-20060307-Ported-to-C-now-in-CVS",
    """

    def build_mesh_graph(verts, edges):
        mg = {}
        for v in verts:
            mg[v] = []

        for e in edges:
            mg[e.verts[0]].append((e.verts[1], e.calc_length()))
            mg[e.verts[1]].append((e.verts[0], e.calc_length()))

        return mg

    def dijkstra(mg, vstart, vend):
        d = dict.fromkeys(mg.keys(), sys.maxsize)
        predecessor = dict.fromkeys(mg.keys())

        # The distance of the start vert to itself is 0
        d[vstart] = 0

        unknownverts = []
        unknownverts.append((0, vstart))

        while vstart != vend:
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

        # print(unknownverts)

        while endvert is not None:  # Backtrace rom the end vertex using the "predecessor" dict
            path.append(endvert)
            endvert = predecessor[endvert]

        return reversed(path)


    def f7(seq):
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x))]


    # create bmesh
    bm = bmesh.from_edit_mesh(obj.data)
    bm.normal_update()
    bm.verts.ensure_lookup_table()

    verts = [v for v in bm.verts]
    edges = [e for e in bm.edges]

    mg = build_mesh_graph(verts, edges)

    # for m in mg:
        # print([(v.index, dist) for v, dist in mg[m]])

    # """


    selection = [v for v in verts if v.select]

    # [(shortest dist from s (start vert) to vert, vert)]
    path = dijkstra(mg, selection[0], selection[1])

    # remove duplicates, keeps order, see https://stackoverflow.com/a/480227
    path = f7(path)


    for v in path:
        v.select = True

    # """


    bmesh.update_edit_mesh(obj.data)


####



class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}
        # Set distance to infinity for all nodes
        self.distance = sys.maxsize
        # Mark all nodes unvisited
        self.visited = False
        # Predecessor
        self.previous = None


    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight


    def get_connections(self):
        return self.adjacent.keys()


    def get_id(self):
        return self.id


    def get_weight(self, neighbor):
        return self.adjacent[neighbor]


    def set_distance(self, dist):
        self.distance = dist


    def get_distance(self):
        return self.distance


    def set_previous(self, prev):
        self.previous = prev


    def set_visited(self):
        self.visited = True


    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])

    def __lt__(self, other):
        return self.distance < other.distance


class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0


    def __iter__(self):
        return iter(self.vert_dict.values())


    def add_vertex(self, node):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex


    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None


    def add_edge(self, frm, to, cost=0):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)


        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)


    def get_vertices(self):
        return self.vert_dict.keys()


    def set_previous(self, current):
        self.previous = current


    def get_previous(self, current):
        return self.previous


def shortest(v, path):
    ''' make shortest path from v.previous'''
    if v.previous:
        path.append(v.previous.get_id())
        shortest(v.previous, path)
    return


import heapq


def dijkstra(aGraph, start):
    print("Dijkstra's shortest path")
    # Set the distance for the start node to zero
    start.set_distance(0)


    # Put tuple pair into the priority queue
    unvisited_queue = [(v.get_distance(), v) for v in aGraph]
    heapq.heapify(unvisited_queue)


    while len(unvisited_queue):
        # Pops a vertex with the smallest distance
        uv = heapq.heappop(unvisited_queue)
        current = uv[1]
        current.set_visited()


        # for next in v.adjacent:
        for next in current.adjacent:
            # if visited, skip
            if next.visited:
                continue
            new_dist = current.get_distance() + current.get_weight(next)

            if new_dist < next.get_distance():
                next.set_distance(new_dist)
                next.set_previous(current)
                # print('updated : current = %s next = %s new_dist = %s' %(current.get_id(), next.get_id(), next.get_distance()))
            # else:
                # print('not updated : current = %s next = %s new_dist = %s' %(current.get_id(), next.get_id(), next.get_distance()))


        # Rebuild heap
        # 1. Pop every item
        while len(unvisited_queue):
            heapq.heappop(unvisited_queue)
        # 2. Put all vertices not visited into the queue
        unvisited_queue = [(v.get_distance(), v) for v in aGraph if not v.visited]
        heapq.heapify(unvisited_queue)



def select_shortest_path_bomb(obj):
    # from here https://blenderartists.org/t/will-this-dijkstra-shortest-path-algorithm-in-the-bge/689127
    # will this modification: https://github.com/laurentluce/python-algorithms/issues/6

    # create bmesh
    bm = bmesh.from_edit_mesh(obj.data)
    bm.normal_update()
    bm.verts.ensure_lookup_table()

    g = Graph()

    for v in bm.verts:
        g.add_vertex(v.index)


    for e in bm.edges:
        # g.add_edge(e.verts[0].index, e.verts[1].index, 1)
        g.add_edge(e.verts[0].index, e.verts[1].index, e.calc_length())


    # g.add_vertex('a')
    # g.add_vertex('b')
    # g.add_vertex('c')
    # g.add_vertex('d')
    # g.add_vertex('e')
    # g.add_vertex('f')


    # g.add_edge('a', 'b', 7)
    # g.add_edge('a', 'c', 9)
    # g.add_edge('a', 'f', 14)
    # g.add_edge('b', 'c', 10)
    # g.add_edge('b', 'd', 15)
    # g.add_edge('c', 'd', 11)
    # g.add_edge('c', 'f', 2)
    # g.add_edge('d', 'e', 6)
    # g.add_edge('e', 'f', 9)



    """
    print('Graph data:')
    for v in g:
        for w in v.get_connections():
            vid = v.get_id()
            wid = w.get_id()
            print('( %s , %s, %3d)' % (vid, wid, v.get_weight(w)))
    # """

    # """

    sel = [v.index for v in bm.verts if v.select]


    dijkstra(g, g.get_vertex(sel[0]))
    # dijkstra(g, g.get_vertex('a'))

    target = g.get_vertex(sel[1])
    # target = g.get_vertex('e')
    path = [target.get_id()]
    shortest(target, path)

    print('The shortest path : %s' %(path[::-1]))

    # """

    print(path)

    for p in path:
        bm.verts[p].select = True


    bmesh.update_edit_mesh(obj.data)
