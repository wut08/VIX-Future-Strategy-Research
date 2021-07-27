import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from varname import argname2


def regression(df,i):

    df.fillna(0, inplace = True)
    y = df.iloc[:, 0]
    spot = df.iloc[:, 1]
    ps = df.iloc[:, 2]
    spx = df.iloc[:, 4]
    res1 = stats.linregress(spot, y)
    res2 = stats.linregress(ps, y)
    res3 = stats.linregress(spx, y)

    co = pd.DataFrame([res1.slope, res2.slope, res3.slope], index=['SPOT VIX Beta', 'Normalized Future Basis Beta', 'SPX Beta'],
                      columns=[i])
    r2 = pd.DataFrame([res1.rvalue ** 2, res2.rvalue ** 2, res3.rvalue ** 2], index=['SPOT VIX_r2', 'Normalized Future Basis_r2', 'SPX_r2'],
                      columns=[i])

    return co, r2



def regress_30(c6):
    loadings_all = pd.DataFrame([])
    R2_all = pd.DataFrame([])

    loadings_low = pd.DataFrame([])
    R2_low = pd.DataFrame([])

    loadings_high = pd.DataFrame([])
    R2_high = pd.DataFrame([])
    for i in range(1, 29):
        #df for all vol
        df = c6[[f'T-{i}_cr', f'T-{i}_vix', f'T-{i}_ps', f'T-{i}_h', f'T-{i}_spx']].copy()

        #separate dfs for low vol and high vol
        df_lowVol = df.loc[df[f'T-{i}_h'] == 0].copy()
        df_highVol = df.loc[df[f'T-{i}_h'] != 0].copy()

        co_all, r2_all =regression(df,i)
        co_low, r2_low = regression(df_lowVol,i)
        co_high, r2_high = regression(df_highVol,i)

        loadings_all = pd.concat([loadings_all, co_all], axis=1)
        R2_all = pd.concat([R2_all, r2_all], axis=1)

        loadings_low = pd.concat([loadings_low, co_low], axis=1)
        R2_low = pd.concat([R2_low, r2_low], axis=1)

        loadings_high = pd.concat([loadings_high, co_high], axis=1)
        R2_high = pd.concat([R2_high, r2_high], axis=1)
    # sort them in order of T-
    for n in loadings_all, loadings_low, loadings_high, R2_all, R2_low, R2_high:
        n.sort_index(ascending=False, axis=1, inplace= True)
    return loadings_all,loadings_low,loadings_high,R2_all, R2_low, R2_high

def plot_regression(loadings, R2):
    combo = pd.concat([loadings, R2], axis=0)
    combo.columns = [f'T-{n}' for n in combo.columns.values]
    fig, ax = plt.subplots()

    combo2 = combo.transpose().copy()

    name = (''.join(argname2('*loadings'))).split('_')[1]

    for m in ['SPOT VIX', 'Normalized Future Basis','SPX' ] :
        ax = combo2[f'{m} Beta'].plot(label= f'{m} Beta', legend=True, xlabel="Days", ylabel="Values", fontsize=5,
                                        title=f"{m} Beta in {name} Vol Environment")
        plt.figtext(0.6, 0.3, 'R2 Range =\n' + str(np.round(min(combo2[[f'{m}_r2']].values), 3)) + str(
            np.round(max(combo2[[f'{m}_r2']].values), 3)) + '\nR2 Average = ' + str(
            np.round(combo2[[f'{m}_r2']].values.mean(), 3)))

        ax.set_xticks(np.arange(0, 28, 1))
        ax.set_xticklabels(combo.columns)
        plt.savefig(f"{m} beta in {name} vol.jpeg", format='jpeg', dpi=100)
        plt.show()
        plt.close()
    return None
