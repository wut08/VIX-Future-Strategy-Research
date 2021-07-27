import pandas as pd
import numpy as np

#iterate through all these files and create dataframe
def get_pos_dist(filepath):
    differences = []
    for contracts in filepath.glob('**/*'):

        contract = pd.read_excel(contracts)
        name = contract.columns[1]

        # get the final settlement price
        settlement = np.array(contract.iloc[:,5])

        settlement_num = np.delete(settlement,[0])
        settlement_num30 = settlement_num[-30:]
        final_settlement = settlement_num30[-1]

        OHLC = np.array(contract.iloc[:,1:5])

        OHLC_num = np.delete(OHLC,(0),axis=0)

        OHLC_num30 = np.delete(OHLC_num, (-1),axis=0)

        # get all the differences between T30, T29... T and T

        diffMatrix = (OHLC_num30[-29:] - final_settlement)*-1

        # find the pos days
        pos_count = np.sum(diffMatrix>0,axis=1)

        # how many days are pos in total in 30 days period
        pos_days= np.sum(pos_count>0)
        # find the pos values for each period
        pos_days_with_name = np.append(name,pos_count)
        pos_days_dist = np.append(np.sum(pos_days),pos_days_with_name)
        differences.append(pos_days_dist)

    df = pd.DataFrame(differences,columns=['Total Days','name','T-29', 'T-28', 'T-27', 'T-26', 'T-25', 'T-24', 'T-23', 'T-22', 'T-21', 'T-20', 'T-19', 'T-18',
                      'T-17', 'T-16', 'T-15', 'T-14', 'T-13', 'T-12', 'T-11', 'T-10', 'T-9', 'T-8', 'T-7', 'T-6', 'T-5',
                      'T-4', 'T-3', 'T-2', 'T-1'])
    return df

def heatmap(pos_dist, highest_day):
    pos_dist[['T-29', 'T-28', 'T-27', 'T-26', 'T-25', 'T-24', 'T-23', 'T-22', 'T-21', 'T-20', 'T-19', 'T-18',
              'T-17', 'T-16', 'T-15', 'T-14', 'T-13', 'T-12', 'T-11', 'T-10', 'T-9', 'T-8', 'T-7', 'T-6', 'T-5',
              'T-4', 'T-3', 'T-2', 'T-1']] = pos_dist[
        ['T-29', 'T-28', 'T-27', 'T-26', 'T-25', 'T-24', 'T-23', 'T-22', 'T-21', 'T-20', 'T-19', 'T-18',
         'T-17', 'T-16', 'T-15', 'T-14', 'T-13', 'T-12', 'T-11', 'T-10', 'T-9', 'T-8', 'T-7', 'T-6', 'T-5',
         'T-4', 'T-3', 'T-2', 'T-1']].astype(int)


    pos_dist.loc['No. Lower Px'] = pos_dist.iloc[:, 2:32].sum(axis=0)
    pos_dist.loc['% Lower Px'] = (pos_dist.loc['No. Lower Px'] / ((len(pos_dist)) * 4)).fillna(0).map("{:.2%}".format)
    pos_dist.loc['Days with Lower Px'] = (pos_dist.iloc[:, 2:32] != 0).sum(axis=0)
    pos_dist.loc['% Days with Lower Px'] = (pos_dist.loc['Days with Lower Px'] / (len(pos_dist))).fillna(0).map(
        "{:.2%}".format)

    pos_all = pd.concat([pos_dist, highest_day], sort=False).fillna(0)
    heat_map = pos_all.iloc[-5:].drop(['Total Days', 'name'], axis=1)
    heat_map.columns = ['T-29', 'T-28', 'T-27', 'T-26', 'T-25', 'T-24', 'T-23', 'T-22', 'T-21', 'T-20', 'T-19', 'T-18',
                        'T-17', 'T-16', 'T-15', 'T-14', 'T-13', 'T-12', 'T-11', 'T-10', 'T-9', 'T-8', 'T-7', 'T-6',
                        'T-5',
                        'T-4', 'T-3', 'T-2', 'T-1']
    return heat_map
