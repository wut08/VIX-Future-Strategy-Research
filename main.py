from pathlib import Path
import pandas as pd

#below are functions written for this project
import outlier_analysis as oa
import boxplot as bp
import consolidate_prices as cp
import positive_days as psd
import find_highest_day as fhd
import VIX_term as vt
import starting_price_analysis as sp
import last_trading_session as ls
import regression_dataframe as rd
import standarizing_ps as sps
import regresion_29days as r29

#input file path inside of '' (keep the r) including all cleaned and formatted price files in FULL CYCLE

filepath = Path("FULL CYCLE")
#files below include formula in the excel spreadsheet, open them will update the data till today
vix = pd.read_excel('VIX Spot.xlsx')
spx = pd.read_excel("SPX prices.xlsx")
spx_vol = pd.read_excel("SPX hist vol.xlsx")
spx_iv = pd.read_excel("SPX_IV.xlsx")

#files below were acquired using BQNT, script in notes

ma_spx = pd.read_excel("ma_spx.xlsx")
ma_vix = pd.read_excel("ma_vix.xlsx")


# Consolidate all price files into all prices and differences

prices, differences, ol, percentile, differences_for_plot = cp.consolidate(filepath)
# change path/name inside of '' to the name/anywhere you want to save the file to, don't forget the r if it's an actual path, default in program folder
prices.to_csv('all_prices.csv')
differences.to_csv('all_differences.csv')

# plot the percentile of final settlement prices in the last 30 trading days (saves a copy in the default folder)
cp.percentile_plot(percentile)

# Horizontally plot all futures
cp.horizontal_plot(differences_for_plot)

# get stats for T-5 table
stats = cp.get_stats(differences[['T-5', 'T-4', 'T-3', 'T-2', 'T-1', 'T']])
stats.to_csv('T-5Stats.csv')

# box plots
bp.boxplot(filepath)

#get positive days distribution
pos_dist= psd.get_pos_dist(filepath)
pos_dist.to_csv('pos_days_dist.csv', index=False)

# find highest day
highest_day = fhd.find_highest_day(filepath)

#get heat map table for high prices
heat_map = psd.heatmap(pos_dist, highest_day)
heat_map.to_csv('heat_map.csv')

#full cycle return analysis
df_future, df_vix, df_term, future, VIX, term = vt.term_analysis(filepath, vix)

#plot monthly spot and future correlation
vt.plot_spot_future(VIX, future)

#plot vix spot, term, and future return at the beginning of each cycle
for i in df_vix, df_term, df_future:
    vt.plot_return(i)

#starting price plots
sp.starting_vix_plot(filepath)

#last trading session plots
ls.last_session_plots(filepath)

# get the combo spreadsheet including the standarized previous day spread, SPX, and Spot ViX, and future return
spot, previous_spread, futures_ret, is_high_vol, spx_log_ret = rd.get_returns_for_regression(filepath, spx, vix)
previous_spread.to_csv('ps.csv')

#standarize previous spread with time to expiration
ps_standarized = sps.standarize_ps(previous_spread)

#make combo dataframe
comb = rd.comb_for_regression(spot, ps_standarized, futures_ret, is_high_vol, spx_log_ret)
comb.to_csv('comb_new.csv', index= False )

#geting loadings and R2 30 days,comb = c6
loadings_All, loadings_Low, loadings_High, R2_all, R2_low, R2_high = r29.regress_30(comb)

# plot them
r29.plot_regression(loadings_All, R2_all)
r29.plot_regression(loadings_Low, R2_low)
r29.plot_regression(loadings_High, R2_high)

# get outliers
outliers = cp.outliers(ol)
outliers.to_csv('outliers_n.csv')

#get the unique dates for the outliers
dates = outliers.groupby('DATES').first()
dates.to_csv('dates.csv')
dates.reset_index(inplace=True)


oll = oa.outlier_signal_analysis(dates, vix, spx, spx_vol, ma_spx, ma_vix, spx_iv)
oll.to_csv('outliers_analysis_output.csv')

# get stats for signals
signal_stats = cp.get_stats(oll[['VIX Index', 'vsts', 'vmts', 'vlts', 'ssts', 'smts', 'slts', 'SPX_vol', 'SPX_IV', 'r_v', 'is_high_vol', 'rv_spread']])
signal_stats.columns = ['VIX Index','VIX Short term', 'VIX Medium Term', 'VIX Long Term', 'SPX Short Term', 'SPX Medium Term', 'SPX Long Term', 'SPX_realized_vol', 'SPX_IV', 'realized > implied', 'VIX>20', 'realized_implied_spread']
signal_stats.to_csv('signal_stats.csv')
