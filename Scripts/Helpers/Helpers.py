import pandas as pd
import statsmodels.api as sm
import numpy as np
from sklearn.linear_model import BayesianRidge
from sklearn.metrics import r2_score
from scipy.stats import norm
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import pandas as pd
from matplotlib.ticker import LogLocator, LogFormatter, NullFormatter
from numpy import log10 as log
import matplotlib.colors as mcolors
import getpass
from pathlib import Path
user = getpass.getuser()
PROJECT_ROOT = Path(f"/Users/{user}/Final_Lawyer_Git July10")

def scale(x, y, n_perm=100000):    
    x_log = log(x).reshape(-1, 1)
    y_log = log(y)
    
    model = BayesianRidge()
    model.fit(x_log, y_log)
    
    beta = model.coef_[0]
    
    y_pred = model.predict(x_log)
    r2 = r2_score(y_log, y_pred)
    
    betas_perm = []
    n = len(y_log)
    
    for _ in range(n_perm):
        idx = np.random.choice(n, n, replace=True)
        X_perm = x_log[idx]
        y_perm = y_log[idx]
        
        model_perm = BayesianRidge()
        model_perm.fit(X_perm, y_perm)
        betas_perm.append(model_perm.coef_[0])
    
    ci_lower = np.percentile(betas_perm, 2.5)
    ci_upper = np.percentile(betas_perm, 97.5)
    
    return beta, ci_lower, ci_upper, r2


def scale_ols(x, y, alpha=0.05):
    
    x_log = log(x)
    y_log = log(y)
    
    X = sm.add_constant(x_log)
    
    model = sm.OLS(y_log, X).fit()
    
    beta = model.params[1]  
    
    y_pred = model.predict(X)
    r2 = r2_score(y_log, y_pred)
    
    ci_lower, ci_upper = model.conf_int(alpha=alpha)[1]
    
    return beta, ci_lower, ci_upper, r2



def cob(y, x1, x2, n_perm=100000):
    
    y_log = np.log(y)
    X = np.vstack([np.log(x1), np.log(x2)]).T
    
    model = BayesianRidge()
    model.fit(X, y_log)
    
    beta_mean = model.coef_
    sum_beta = np.sum(beta_mean)
    
    y_pred = model.predict(X)
    r2 = r2_score(y_log, y_pred)
    
    betas_perm = []
    sum_perm = []
    n = len(y_log)
    
    for _ in range(n_perm):
        idx = np.random.choice(n, n, replace=True)
        X_perm = X[idx]
        y_perm = y_log[idx]
        
        model_perm = BayesianRidge()
        model_perm.fit(X_perm, y_perm)
        
        b = model_perm.coef_
        betas_perm.append(b)
        sum_perm.append(np.sum(b))
    
    betas_perm = np.array(betas_perm)
    
    ci_lower = np.percentile(betas_perm, 2.5, axis=0)
    ci_upper = np.percentile(betas_perm, 97.5, axis=0)
    
    ci_sum_lower = np.percentile(sum_perm, 2.5)
    ci_sum_upper = np.percentile(sum_perm, 97.5)
    
    return beta_mean, ci_lower, ci_upper, sum_beta, ci_sum_lower, ci_sum_upper, r2




def darker(color, factor=0.7):
    r, g, b = mcolors.to_rgb(color)
    return (r*factor, g*factor, b*factor)


def plot_scaling_trip(df, law, pop_col="B01003_001E", area_col="land_area_sqmi", file_tag=""):
    df_reg = df[[law, pop_col, area_col]].copy()
    df_reg = df_reg[(df_reg[law] > 0) & (df_reg[pop_col] > 0) & (df_reg[area_col] > 0)]

    L = df_reg[law].values
    P = df_reg[pop_col].values
    A = df_reg[area_col].values

    y = log(L)


    model_P = BayesianRidge()
    model_P.fit(log(P).reshape(-1, 1), y)

    x_line = np.array([P.min(), P.max()])
    y_line = 10**(model_P.predict(log(x_line).reshape(-1, 1)))

    alpha1_P = np.mean(y - log(P))
    y_beta1 = 10**(alpha1_P) * x_line

    fig, axes = plt.subplots(1, 3, figsize=(12, 5), sharey=True)

    base = mcolors.to_rgba("C2", alpha=0.6)   
    edge = mcolors.to_rgba("C2", alpha=1.0) 

        
    ax = axes[0]
    ax.scatter(P, L, alpha=1, color="C2",  edgecolor = darker("C2"), linewidths=0.6)
    ax.plot(x_line, y_line, color="k", lw=3)
    ax.plot(x_line, y_beta1, "--", color="k", lw=3)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel(r"$\it{P}$")
    ax.set_ylabel(r"$\it{L}$")

    pop_results = scale(P, L, n_perm=100000)
    pop_beta, pop_CI_low, pop_CI_Hi, pop_R2 = np.array([f"{v:.2f}" for v in pop_results])
    ax.text(0.05,0.95,r'$\beta_\mathit{{P}} = {}$'.format(pop_beta)+r'$ \, \in \,({}$'.format(pop_CI_low) + r'$,{})$'.format(pop_CI_Hi),
            ha='left', va='top',transform=ax.transAxes, fontsize = 18)
    ax.text(0.05,0.85,r'$\mathit{R}^2 = $' +r'${}$'.format(pop_R2), ha='left', va='top',transform=ax.transAxes, fontsize = 18)

    ax.set_ylim([10, 10**6])
    ax.set_xlim([10**4, 10**8])
    ax.set_xticks(np.logspace(4,8,5))


    model_A = BayesianRidge()
    model_A.fit(log(A).reshape(-1, 1), y)

    x_line = np.array([A.min(), A.max()])
    y_line = 10**(model_A.predict(log(x_line).reshape(-1, 1)))

    alpha1_A = np.mean(y - log(A))
    y_beta1 = 10**(alpha1_A) * x_line

    ax = axes[1]
    ax.scatter(A, L, alpha=1, color="C1",  edgecolor = darker("C1"), linewidths=0.6)
    ax.plot(x_line, y_line, color="k", lw=3)
    ax.plot(x_line, y_beta1, "--", color="k", lw=3)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel(r"$\it{A}$")

    area_results = scale(A, L, n_perm=100000)
    area_beta, area_CI_low, area_CI_Hi, area_R2 = np.array([f"{v:.2f}" for v in area_results])
    ax.text(0.05,0.95,r'$\beta_\mathit{{A}} = {}$'.format(area_beta)+r'$ \, \in \,({}$'.format(area_CI_low) + r'$,{})$'.format(area_CI_Hi),
            ha='left', va='top',transform=ax.transAxes, fontsize = 18)
    ax.text(0.05,0.85,r'$\mathit{R}^2 = $' +r'${}$'.format(area_R2), ha='left', va='top',transform=ax.transAxes, fontsize = 18)

    ax.set_xlim([10**2, 10**5])
    ax.set_xticks(np.logspace(2,5,4))
    ax.set_ylabel("")  


    X = np.vstack([log(P), log(A)]).T

    model_CD = BayesianRidge()
    model_CD.fit(X, y)

    L_pred = 10**(model_CD.predict(X))

    ax = axes[2]
    ax.scatter(L_pred, L, alpha=1, color="C4", edgecolor = darker("C4"), linewidths=0.6)

    lims = [min(L.min(), L_pred.min()), max(L.max(), L_pred.max())]
    ax.plot(lims, lims, "--", color="k", lw=3)


    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim([10, 10**6])
    ax.set_xticks(np.logspace(1,6,6))
    ax.set_ylabel("")  # shared y-axis
    ax.set_xlabel(r"$\it{\hat{L}}$")

    beta_cd, ci_cd_low, ci_cd_high, sum_cd_val, sum_cd_low_val, sum_cd_high_val, r2_cd  = cob(L, P, A, n_perm=100000)
    beta_cd = np.array([f"{v:.2f}" for v in beta_cd])
    ci_cd_low = np.array([f"{v:.2f}" for v in ci_cd_low])
    ci_cd_high = np.array([f"{v:.2f}" for v in ci_cd_high])
    sum_cd_val = f"{sum_cd_val:.2f}"
    sum_cd_low_val = f"{sum_cd_low_val:.2f}"
    sum_cd_high_val = f"{sum_cd_high_val:.2f}"
    r2_cd = f"{r2_cd:.2f}"

    # ax.text(0.02,0.98,r'$\alpha_\mathit{{P}} = {}$'.format(beta_cd[0])+r'$ \, \in \,({}$'.format(ci_cd_low[0]) + r'$,{})$'.format(ci_cd_high[0]),
    #         ha='left', va='top',transform=ax.transAxes, fontsize = 20)
    # ax.text(0.02,0.98,r'$\alpha_\mathit{{A}} = {}$'.format(beta_cd[1])+r'$ \, \in \,({}$'.format(ci_cd_low[1]) + r'$,{})$'.format(ci_cd_high[1]),
    #         ha='left', va='top',transform=ax.transAxes, fontsize = 20)
    ax.text(0.05,0.95,r'$\Sigma = {}$'.format(sum_cd_val)+r'$ \, \in \,({}$'.format(sum_cd_low_val) + r'$,{})$'.format(sum_cd_high_val),
            ha='left', va='top',transform=ax.transAxes, fontsize = 18)
    ax.text(0.05,0.85,r'$\mathit{R}^2 = $' +r'${}$'.format(r2_cd), ha='left', va='top',transform=ax.transAxes, fontsize = 18)

    plt.tight_layout()
    plt.subplots_adjust(wspace=0.14)
    # Define the output directory and ensure it exists
    save_dir = PROJECT_ROOT / "Figures/Supplementary Figure 1"
    save_dir.mkdir(parents=True, exist_ok=True)
    
    # Save the file 
    plt.savefig(save_dir / "Supplementary_Figure_1.pdf", bbox_inches='tight')
    plt.show()
    plt.close(fig)



def plot_population_scaling_grid(df, laws, pop_col="B01003_001E", file_tag=""):
    fig, axes = plt.subplots(4, 3, figsize=(15, 18), sharex=True, sharey=True)
    axes = axes.flatten()

    for i, law in enumerate(laws[::-1]):
        ax = axes[i]

        df_reg = df[[law, pop_col]].copy()
        df_reg = df_reg[(df_reg[law] > 0) & (df_reg[pop_col] > 0)]

        L = df_reg[law].values
        P = df_reg[pop_col].values

        y = log(L)

        model_P = BayesianRidge()
        model_P.fit(log(P).reshape(-1, 1), y)

        x_line = np.array([P.min(), P.max()])
        y_line = 10**(model_P.predict(log(x_line).reshape(-1, 1)))

        alpha1_P = np.mean(y - log(P))
        y_beta1 = 10**(alpha1_P) * x_line

        ax.scatter(P, L, alpha=1, color="C2", edgecolor=darker("C2"), linewidths=0.6)
        ax.plot(x_line, y_line, color="k", lw=3)
        ax.plot(x_line, y_beta1, "--", color="k", lw=3)

        ax.set_xscale("log")
        ax.set_yscale("log")

        pop_results = scale(P, L, n_perm=100000)
        pop_beta, pop_CI_low, pop_CI_Hi, pop_R2 = np.array([f"{v:.2f}" for v in pop_results])

        ax.text(
            0.05, 0.95,
            r'$\beta_\mathit{{P}} = {}$'.format(pop_beta)
            + r'$ \, \in \,({}$'.format(pop_CI_low)
            + r'$,{})$'.format(pop_CI_Hi),
            ha="left", va="top", transform=ax.transAxes, fontsize=23
        )

        ax.text(
            0.05, 0.85,
            r'$\mathit{R}^2 = $' + r'${}$'.format(pop_R2),
            ha="left", va="top", transform=ax.transAxes, fontsize=23
        )

        ax.set_xlim([10**4, 10**8])
        ax.set_ylim([1, 10**6])
        ax.set_xticks(np.logspace(4, 8, 5))
        ax.set_yticks(np.logspace(0, 6, 7))

        title = law.replace("_binary_count", "").replace("_normalized_1overN_count", "")

        if law.endswith("_normalized_1overN_count"):
            if not title.endswith("Law"):
                title = title + " Law"
            title = title + " Normalized"

        ax.set_title(title)

        if i % 3 == 0:
            ax.set_ylabel(r"$\it{L}$")
        else:
            ax.set_ylabel("")

        if i >= 9:
            ax.set_xlabel(r"$\it{P}$")
        else:
            ax.set_xlabel("")

    plt.tight_layout()
    plt.subplots_adjust(wspace=0.1, hspace=0.2)

    # Define the output directory and ensure it exists
    save_dir = PROJECT_ROOT / "Figures/Supplementary Figure 2"
    save_dir.mkdir(parents=True, exist_ok=True)
    
    # Save the file 
    plt.savefig(save_dir / "Supplementary_Figure_2.pdf", bbox_inches='tight')
    plt.show()
    plt.close(fig)




def plot_area_scaling_grid(df, laws, area_col="land_area_sqmi", file_tag=""):
    """
    4x3 grid of area scaling plots (one per law)
    Matches styling of original middle panel exactly
    """

    fig, axes = plt.subplots(4, 3, figsize=(15, 18), sharex=True, sharey=True)
    axes = axes.flatten()

    for i, law in enumerate(laws[::-1]):
        ax = axes[i]

        df_reg = df[[law, area_col]].copy()
        df_reg = df_reg[(df_reg[law] > 0) & (df_reg[area_col] > 0)]

        L = df_reg[law].values
        A = df_reg[area_col].values

        y = log(L)

        # Bayesian fit
        model_A = BayesianRidge()
        model_A.fit(log(A).reshape(-1, 1), y)

        x_line = np.array([A.min(), A.max()])
        y_line = 10**(model_A.predict(log(x_line).reshape(-1, 1)))

        # beta = 1 reference
        alpha1_A = np.mean(y - log(A))
        y_beta1 = 10**(alpha1_A) * x_line

        # Plot
        ax.scatter(A, L, alpha=1, color="C1", edgecolor=darker("C1"), linewidths=0.6)
        ax.plot(x_line, y_line, color="k", lw=3)
        ax.plot(x_line, y_beta1, "--", color="k", lw=3)

        ax.set_xscale("log")
        ax.set_yscale("log")

        area_results = scale(A, L, n_perm=100000)
        area_beta, area_CI_low, area_CI_Hi, area_R2 = np.array([f"{v:.2f}" for v in area_results])

        ax.text(
            0.05, 0.95,
            r'$\beta_\mathit{{A}} = {}$'.format(area_beta)
            + r'$ \, \in \,({}$'.format(area_CI_low)
            + r'$,{})$'.format(area_CI_Hi),
            ha="left", va="top", transform=ax.transAxes, fontsize=23
        )

        ax.text(
            0.05, 0.85,
            r'$\mathit{R}^2 = $' + r'${}$'.format(area_R2),
            ha="left", va="top", transform=ax.transAxes, fontsize=23
        )

        ax.set_xlim([10**2, 10**5])
        ax.set_ylim([1, 10**6])
        ax.set_xticks(np.logspace(2, 5, 4))
        ax.set_yticks(np.logspace(0, 6, 7))

        title = law.replace("_binary_count", "").replace("_normalized_1overN_count", "")

        if law.endswith("_normalized_1overN_count"):
            if not title.endswith("Law"):
                title = title + " Law"
            title = title + " Normalized"

        ax.set_title(title)

        # Labels only on outer plots
        if i % 3 == 0:
            ax.set_ylabel(r"$\it{L}$")
        else:
            ax.set_ylabel("")

        if i >= 9:
            ax.set_xlabel(r"$\it{A}$")
        else:
            ax.set_xlabel("")

    plt.tight_layout()
    plt.subplots_adjust(wspace=0.1, hspace=0.2)

    # Define the output directory and ensure it exists
    save_dir = PROJECT_ROOT / "Figures/Supplementary Figure 3"
    save_dir.mkdir(parents=True, exist_ok=True)
    
    # Save the file 
    plt.savefig(save_dir / "Supplementary_Figure_3.pdf", bbox_inches='tight')
    plt.show()
    plt.close(fig)





def plot_cobb_douglas_grid(df, laws, pop_col="B01003_001E", area_col="land_area_sqmi", file_tag=""):
    """
    4x3 grid of Cobb-Douglas predictions vs actual
    """

    fig, axes = plt.subplots(4, 3, figsize=(15, 18), sharex=True, sharey=True)
    axes = axes.flatten()

    for i, law in enumerate(laws[::-1]):
        ax = axes[i]

        df_reg = df[[law, pop_col, area_col]].copy()
        df_reg = df_reg[
            (df_reg[law] > 0) &
            (df_reg[pop_col] > 0) &
            (df_reg[area_col] > 0)
        ]

        L = df_reg[law].values
        P = df_reg[pop_col].values
        A = df_reg[area_col].values

        y = log(L)

        # Cobb-Douglas model
        X = np.vstack([log(P), log(A)]).T

        model_CD = BayesianRidge()
        model_CD.fit(X, y)

        L_pred = 10**(model_CD.predict(X))

        # Plot predicted vs actual
        ax.scatter(L_pred, L, alpha=1, color="C4", edgecolor=darker("C4"), linewidths=0.6)

        lims = [min(L.min(), L_pred.min()), max(L.max(), L_pred.max())]
        ax.plot(lims, lims, "--", color="k", lw=3)

        ax.set_xscale("log")
        ax.set_yscale("log")

        beta_cd, ci_cd_low, ci_cd_high, sum_cd_val, sum_cd_low_val, sum_cd_high_val, r2_cd = cob(
            L, P, A, n_perm=100000
        )

        beta_cd = np.array([f"{v:.2f}" for v in beta_cd])
        ci_cd_low = np.array([f"{v:.2f}" for v in ci_cd_low])
        ci_cd_high = np.array([f"{v:.2f}" for v in ci_cd_high])
        sum_cd_val = f"{sum_cd_val:.2f}"
        sum_cd_low_val = f"{sum_cd_low_val:.2f}"
        sum_cd_high_val = f"{sum_cd_high_val:.2f}"
        r2_cd = f"{r2_cd:.2f}"

        ax.text(
            0.05, 0.95,
            r'$\Sigma = {}$'.format(sum_cd_val)
            + r'$ \, \in \,({}$'.format(sum_cd_low_val)
            + r'$,{})$'.format(sum_cd_high_val),
            ha="left", va="top", transform=ax.transAxes, fontsize=23
        )

        ax.text(
            0.05, 0.85,
            r'$\mathit{R}^2 = $' + r'${}$'.format(r2_cd),
            ha="left", va="top", transform=ax.transAxes, fontsize=23
        )

        ax.set_xlim([1, 10**6])
        ax.set_ylim([1, 10**6])
        ax.set_xticks(np.logspace(0, 6, 7))
        ax.set_yticks(np.logspace(0, 6, 7))

        title = law.replace("_binary_count", "").replace("_normalized_1overN_count", "")

        if law.endswith("_normalized_1overN_count"):
            if not title.endswith("Law"):
                title = title + " Law"
            title = title + " Normalized"

        ax.set_title(title)

        # Labels only on outer plots
        if i % 3 == 0:
            ax.set_ylabel(r"$\it{L}$")
        else:
            ax.set_ylabel("")

        if i >= 9:
            ax.set_xlabel(r"$\it{\hat{L}}$")
        else:
            ax.set_xlabel("")

    plt.tight_layout()
    plt.subplots_adjust(wspace=0.1, hspace=0.2)

   # Define the output directory and ensure it exists
    save_dir = PROJECT_ROOT / "Figures/Supplementary Figure 4"
    save_dir.mkdir(parents=True, exist_ok=True)
    
    # Save the file 
    plt.savefig(save_dir / "Supplementary_Figure_4.pdf", bbox_inches='tight')
    plt.show()
    plt.close(fig)




def plot_panel(ax, x, y, xlab, ylab, color, lim):
    xmin_e, xmax_e, ymin_e, ymax_e = lim

    mask = (x > 0) & (y > 0)
    x = x[mask]
    y = y[mask]
    print(len(x))
    ax.scatter(x, y, alpha=1, color=color,
               edgecolor=darker(color), linewidths=0.6)

    y_log = log(y)
    model = BayesianRidge()
    model.fit(log(x).reshape(-1, 1), y_log)

    x_line = np.array([x.min(), x.max()])
    y_line = 10**model.predict(log(x_line).reshape(-1, 1))

    alpha1 = np.mean(y_log - log(x))
    y_beta1 = 10**alpha1 * x_line

    ax.plot(x_line, y_line, color="k", lw=3)
    ax.plot(x_line, y_beta1, "--", color="k", lw=3)

    beta, ci_low, ci_high, r2 = scale(x, y, n_perm=100000)

    ax.text(
        0.05, 0.95,
        rf'$\beta_\mathit{{D}} = {beta:.2f} \in ({ci_low:.2f},{ci_high:.2f})$',
        transform=ax.transAxes,
        ha='left', va='top', fontsize=22
    )
    ax.text(
        0.05, 0.85,
        rf'$\mathit{{R}}^2 = {r2:.2f}$',
        transform=ax.transAxes,
        ha='left', va='top', fontsize=22
    )

    ax.set_xscale("log")
    ax.set_yscale("log")

    # APPLY LIMITS (convert exponents -> actual values)
    ax.set_xlim(10**xmin_e, 10**xmax_e)
    ax.set_ylim(10**ymin_e, 10**ymax_e)
    ax.set_xticks(10.0 ** np.arange(xmin_e, xmax_e + 1))
    ax.set_yticks(10.0 ** np.arange(ymin_e, ymax_e + 1))

    ax.set_xlabel(xlab)
    ax.set_ylabel(ylab)

























