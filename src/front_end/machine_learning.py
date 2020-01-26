import pandas as pd
import numpy as np
import pickle
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

SAMPLE_FREQUENCY_COMBO_BOX = {
    '2.86MHz': {
        'MLP': {
            'Train Model Human Non Human': {
                'solver': 'adam',
                'activation': 'tanh',
                'hidden_layer_sizes': (31)

            },
            'Train Model Other Objects': {
                'solver': 'adam',
                'activation': 'tanh',
                'hidden_layer_sizes': (31)
            }
        },
        'Random_Forest': {
            'Train Model Human Non Human': {
                'n_estimators': 300,
                'min_samples_split': 2,
                'min_samples_leaf': 3,
                'max_depth': 110,

            },
            'Train Model Other Objects': {
                'n_estimators': 300,
                'min_samples_split': 2,
                'min_samples_leaf': 3,
                'max_depth': 110,
            },
        }
    },
    '1.14MHz': {
        'MLP': {
            'Train Model Human Non Human': {
                'solver': 'adam',
                'activation': 'relu',
                'hidden_layer_sizes': (31)

            },
            'Train Model Other Objects': {
                'solver': 'adam',
                'activation': 'relu',
                'hidden_layer_sizes': (31)
            }
        }, 'Random_Forest': {
            'Train Model Human Non Human': {
                'n_estimators': 300,
                'min_samples_split': 2,
                'min_samples_leaf': 3,
                'max_depth': 110,

            },
            'Train Model Other Objects': {
                'n_estimators': 300,
                'min_samples_split': 2,
                'min_samples_leaf': 3,
                'max_depth': 110,
            },
        }
    }, '114KHz': {
        'MLP': {
            'Train Model Human Non Human': {
                'solver': 'adam',
                'activation': 'relu',
                'hidden_layer_sizes': (13, 10)

            },
            'Train Model Other Objects': {
                'solver': 'adam',
                'activation': 'tanh',
                'hidden_layer_sizes': (13, 10)
            }
        }, 'Random_Forest': {
            'Train Model Human Non Human': {
                'n_estimators': 300,
                'min_samples_split': 2,
                'min_samples_leaf': 3,
                'max_depth': 110,

            },
            'Train Model Other Objects': {
                'n_estimators': 300,
                'min_samples_split': 2,
                'min_samples_leaf': 3,
                'max_depth': 110,
            },
        }
    }
}


class MachineLearningHelper:
    def __init__(self):
        self.sample_frequency = '2.86MHz'
        self.selected_element = SAMPLE_FREQUENCY_COMBO_BOX[self.sample_frequency]
        self.selected_algorithm = 'MLP'
        self.selected_type = 'Train Model Human Non Human'
        self.clf_ready = False
        self.clf_loaded = None
        self.select_classifier()

    def change_selected_element(self, element_name):
        if element_name in SAMPLE_FREQUENCY_COMBO_BOX:
            self.sample_frequency = element_name
            self.selected_element = SAMPLE_FREQUENCY_COMBO_BOX[element_name]
            self.select_classifier()

    def change_type(self, element_name):
        self.selected_type = element_name
        self.select_classifier()

    def select_classifier(self):
        a_type = self.selected_element['MLP'][self.selected_type]
        solver = a_type['solver']
        activation = a_type['activation']
        hidden_layer_sizes = a_type['hidden_layer_sizes']
        self.clf_mlp = MLPClassifier(solver=solver, activation=activation, max_iter=2000,
                                     alpha=1e-5, hidden_layer_sizes=hidden_layer_sizes, random_state=12)

        a_type = self.selected_element['Random_Forest'][self.selected_type]
        n_estimators = a_type['n_estimators']
        min_samples_split = a_type['min_samples_split']
        n_estimators = a_type['n_estimators']
        min_samples_leaf = a_type['min_samples_leaf']
        max_depth = a_type['max_depth']
        self.clf_rf = RandomForestClassifier(
            n_estimators=n_estimators, min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf, max_depth=max_depth, bootstrap=True)

    def train(self, X_train, y_train):
        self.clf_mlp.fit(X_train, y_train)
        self.clf_rf.fit(X_train, y_train)
        self.clf_ready = True

    def predict(self, X_test):
        result_mlp = self.clf_mlp.predict(X_test)
        result_rf = self.clf_rf.predict(X_test)
        return result_mlp, result_rf

    def save_model(self):

        from datetime import datetime
        import os
        if not os.path.isdir(os.getcwd()+'/data/model'):
            os.makedirs('data/model')
        date_str = str(datetime.now().date())
        if self.selected_type == 'Train Model Human Non Human':
            file_mlp = f'./data/model/mlp_human_non_human_{date_str}_{self.sample_frequency}'
            file_rf = f'./data/model/rf_human_non_human_{date_str}_{self.sample_frequency}'
        else:
            file_mlp = f'./data/model/mlp_all_objects_{date_str}_{self.sample_frequency}'
            file_rf = f'./data/model/rf_all_objects_{date_str}_{self.sample_frequency}'
        pickle.dump(self.clf_mlp, open(file_mlp, 'wb'))
        pickle.dump(self.clf_rf, open(file_rf, 'wb'))

    def load_model(self, model):
        self.clf_loaded = model
        self.clf_ready = True

    def loaded_predict(self, X_test):
        result = self.clf_loaded.predict(X_test)
        return result
