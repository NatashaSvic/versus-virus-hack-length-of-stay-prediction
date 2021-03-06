import numpy as np
import pandas as pd
from sklearn.feature_selection import SelectPercentile, f_regression
from sklearn.linear_model import LassoLarsCV, RidgeCV
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline, make_union
from sklearn.preprocessing import Normalizer, RobustScaler
from sklearn.tree import DecisionTreeRegressor
from tpot.builtins import StackingEstimator

# NOTE: Make sure that the outcome column is labeled 'target' in the data file
tpot_data = pd.read_csv('PATH/TO/DATA/FILE', sep='COLUMN_SEPARATOR', dtype=np.float64)
features = tpot_data.drop('target', axis=1)
training_features, testing_features, training_target, testing_target = \
            train_test_split(features, tpot_data['target'], random_state=None)

# Average CV score on the training set was: -4.811141924516791
exported_pipeline = make_pipeline(
    Normalizer(norm="l1"),
    SelectPercentile(score_func=f_regression, percentile=7),
    StackingEstimator(estimator=RidgeCV()),
    RobustScaler(),
    StackingEstimator(estimator=LassoLarsCV(normalize=False)),
    DecisionTreeRegressor(max_depth=3, min_samples_leaf=10, min_samples_split=7)
)

exported_pipeline.fit(training_features, training_target)
results = exported_pipeline.predict(testing_features)
