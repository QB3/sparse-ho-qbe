import numpy as np
import pandas
import seaborn as sns
import matplotlib.pyplot as plt
from expes.utils import configure_plt

save_fig = True
fig_dir = "../../../CD_SUGAR/tex/journal/prebuiltimages/"
fig_dir_svg = "../../../CD_SUGAR/tex/journal/images/"

configure_plt()

# init()

fontsize = 16

current_palette = sns.color_palette("colorblind")
dict_color = {}
dict_color["grid_search"] = current_palette[3]
dict_color["random"] = current_palette[5]
dict_color["bayesian"] = current_palette[0]
dict_color["implicit_forward"] = current_palette[2]
dict_color["fast_iterdiff"] = current_palette[2]
dict_color["forward"] = current_palette[4]
dict_color["implicit"] = current_palette[1]
dict_color["lhs"] = current_palette[6]

dict_method = {}
dict_method["forward"] = 'F. Iterdiff.'
dict_method["implicit_forward"] = 'Imp. F. Iterdiff. (ours)'
dict_method["fast_iterdiff"] = 'Imp. F. Iterdiff. (ours)'
dict_method['implicit'] = 'Implicit'
dict_method['grid_search'] = 'Grid-search'
dict_method['bayesian'] = 'Bayesian'
dict_method['random'] = 'Random-search'
dict_method['hyperopt'] = 'Random-search'
dict_method['backward'] = 'B. Iterdiff.'
dict_method['lhs'] = 'Lattice Hyp.'


dict_markers = {}
dict_markers["forward"] = 'o'
dict_markers["implicit_forward"] = 'X'
dict_markers["fast_iterdiff"] = 'X'
dict_markers['implicit'] = 'v'
dict_markers['grid_search'] = 'd'
dict_markers['bayesian'] = 'P'
dict_markers['random'] = '*'
dict_markers['lhs'] = 'H'

# current_palette = sns.color_palette("colorblind")
# dict_method = {}
# dict_method["forward"] = 'F. iterdiff.'
# dict_method["implicit_forward"] = 'Imp. F. iterdiff. (ours)'
# dict_method['implicit'] = 'Implicit diff. (ours)'
# dict_method['grid_search'] = 'Grid-search'
# dict_method['bayesian'] = 'Bayesian'
# dict_method['random'] = 'Random-search'
# dict_method['hyperopt'] = 'Random-search'

# TODO isolate
# current_palette[i]
# dict_color = {}
# dict_color["implicit_forward"] = current_palette[0]
# dict_color['implicit'] = current_palette[1]
# dict_color["forward"] = current_palette[2]
# dict_color['grid_search'] = current_palette[3]
# dict_color['bayesian'] = current_palette[4]
# dict_color['random'] = current_palette[5]
# dict_color['hyperopt'] = current_palette[6]

dict_title = {}
dict_title["rcv1"] = "rcv1"
dict_title["20news"] = "20news"
dict_title["finance"] = "finance"
dict_title["kdda_train"] = "kdda"
dict_title["climate"] = "climate"
dict_title["leukemia"] = "leukemia"
dict_title["real-sim"] = "real-sim"

dict_markevery = {}
dict_markevery["20news"] = 5
dict_markevery["finance"] = 10
dict_markevery["rcv1"] = 5
dict_markevery["leukemia"] = 1
dict_markevery["real-sim"] = 5

dict_n_feature = {}
dict_n_feature["rcv1"] = r"($p=19,959$)"
dict_n_feature["20news"] = r"($p=130,107$)"
dict_n_feature["finance"] = r"($p=1,668,737$)"
dict_n_feature["leukemia"] = r"($p=7,129$)"
dict_n_feature["real-sim"] = r"($p=20,958$)"

markersize = 8

dict_marker_size = {}
dict_marker_size["forward"] = 4
dict_marker_size["implicit_forward"] = 9
dict_marker_size["fast_iterdiff"] = 4
dict_marker_size['implicit'] = 4
dict_marker_size['grid_search'] = 5
dict_marker_size['bayesian'] = 4
dict_marker_size['random'] = 5
dict_marker_size['lhs'] = 4

# dataset_names = ["rcv1", "real-sim"]
dataset_names = ["rcv1", "real-sim", '20news']
# dataset_names = ["20newsgroups"]
# dataset_names = ["finance"]
# dataset_names = ["leukemia"]
# dataset_names = [
#     "leukemia", "climate", "rcv1", "20newsgroups", "finance", "kdda_train"]


plt.close('all')
fig, axarr = plt.subplots(
    1, 3, sharex=False, sharey=False, figsize=[14, 4],)

fig2, axarr2 = plt.subplots(
    1, 3, sharex=False, sharey=False, figsize=[14, 4],)


fig3, axarr3 = plt.subplots(
    1, 3, sharex=False, sharey=False, figsize=[14, 4],)


for idx, dataset in enumerate(dataset_names):
    df_data = pandas.read_pickle("%s.pkl" % dataset)
    df_data = df_data[df_data['tolerance_decrease'] == 'constant']

    methods = df_data['method']
    times = df_data['times']
    objs = df_data['objs']
    objs_tests = df_data['objs_test']
    log_alphas = df_data['log_alphas']
    tols = df_data['tolerance_decrease']
    norm_y_vals = df_data['norm y_val']
    norm_val = 0
    for norm_y_valss in norm_y_vals:
        norm_val = norm_y_valss

    min_objs = np.infty
    for obj in objs:
        min_objs = np.minimum(min_objs, obj.min())
        # obj = [np.min(obj[:k]) for k in np.arange(len(obj)) + 1]

    lines = []

    plt.figure()
    for i, (time, obj, log_alpha, method, tol) in enumerate(
            zip(times, objs, log_alphas, methods, tols)):
        marker = dict_markers[method]
        # objs_test = [np.min(objs_test[:k]) for k in np.arange(
        #     len(objs_test)) + 1]
        # if method == 'grid_search' or method == "implicit_forward":
        if method.startswith(('grid_search', "implicit_forward", "random")):
            # import ipdb; ipdb.set_trace()
            axarr3.flat[idx].plot(
                np.array(log_alpha), obj,
                "bX", color=dict_color[method],
                label="%s" % (dict_method[method]),
                marker=marker, markersize=dict_marker_size[method],
                markevery=1)

    for i, (time, obj, objs_test, method, tol) in enumerate(
            zip(times, objs, objs_tests, methods, tols)):
        marker = dict_markers[method]
        objs_test = [np.min(objs_test[:k]) for k in np.arange(
            len(objs_test)) + 1]
        axarr2.flat[idx].semilogy(
            time, objs_test, color=dict_color[method],
            label="%s" % (dict_method[method]),
            marker=marker, markersize=markersize,
            markevery=dict_markevery[dataset])

    for i, (time, obj, method, tol) in enumerate(
            zip(times, objs, methods, tols)):
        marker = dict_markers[method]
        obj = [np.min(obj[:k]) for k in np.arange(len(obj)) + 1]
        lines.append(
            axarr.flat[idx].semilogy(
                time, (obj-min_objs),
                # time, (obj-min_objs) / norm_val,
                color=dict_color[method],
                label="%s" % (dict_method[method]),
                # label="%s, %s" % (dict_method[method], tol),
                marker=marker, markersize=markersize,
                markevery=dict_markevery[dataset]))
        # axarr.flat[i].legend()

    axarr3.flat[idx].set_title("%s %s" % (
        dict_title[dataset], dict_n_feature[dataset]), size=fontsize)
    # axarr.flat[idx].title.set_text(dict_title[dataset], size=18)
    axarr.flat[0].set_xlim(0, 15)
    axarr.flat[1].set_xlim(0, 40)
    axarr.flat[2].set_xlim(0, 210)

    axarr2.flat[0].set_xlim(0, 15)
    axarr2.flat[1].set_xlim(0, 40)
    axarr2.flat[2].set_xlim(0, 210)

axarr.flat[0].set_ylabel("Objective minus optimum", fontsize=fontsize)
# axarr.flat[0].set_ylabel("Objective minus optimum", fontsize=fontsize)


axarr2.flat[0].set_ylabel("Loss on test set", fontsize=fontsize)
axarr2.flat[0].set_xlabel("Time (s)", fontsize=fontsize)
axarr2.flat[1].set_xlabel("Time (s)", fontsize=fontsize)
axarr2.flat[2].set_xlabel("Time (s)", fontsize=fontsize)

axarr3.flat[0].set_ylabel("Loss on validation set", fontsize=fontsize)
axarr3.flat[0].set_xlabel(
    r"$\lambda - \lambda_{\max}$", fontsize=fontsize)
axarr3.flat[1].set_xlabel(
    r"$\lambda - \lambda_{\max}$", fontsize=fontsize)
axarr3.flat[2].set_xlabel(
    r"$\lambda - \lambda_{\max}$", fontsize=fontsize)

fig.tight_layout()
if save_fig:
    fig.savefig(
        fig_dir + "pred_log_reg_validation_set.pdf",
        bbox_inches="tight")
    fig.savefig(
        fig_dir_svg + "pred_log_reg_validation_set.svg",
        bbox_inches="tight")
fig.show()

fig2.tight_layout()
if save_fig:
    fig2.savefig(
        fig_dir + "pred_log_reg_test_set.pdf",
        bbox_inches="tight")
    fig2.savefig(
        fig_dir_svg + "pred_log_reg_test_set.svg",
        bbox_inches="tight")
fig2.show()

fig3.tight_layout()
if save_fig:
    fig3.savefig(
        fig_dir + "pred_vs_alpha_log_reg_validation_set.pdf",
        bbox_inches="tight")
    fig3.savefig(
        fig_dir_svg + "pred_vs_alpha_log_reg_validation_set.svg",
        bbox_inches="tight")
fig3.show()
