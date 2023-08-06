# LaPros
> LaPros stands for label probability and label problems


## Install

`pip install lapros`

## How to use

The first version of LaPros works with binary classifiers.
It ranks the suspicious labels given probabilies of positive cases. 
You can use normal Python lists, Numpy arrays or Pandas data. 
Return values are in a Numpy array or a Pandas series, 
the larger the value, the more suspicious are the coresponding labels.

```python
from lapros.noise import suspect
```

```python
suspect(
    [1, 0, 0, 1, 1],
    probas=[0.5, 0.6, 0.7, 0.8, 0.9],
)
```

    2022-07-11 13:05:55.445 | DEBUG    | lapros.noise:suspect:56 - Normal Python lists
    2022-07-11 13:05:55.446 | DEBUG    | lapros.noise:suspect:23 - Numpy arrays labels and probas must have same length 5 vs 5
    2022-07-11 13:05:55.446 | DEBUG    | lapros.noise:suspect:26 - Unique labels [0 1]
    2022-07-11 13:05:55.446 | DEBUG    | lapros.noise:suspect:28 - Trying to reshape probas
    2022-07-11 13:05:55.447 | DEBUG    | lapros.noise:suspect:30 - Shape of labels and probas: (5,) vs (5, 1)
    2022-07-11 13:05:55.447 | DEBUG    | lapros.noise:suspect:38 - ranks [0.5 0.6 0.7 0.2 0.1]





    [array([0.5, 0.6, 0.7, 0.2, 0.1])]



```python
suspect(
    [1, 0, 0, 1, 1],
    probas=[[0.5, 0.6, 0.7, 0.8, 0.9]],
)
```

    2022-07-11 13:05:55.499 | DEBUG    | lapros.noise:suspect:56 - Normal Python lists
    2022-07-11 13:05:55.500 | DEBUG    | lapros.noise:suspect:23 - Numpy arrays labels and probas must have same length 5 vs 1
    2022-07-11 13:05:55.501 | DEBUG    | lapros.noise:suspect:26 - Unique labels [0 1]
    2022-07-11 13:05:55.501 | DEBUG    | lapros.noise:suspect:28 - Trying to reshape probas
    2022-07-11 13:05:55.501 | DEBUG    | lapros.noise:suspect:30 - Shape of labels and probas: (5,) vs (5, 1)
    2022-07-11 13:05:55.502 | DEBUG    | lapros.noise:suspect:38 - ranks [0.5 0.6 0.7 0.2 0.1]





    [array([0.5, 0.6, 0.7, 0.2, 0.1])]



```python
suspect(
    np.array([1, 0, 0, 1, 1]),
    probas=np.array([0.5, 0.6, 0.7, 0.8, 0.9]),
)
```

    2022-07-11 13:05:55.553 | DEBUG    | lapros.noise:suspect:23 - Numpy arrays labels and probas must have same length 5 vs 5
    2022-07-11 13:05:55.555 | DEBUG    | lapros.noise:suspect:26 - Unique labels [0 1]
    2022-07-11 13:05:55.556 | DEBUG    | lapros.noise:suspect:28 - Trying to reshape probas
    2022-07-11 13:05:55.556 | DEBUG    | lapros.noise:suspect:30 - Shape of labels and probas: (5,) vs (5, 1)
    2022-07-11 13:05:55.556 | DEBUG    | lapros.noise:suspect:38 - ranks [0.5 0.6 0.7 0.2 0.1]





    array([0.5, 0.6, 0.7, 0.2, 0.1])



```python
suspect(
    pd.Series([1, 0, 0, 1, 1]),
    probas=pd.DataFrame([0.5, 0.6, 0.7, 0.8, 0.9]),
)
```

    2022-07-11 13:05:55.597 | DEBUG    | lapros.noise:suspect:47 - Pandas series labels and dataframe probas must have same length 5 vs 5
    2022-07-11 13:05:55.598 | DEBUG    | lapros.noise:suspect:23 - Numpy arrays labels and probas must have same length 5 vs 5
    2022-07-11 13:05:55.599 | DEBUG    | lapros.noise:suspect:26 - Unique labels [0 1]
    2022-07-11 13:05:55.599 | DEBUG    | lapros.noise:suspect:30 - Shape of labels and probas: (5,) vs (5, 1)
    2022-07-11 13:05:55.599 | DEBUG    | lapros.noise:suspect:38 - ranks [0.5 0.6 0.7 0.2 0.1]





    0    0.5
    1    0.6
    2    0.7
    3    0.2
    4    0.1
    dtype: float64


