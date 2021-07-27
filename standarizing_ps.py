
def standarize_ps(ps):

    ps.reset_index(drop=True, inplace = True)
    ps1 = ps.T
    ps1.reset_index(drop=True, inplace = True)
    # make sure index 0 aligns with first value since it needs to standarize by 30 for T-29
    ps_divided = ps1.div((29 - ps1.index.values),axis = 0)
    ps_standarized = ps_divided.T.copy()

    ps_standarized.columns = [f'T-{28-i}_ps'for i in ps_standarized.columns.values]
    return ps_standarized
