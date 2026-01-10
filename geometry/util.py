import numpy as np


def compute_affine_transform(src_pts, dst_pts):
    def to_matrix(p1, p2, p3):
        return np.array([
            [p1[0], p2[0], p3[0]],
            [p1[1], p2[1], p3[1]],
            [1,     1,     1]
        ])

    A = to_matrix(*src_pts)
    B = to_matrix(*dst_pts)
    T = B @ np.linalg.inv(A)

    a, c, e = T[0]
    b, d, f = T[1]

    return f"matrix({a:.6f},{b:.6f},{c:.6f},{d:.6f},{e:.2f},{f:.2f})"
