from pandas.core.interchange.dataframe_protocol import DataFrame


def clip_outliers_iqr(df: DataFrame, cols: list) -> DataFrame:
    r""" clips data by standard clipping (comparing quantiles).
    :param df: DataFrame of the raw data
    :param cols: columns that includes df
    :return: Dataframe with clipped data
    :rtype: DataFrame
    """
    df = df.copy()
    for col in cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        df[col] = df[col].clip(lower, upper)
    return df