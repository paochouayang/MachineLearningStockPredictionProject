from django.apps import AppConfig
import tensorflow as tf
import pickle


class MlapiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mlapi'

    lstm_1d_model = tf.keras.models.load_model('mlapi/blobStorage/lstm_1day_model')
    lstm_5d_model = tf.keras.models.load_model('mlapi/blobStorage/lstm_5day_model')
    lstm_1mo_model = tf.keras.models.load_model('mlapi/blobStorage/lstm_1month_model')
    #rf_1d_model = pickle.load(open('mlapi/blobStorage/randomforest_1day_model.sav', 'rb'))
    #rf_5d_model = pickle.load(open('mlapi/blobStorage/randomforest_5day_model.sav', 'rb'))
    #rf_1mo_model = pickle.load(open('mlapi/blobStorage/randomforest_1month_model.sav', 'rb'))
