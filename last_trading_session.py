import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import describe
import seaborn as sns


#iterate through all these files and create dataframe
def last_session_plots(filepath):
    differences = []
    for contracts in filepath.glob('**/*'):


        contract = pd.read_excel(contracts)
        name = contract.columns[1]
        # get the final settlement price
        settlement = np.array(contract.iloc[:,5])
        settlement_num = np.delete(settlement,[0])
        settlement_num30 = settlement_num[-30:]
        #format all OHLC data
        OHLC = np.array(contract.iloc[:,1:5])
        OHLC_num = np.delete(OHLC,(0),axis=0)

        # drop NA row so that the last sessions align
        OHLC_num = pd.DataFrame(OHLC_num).dropna()

        # get all the differences between T30, T29... T and T
        OHLC_num = np.array(OHLC_num)
        diffMatrix = (OHLC_num[-29:] - settlement_num30[-1])*-1

        diffMatrix_OHLC = diffMatrix[:,0:4]

        #take the differences of the last session

        diffMatrix_OHLC_last = diffMatrix_OHLC[-1:]

        differences.append(diffMatrix_OHLC_last)

    differences=np.array(differences)
    differences = differences.reshape(differences.shape[0],-1)


    #separate out each columns for OHLC
    differences_open = differences[:,0]
    differences_high = differences[:,1]
    differences_low = differences[:,2]
    differences_close = differences[:,3]


    df_open = pd.DataFrame(differences_open)
    df_high = pd.DataFrame(differences_high)
    df_low = pd.DataFrame(differences_low)
    df_close = pd.DataFrame(differences_close)

    df = pd.DataFrame(differences)
    df.columns=['open','high','low','close']

    # plot OHLC for the last trading session together 812 data points

    df2 = np.array(df)
    df2 = pd.DataFrame(df2.reshape(-1))

    df2[0].plot(kind = 'density', bw_method = 1, title = 'Last Trading Session All Data Points')
    mean = round(np.array(describe(df2[0]))[2], 3)
    plt.axvline(mean, 0, 1, linestyle='dotted', color='black')
    nobs = np.array(describe(df2[0]))[0]
    min = round(np.array(describe(df2[0]))[1][0], 3)
    max = round(np.array(describe(df2[0]))[1][1], 3)
    std = round(np.sqrt(np.array(describe(df2[0]))[3]), 3)
    skew = round(np.array(describe(df2[0]))[4], 3)
    kurtosis = round(np.array(describe(df2[0]))[5], 3)

    plt.axvline(mean, 0, 1, linestyle = 'dotted', color = 'black')
    plt.figtext(0.75,0.5,'nobs='+str(nobs)+'\nmin='+ str(min) + '\nmax='+str(max)+'\nmean='+str(mean)+'\nstd='+str(std)+'\nskew='+str(skew)+'\nkurtosis='+str(kurtosis))
    plot_file_name = "last trading session density graph.jpg"
    plt.savefig(plot_file_name, format= 'jpeg', dpi=100)
    plt.show()
    plt.close()
    #
    bplot = sns.boxplot(data=df2[0], width=0.75, palette='pastel', fliersize=2, linewidth=0.5)
    bplot.axes.set_title('Last Trading Session All Data Points', fontsize=16)
    bplot.set_xlabel("Day", fontsize=14)
    bplot.set_ylabel("Differences", fontsize=14)
    bplot.tick_params(labelsize=5.5)
    plot_file_name = "boxplot for last trading session.jpg"
    bplot.figure.savefig(plot_file_name, format= 'jpeg', dpi=100)
    plt.show()
    plt.close()
    return None