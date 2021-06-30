import pandas as pd
from transformers import DistilBertTokenizerFast
from transformers import TFDistilBertForSequenceClassification
import tensorflow as tf

def apply_BERT_prediction(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Apply BERT prediction layer based on BERT classifier.
    WARN: For now, it's fake code -> random()
    TODO: finish function with real Torch and BERT
    """
    import random
    dataframe['BERT'] = 0 # add column for results
    dataframe['BERT'] = dataframe.apply(
        lambda x: random.random(), axis=1
    ) # add a column for results

    return dataframe