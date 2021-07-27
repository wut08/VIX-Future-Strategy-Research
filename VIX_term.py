import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
from scipy.stats import describe



# we will use log return for SPX, normal return for VIX, and VIX futures in this analysis
# turn price file into return
def term_analysis(filepath,vix):
    vix['vix_ret'] = vix.iloc[:,1].diff()

    # get returns for all future files
    term = []
    termPercent =[]
    future = []
    VIX = []
    all_data = pd.DataFrame()

    for contracts in filepath.glob('**/*'):

        contract = pd.read_excel(contracts)

        settlement = np.array(contract.iloc[:, 5])

        settlement_num = np.delete(settlement, [0])
        settlement_num30 = settlement_num[-30:]
        final_settlement = settlement_num30[-1]

        # get the daily close price ret & log ret for 30 days excluding last session
        contract.drop(contract.tail(1).index,inplace=True)
        contract.drop(contract.head(1).index,inplace = True)

        contract_30 = contract[-30:].copy()

        contract_30['close_ret'] = contract_30.iloc[:,4].diff()

        #set dates as index
        contract_30['DATES'] = pd.to_datetime(contract_30.iloc[:,0])

        # fill the vix_ret in for each contract
        df = pd.merge(contract_30, vix, how= 'inner', on = 'DATES')

        VIX_beg = df['VIX Index'].iloc[-28]
        future_beg = df.iloc[:,4].iloc[-28]
        term30 = future_beg -VIX_beg
        term_percent = term30/(final_settlement - future_beg)
        future_ret = final_settlement-future_beg
        VIX_ret = final_settlement -VIX_beg
        VIX.append(VIX_ret)
        future.append(future_ret)
        term.append(term30)
        termPercent.append(term_percent)

        df['futures_spot'] = df.iloc[:,4] - df['VIX Index']
        df['is_high_vol'] = (df['VIX Index'] > 20)*1
        # change of futures_spot
        df['spread_change'] = df['futures_spot'].diff()
        #previous day spread
        df['previous_spread'] = df['futures_spot'].shift()
        df = df[['DATES','close_ret','vix_ret','futures_spot','spread_change','previous_spread','is_high_vol']].copy()

        # put them into one dataframe
        all_data = all_data.append(df)

    df_f= pd.DataFrame(future,columns=['Future Return 29days'])
    df_v = pd.DataFrame(VIX, columns= ['VIX Spot Return 29days'])
    df_t = pd.DataFrame(term,columns=['Term Spread 29days'])
    return df_f,df_v,df_t,future,VIX,term

def plot_spot_future(VIX,future):

    y = future
    x = VIX
    res1 = stats.linregress(x,y)

    x2= stats.mstats.winsorize(x,limits=[0.05,0.05])

    res2 = stats.linregress(x2,y)
    sns.set_style('ticks')
    sns.regplot(x,y,ci = None, marker = '.', label = 'VIX Spot Return and Future Return')
    sns.despine()
    plt.title('VIX Spot Return and Future Return')
    plt.xlabel('VIX Spot Return')
    plt.ylabel('Future Return')

    plt.figtext(0.7,0.3,'Slope = '+str(np.round(res1.slope,3)) +'\n R2 = '+str(np.round(res1.rvalue**2,3)))
    plt.savefig("VIX Spot and Future Return.jpeg", format='jpeg', dpi=100)
    plt.show()
    plt.close()
    return None


def plot_return(df_t):

    df_t = df_t.interpolate()
    ax = df_t.plot.hist(bins=100, edgecolor = 'black')
    plt.title(df_t.columns[0])
    plt.xlabel(df_t.columns[0][:-6])
    plt.ylabel('Counts')
    std = np.round(np.sqrt(np.array(describe(df_t))[3]), 2)
    skew = np.round(np.array(describe(df_t))[4], 2)
    kurtosis = np.round(np.array(describe(df_t))[5], 2)
    plt.figtext(0.4,0.3,' mean = ' + str(np.round(np.mean(df_t.values),2))+'\n median = '+ str(np.round(np.median(df_t.values))) +'\n std = ' +str(std[0])+'\n skew = ' + str(skew[0]))
    plt.savefig(f"{df_t.columns[0]} Plot.jpeg", format='jpeg', dpi=100)
    plt.show()
    plt.close()
    return None








