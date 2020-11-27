"""
===========================
How to use custom metrics?
===========================
This example shows how to compute customize metrics using a callback function
as in scipy.
"""

# Authors: Quentin Bertrand <quentin.bertrand@inria.fr>
#          Quentin Klopfenstein <quentin.klopfenstein@u-bourgogne.fr>
#
# License: BSD (3-clause)

import numpy as np
from numpy.linalg import norm
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.model_selection import train_test_split

from sparse_ho.models import Lasso
from sparse_ho.criterion import HeldOutMSE
from sparse_ho.implicit_forward import ImplicitForward
from sparse_ho.utils import Monitor
from sparse_ho.ho import grad_search
from sklearn.datasets import make_regression

from libsvmdata.datasets import fetch_libsvm


print(__doc__)

# dataset = 'rcv1'
dataset = 'simu'

if dataset == 'rcv1':
    X, y = fetch_libsvm('rcv1_train')
else:
    X, y = make_regression(
        n_samples=1000, n_features=1000, noise=40, random_state=0)

# The dataset is split in 2: the data for training and validation: X
# Unseen data X_test, asserting the quality of the model
X, X_test, y, y_test = train_test_split(X, y, test_size=0.333, random_state=0)

n_samples = X.shape[0]
idx_train = np.arange(0, n_samples // 2)
idx_val = np.arange(n_samples // 2, n_samples)

alpha_max = np.max(
    np.abs(X[idx_train, :].T.dot(y[idx_train]))) / len(idx_train)


estimator = linear_model.Lasso(
    fit_intercept=False, max_iter=1e5, warm_start=True)

#############################################################################
# Call back definition
objs_test = []


def callback(val, grad, mask, dense, log_alpha):
    beta = np.zeros(len(mask))
    beta[mask] = dense
    # The custom quantity is added at each outer iteration:
    # here the loss on test data
    objs_test.append(
        norm(X_test[:, mask] @ dense - y_test) ** 2 / len(y_test))

##############################################################################
# Grad-search with sparse-ho and callback
# ---------------------------------------


model = Lasso(estimator=estimator)
criterion = HeldOutMSE(idx_train, idx_val)
algo = ImplicitForward(criterion)
# use Monitor(callback) with your custom callback
monitor = Monitor(callback=callback)

grad_search(
    algo, criterion, model, X, y, np.log(alpha_max / 10), monitor,
    n_outer=30, tol=1e-7)


##############################################################################
# Plot results
# ------------

plt.plot(monitor.times, objs_test)
plt.tick_params(width=5)
plt.xlabel("Times (s)")
plt.ylabel("MSE on test")
plt.tight_layout()
plt.show(block=False)
