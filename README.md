Implicit Forward
=====

This package implements the implicit forward differentiation algorithm, a fast algorithm to compute the Jacobian of the Lasso.

It also implements a large number of competitors, such as the foward differentiation, the backward differentiation, and the implicit differentiation.


Install
=====
To be able to run the experiments  you should install the conda environment:

```bash
conda env create -f environment.yml
conda activate sparse-ho-env
```
(you may need to open  fresh new terminal).

To be able to run the code you first need to run, in this folder (root folder):
```bash
pip install -e .
```

You should now be able to run a friendly example which reproduces Figure 1:
```bash
ipython -i examples/plot_time_to_compute_single_gradient.py
```

If you want to compare methods to solve the whole hyperparameter optimization
problem, you can run the friendly example:
```bash
ipython -i examples/plot_friendly_example.py
```
in particular you can play with the parameters of the bayesian solver in
the implicit_forward/bayesian.py file.

You should now be able to play with the methods and the estimators.


Reproduce all experiments
=====
Scripts to reproduce all the experiments: Figure 2, 3, 4, 5.

Be careful, you may want to run these scripts on a server with multiple CPUs.

All the figures of the paper can be reproduced.
What is needed is in the implicit_forward/expes folder:
- Figure 2:
    ```bash
    run main_lasso_pred.py
    ipython -i plot_lasso_pred.py
    ```
- Figure 3:
    ```bash
    run main_lasso_est.py
    ipython -i plot_lasso_est.py
    ```
- Figure 4:
    ```bash
    run main_wLasso.py
    ipython -i plot_wLasso.py
    ```
- Figure 5 in Appendix:
    ```bash
    run main_mcp_pred.py
    ipython -i plot_mcp_pred.py
    ```