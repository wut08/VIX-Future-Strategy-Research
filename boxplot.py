import numpy
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def boxplot(filepath):
#iterate through all these files and create dataframe
    differences = pd.DataFrame([])

    for contracts in filepath.glob('**/*'):

        contract = pd.read_excel(contracts)

        # get the final settlement price
        settlement = np.array(contract.iloc[:,5])

        settlement_num = np.delete(settlement,[0])
        settlement_num30 = settlement_num[-30:]
        #format all OHLC data
        OHLCS = np.array(contract.iloc[:,1:6])
        OHLCS_num = np.delete(OHLCS,(0),axis=0)
        OHLCS_num30 = np.delete(OHLCS_num, (-1),axis=0)

        # get all the differences between T30, T29... T and T

        diffMatrix = pd.DataFrame(OHLCS_num30[-29:] - settlement_num30[-1]).apply(lambda x:x*-1)

        diffMatrix_OHLC = np.array(diffMatrix)[:,0:4]

        diffMatrix_OHLC = diffMatrix_OHLC.T

        diff30 = pd.DataFrame(diffMatrix_OHLC, columns=['T-29', 'T-28', 'T-27', 'T-26', 'T-25', 'T-24', 'T-23', 'T-22', 'T-21', 'T-20', 'T-19',
                                    'T-18',
                                    'T-17', 'T-16', 'T-15', 'T-14', 'T-13', 'T-12', 'T-11', 'T-10', 'T-9', 'T-8', 'T-7',
                                    'T-6', 'T-5',
                                    'T-4', 'T-3', 'T-2', 'T-1'])

        differences = differences.append(diff30)

    # add a row with mean, median, mode of each column
    df_sum = pd.DataFrame()

    df_sum['mean'] = differences.mean()
    df_sum['median'] = differences.median()

    fig, ax = plt.subplots()
    for column in df_sum.columns:
        df_sum[column].plot(label = column, ax = ax, legend= True, xlabel = "Days", ylabel = "Values", fontsize = 5, title = "Price Difference Mean and Median for 30 Days till Settlement")
        ax.set_xticks(np.arange(0,len(df_sum[column])+1,1))
        plt.savefig("Mean-Median Plot.jpeg", format='jpeg', dpi=100)
    plt.show()
    plt.close()

    bplot = sns.boxplot(data = differences, width = 0.75, palette = 'pastel',fliersize = 0.75, linewidth = 0.5)
    bplot.axes.set_title("T-29 to T-1 Price Difference Boxplot", fontsize = 16)
    bplot.set_xlabel("Days", fontsize = 14)
    bplot.set_ylabel("Price Differences", fontsize =14)
    bplot.tick_params(labelsize = 5.5)
    plot_file_name = "boxplot for 30days single day_new.jpg"
    bplot.figure.savefig(plot_file_name, format= 'jpeg', dpi=100)
    plt.show()
    plt.close()

    return None

