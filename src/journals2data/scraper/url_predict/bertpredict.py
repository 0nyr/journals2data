import pandas as pd
from transformers import DistilBertTokenizerFast
from transformers import TFDistilBertForSequenceClassification
import tensorflow as tf

from journals2data import utils
from journals2data import data

def apply_BERT_prediction(
    dataframe: pd.DataFrame,
    source: data.Source
) -> pd.DataFrame:
    """
    Apply BERT prediction layer based on BERT classifier.
    """

    # get model_path depending on the language
    model_dirpath: str = utils.Global.BASE_BERT_MODEL_BASEPATH + \
        utils.Global.BERT_LANGUAGE_DIRS[source.language]
    model = TFDistilBertForSequenceClassification.from_pretrained(
        model_dirpath
    )
    tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')

    def predict(model, tokenizer, sentence):
        predict_input = tokenizer.encode(sentence, truncation=True, padding=True, return_tensors="tf")
        tf_output = model.predict(predict_input)[0]
        tf_prediction = tf.nn.softmax(tf_output, axis=1).numpy()[0]
        return tf_prediction[1]

    dataframe['BERT'] = 0 # add column for results
    dataframe['BERT'] = dataframe.apply(
        lambda x: predict(model,tokenizer, x.title), axis=1) # add a column for results

    return dataframe
