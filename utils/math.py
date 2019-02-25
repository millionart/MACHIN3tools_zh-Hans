from mathutils import Matrix


def get_sca_matrix(vector):
    scale_mx = Matrix()
    for i in range(3):
        scale_mx[i][i] = vector[i]
    return scale_mx


def get_rot_matrix(quaternion):
    return quaternion.to_matrix().to_4x4()


def get_loc_matrix(vector):
    return Matrix.Translation(vector)
