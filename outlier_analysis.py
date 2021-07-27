import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


#USE PRICE SUBTRACT MA SIGNALS TO GET TREND; # use 10 days to calculate MA slopes
def outlier_signal_analysis(outliers,vix,spx,spx_vol,ma_spx,ma_vix,spx_iv):
    def calc_slope(x):
        slope = np.polyfit(range(len(x)),x,1)[0]
        return slope



    ma_vix['DATES'] = pd.to_datetime(ma_vix.iloc[:,0])
    vix_df = pd.merge(vix,ma_vix, how='inner', on='DATES')

    df2 = vix_df[['MA_5','MA_15','MA_20','MA_30','MA_50','MA_100','MA_200']].copy()
    # the differences between MA and price
    vix_df[['vix_5','vix_15','vix_20','vix_30','vix_50','vix_100','vix_200']] = df2.sub(vix_df['VIX Index'], axis = 0).apply(lambda x:x*-1)
    # rolling 10 day slope of MAs
    vix_df[['vix_5_s','vix_15_s','vix_20_s','vix_30_s','vix_50_s','vix_100_s','vix_200_s']] = df2.rolling(10,min_periods=2).apply(calc_slope)
    #code dummy
    # price difference >0 or not
    vix_df[['pmv_5','pmv_15','pmv_20','pmv_30','pmv_50','pmv_100','pmv_200']] = (vix_df[['vix_5','vix_15','vix_20','vix_30','vix_50','vix_100','vix_200']]>0)*1
    #slope > 0 or not
    vix_df[['sv_5','sv_15','sv_20','sv_30','sv_50','sv_100','sv_200']] = (vix_df[['vix_5_s','vix_15_s','vix_20_s','vix_30_s','vix_50_s','vix_100_s','vix_200_s']]>0)*1
    #short term signals comparison
    vix_df['vstc'] = np.where(vix_df['MA_5'] > vix_df['MA_15'],1,0)
    #medium term signals comparison
    vix_df['vmtc'] = np.where(vix_df['MA_20'] > vix_df['MA_50'],1,0)
    #long term signals comparison
    vix_df['vltc'] = np.where(vix_df['MA_50'] > vix_df['MA_200'],1,0)
    # short term signal if all 5 >2(3 and up integers) it is 1, otherwise 0
    vix_df['vsts'] = (vix_df['pmv_5'] + vix_df['pmv_15'] + vix_df['sv_5'] + vix_df['sv_15'] + vix_df['vstc'] > 2) *1
    #medium term
    vix_df['vmts'] = (vix_df['pmv_20'] + vix_df['pmv_50'] + vix_df['sv_20'] + vix_df['sv_50'] + vix_df['vmtc'] > 2) *1
    #long term
    vix_df['vlts'] = (vix_df['pmv_50'] + vix_df['pmv_200'] + vix_df['sv_50'] + vix_df['sv_200'] + vix_df['vltc'] > 2) *1



    ma_spx['DATES'] = pd.to_datetime(ma_spx.iloc[:,0])
    spx_df = pd.merge(spx,ma_spx, how='inner', on='DATES')

    df3 = spx_df[['MA_5','MA_15','MA_20','MA_30','MA_50','MA_100','MA_200']].copy()
    spx_df[['spx_5','spx_15','spx_20','spx_30','spx_50','spx_100','spx_200']] = df3.sub(spx_df['SPX Index'], axis = 0).apply(lambda x:x*-1)
    spx_df[['spx_5_s','spx_15_s','spx_20_s','spx_30_s','spx_50_s','spx_100_s','spx_200_s']] = df3.rolling(10,min_periods=2).apply(calc_slope)

    spx_df[['pms_5','pms_15','pms_20','pms_30','pms_50','pms_100','pms_200']] = (spx_df[['spx_5','spx_15','spx_20','spx_30','spx_50','spx_100','spx_200']]>0)*1
    spx_df[['ss_5','ss_15','ss_20','ss_30','ss_50','ss_100','ss_200']] = (spx_df[['spx_5_s','spx_15_s','spx_20_s','spx_30_s','spx_50_s','spx_100_s','spx_200_s']]>0)*1
    spx_df['sstc'] = np.where(spx_df['MA_5'] > spx_df['MA_15'],1,0)
    spx_df['smtc'] = np.where(spx_df['MA_20'] > spx_df['MA_50'],1,0)
    spx_df['sltc'] = np.where(spx_df['MA_50'] > spx_df['MA_200'],1,0)

    # short term signal if all 5 >2(3 and up integers) it is 1, otherwise 0
    spx_df['ssts'] = (spx_df['pms_5'] + spx_df['pms_15'] + spx_df['ss_5'] + spx_df['ss_15'] + spx_df['sstc'] > 2) *1
    #medium term
    spx_df['smts'] = (spx_df['pms_20'] + spx_df['pms_50'] + spx_df['ss_20'] + spx_df['ss_50'] + spx_df['smtc'] > 2) *1
    #long term
    spx_df['slts'] = (spx_df['pms_50'] + spx_df['pms_200'] + spx_df['ss_50'] + spx_df['ss_200'] + spx_df['sltc'] > 2) *1

    #add realized and iv to spx dataframe
    spx_dfv = pd.merge(spx_df, spx_vol, how= 'inner', on= 'DATES')

    # code dummy for if realized vol is higher than 30 day rolling average
    spx_dfv['realized_volMA'] = spx_dfv['SPX_vol'].rolling(30,min_periods=2).mean()
    spx_dfv['rh'] = np.where(spx_dfv['SPX_vol'] > spx_dfv['realized_volMA'],1,0)


    spx_dfvv = pd.merge(spx_dfv,spx_iv, how = 'inner', on= 'DATES')

    # code dummy for if realized vol is higher than implied
    spx_dfvv['r_v'] = np.where(spx_dfvv['SPX_vol']> spx_dfvv['SPX_IV'],1,0)
    spx_dfvv['rv_spread'] = spx_dfvv['SPX_vol'].sub(spx_dfvv['SPX_IV'],axis = 0)

    outliers['DATES'] = pd.to_datetime(outliers.iloc[:,0])

    ol = pd.merge(outliers,vix_df,how = 'inner', on= 'DATES')
    oll = pd.merge(ol,spx_dfvv, how='inner', on= 'DATES')

    oll['is_high_vol'] = (oll['VIX Index'] > 20)*1

    #plot spx short term signal with VIX index

    spx_vix = pd.merge(spx_df[['DATES','ssts']],vix_df[['DATES','VIX Index']], how = 'inner', on = 'DATES')
    spx_vix.plot(x = "DATES", y = spx_vix[['ssts', 'VIX Index']])
    #plt.show()
    plt.close()
    return oll





