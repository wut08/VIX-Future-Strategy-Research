import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mtick
from scipy import stats


def consolidate(filepath):

#iterate through all these files and create dataframe
    differences = pd.DataFrame([])
    prices = pd.DataFrame([])
    percentile = []
    differences_for_plot = pd.DataFrame([])
    ol = pd.DataFrame([])

    for contracts in filepath.glob('**/*'):

        contract = pd.read_excel(contracts)
        name = contract.columns[1]

    # get the final settlement price
        settlement = np.array(contract.iloc[:,5])

        settlement_num = np.delete(settlement,[0])
        settlement_num30 = settlement_num[-30:]
        final_settlement= settlement_num30[-1]
        # all prices except for settle
        pd_OHLC = contract.iloc[:, 1:5]

        pd_OHLC30 = pd_OHLC.iloc[-30:].dropna().copy()

        pd_OHLC30 = np.array((pd_OHLC30 - final_settlement).apply(lambda x: x * -1)).reshape(-1, 1)

        differences_for_plot = pd.concat([differences_for_plot, pd.DataFrame(pd_OHLC30, columns=[name])], axis=1)

        outlier_days = pd.DataFrame({'days':['T-29', 'T-28', 'T-27', 'T-26', 'T-25', 'T-24', 'T-23', 'T-22', 'T-21', 'T-20', 'T-19', 'T-18',
                  'T-17', 'T-16', 'T-15', 'T-14', 'T-13', 'T-12', 'T-11', 'T-10', 'T-9', 'T-8', 'T-7', 'T-6', 'T-5',
                  'T-4', 'T-3', 'T-2', 'T-1','T']})
        contract1= contract.drop(contract.head(1).index)

        contract1['DATES'] = pd.to_datetime(contract1.iloc[:, 0])

    # outliers analysis this gets the outlier for each contract

        contract1[['open','high','low','close']] = (contract1.iloc[:,1:5].iloc[:30] - final_settlement).apply(lambda x:x*-1)

        diff = contract1[['DATES','open','high','low','close']].iloc[-30:].copy()

    #below we do outlier for T-29 to T-1
        diff['days'] = ['T-29', 'T-28', 'T-27', 'T-26', 'T-25', 'T-24', 'T-23', 'T-22', 'T-21', 'T-20', 'T-19', 'T-18',
                  'T-17', 'T-16', 'T-15', 'T-14', 'T-13', 'T-12', 'T-11', 'T-10', 'T-9', 'T-8', 'T-7', 'T-6', 'T-5',
                  'T-4', 'T-3', 'T-2', 'T-1','T-0']

        ol = ol.append(diff)
        pd_OHLCS = contract.iloc[:,1:6].T

        pd_OHLCS30 = pd_OHLCS.iloc[:,[0] + list(range(-30,0))].copy()

        pd_OHLCS30.columns = ['price','T-29', 'T-28', 'T-27', 'T-26', 'T-25', 'T-24', 'T-23', 'T-22', 'T-21', 'T-20', 'T-19', 'T-18',
                  'T-17', 'T-16', 'T-15', 'T-14', 'T-13', 'T-12', 'T-11', 'T-10', 'T-9', 'T-8', 'T-7', 'T-6', 'T-5',
                  'T-4', 'T-3', 'T-2', 'T-1','T']

        all_percentile = pd.DataFrame(pd_OHLCS30.iloc[:,1:32].values.reshape(-1)).rank(pct= True)
        settle_percent = all_percentile.iloc[-1]
        percentile.append(settle_percent)

        prices = prices.append(pd_OHLCS30)
        pd_OHLCS30[['T-29', 'T-28', 'T-27', 'T-26', 'T-25', 'T-24', 'T-23', 'T-22', 'T-21', 'T-20', 'T-19', 'T-18',
                  'T-17', 'T-16', 'T-15', 'T-14', 'T-13', 'T-12', 'T-11', 'T-10', 'T-9', 'T-8', 'T-7', 'T-6', 'T-5',
                  'T-4', 'T-3', 'T-2', 'T-1','T']] = (pd_OHLCS30[['T-29', 'T-28', 'T-27', 'T-26', 'T-25', 'T-24', 'T-23', 'T-22', 'T-21', 'T-20', 'T-19', 'T-18',
                  'T-17', 'T-16', 'T-15', 'T-14', 'T-13', 'T-12', 'T-11', 'T-10', 'T-9', 'T-8', 'T-7', 'T-6', 'T-5',
                  'T-4', 'T-3', 'T-2', 'T-1','T']] - final_settlement).apply(lambda x:x*-1)

        differences = differences.append(pd_OHLCS30)

    return prices, differences, ol, percentile,differences_for_plot


def horizontal_plot(differences_for_plot):

    fig, ax = plt.subplots()
    for n in differences_for_plot.columns:

        plt.hist(differences_for_plot[n], color= 'skyblue', density=True, alpha=0.5, edgecolor='black', label=n)
    plt.xlabel("Value")
    plt.title("Price Difference Distributions of All Futures")
    plt.ylabel("Density ")
    plt.savefig("Horizontal All Futures Plot.jpeg", format='jpeg', dpi=100)
    plt.show()
    plt.close()
    return None
def get_stats(differences):

    stats = pd.DataFrame(index=['Max','Mean','Median','Min','Skew', 'Std Dev'])

    for i in differences:
        name = i
        mean = np.round(differences[i].mean(),2)
        std = np.round(differences[i].std(),2)
        median = np.round(differences[i].median(),2)
        min = np.round(differences[i].min(),2)
        max = np.round(differences[i].max(),2)
        if i == 'T':

            d = differences[i].replace(0, np.nan).dropna()
            skew = np.round(d.skew(),2)
        else:

            skew = np.round(differences[i].skew(),2)
        stat = pd.DataFrame([max,mean,median,min,skew,std],index=['Max','Mean','Median','Min','Skew', 'Std Dev'],columns=[name])

        stats = pd.concat([stats,stat], axis=1)
    return stats

def outliers (ol):
    outlier_30days = pd.DataFrame([])
    ol.index = ol['days']

    for i in range(0,30):
        df = ol.groupby(level = 0).get_group(f'T-{i}').copy()
        df.set_index('DATES',inplace= True)
        df2 = df.iloc[:,:-1].copy()
        df2=df2.stack(dropna=True).copy()

    # for OHLC all data reshape to (808,1); for close only, reshape to (202,1)
        outlier = df2[(np.abs(stats.zscore(np.array(df2, dtype = np.float64).reshape(df2.shape[0],1))) > 3).any(axis=1)]

        outlier.name = f'T-{i}'

        outlier_30days = outlier_30days.append(outlier)

    outlier_30days = outlier_30days.T.copy()

    outlier_30days.reset_index(inplace=True)
    outlier_30days['DATES'], outlier_30days['price'] = outlier_30days['index'].str

    outlier30 = outlier_30days.drop(['index','price'],axis=1).set_index('DATES')

    return outlier30


def percentile_plot(percentile):
    df = pd.DataFrame(percentile).reset_index().iloc[:,1]*100

    fig,ax = plt.subplots()

    ax1 = df.plot.hist(bins=100,alpha = 0.5)
    ax2= ax1.twinx()
    ax2.spines['right'].set_position(('axes',1.0))

    hist,bins = np.histogram(df, bins = 100)

    pd.DataFrame(100*(np.cumsum(hist)/np.sum(hist)),columns=['Cumulative']).plot(ax = ax2)
    plt.title('Percentile of Final Settlement Prices in the Last 30 Trading Days')
    ax1.set_xlabel('Percentile')
    ax1.set_ylabel('Counts')
    ax2.set_ylabel('Cumulative Percent')
    ax2.yaxis.set_label_coords(1.1, 0.5)
    ax2.yaxis.set_major_formatter(mtick.PercentFormatter())
    ax.xaxis.set_major_formatter(mtick.PercentFormatter())

    plt.savefig("Percentile Plot.jpeg", format= 'jpeg', dpi=100)
    plt.show()
    plt.close()
    return None













