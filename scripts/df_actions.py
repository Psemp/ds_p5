import pandas as pd
import numpy as np

from sklearn.preprocessing import OneHotEncoder


def remove_outliers(column_eval: str,  df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates the IQR (Inter Quartile Range) for each column value of the column_subset of a DataFrame using
     the column to evaluate.
    Applies the method to clean the data for col passed in parameter by dropping the index/row
    Args:
     - column_eval : name of the column to evaluate, dtype must be int or float
     - df : the dataframe to clean
    Returns : Void function
    """
    dtype = str(df[column_eval].dtype)
    if not (dtype.startswith("int") or dtype.startswith("float") or dtype.startswith("uint")):
        print(dtype, "trying using column.astype(float)")

        try:
            df[column_eval] = df[column_eval].astype(float)

        except Exception:
            raise Exception(f"Error : Data Type of {column_eval} not a number")

    q3, q1 = np.percentile(df[column_eval], [75, 25])
    iqr = (q3 - q1) * 1.5
    q3_max = q3 + iqr
    q1_min = q1 - iqr

    for index, row in df.iterrows():
        if (row[column_eval] < q1_min) or (row[column_eval] > q3_max):
            df.drop(index=index, axis=1, inplace=True)


def one_hot_dataframe(dataframe: pd.DataFrame, subset: list, prefix: list = None, drop_og: bool = False):

    """
    Takes in argument a dataframe and a subset (the col names to encode), and encodes the subset with one hot encoder\
    , uses numeric index by default for new cols but can be overriden with a prefix list.\
    Can drop original cols or keep them with parameter "drop_og"

    Args:
    - dataframe : pandas.DataFrame object containing the columns to encode
    - subset : list of names of the columns to encode
    - prefix : list (default is None), if not None, provides a prefix for each col in subset, hence :\
        len(subset) must be == to len(prefix), or leave prefix to None and it will provide an index
    - drop_og : boolean, False by default. Determines whether or not to keep the original columns in\
        the returned dataframe

    Returns:
    - pandas.DataFrame object with columns encoded with OHE and args preferences.
    """

    if prefix is not None and len(subset) != len(prefix):
        raise Exception("Lenght of subset and prefix must be equal (if prefix not None)")

    ohe_idx = 0
    df_ohe = dataframe.copy(deep=True)

    for original in subset:

        ohe_col = OneHotEncoder()

        transformed = ohe_col.fit_transform(df_ohe[[original]])

        df_ohe[ohe_col.categories_[0]] = transformed.toarray()

        col_names = list(ohe_col.categories_[0])

        rename_cols = dict.fromkeys(col_names)

        if prefix is not None:
            for key in rename_cols.keys():
                rename_cols[key] = f"ohe_{str(prefix[ohe_idx])}_{key}"
        else:
            for key in rename_cols.keys():
                rename_cols[key] = f"ohe_{ohe_idx}_{key}"
        df_ohe.rename(columns=rename_cols, inplace=True)

        ohe_idx += 1

    if drop_og:
        df_ohe.drop(columns=subset, inplace=True)
        return df_ohe

    elif not drop_og:
        return df_ohe
