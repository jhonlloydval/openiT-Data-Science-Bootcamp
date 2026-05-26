"""
╔══════════════════════════════════════════════════════════╗
║       NumPy Comprehensive Guide — Basic → Professional  ║
╚══════════════════════════════════════════════════════════╝
"""

import numpy as np
import os

# ─── Terminal helpers ─────────────────────────────────────

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input("\n  ↵  Press Enter to continue...")

def title(text, char="═"):
    w = 60
    print(f"\n{char * w}\n  {text}\n{char * w}\n")

def sub(text):
    pad = 52 - len(text)
    print(f"\n  ┌─ {text} {'─' * max(pad, 2)}")

def note(text):
    print(f"  ▸ {text}")


# ══════════════════════════════════════════════════════════
# BASIC
# ══════════════════════════════════════════════════════════

def s1_creation():
    clear()
    title("1 · ARRAY CREATION  ── BASIC")

    sub("From Python sequences")
    a = np.array([10, 20, 30, 40])
    b = np.array([[1, 2, 3], [4, 5, 6]], dtype=float)
    print(f"  1D : {a}")
    print(f"  2D :\n{b}")
    note("dtype is inferred unless you pass dtype=…")

    pause()
    sub("Built-in constructors")
    print(f"  zeros(3)          → {np.zeros(3)}")
    print(f"  ones((2,3))       →\n{np.ones((2, 3))}")
    print(f"  full((2,3), 9)    →\n{np.full((2, 3), 9)}")
    print(f"  eye(3)            →\n{np.eye(3, dtype=int)}")
    print(f"  diag([1,2,3])     →\n{np.diag([1, 2, 3])}")
    print(f"  empty((2,2))      → uninitialized (fast placeholder)")

    pause()
    sub("Ranges & spacing")
    print(f"  arange(0, 10, 2)  → {np.arange(0, 10, 2)}")
    print(f"  linspace(0, 1, 6) → {np.linspace(0, 1, 6).round(3)}")
    print(f"  logspace(1, 3, 4) → {np.logspace(1, 3, 4).round(2)}")

    pause()
    sub("Views vs copies — critical concept")
    original = np.array([1, 2, 3])
    view = original[:]
    copy = original.copy()
    original[0] = 99
    print(f"  original after change : {original}")
    print(f"  view[:]               : {view}   ← shares memory, changed too!")
    print(f"  .copy()               : {copy}   ← independent, unchanged")
    note("Always use .copy() when you need an independent array")


def s2_attributes():
    clear()
    title("2 · ARRAY ATTRIBUTES & dtypes  ── BASIC")

    a = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.int32)
    sub("Core attributes")
    print(f"  Array        :\n{a}")
    print(f"  .shape       : {a.shape}      → (rows, cols)")
    print(f"  .ndim        : {a.ndim}          → number of dimensions")
    print(f"  .size        : {a.size}          → total element count")
    print(f"  .dtype       : {a.dtype}      → element data type")
    print(f"  .itemsize    : {a.itemsize}          → bytes per element")
    print(f"  .nbytes      : {a.nbytes}         → total bytes in array")

    pause()
    sub("Common dtypes at a glance")
    dtypes = [np.int8, np.int16, np.int32, np.int64,
              np.float32, np.float64, np.complex128, np.bool_]
    for dt in dtypes:
        arr = np.array([1], dtype=dt)
        print(f"  {str(dt.__name__):15s} → {arr.dtype}  ({arr.itemsize} bytes)")

    pause()
    sub("Type casting with .astype()")
    x = np.array([1.7, 2.9, 3.1])
    print(f"  float64 : {x}")
    print(f"  → int   : {x.astype(int)}    (truncates, does NOT round!)")
    print(f"  → str   : {x.astype(str)}")
    note("Use np.round() first if you need rounding, then cast to int")


def s3_indexing():
    clear()
    title("3 · INDEXING & SLICING  ── BASIC")

    a = np.arange(10)
    sub("1D indexing")
    print(f"  array    : {a}")
    print(f"  a[3]     : {a[3]}")
    print(f"  a[-1]    : {a[-1]}   (last element)")
    print(f"  a[2:7]   : {a[2:7]}")
    print(f"  a[::2]   : {a[::2]}  (every other)")
    print(f"  a[::-1]  : {a[::-1]}  (reversed)")

    pause()
    sub("2D indexing  [row, col]")
    m = np.arange(1, 13).reshape(3, 4)
    print(f"  matrix (3×4) :\n{m}")
    print(f"  m[1, 2]      : {m[1, 2]}  → row 1, col 2")
    print(f"  m[0, :]      : {m[0, :]}  → entire row 0")
    print(f"  m[:, 1]      : {m[:, 1]}     → entire col 1")
    print(f"  m[0:2, 1:3]  :\n{m[0:2, 1:3]}  → sub-matrix")
    note("Slices return VIEWS; single-index steps return VIEWS too")

    pause()
    sub("3D indexing — think [layer, row, col]")
    t = np.arange(24).reshape(2, 3, 4)
    print(f"  shape (2,3,4)  → t[1, 2, 3] = {t[1, 2, 3]}")
    print(f"  t[0]     :\n{t[0]}    → first layer (3×4 matrix)")
    print(f"  t[:, 1]  :\n{t[:, 1]}  → row 1 from every layer")


# ══════════════════════════════════════════════════════════
# INTERMEDIATE
# ══════════════════════════════════════════════════════════

def s4_reshape():
    clear()
    title("4 · RESHAPING & MANIPULATION  ── INTERMEDIATE")

    a = np.arange(1, 13)
    sub("Reshape — same data, new shape")
    print(f"  arange(1,13)        : {a}")
    print(f"  .reshape(3,4)       :\n{a.reshape(3, 4)}")
    print(f"  .reshape(2,2,3)     :\n{a.reshape(2, 2, 3)}")
    print(f"  .reshape(-1, 4)     : -1 lets NumPy infer that dimension")
    note("Total elements must stay the same after reshape")

    pause()
    sub("Flatten vs Ravel")
    m = a.reshape(3, 4)
    print(f"  matrix :\n{m}")
    print(f"  .flatten() : {m.flatten()}  → always a copy")
    print(f"  .ravel()   : {m.ravel()}  → view when possible (faster)")

    pause()
    sub("Transpose & axis manipulation")
    print(f"  m.T  (3×4 → 4×3):\n{m.T}")
    print(f"  np.moveaxis(3D): reorders axes by index")
    t = np.zeros((2, 3, 4))
    moved = np.moveaxis(t, 0, -1)
    print(f"  moveaxis(shape(2,3,4), 0→-1) → shape {moved.shape}")

    pause()
    sub("Insert, Delete, Append  (return new arrays)")
    x = np.array([1, 2, 3, 4])
    print(f"  x                  : {x}")
    print(f"  insert(x, 2, [10,11]) : {np.insert(x, 2, [10, 11])}")
    print(f"  delete(x, 1)          : {np.delete(x, 1)}")
    print(f"  append(x, [5,6])      : {np.append(x, [5, 6])}")
    note("None of these modify x in-place; they always return NEW arrays")


def s5_math_stats():
    clear()
    title("5 · MATH & STATISTICAL OPERATIONS  ── INTERMEDIATE")

    data = np.array([4., 7., 13., 2., 1., 9., 15., 6., 11., 8.])
    sub("Basic statistics")
    print(f"  data      : {data}")
    print(f"  sum       : {data.sum()}")
    print(f"  mean      : {data.mean():.2f}")
    print(f"  median    : {np.median(data)}")
    print(f"  std       : {data.std():.4f}")
    print(f"  var       : {data.var():.4f}")
    print(f"  min/max   : {data.min()} / {data.max()}")
    print(f"  argmin/max: {data.argmin()} / {data.argmax()}  (indices)")
    print(f"  peak-to-peak: {data.max() - data.min()}")
    print(f"  percentiles [25,50,75]: {np.percentile(data, [25, 50, 75])}")

    pause()
    sub("Axis-aware operations — essential for data science")
    m = np.array([[1, 2, 3], [4, 5, 6]])
    print(f"  matrix :\n{m}")
    print(f"  sum(axis=0) : {m.sum(axis=0)}  → collapse rows  (per column)")
    print(f"  sum(axis=1) : {m.sum(axis=1)}  → collapse cols (per row)")
    print(f"  mean(axis=0): {m.mean(axis=0)}")
    print(f"  cumsum()    : {m.cumsum()}  (axis=None → flatten first)")
    note("axis=0 collapses along rows; axis=1 collapses along columns")

    pause()
    sub("Math functions")
    x = np.array([0., np.pi / 6, np.pi / 4, np.pi / 2])
    print(f"  sin(x)          : {np.sin(x).round(3)}")
    print(f"  cos(x)          : {np.cos(x).round(3)}")
    print(f"  exp([0,1,2])    : {np.exp([0, 1, 2]).round(3)}")
    print(f"  log([1,e,e²])   : {np.log([1, np.e, np.e**2]).round(3)}")
    print(f"  sqrt([4,9,16])  : {np.sqrt([4, 9, 16])}")
    print(f"  abs([-3,4,-1])  : {np.abs([-3, 4, -1])}")
    print(f"  power([2,3],3)  : {np.power([2, 3], 3)}")

    pause()
    sub("Normalization techniques")
    d = np.array([10., 20., 30., 40., 50.])
    min_max = (d - d.min()) / (d.max() - d.min())
    z_score = (d - d.mean()) / d.std()
    print(f"  data               : {d}")
    print(f"  min-max [0,1]      : {min_max}")
    print(f"  z-score            : {z_score.round(2)}")

    pause()
    sub("Clipping & rounding")
    noisy = np.array([5., 15., 150., -10., 30.])
    print(f"  data              : {noisy}")
    print(f"  clip(0, 50)       : {np.clip(noisy, 0, 50)}")
    vals = np.array([-1.7, 0.5, 2.3, 4.8])
    print(f"  round(vals)       : {np.round(vals)}")
    print(f"  floor(vals)       : {np.floor(vals)}")
    print(f"  ceil(vals)        : {np.ceil(vals)}")


def s6_boolean_fancy():
    clear()
    title("6 · BOOLEAN & FANCY INDEXING  ── INTERMEDIATE")

    a = np.array([3, 8, 15, 22, 30, 41, 5, 18])
    sub("Boolean indexing")
    mask = a > 15
    print(f"  array           : {a}")
    print(f"  mask (>15)      : {mask}")
    print(f"  a[mask]         : {a[mask]}")
    print(f"  a[a % 2 == 0]   : {a[a % 2 == 0]}  (even numbers)")
    print(f"  a[(a>5) & (a<25)]: {a[(a > 5) & (a < 25)]}")
    note("Use & | ~ for AND OR NOT on boolean arrays (not 'and'/'or'/'not')")

    pause()
    sub("np.where — indices or conditional replacement")
    print(f"  array              : {a}")
    print(f"  where(a>15) indices: {np.where(a > 15)[0]}")
    replaced = np.where(a > 20, 99, a)
    print(f"  where(a>20, 99, a) : {replaced}  (ternary replacement)")

    pause()
    sub("Fancy indexing — integer array as index")
    b = np.array([100, 200, 300, 400, 500])
    idx = np.array([0, 2, 4, 2])
    print(f"  array    : {b}")
    print(f"  idx      : {idx}")
    print(f"  b[idx]   : {b[idx]}  (repeats allowed)")

    pause()
    sub("np.select — multi-condition branching")
    grades = np.array([45, 72, 88, 55, 95, 61])
    conds   = [grades >= 90, grades >= 75, grades >= 60]
    choices = ["A",           "B",           "C"]
    labels  = np.select(conds, choices, default="F")
    print(f"  grades : {grades}")
    print(f"  labels : {labels}")
    note("Conditions are evaluated in order; first True wins")


def s7_broadcasting():
    clear()
    title("7 · BROADCASTING  ── INTERMEDIATE")

    note("Broadcasting: NumPy auto-expands smaller arrays to match shapes")
    note("Rule: align dims from the RIGHT; each must be equal OR 1\n")

    sub("Scalar broadcast")
    a = np.array([1, 2, 3])
    print(f"  [1,2,3] + 10 = {a + 10}")
    print(f"  [1,2,3] * 2  = {a * 2}")

    pause()
    sub("Vector broadcast over matrix (row-wise)")
    m = np.ones((3, 3), dtype=int)
    v = np.array([10, 20, 30])
    print(f"  matrix (3×3)  :\n{m}")
    print(f"  vector (3,)   : {v}")
    print(f"  matrix + row  :\n{m + v}  → added to each row")

    pause()
    sub("Column vector broadcast (column-wise)")
    col = np.array([[1], [2], [3]])
    print(f"  col (3×1)     :\n{col}")
    print(f"  matrix + col  :\n{m + col}  → added to each col")

    pause()
    sub("np.newaxis — adding dimensions for broadcasting")
    r = np.arange(1, 4)
    c = np.arange(1, 5)
    outer = r[:, np.newaxis] * c
    print(f"  rows {r}  ×  cols {c}  →  outer product:\n{outer}")
    note("r[:, np.newaxis] turns shape (3,) into (3,1) → broadcasts with (4,)")


def s8_stacking_splitting():
    clear()
    title("8 · STACKING & SPLITTING  ── INTERMEDIATE")

    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])
    sub("1D stacking")
    print(f"  a = {a},  b = {b}")
    print(f"  hstack        : {np.hstack([a, b])}  (along axis 1 / cols)")
    print(f"  vstack        :\n{np.vstack([a, b])}  (along axis 0 / rows)")
    print(f"  stack(axis=0) :\n{np.stack([a, b], axis=0)}")
    print(f"  stack(axis=1) :\n{np.stack([a, b], axis=1)}")
    print(f"  concatenate   : {np.concatenate([a, b])}")

    pause()
    sub("2D stacking")
    m1 = np.array([[1, 2], [3, 4]])
    m2 = np.array([[5, 6], [7, 8]])
    print(f"  m1:\n{m1}\n  m2:\n{m2}")
    print(f"  vstack:\n{np.vstack([m1, m2])}")
    print(f"  hstack:\n{np.hstack([m1, m2])}")
    print(f"  dstack (depth):\n{np.dstack([m1, m2])}")

    pause()
    sub("Splitting")
    x = np.arange(12)
    print(f"  arange(12): {x}")
    print(f"  split(x,3): {np.split(x, 3)}")
    m = np.arange(16).reshape(4, 4)
    print(f"  matrix(4×4):\n{m}")
    print(f"  hsplit(m,2):\n{np.hsplit(m, 2)}")
    print(f"  vsplit(m,2):\n{np.vsplit(m, 2)}")
    note("array_split() allows unequal splits; split() requires equal sizes")


# ══════════════════════════════════════════════════════════
# PROFESSIONAL
# ══════════════════════════════════════════════════════════

def s9_linalg():
    clear()
    title("9 · LINEAR ALGEBRA  ── PROFESSIONAL")

    v1 = np.array([1., 2., 3.])
    v2 = np.array([4., 5., 6.])
    sub("Dot product & matrix multiplication")
    print(f"  v1 · v2  (dot)   : {np.dot(v1, v2)}")
    print(f"  v1 @ v2  (matmul): {v1 @ v2}  ← preferred syntax")
    A = np.array([[1., 2.], [3., 4.]])
    B = np.array([[5., 6.], [7., 8.]])
    print(f"  A @ B:\n{A @ B}")

    pause()
    sub("Determinant, trace, rank")
    M = np.array([[4., 7.], [2., 6.]])
    print(f"  M:\n{M}")
    print(f"  det(M)          : {np.linalg.det(M):.2f}")
    print(f"  trace(M)        : {np.trace(M)}")
    print(f"  matrix_rank(M)  : {np.linalg.matrix_rank(M)}")

    pause()
    sub("Inverse & solving linear systems")
    print(f"  inv(M):\n{np.linalg.inv(M)}")
    b_vec = np.array([19., 8.])
    x_sol = np.linalg.solve(M, b_vec)
    print(f"  solve(M, b): {x_sol}  → Mx = b")
    note("Use linalg.solve() instead of inv() @ b — numerically more stable")

    pause()
    sub("Eigenvalues & eigenvectors")
    eigenvals, eigenvecs = np.linalg.eig(M)
    print(f"  eigenvalues  : {eigenvals.round(4)}")
    print(f"  eigenvectors :\n{eigenvecs.round(4)}")

    pause()
    sub("SVD & vector norms")
    U, S, Vt = np.linalg.svd(M)
    print(f"  SVD singular values: {S.round(4)}")
    print(f"  U :\n{U.round(3)}")
    print(f"  Vt:\n{Vt.round(3)}")
    print(f"  L1 norm  (v1): {np.linalg.norm(v1, ord=1):.3f}")
    print(f"  L2 norm  (v1): {np.linalg.norm(v1):.3f}")
    print(f"  Frobenius (M): {np.linalg.norm(M):.3f}")


def s10_random():
    clear()
    title("10 · RANDOM MODULE  ── PROFESSIONAL")

    sub("Two APIs — legacy vs modern")
    note("Legacy:  np.random.seed(42); np.random.randn(5)")
    note("Modern:  rng = np.random.default_rng(42)  ← recommended\n")
    rng = np.random.default_rng(seed=42)

    pause()
    sub("Distributions")
    print(f"  uniform(0,1, 5)     : {rng.uniform(0, 1, 5).round(3)}")
    print(f"  standard_normal(5)  : {rng.standard_normal(5).round(3)}")
    print(f"  normal(μ=5, σ=2, 5) : {rng.normal(5, 2, 5).round(3)}")
    print(f"  integers(1, 7, 5)   : {rng.integers(1, 7, 5)}  (dice rolls)")
    print(f"  binomial(10, 0.5,5) : {rng.binomial(10, 0.5, 5)}")
    print(f"  poisson(λ=3, 5)     : {rng.poisson(3, 5)}")
    print(f"  exponential(2, 5)   : {rng.exponential(2, 5).round(3)}")
    print(f"  choice([A,B,C], 4)  : {rng.choice(['A','B','C'], 4)}")

    pause()
    sub("Shuffle & sampling")
    arr = np.arange(10)
    rng.shuffle(arr)
    print(f"  shuffle(arange(10))       : {arr}")
    arr2 = np.arange(10)
    print(f"  choice(arr, 4)            : {rng.choice(arr2, 4)}")
    print(f"  choice(arr, 4, replace=F) : {rng.choice(arr2, 4, replace=False)}")

    pause()
    sub("Simulating real data (common DS pattern)")
    heights = rng.normal(170, 10, 1000)
    print(f"  1000 heights  (μ=170, σ=10):")
    print(f"    mean         : {heights.mean():.2f} cm")
    print(f"    std          : {heights.std():.2f} cm")
    print(f"    95% CI       : ({np.percentile(heights,2.5):.2f}, {np.percentile(heights,97.5):.2f})")
    print(f"    quartiles    : {np.percentile(heights, [25,50,75]).round(2)}")


def s11_ufuncs():
    clear()
    title("11 · UNIVERSAL FUNCTIONS (ufuncs)  ── PROFESSIONAL")

    note("ufuncs operate element-wise; implemented in C — very fast\n")

    sub("Built-in ufuncs")
    a = np.array([1., 4., 9., 16.])
    print(f"  np.sqrt    : {np.sqrt(a)}")
    print(f"  np.log2    : {np.log2(a)}")
    print(f"  np.add     : {np.add(a, a)}")
    print(f"  np.maximum : {np.maximum(a, np.array([2., 2., 8., 20.]))}")
    print(f"  np.floor_divide: {np.floor_divide(a, 3)}")

    pause()
    sub("ufunc methods: reduce, accumulate, outer")
    x = np.array([1, 2, 3, 4, 5])
    print(f"  x                    : {x}")
    print(f"  add.reduce(x)        : {np.add.reduce(x)}  (total sum)")
    print(f"  add.accumulate(x)    : {np.add.accumulate(x)}  (running sum)")
    print(f"  multiply.accumulate  : {np.multiply.accumulate(x)}  (factorial-like)")
    print(f"  multiply.outer:\n{np.multiply.outer([1,2,3],[1,2,3])}  (multiplication table)")

    pause()
    sub("np.vectorize — apply Python functions element-wise")
    def grade_label(x):
        if x >= 90: return "A"
        if x >= 75: return "B"
        if x >= 60: return "C"
        return "F"
    vlabel = np.vectorize(grade_label)
    scores = np.array([45, 72, 88, 55, 95, 61])
    print(f"  scores : {scores}")
    print(f"  grades : {vlabel(scores)}")
    note("np.vectorize is convenient; but NOT faster than real ufuncs")

    pause()
    sub("np.einsum — Einstein summation (advanced indexing)")
    A = np.arange(1, 10).reshape(3, 3)
    B = np.arange(9).reshape(3, 3)
    print(f"  A:\n{A}")
    print(f"  matmul    'ij,jk->ik' :\n{np.einsum('ij,jk->ik', A, B)}")
    print(f"  element   'ij,ij->ij' :\n{np.einsum('ij,ij->ij', A, B)}")
    print(f"  trace     'ii->'      : {np.einsum('ii->', A)}")
    print(f"  sum all   'ij->'      : {np.einsum('ij->', A)}")
    note("einsum is often the fastest path for complex tensor operations")


def s12_structured():
    clear()
    title("12 · STRUCTURED ARRAYS  ── PROFESSIONAL")

    note("Structured arrays hold heterogeneous column data — like a table\n")

    sub("Defining a structured dtype")
    dt = np.dtype([
        ('name',  'U10'),
        ('age',   np.int32),
        ('score', np.float64)
    ])
    data = np.array([
        ('Alice', 24, 88.5),
        ('Bob',   31, 72.3),
        ('Carol', 28, 95.0)
    ], dtype=dt)
    print(f"  dtype:\n  {dt}")
    print(f"  data :\n{data}")

    pause()
    sub("Field access")
    print(f"  data['name']  : {data['name']}")
    print(f"  data['score'] : {data['score']}")
    print(f"  data[0]       : {data[0]}")

    pause()
    sub("Sorting & filtering by field")
    by_score = np.sort(data, order='score')
    print(f"  sorted by score:\n{by_score}")
    top = data[data['score'] > 80]
    print(f"  score > 80    : {top['name']}")
    note("Great for lightweight tabular data when Pandas is overkill")


def s13_memory():
    clear()
    title("13 · VIEWS, COPIES & MEMORY LAYOUT  ── PROFESSIONAL")

    sub("Views vs Copies — the fundamental rule")
    a = np.arange(10)
    view = a[2:6]
    copy = a[2:6].copy()
    view[0] = 99
    print(f"  original after view[0]=99 : {a}  ← original changed!")
    print(f"  copy is unchanged          : {copy}")
    print(f"  view.base is a  : {view.base is a}  (shares memory)")
    print(f"  copy.base       : {copy.base}        (owns its data)")

    pause()
    sub("C order (row-major) vs F order (col-major)")
    m = np.arange(9).reshape(3, 3)
    print(f"  matrix:\n{m}")
    print(f"  C order (row-major): {m.flatten(order='C')}")
    print(f"  F order (col-major): {m.flatten(order='F')}")
    note("Default is C order; F order matches Fortran/MATLAB convention")

    pause()
    sub("Strides — how NumPy steps through memory")
    x = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.int32)
    print(f"  shape   : {x.shape}")
    print(f"  strides : {x.strides}  bytes to advance per axis")
    note(f"  int32=4 bytes → stride 12 = next row, stride 4 = next col")

    pause()
    sub("Contiguous arrays")
    t = x.T
    print(f"  x.T.flags.c_contiguous  : {t.flags['C_CONTIGUOUS']}")
    t_cont = np.ascontiguousarray(t)
    print(f"  after ascontiguousarray : {t_cont.flags['C_CONTIGUOUS']}")
    note("Non-contiguous layouts can hurt performance; make contiguous when needed")


def s14_advanced():
    clear()
    title("14 · ADVANCED TRICKS  ── PROFESSIONAL")

    sub("np.unique — fast unique values with counts")
    arr = np.array([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5])
    u, counts = np.unique(arr, return_counts=True)
    print(f"  array   : {arr}")
    print(f"  unique  : {u}")
    print(f"  counts  : {counts}")

    pause()
    sub("np.argsort & indirect sorting")
    a = np.array([3, 1, 4, 1, 5, 9, 2, 6])
    print(f"  array           : {a}")
    print(f"  sort            : {np.sort(a)}")
    idx = np.argsort(a)
    print(f"  argsort indices : {idx}")
    print(f"  a[argsort]      : {a[idx]}  (same as sort)")
    note("argsort is useful for sorting parallel arrays by a key column")

    pause()
    sub("np.searchsorted — binary search on sorted arrays")
    s = np.array([10, 20, 30, 40, 50])
    print(f"  sorted : {s}")
    print(f"  searchsorted(25): {np.searchsorted(s, 25)}  (insert position)")
    print(f"  searchsorted(20, 'right'): {np.searchsorted(s, 20, side='right')}")

    pause()
    sub("np.tile & np.repeat")
    x = np.array([1, 2, 3])
    print(f"  x             : {x}")
    print(f"  repeat(x, 3)  : {np.repeat(x, 3)}")
    print(f"  tile(x, 3)    : {np.tile(x, 3)}")
    print(f"  tile(x,(2,3)) :\n{np.tile(x, (2, 3))}")

    pause()
    sub("np.apply_along_axis")
    m = np.array([[1, 5, 3], [7, 2, 9], [4, 8, 6]])
    centered = np.apply_along_axis(lambda r: r - r.mean(), axis=1, arr=m)
    print(f"  matrix:\n{m}")
    print(f"  mean-centered rows:\n{centered.round(2)}")

    pause()
    sub("Masked arrays — handle NaN / missing data")
    data = np.array([1.0, 2.0, np.nan, 4.0, np.nan, 6.0])
    masked = np.ma.masked_invalid(data)
    print(f"  data with NaN  : {data}")
    print(f"  masked mean    : {masked.mean():.2f}  (ignores NaN)")
    print(f"  masked sum     : {masked.sum():.2f}")
    note("np.ma gives you NaN-safe statistics without dropping data")

    pause()
    sub("np.poly1d — polynomial operations")
    p = np.poly1d([2, -3, 1])  # 2x² - 3x + 1
    print(f"  polynomial: {p}")
    print(f"  p(0)={p(0)},  p(1)={p(1)},  p(2)={p(2)}")
    roots = np.roots([2, -3, 1])
    print(f"  roots: {roots}")
    note("np.polyfit(x, y, deg) fits a polynomial to data points")


# ══════════════════════════════════════════════════════════
# MENU
# ══════════════════════════════════════════════════════════

SECTIONS = {
    # ── BASIC ──────────────────────────────────────────────
    "1":  ("Array Creation",                    s1_creation),
    "2":  ("Array Attributes & dtypes",         s2_attributes),
    "3":  ("Indexing & Slicing",                s3_indexing),
    # ── INTERMEDIATE ───────────────────────────────────────
    "4":  ("Reshaping & Manipulation",          s4_reshape),
    "5":  ("Math & Statistical Operations",     s5_math_stats),
    "6":  ("Boolean & Fancy Indexing",          s6_boolean_fancy),
    "7":  ("Broadcasting",                      s7_broadcasting),
    "8":  ("Stacking & Splitting",              s8_stacking_splitting),
    # ── PROFESSIONAL ───────────────────────────────────────
    "9":  ("Linear Algebra",                    s9_linalg),
    "10": ("Random Module",                     s10_random),
    "11": ("Universal Functions (ufuncs)",      s11_ufuncs),
    "12": ("Structured Arrays",                 s12_structured),
    "13": ("Views, Copies & Memory Layout",     s13_memory),
    "14": ("Advanced Tricks",                   s14_advanced),
}


def show_menu():
    clear()
    print("""
╔══════════════════════════════════════════════════════════╗
║       NumPy Comprehensive Guide — Basic → Professional  ║
╚══════════════════════════════════════════════════════════╝

  ── BASIC ─────────────────────────────────────────────────
   [1]  Array Creation
   [2]  Array Attributes & dtypes
   [3]  Indexing & Slicing

  ── INTERMEDIATE ──────────────────────────────────────────
   [4]  Reshaping & Manipulation
   [5]  Math & Statistical Operations
   [6]  Boolean & Fancy Indexing
   [7]  Broadcasting
   [8]  Stacking & Splitting

  ── PROFESSIONAL ──────────────────────────────────────────
   [9]  Linear Algebra
   [10] Random Module
   [11] Universal Functions (ufuncs)
   [12] Structured Arrays
   [13] Views, Copies & Memory Layout
   [14] Advanced Tricks

  ──────────────────────────────────────────────────────────
   [A]  Run ALL sections     [0]  Exit
    """)


def main():
    while True:
        show_menu()
        choice = input("  Select section: ").strip().lower()

        if choice == "0":
            clear()
            print("  Goodbye! Keep practicing NumPy.\n")
            break

        elif choice == "a":
            for key in SECTIONS:
                SECTIONS[key][1]()
                pause()

        elif choice in SECTIONS:
            SECTIONS[choice][1]()
            input("\n  ↵  Back to menu...")

        else:
            input("  Invalid choice. Press Enter to try again...")


if __name__ == "__main__":
    main()
