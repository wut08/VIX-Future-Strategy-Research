import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


#iterate through all these files and create dataframe
def starting_vix_plot(filepath):
    prices10 = pd.DataFrame([])
    prices20 = pd.DataFrame([])
    prices30 = pd.DataFrame([])
    prices40 = pd.DataFrame([])
    prices50 = pd.DataFrame([])
    for contracts in filepath.glob('**/*'):

        contract = pd.read_excel(contracts)

        # get the final settlement price
        settlement = np.array(contract.iloc[:,5])

        settlement_num = np.delete(settlement,[0])
        settlement_num30 = settlement_num[-30:]
        #format all OHLC data

        pd_OHLC = contract.iloc[:,1:5].T

        pd_OHLC30 = pd_OHLC.iloc[:,[0] + list(range(-30,0))].copy()
        pd_OHLC30.columns = ['price','T-29', 'T-28', 'T-27', 'T-26', 'T-25', 'T-24', 'T-23', 'T-22', 'T-21', 'T-20', 'T-19', 'T-18',
                      'T-17', 'T-16', 'T-15', 'T-14', 'T-13', 'T-12', 'T-11', 'T-10', 'T-9', 'T-8', 'T-7', 'T-6', 'T-5',
                      'T-4', 'T-3', 'T-2', 'T-1','T']

        # separate them according to the average prices from T-29 to T-26
        if np.mean(pd_OHLC30[['T-29', 'T-28', 'T-27', 'T-26']].values) <20:
            differences10 = (pd_OHLC30[['T-29', 'T-28', 'T-27', 'T-26', 'T-25', 'T-24', 'T-23', 'T-22', 'T-21', 'T-20', 'T-19',
                                 'T-18',
                                 'T-17', 'T-16', 'T-15', 'T-14', 'T-13', 'T-12', 'T-11', 'T-10', 'T-9', 'T-8', 'T-7', 'T-6',
                                 'T-5',
                                 'T-4', 'T-3', 'T-2', 'T-1']].copy() - settlement_num30[-1]).apply(lambda x:x*-1)
            prices10 = prices10.append(differences10)
        elif np.mean(pd_OHLC30[['T-29', 'T-28', 'T-27', 'T-26']].values) < 30:
            differences20 = (pd_OHLC30[
                                ['T-29', 'T-28', 'T-27', 'T-26', 'T-25', 'T-24', 'T-23', 'T-22', 'T-21', 'T-20', 'T-19',
                                 'T-18',
                                 'T-17', 'T-16', 'T-15', 'T-14', 'T-13', 'T-12', 'T-11', 'T-10', 'T-9', 'T-8', 'T-7', 'T-6',
                                 'T-5',
                                 'T-4', 'T-3', 'T-2', 'T-1']].copy() - settlement_num30[-1]).apply(lambda x:x*-1)
            prices20 = prices20.append(differences20)
        elif np.mean(pd_OHLC30[['T-29', 'T-28', 'T-27', 'T-26']].values) < 40:
            differences30 = (pd_OHLC30[
                                ['T-29', 'T-28', 'T-27', 'T-26', 'T-25', 'T-24', 'T-23', 'T-22', 'T-21', 'T-20', 'T-19',
                                 'T-18',
                                 'T-17', 'T-16', 'T-15', 'T-14', 'T-13', 'T-12', 'T-11', 'T-10', 'T-9', 'T-8', 'T-7', 'T-6',
                                 'T-5',
                                 'T-4', 'T-3', 'T-2', 'T-1']].copy() - settlement_num30[-1]).apply(lambda x:x*-1)
            prices30 = prices30.append(differences30)
        elif np.mean(pd_OHLC30[['T-29', 'T-28', 'T-27', 'T-26']].values) <50:
            differences40 = (pd_OHLC30[
                                ['T-29', 'T-28', 'T-27', 'T-26', 'T-25', 'T-24', 'T-23', 'T-22', 'T-21', 'T-20', 'T-19',
                                 'T-18',
                                 'T-17', 'T-16', 'T-15', 'T-14', 'T-13', 'T-12', 'T-11', 'T-10', 'T-9', 'T-8', 'T-7', 'T-6',
                                 'T-5',
                                 'T-4', 'T-3', 'T-2', 'T-1']].copy() - settlement_num30[-1]).apply(lambda x:x*-1)
            prices40 = prices40.append(differences40)
        else:
            differences50 = (pd_OHLC30[
                                ['T-29', 'T-28', 'T-27', 'T-26', 'T-25', 'T-24', 'T-23', 'T-22', 'T-21', 'T-20', 'T-19',
                                 'T-18',
                                 'T-17', 'T-16', 'T-15', 'T-14', 'T-13', 'T-12', 'T-11', 'T-10', 'T-9', 'T-8', 'T-7', 'T-6',
                                 'T-5',
                                 'T-4', 'T-3', 'T-2', 'T-1']].copy() - settlement_num30[-1]).apply(lambda x:x*-1)
            prices50 = prices50.append(differences50)

    prices10.index.names = ['between 10 and 20']
    prices20.index.names = ['between 20 and 30']
    prices30.index.names = ['between 30 and 40']
    prices40.index.names = ['between 40 and 50']
    prices50.index.names = ['above 50']

    for i in prices10,prices20,prices30,prices40,prices50:
        bplot = sns.boxplot(data = i, width = 0.75, palette = 'pastel',fliersize = 0.75, linewidth = 0.5)
        bplot.axes.set_title(f"boxplot for starting price {i.index.names[0]}", fontsize = 16)
        bplot.set_xlabel("Days", fontsize = 14)
        bplot.set_ylabel("Differences", fontsize =14)
        bplot.tick_params(labelsize = 5.5)
        plot_file_name = f"boxplot for starting price {i.index.names[0]}.jpg"
        bplot.figure.savefig(plot_file_name, format= 'jpeg', dpi=100)
        plt.show()
        plt.close()
    return None








