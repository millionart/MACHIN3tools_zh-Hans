from mathutils import Matrix, Vector
from math import degrees


def get_center_between_points(point1, point2, center=0.5):
    return point1 + (point2 - point1) * center


def get_center_between_verts(vert1, vert2, center=0.5):
    return get_center_between_points(vert1.co, vert2.co, center=center)


def get_edge_normal(edge):
    return average_normals([f.normal for f in edge.link_faces])


def average_normals(normalslist):
    avg = Vector()

    for n in normalslist:
        avg += n

    return avg.normalized()


def flatten_matrix(mx):
    dimension = len(mx)
    return [mx[j][i] for i in range(dimension) for j in range(dimension)]


def get_loc_matrix(location):
    return Matrix.Translation(location)


def get_rot_matrix(rotation):
    return rotation.to_matrix().to_4x4()


def get_sca_matrix(scale):
    scale_mx = Matrix()
    for i in range(3):
        scale_mx[i][i] = scale[i]
    return scale_mx


def create_rotation_matrix_from_normal(obj, normal):
    mx = obj.matrix_world

    objup = mx.to_3x3() @ Vector((0, 0, 1))

    dot = normal.dot(objup)
    if abs(round(dot, 6)) == 1:
        # use x instead of z as the up axis
        objup = mx.to_3x3() @ Vector((1, 0, 0))

    tangent = objup.cross(normal)
    binormal = tangent.cross(-normal)

    # create rotation matrix from coordnate vectors, see http://renderdan.blogspot.com/2006/05/rotation-matrix-from-axis-vectors.html
    rotmx = Matrix()
    rotmx[0].xyz = tangent.normalized()
    rotmx[1].xyz = binormal.normalized()
    rotmx[2].xyz = normal.normalized()

    # transpose, because blender is column major?
    return rotmx.transposed()


def create_rotation_matrix_from_edge(obj, edge):
    mx = obj.matrix_world

    # call the direction, the binormal, we want this to be the y axis at the end
    binormal = mx.to_3x3() @ (edge.verts[1].co - edge.verts[0].co)

    # get a normal from the linked faces
    if edge.link_faces:
        normal = mx.to_3x3() @ get_edge_normal(edge)

    # without linked faces get a normal from the objects up vector
    else:
        objup = mx.to_3x3() @ Vector((0, 0, 1))

        # use the x axis if the edge is already pointing in z
        dot = binormal.dot(objup)
        if abs(round(dot, 6)) == 1:
            objup = mx.to_3x3() @ Vector((1, 0, 0))

        normal = objup.cross(binormal)

    # get the tangent
    tangent = normal.cross(-binormal)

    # create rotation matrix from coordnate vectors, see http://renderdan.blogspot.com/2006/05/rotation-matrix-from-axis-vectors.html
    rotmx = Matrix()
    rotmx[0].xyz = tangent.normalized()
    rotmx[1].xyz = binormal.normalized()
    rotmx[2].xyz = normal.normalized()

    # transpose, because blender is column major?
    return rotmx.transposed()


def create_rotation_difference_matrix_from_quat(v1, v2):
    q = v1.rotation_difference(v2)
    return q.to_matrix().to_4x4()


def create_selection_bbox(coords):
    minx = min(coords, key=lambda x: x[0])
    maxx = max(coords, key=lambda x: x[0])

    miny = min(coords, key=lambda x: x[1])
    maxy = max(coords, key=lambda x: x[1])

    minz = min(coords, key=lambda x: x[2])
    maxz = max(coords, key=lambda x: x[2])

    midx = get_center_between_points(minx, maxx)
    midy = get_center_between_points(miny, maxy)
    midz = get_center_between_points(minz, maxz)

    mid = Vector((midx[0], midy[1], midz[2]))

    bbox = [Vector((minx.x, miny.y, minz.z)), Vector((maxx.x, miny.y, minz.z)),
            Vector((maxx.x, maxy.y, minz.z)), Vector((minx.x, maxy.y, minz.z)),
            Vector((minx.x, miny.y, maxz.z)), Vector((maxx.x, miny.y, maxz.z)),
            Vector((maxx.x, maxy.y, maxz.z)), Vector((minx.x, maxy.y, maxz.z))]

    return bbox, mid


def get_right_and_up_axes(context, mx):
    r3d = context.space_data.region_3d

    # get view right (and up) vectors in 3d space
    view_right = r3d.view_rotation @ Vector((1, 0, 0))
    view_up = r3d.view_rotation @ Vector((0, 1, 0))

    # get the right and up axes in the objects or world space, depending on the axis that was passed in
    axes_right = []
    axes_up = []

    for idx, axis in enumerate([Vector((1, 0, 0)), Vector((0, 1, 0)), Vector((0, 0, 1))]):
        dot = view_right.dot(mx.to_3x3() @ axis)
        axes_right.append((dot, idx))

        dot = view_up.dot(mx.to_3x3() @ axis)
        axes_up.append((dot, idx))

    axis_right = max(axes_right, key=lambda x: abs(x[0]))
    axis_up = max(axes_up, key=lambda x: abs(x[0]))

    # determine flip
    flip_right = True if axis_right[0] < 0 else False
    flip_up = True if axis_up[0] < 0 else False

    return axis_right[1], axis_up[1], flip_right, flip_up
