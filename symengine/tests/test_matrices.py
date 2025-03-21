from symengine import symbols
from symengine.lib.symengine_wrapper import (DenseMatrix, Symbol, Integer,
    function_symbol, I, NonSquareMatrixError, ShapeError, zeros, ones, eye,
    ImmutableMatrix)
from symengine.utilities import raises


try:
    import numpy as np
    HAVE_NUMPY = True
except ImportError:
    HAVE_NUMPY = False


def test_get():
    A = DenseMatrix([[1, 2], [3, 4]])

    assert A.get(0, 0) == 1
    assert A.get(0, 1) == 2
    assert A.get(1, 1) == 4

    a = Symbol("a")
    b = Symbol("b")
    c = Symbol("c")
    d = Symbol("d")
    A = DenseMatrix(2, 2, [a, b, c, d])

    assert A.get(0, 0) == a
    assert A.get(1, 0) == c
    assert A.get(1, 1) == d

    assert A.get(-1, 0) == c
    assert A.get(-1, -1) == d

    raises(IndexError, lambda: A.get(2, 0))
    raises(IndexError, lambda: A.get(0, 2))
    raises(IndexError, lambda: A.get(-3, 0))


def test_tolist():
    A = DenseMatrix([2, 3])
    assert A.shape == (2, 1)
    assert A.tolist() == [[2], [3]]


def test_get_item():
    A = DenseMatrix(3, 3, [1, 2, 3, 4, 5, 6, 7, 8, 9])

    assert A[5] == 6
    assert A[-1] == 9
    assert A[2, 2] == 9
    assert A[-2, 2] == 6

    assert A[1:2, 0] == DenseMatrix(1, 1, [4])
    assert A[1:3, 0] == DenseMatrix(2, 1, [4, 7])
    assert A[1:3, 0] == DenseMatrix(2, 1, [4, 7])
    assert A[1:3, 1:] == DenseMatrix(2, 2, [5, 6, 8, 9])
    assert A[1:3, :1] == DenseMatrix(2, 1, [4, 7])
    assert A[0, 0:] == DenseMatrix(1, 3, [1, 2, 3])
    assert A[2, :] == DenseMatrix(1, 3, [7, 8, 9])
    assert A[:2, -2:] == DenseMatrix(2, 2, [2, 3, 5, 6])
    assert A[1:, :3] == DenseMatrix(2, 3, [4, 5, 6, 7, 8, 9])
    assert A[1:] == [2, 3, 4, 5, 6, 7, 8, 9]
    assert A[-2:] == [8, 9]
    assert A[[0, 2], 0] == DenseMatrix(2, 1, [1, 7])
    assert A[[0, 2], [0]] == DenseMatrix(2, 1, [1, 7])
    assert A[0, [0, 2]] == DenseMatrix(1, 2, [1, 3])
    assert A[[0], [0, 2]] == DenseMatrix(1, 2, [1, 3])

    raises(IndexError, lambda: A[-10])
    raises(IndexError, lambda: A[9])

    raises(IndexError, lambda: A[1:3, 3])
    raises(IndexError, lambda: A[1:3, -4])

    A = zeros(3, 4)
    assert list(A[0, :]) == [0, 0, 0, 0]
    assert list(A[:, 0]) == [0, 0, 0]

    A = zeros(4, 3)
    assert list(A[:, 0]) == [0, 0, 0, 0]
    assert list(A[0, :]) == [0, 0, 0]


def test_set_item():
    A = DenseMatrix(3, 3, [1, 2, 3, 4, 5, 6, 7, 8, 9])

    A[2] = 7
    A[2, 2] = 8
    A[-2] = 3
    A[-2, -1] = 1

    assert A == DenseMatrix(3, 3, [1, 2, 7, 4, 5, 1, 7, 3, 8])

    A[0, :] = [10, 11, 12]
    assert A == DenseMatrix(3, 3, [10, 11, 12, 4, 5, 1, 7, 3, 8])

    A[:, 1] = [13, 14, 15]
    assert A == DenseMatrix(3, 3, [10, 13, 12, 4, 14, 1, 7, 15, 8])

    A[0::2, :] = [[1, 2, 3], [4, 5, 6]]
    assert A == DenseMatrix(3, 3, [1, 2, 3, 4, 14, 1, 4, 5, 6])

    B = DenseMatrix(A)
    B[[0, 2], 0] = -1
    assert B == DenseMatrix(3, 3, [-1, 2, 3, 4, 14, 1, -1, 5, 6])

    B = DenseMatrix(A)
    B[[0, 2], 0] = [-1, -2]
    assert B == DenseMatrix(3, 3, [-1, 2, 3, 4, 14, 1, -2, 5, 6])

    B = DenseMatrix(A)
    B[[0, 2], 0] = [[-1], [-2]]
    assert B == DenseMatrix(3, 3, [-1, 2, 3, 4, 14, 1, -2, 5, 6])

    B = DenseMatrix(A)
    B[[0, 2], [0]] = [-1, -2]
    assert B == DenseMatrix(3, 3, [-1, 2, 3, 4, 14, 1, -2, 5, 6])

    B = DenseMatrix(A)
    B[[0, 2], [0]] = [[-1], [-2]]
    assert B == DenseMatrix(3, 3, [-1, 2, 3, 4, 14, 1, -2, 5, 6])

    B = DenseMatrix(A)
    B[0, [0, 2]] = [-1, -2]
    assert B == DenseMatrix(3, 3, [-1, 2, -2, 4, 14, 1, 4, 5, 6])

    B = DenseMatrix(A)
    B[0, [0, 2]] = -1
    assert B == DenseMatrix(3, 3, [-1, 2, -1, 4, 14, 1, 4, 5, 6])

    B = DenseMatrix(A)
    B[:, [0, 2]] = -1
    assert B == DenseMatrix(3, 3, [-1, 2, -1, -1, 14, -1, -1, 5, -1])

    B = DenseMatrix(A)
    B[[0, 1], [0, 2]] = -1
    assert B == DenseMatrix(3, 3, [-1, 2, -1, -1, 14, -1, 4, 5, 6])

    A = zeros(3, 4)
    B = ones(1, 4)
    A[0, :] = B
    assert A[0, :] == B

    A = zeros(3, 4)
    B = ones(3, 1)
    A[:, 0] = B
    assert A[:, 0] == B


def test_set():
    i7 = Integer(7)
    y = Symbol("y")
    g = function_symbol("g", y)
    c = 2*I + 3
    A = DenseMatrix(2, 2,
                    [Integer(5), Symbol("x"),
                     function_symbol("f", Symbol("x")), 1 + I])

    A.set(0, 0, i7)
    assert A.get(0, 0) == i7
    A.set(0, 1, y)
    assert A.get(0, 1) == y
    A.set(1, 0, g)
    assert A.get(1, 0) == g
    A.set(1, 1, c)
    assert A.get(1, 1) == c


def test_det():
    A = DenseMatrix(2, 2, [1, 2, 3, 4])
    assert A.det() == -2

    a = Symbol("a")
    b = Symbol("b")
    c = Symbol("c")
    d = Symbol("d")
    A = DenseMatrix(2, 2, [a, b, c, d])
    assert A.det() == a*d - b*c

    A = DenseMatrix(3, 2, [1, 2, 3, 4, 5, 6])
    raises(NonSquareMatrixError, lambda: A.det())


def test_inv():
    A = DenseMatrix(2, 2, [1, 0, 0, 1])
    assert A.inv() == A

    A = DenseMatrix(2, 2, [1, 2, 2, 3])
    B = DenseMatrix(2, 2, [-3, 2, 2, -1])

    assert A.inv('LU') == B
    assert A.inv('FFLU') == B
    assert A.inv('GJ') == B


def test_add_matrix():
    A = DenseMatrix(2, 2, [1, 2, 3, 4])
    B = DenseMatrix(2, 2, [1, 0, 0, 1])

    assert A.add_matrix(B) == DenseMatrix(2, 2, [2, 2, 3, 5])

    a = Symbol("a")
    b = Symbol("b")
    c = Symbol("c")
    d = Symbol("d")
    A = DenseMatrix(2, 2, [a + b, a - b, a, b])
    B = DenseMatrix(2, 2, [a - b, a + b, -a, b])

    assert A.add_matrix(B) == DenseMatrix(2, 2, [2*a, 2*a, 0, 2*b])
    assert A + B == DenseMatrix(2, 2, [2*a, 2*a, 0, 2*b])

    C = DenseMatrix(1, 2, [a, b])
    raises(ShapeError, lambda: A + C)


def test_mul_matrix():
    A = DenseMatrix(2, 2, [1, 2, 3, 4])
    B = DenseMatrix(2, 2, [1, 0, 0, 1])

    assert A.mul_matrix(B) == A

    a = Symbol("a")
    b = Symbol("b")
    c = Symbol("c")
    d = Symbol("d")
    A = DenseMatrix(2, 2, [a, b, c, d])
    B = DenseMatrix(2, 2, [1, 0, 1, 0])

    assert A.mul_matrix(B) == DenseMatrix(2, 2, [a + b, 0, c + d, 0])
    assert A * B == DenseMatrix(2, 2, [a + b, 0, c + d, 0])

    C = DenseMatrix(2, 3, [1, 2, 3, 2, 3, 4])
    D = DenseMatrix(3, 2, [3, 4, 4, 5, 5, 6])

    assert C.mul_matrix(D) == DenseMatrix(2, 2, [26, 32, 38, 47])

    raises(ShapeError, lambda: A*D)


def test_add_scalar():
    A = DenseMatrix(2, 2, [1, 2, 3, 4])

    a = Symbol("a")
    assert A.add_scalar(a) == DenseMatrix(2, 2, [1 + a, 2 + a, 3 + a, 4 + a])

    i5 = Integer(5)
    assert A.add_scalar(i5) == DenseMatrix(2, 2, [6, 7, 8, 9])
    raises(TypeError, lambda: A + 5)
    raises(TypeError, lambda: 5 + A)


def test_mul_scalar():
    A = DenseMatrix(2, 2, [1, 2, 3, 4])

    a = Symbol("a")
    assert A.mul_scalar(a) == DenseMatrix(2, 2, [a, 2*a, 3*a, 4*a])

    i5 = Integer(5)
    assert A.mul_scalar(i5) == DenseMatrix(2, 2, [5, 10, 15, 20])
    assert A * 5 == DenseMatrix(2, 2, [5, 10, 15, 20])
    assert 5 * A == DenseMatrix(2, 2, [5, 10, 15, 20])
    assert a * A == DenseMatrix(2, 2, [a, 2*a, 3*a, 4*a])


def test_neg():
    A = DenseMatrix(2, 3, [1, 2, 3, 4, 5, 6])
    B = DenseMatrix(2, 3, [-1, -2, -3, -4, -5, -6])
    assert -A == B


def test_sub():
    A = DenseMatrix(2, 2, [1, 2, 3, 4])
    B = DenseMatrix(2, 2, [0, -1, -2, -3])
    a = Symbol("a")
    assert A - B == DenseMatrix(2, 2, [1, 3, 5, 7])

    C = DenseMatrix(2, 1, [1, 2])
    raises(ShapeError, lambda: A - C)
    raises(TypeError, lambda: A - 5)
    raises(TypeError, lambda: 5 - A)


def test_div():
    w, x, y, z = symbols("w, x, y, z")
    A = DenseMatrix([[w, x], [y, z]])
    B = DenseMatrix([[1, 1], [1, 0]])
    C = DenseMatrix([[x, w - x], [z, y - z]])

    assert A / 2 == DenseMatrix([[w/2, x/2], [y/2, z/2]])
    assert C * B == A
    assert A / B == C

    raises(TypeError, lambda: 2/A)


def test_transpose():
    A = DenseMatrix(3, 3, [1, 2, 3, 4, 5, 6, 7, 8, 9])

    assert A.transpose() == DenseMatrix(3, 3, [1, 4, 7, 2, 5, 8, 3, 6, 9])

    A = DenseMatrix(2, 2, [1, 2, 2, 1])

    assert A.transpose() == A


def test_LU():
    A = DenseMatrix(3, 3, [1, 3, 5, 2, 5, 6, 8, 3, 1])
    L, U = A.LU()

    assert L == DenseMatrix(3, 3, [1, 0, 0, 2, 1, 0, 8, 21, 1])
    assert U == DenseMatrix(3, 3, [1, 3, 5, 0, -1, -4, 0, 0, 45])


def test_LDL():
    A = DenseMatrix(3, 3, [4, 12, -16, 12, 37, -43, -16, -43, 98])

    L, D = A.LDL()

    assert L == DenseMatrix(3, 3, [1, 0, 0, 3, 1, 0, -4, 5, 1])
    assert D == DenseMatrix(3, 3, [4, 0, 0, 0, 1, 0, 0, 0, 9])


def test_solve():
    A = DenseMatrix(4, 4, [1, 2, 3, 4, 2, 2, 3, 4, 3, 3, 3, 4, 9, 8, 7, 6])
    b = DenseMatrix(4, 1, [10, 11, 13, 30])
    y = DenseMatrix(4, 1, [1, 1, 1, 1])

    x = A.solve(b, 'LU')
    assert x == y
    x = A.solve(b, 'FFLU')
    assert x == y
    x = A.solve(b, 'FFGJ')
    assert x == y


def test_FFLU():
    A = DenseMatrix(4, 4, [1, 2, 3, 4, 2, 2, 3, 4, 3, 3, 3, 4, 9, 8, 7, 6])

    L, U = A.FFLU()
    assert L == DenseMatrix(4, 4, [1, 0, 0, 0, 2, -2, 0, -0, 3,
                                   -3, 3, 0, 9, -10, 10, -10])
    assert U == DenseMatrix(4, 4, [1, 2, 3, 4, 0, -2, -3, -4,
                                   0, 0, 3, 4, 0, 0, 0, -10])


def test_FFLDU():
    A = DenseMatrix(3, 3, [1, 2, 3, 5, -3, 2, 6, 2, 1])
    L, D, U = A.FFLDU()

    assert L == DenseMatrix(3, 3, [1, 0, 0, 5, -13, 0, 6, -10, 1])
    assert D == DenseMatrix(3, 3, [1, 0, 0, 0, -13, 0, 0, 0, -13])
    assert U == DenseMatrix(3, 3, [1, 2, 3, 0, -13, -13, 0, 0, 91])


def test_str_repr():
    d = DenseMatrix(3, 2, [1, 2, 3, 4, 5, 6])
    assert str(d) == '[1, 2]\n[3, 4]\n[5, 6]\n'
    assert str(d) == repr(d)


def test_DenseMatrix_symbols():
    x, y, z = symbols("x y z")
    D = DenseMatrix(4, 4,
                    [1, 0, 1, 0,
                     0, z, y, 0,
                     z, 1, x, 1,
                     1, 1, 0, 0])
    assert D.get(1, 2) == y


def test_jacobian():
    x, y, z, t = symbols("x y z t")
    J_correct = DenseMatrix(4, 4,
                            [1, 0, 1, 0,
                             0, z, y, 0,
                             z, 1, x, 1,
                             1, 1, 0, 0])
    D = DenseMatrix(4, 1, [x+z, y*z, z*x+y+t, x+y])
    x = DenseMatrix(4, 1, [x, y, z, t])
    J = D.jacobian(x)
    assert J == J_correct


def test_size():
    A = DenseMatrix(2, 2, [1, 2, 3, 4])
    assert A.size == 4


def test_shape():
    A = DenseMatrix(2, 2, [1, 2, 3, 4])
    assert A.shape == (2, 2)


def test_reshape():
    A = DenseMatrix(2, 2, [1, 2, 3, 4])
    B = DenseMatrix(4, 1, [1, 2, 3, 4])
    C = A.reshape(4, 1)
    assert C == B
    assert C != A


# @pytest.mark.skipif(not HAVE_NUMPY, reason='requires numpy')
def test_dump_real():
    if not HAVE_NUMPY:  # nosetests work-around
        return
    ref = [1, 2, 3, 4]
    A = DenseMatrix(2, 2, ref)
    out = np.empty(4)
    A.dump_real(out)
    assert np.allclose(out, ref)


# @pytest.mark.skipif(not HAVE_NUMPY, reason='requires numpy')
def test_dump_complex():
    if not HAVE_NUMPY:  # nosetests work-around
        return
    ref = [1j, 2j, 3j, 4j]
    A = DenseMatrix(2, 2, ref)
    out = np.empty(4, dtype=np.complex128)
    A.dump_complex(out)
    assert np.allclose(out, ref)


def test_col_swap():
    A = DenseMatrix(2, 2, [1, 2, 3, 4])
    B = DenseMatrix(2, 2, [2, 1, 4, 3])
    A.col_swap(0, 1)
    assert A == B


def test_fill():
    A = zeros(4, 4)
    A.fill(1)
    B = ones(4, 4)
    assert A == B
    assert A.rows == B.rows
    assert A.cols == B.cols
    assert A.shape == B.shape == (4, 4)


def test_row_swap():
    A = DenseMatrix(2, 2, [1, 2, 3, 4])
    B = DenseMatrix(2, 2, [3, 4, 1, 2])
    A.row_swap(0, 1)
    assert A == B


def test_row_col_del():
    e = DenseMatrix(3, 3, [1, 2, 3, 4, 5, 6, 7, 8, 9])
    raises(IndexError, lambda: e.row_del(5))
    raises(IndexError, lambda: e.row_del(-5))
    raises(IndexError, lambda: e.col_del(5))
    raises(IndexError, lambda: e.col_del(-5))

    assert e.row_del(-1) == DenseMatrix([[1, 2, 3], [4, 5, 6]])
    assert e.col_del(-1) == DenseMatrix([[1, 2], [4, 5]])

    e = DenseMatrix(3, 3, [1, 2, 3, 4, 5, 6, 7, 8, 9])
    assert e.row_del(1) == DenseMatrix([[1, 2, 3], [7, 8, 9]])
    assert e.col_del(1) == DenseMatrix([[1, 3], [7, 9]])


def test_row_join():
    assert eye(3).row_join(DenseMatrix([7, 7, 7])) == \
           DenseMatrix([[1, 0, 0, 7],
                        [0, 1, 0, 7],
                        [0, 0, 1, 7]])


def test_col_join():
    assert eye(3).col_join(DenseMatrix([[7, 7, 7]])) == \
           DenseMatrix([[1, 0, 0],
                        [0, 1, 0],
                        [0, 0, 1],
                        [7, 7, 7]])


def test_row_insert():
    M = zeros(3)
    V = ones(1, 3)
    assert M.row_insert(1, V) == DenseMatrix([[0, 0, 0],
                                              [1, 1, 1],
                                              [0, 0, 0],
                                              [0, 0, 0]])


def test_col_insert():
    M = zeros(3)
    V = ones(3, 1)
    assert M.col_insert(1, V) == DenseMatrix([[0, 1, 0, 0],
                                              [0, 1, 0, 0],
                                              [0, 1, 0, 0]])


def test_rowmul():
    M = ones(3)
    assert M.rowmul(2, 2) == DenseMatrix([[1, 1, 1],
                                          [1, 1, 1],
                                          [2, 2, 2]])


def test_rowadd():
    M = ones(3)
    assert M.rowadd(2, 1, 1) == DenseMatrix([[1, 1, 1],
                                             [1, 1, 1],
                                             [2, 2, 2]])


def test_row_col():
    m = DenseMatrix(3, 3, [1, 2, 3, 4, 5, 6, 7, 8, 9])
    assert m.row(0) == DenseMatrix(1, 3, [1, 2, 3])
    assert m.col(0) == DenseMatrix(3, 1, [1, 4, 7])


def test_is_square():
    m = DenseMatrix([[1],[1]])
    m2 = DenseMatrix([[2, 2], [2, 2]])
    assert not m.is_square
    assert m2.is_square


def test_dot():
    A = DenseMatrix(2, 3, [1, 2, 3, 4, 5, 6])
    B = DenseMatrix(2, 1, [7, 8])
    assert A.dot(B) == DenseMatrix(1, 3, [39, 54, 69])
    assert ones(1, 3).dot(ones(3, 1)) == 3


def test_cross():
    M = DenseMatrix(1, 3, [1, 2, 3])
    V = DenseMatrix(1, 3, [3, 4, 5])
    assert M.cross(V) == DenseMatrix(1, 3, [-2, 4, -2])
    raises(ShapeError, lambda:
        DenseMatrix(1, 2, [1, 1]).cross(DenseMatrix(1, 2, [1, 1])))


def test_immutablematrix():
    A = ImmutableMatrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    assert A.shape == (3, 3)
    assert A[1, 2] == 6
    assert A[2, 2] == 9

    assert A[1, :] == ImmutableMatrix([[4, 5, 6]])
    assert A[:2, :2] == ImmutableMatrix([[1, 2], [4, 5]])

    with raises(TypeError):
        A[2, 2] = 5

    X = DenseMatrix([[1, 2], [3, 4]])
    assert X.as_immutable() == ImmutableMatrix([[1, 2], [3, 4]])

    assert X.det() == -2

    X = ImmutableMatrix(eye(3))
    assert isinstance(X + A, ImmutableMatrix)
    assert isinstance(X * A, ImmutableMatrix)
    assert isinstance(X * 2, ImmutableMatrix)
    assert isinstance(2 * X, ImmutableMatrix)

    X = ImmutableMatrix([[1, 2], [3, 4]])
    Y = ImmutableMatrix([[1], [0]])
    assert type(X.LUsolve(Y)) == ImmutableMatrix

    x = Symbol("x")
    X = ImmutableMatrix([[1, 2], [3, 4]])
    Y = ImmutableMatrix([[1, 2], [x, 4]])
    assert Y.subs(x, 3) == X
    assert Y.xreplace(x, 3) == X

    X = ImmutableMatrix([[1, 2], [3, 4]])
    Y = ImmutableMatrix([[5], [6]])
    Z = X.row_join(Y)
    assert isinstance(Z, ImmutableMatrix)
    assert Z == ImmutableMatrix([[1, 2, 5], [3, 4, 6]])

    X = ImmutableMatrix([[1, 2], [3, 4]])
    Y = ImmutableMatrix([[5, 6]])
    Z = X.col_join(Y)
    assert isinstance(Z, ImmutableMatrix)
    assert Z == ImmutableMatrix([[1, 2], [3, 4], [5, 6]])

def test_atoms():
    a = Symbol("a")
    b = Symbol("b")
    X = DenseMatrix([[a, 2], [b, 4]])
    assert X.atoms(Symbol) == set([a, b])
