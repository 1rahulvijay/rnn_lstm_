import pandas as pd

def split_dataframe_by_column(df, col_name):
    """
    Splits a DataFrame into a dictionary of DataFrames grouped by a specified column.

    Parameters:
    df (pd.DataFrame): The DataFrame to split.
    col_name (str): The name of the column to group by.

    Returns:
    dict: A dictionary where the keys are the unique values in the column and the values are DataFrames of the grouped data.

    Example:
    >>> data = {'A': ['foo', 'bar', 'foo', 'bar', 'foo', 'bar'], 'B': [1, 2, 3, 4, 5, 6]}
    >>> df = pd.DataFrame(data)
    >>> result = split_dataframe_by_column(df, 'A')
    >>> sorted(result.keys())
    ['bar', 'foo']
    >>> result['foo']
       A  B
    0  foo  1
    2  foo  3
    4  foo  5
    >>> result['bar']
       A  B
    1  bar  2
    3  bar  4
    5  bar  6
    """
    grouped = df.groupby(col_name)
    return {category: group.copy() for category, group in grouped}

if __name__ == "__main__":
    import doctest
    doctest.testmod()
