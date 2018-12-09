import pandas as pd
import numpy as np

def parameter_estimation(data, biased_data, apply_correction = True):

    """
    Estimate parameters for BN

    Parameters
    ----------
    parent :


    Returns
    -------

    Notes
    -----
    1. Need to create overarching architecture for tool...  
    """
    common_cols = np.intersect1d(data.columns, biased_data.columns)
    parent = common_cols.item(0)

    biased_col_list = list(biased_data)
    biased_children = [child for child in biased_col_list if child not in common_cols]
    child = biased_children[0]

    unbiased_col_list = list(data)
    unbiased_children = [child for child in unbiased_col_list if child not in common_cols]
    ub_child = unbiased_children[0]


    ### apply correction
    p_x1 = data[parent].sum()/len(data[parent])
    p_x0 = 1 - p_x1

    q_x1 = biased_data[parent].sum()/len(biased_data[parent])
    q_x0 = 1 - q_x1
    # print(p_x1, p_x0, q_x1, q_x0)

    # calculate weights
    # weight only depends on x (parent)
    w_1 = p_x1/q_x1
    w_0 = p_x0/q_x0

    p_parent = ((biased_data[parent].sum() * w_1)/
               ((biased_data[parent].sum() * w_1) + ((len(biased_data[parent]) - biased_data[parent].sum()) * w_0)))

    data_x0 = biased_data[child][biased_data[parent]==0]
    c_child_y1x0 = data_x0.sum()
    c_child_y0x0 = len(data_x0) - data_x0.sum()

    data_x1 = biased_data[child][biased_data[parent]==1]
    c_child_y1x1 = data_x1.sum()
    c_child_y0x1 = len(data_x1) - data_x1.sum()

    p_biased_child_y1x0 = (c_child_y1x0/
               (c_child_y1x0 + c_child_y0x0))

    p_biased_child_y1x1 = (c_child_y1x1/
               (c_child_y1x1 + c_child_y0x1))


    ### Parameter estimation for unbiased data

    df_parent_0 = data[ub_child][data[parent]==0]
    df_parent_1 = data[ub_child][data[parent]==1]
    p_child_y1x0 = (df_parent_0.sum()) / len(df_parent_0)
    p_child_y1x1 = (df_parent_1.sum()) / len(df_parent_1)



    return round(p_parent, 4), round(p_biased_child_y1x0, 4), round(p_biased_child_y1x1, 4), round(p_child_y1x0, 4), round(p_child_y1x1, 4)
