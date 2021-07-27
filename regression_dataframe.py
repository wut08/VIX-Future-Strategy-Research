import numpy as np
import pandas as pd

def get_returns_for_regression(filepath,spx,vix):
    all_data = pd.DataFrame()
    all_data_30 = pd.DataFrame()
    spx['spx_ret'] = spx.iloc[:, 1].pct_change()

    spx['spx_log_ret'] = np.log(spx.spx_ret + 1)

    vix['vix_ret'] = vix.iloc[:, 1].diff()
    for contracts in filepath.glob('**/*'):

        contract = pd.read_excel(contracts)

        # get the daily close price ret & log ret for 30 days excluding last session
        contract.drop(contract.tail(1).index,inplace=True)
        contract.drop(contract.head(1).index,inplace = True)

        contract_30 = contract[-30:].copy()

        contract_30['close_ret'] = contract_30.iloc[:,4].diff()

        #set dates as index
        contract_30['DATES'] = pd.to_datetime(contract_30.iloc[:,0])

        #fill spx in for each contract
        spx['DATES'] = pd.to_datetime(spx.iloc[:,0])
        df = pd.merge(contract_30,spx,how='inner',on='DATES')

        # fill the vix_ret in for each contract
        df = pd.merge(df, vix, how= 'inner', on = 'DATES')

        df['futures_spot'] = df.iloc[:,4] - df['VIX Index']
        df['is_high_vol'] = (df['VIX Index'] > 20)*1
        # change of futures_spot
        df['spread_change'] = df['futures_spot'].diff()
        #previous day spread
        df['previous_spread'] = df['futures_spot'].shift()

        df = df[['DATES','close_ret','vix_ret','futures_spot','spread_change','previous_spread','is_high_vol','spx_log_ret']].copy()

        df = df[-28:].copy()

        df['days'] = [ 'T-28', 'T-27', 'T-26', 'T-25', 'T-24', 'T-23', 'T-22', 'T-21', 'T-20', 'T-19', 'T-18',
                      'T-17', 'T-16', 'T-15', 'T-14', 'T-13', 'T-12', 'T-11', 'T-10', 'T-9', 'T-8', 'T-7', 'T-6', 'T-5',
                      'T-4', 'T-3', 'T-2', 'T-1']

        df2 = df.T.copy()

        df2.columns = df2.iloc[8]

        # put them into one dataframe
        all_data_30 = all_data_30.append(df)
        all_data = all_data.append(df2)

    spot = all_data.groupby(level = 0).get_group('vix_ret')
    previous_spread = all_data.groupby(level=0).get_group('previous_spread')
    futures_ret = all_data.groupby(level=0).get_group('close_ret')
    is_high_vol = all_data.groupby(level=0).get_group('is_high_vol')
    spx_log_ret = all_data.groupby(level=0).get_group('spx_log_ret')

    return spot, previous_spread,futures_ret, is_high_vol, spx_log_ret


def comb_for_regression(spot,ps_standarized,futures_ret,is_high_vol,spx_log_ret):
    for i in spot, futures_ret, is_high_vol, spx_log_ret:

        i.reset_index(drop=True, inplace=True)
    spot.columns = [f'{i}_vix' for i in spot.columns.values]
    futures_ret.columns = [f'{i}_cr' for i in futures_ret.columns.values]
    is_high_vol.columns = [f'{i}_h' for i in is_high_vol.columns.values]
    spx_log_ret.columns = [f'{i}_spx' for i in spx_log_ret.columns.values]

    comb = pd.DataFrame([])
    for i in spot,futures_ret,is_high_vol,spx_log_ret,ps_standarized:
        comb = pd.concat([comb,i],axis=1)

    return comb



