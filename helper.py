import pandas as pd 

def biased_subsample(df_data, samples, variable, pr_0 ):
    """

    Parameters:
    -------------
    df_data: dataframe
    samples: # of samples to return
    variable: column to bias on
    pr_0: new p(0)

    """
    pr_1 = 1 - pr_0

    samples_0 = int(pr_0 * samples)
    samples_1 = int(samples - samples_0)

    original_pr_1 = df_data[variable].sum()/len(df_data[variable])
    original_pr_0 = 1 - original_pr_1

    if pr_1 > original_pr_0:
        df_1 = df_data[(df_data[variable]==1)].sample(n=samples_1, replace = True)
    else:
        df_1 = df_data[(df_data[variable]==1)].sample(n=samples_1)


    if pr_0 > original_pr_0:
        df_0 = df_data[(df_data[variable]==0)].sample(n=samples_0, replace = True)
    else:
        df_0 = df_data[(df_data[variable]==0)].sample(n=samples_0)

    df_biased = pd.concat([df_0, df_1], ignore_index=True)


    return df_biased
