"""
=============================
Lasso with Cross-validation
=============================

This example shows how to perform hyperparameter optimisation
for a Lasso using a full cross-validation score.
"""

# Authors: Quentin Bertrand <quentin.bertrand@inria.fr>
#          Quentin Klopfenstein <quentin.klopfenstein@u-bourgogne.fr>
#
# License: BSD (3-clause)

import time
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.datasets import make_regression
from sklearn.linear_model import LassoCV
from sparse_ho.models import Lasso
from sparse_ho.criterion import CV
from sparse_ho.implicit_forward import ImplicitForward
from sparse_ho.utils import Monitor
from sparse_ho.grad_search_CV import grad_search_CV
from sparse_ho.datasets.real import load_libsvm

from sklearn.model_selection import KFold

print(__doc__)

# dataset = 'rcv1'
dataset = 'simu'

if dataset == 'rcv1':
    X, y = load_libsvm('rcv1_train')
else:
    X, y = make_regression(n_samples=500, n_features=1000)

kf = KFold(n_splits=5, shuffle=True)

# for train, test in kf.split(X):
#     print("%s %s" % (train, test))

print("Starting path computation...")
n_samples = len(y)
alpha_max = np.max(np.abs(X.T.dot(y))) / n_samples

n_alphas = 10
p_alphas = np.geomspace(1, 0.0001, n_alphas)
alphas = alpha_max * p_alphas

tol = 1e-8


##############################################################################
# Cross-validation with scikit-learn
# ----------------------------------
print('scikit started')

t0 = time.time()
reg = LassoCV(
    cv=kf, verbose=False, tol=tol, fit_intercept=False,
    alphas=alphas).fit(X, y)
reg.score(X, y)
t_sk = time.time() - t0

print('scikit finished')
print("Time to compute CV for scikit-learn: %.2f" % t_sk)


##############################################################################
# Now do the hyperparameter optimization with implicit differentiation
# --------------------------------------------------------------------
print('sparse-ho started')

t0 = time.time()
Model = Lasso
Criterion = CV
Algo = ImplicitForward
log_alpha0 = np.log(alpha_max / 10)
monitor = Monitor()
grad_search_CV(
    X, y, Model, Criterion, Algo, log_alpha0, monitor, n_outer=10,
    verbose=False, cv=kf, random_state=0, test_size=0.33,
    tolerance_decrease='constant', tol=tol,
    t_max=1000)
t_grad_search = time.time() - t0

print('sparse-ho finished')
print("Time to compute CV for sparse-ho: %.2f" % t_grad_search)


##############################################################################
# Plot results
# ------------
objs = reg.mse_path_.mean(axis=1)

p_alphas_grad = np.exp(np.array(monitor.log_alphas)) / alpha_max
objs_grad = np.array(monitor.objs)

current_palette = sns.color_palette("colorblind")

fig = plt.figure(figsize=(5, 3))
plt.semilogx(
    p_alphas, objs, color=current_palette[0])
plt.semilogx(
    p_alphas, objs, 'bo', label='0-order method (grid-search)',
    color=current_palette[1])
plt.semilogx(
    p_alphas_grad, objs_grad, 'bX', label='1-st order method',
    color=current_palette[2])
plt.xlabel(r"$\lambda / \lambda_{\max}$")
plt.ylabel("Cross-validation loss")
axes = plt.gca()
plt.tick_params(width=5)
plt.legend()
plt.tight_layout()
plt.show(block=False)
