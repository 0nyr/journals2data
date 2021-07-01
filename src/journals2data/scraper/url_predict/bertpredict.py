import pandas as pd
from transformers import DistilBertTokenizerFast
from transformers import TFDistilBertForSequenceClassification
import tensorflow as tf
import random

def apply_BERT_prediction(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Apply BERT prediction layer based on BERT classifier.
    WARN: For now, it's fake code -> random()
    TODO: finish function with real Torch and BERT
    """

    def predict(model, tokenizer, sentence):
        predict_input = tokenizer.encode(sentence, truncation=True, padding=True, return_tensors="tf")
        tf_output = model.predict(predict_input)[0]
        tf_prediction = tf.nn.softmax(tf_output, axis=1).numpy()[0]
        return tf_prediction[1]

    # TODO : Fix model path here
    model = TFDistilBertForSequenceClassification.from_pretrained(
        '/home/cboscher/psat-elod_time_interval/psat-elod_time_interval/PSAT-master/PSAT-master/models/BERT_classifier_en')
    tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')


    dataframe['BERT'] = 0 # add column for results
    dataframe['BERT'] = dataframe.apply(
        lambda x: predict(model,tokenizer, x.title), axis=1) # add a column for results

    return dataframe