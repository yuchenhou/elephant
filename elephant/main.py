import io
import json
import os
import zipfile

import pandas
import requests

import estimator


def main(data_set_name):
    with open(os.path.join(os.path.dirname(__file__), data_set_name + '.json')) as specs_file:
        specs = json.load(specs_file)
    zip_file = zipfile.ZipFile(io.BytesIO(requests.get(specs['url']).content))
    data_file = io.StringIO(zip_file.open(specs['file']).read().decode(errors='ignore'))
    data_set = pandas.read_csv(data_file, sep=specs['separator'], engine=specs['engine'])
    if data_set_name == 'book-crossing':
        data_set = data_set.ix[data_set['Book-Rating'] != 0]
    print(data_set.head())
    with open(os.path.join(os.path.dirname(__file__), 'neural-net.json')) as config_file:
        config = json.load(config_file)
    movie_estimator = estimator.Estimator(config, data_set)
    error = movie_estimator.estimate(specs['test_size'], config['batch_size'], config['learning_rate'])
    print('testing_error =', error)

if __name__ == '__main__':
    main('book-crossing')
    main('movie-lens-1m')
