# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['time_robust_forest']

package_data = \
{'': ['*']}

install_requires = \
['click==8.1.3',
 'numpy==1.23.0',
 'pandas==1.1.3',
 'rich>=9.8.2,<11.0.0',
 'scikit-learn==1.1.0',
 'typer[all]>=0.5.0,<0.6.0']

extras_require = \
{':python_version <= "3.9.12"': ['importlib_metadata>=1.6,<5.0']}

entry_points = \
{'console_scripts': ['time-robust-forest = time_robust_forest.__main__:app']}

setup_kwargs = {
    'name': 'time-robust-forest',
    'version': '0.1.14',
    'description': 'Explores time information to train a robust random forest',
    'long_description': '# time-robust-forest\n\n<div align="center">\n\n[![Build status](https://github.com/lgmoneda/time-robust-forest/workflows/build/badge.svg?branch=main&event=push)](https://github.com/lgmoneda/time-robust-forest/actions?query=workflow%3Abuild)\n[![Python Version](https://img.shields.io/pypi/pyversions/time-robust-forest.svg)](https://pypi.org/project/time-robust-forest/)\n[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/lgmoneda/time-robust-forest/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)\n[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/lgmoneda/time-robust-forest/blob/main/.pre-commit-config.yaml)\n[![Semantic Versions](https://img.shields.io/badge/%F0%9F%9A%80-semantic%20versions-informational.svg)](https://github.com/lgmoneda/time-robust-forest/releases)\n[![License](https://img.shields.io/github/license/lgmoneda/time-robust-forest)](https://github.com/lgmoneda/time-robust-forest/blob/main/LICENSE)\n\n</div>\n\nA Proof of concept model that explores timestamp information to train a random forest with better Out of Distribution generalization power.\n\n## Installation\n\n```bash\npip install -U time-robust-forest\n```\n\n## How to use it\n\nThere are a classifier and a regressor under `time_robust_forest.models`. They follow the sklearn interface, which means you can quickly fit and use a model:\n\n```python\nfrom time_robust_forest.models import TimeForestClassifier\n\nfeatures = ["x_1", "x_2"]\ntime_column = "periods"\ntarget = "y"\n\nmodel = TimeForestClassifier(time_column=time_column)\n\nmodel.fit(training_data[features + [time_column]], training_data[target])\npredictions = model.predict_proba(test_data[features])[:, 1]\n```\n\nThere are only a few arguments that differ from a traditional Random Forest. two arguments\n\n- time_column: the column from the input dataframe containing the time\nperiods the model will iterate over to find the best splits (default: "period")\n- min_sample_periods: the number of examples in every period the model needs\nto keep while it splits.\n- period_criterion: how the performance in every period is going to be\naggregated. Options: {"avg": average, "max": maximum, the worst case}.\n(default: "avg")\n\nTo use the environment-wise optimization:\n\n```python\nfrom time_robust_forest.hyper_opt import env_wise_hyper_opt\n\nparams_grid = {"n_estimators": [30, 60, 120],\n              "max_depth": [5, 10],\n              "min_impurity_decrease": [1e-1, 1e-3, 0],\n              "min_sample_periods": [5, 10, 30],\n              "period_criterion": ["max", "avg"]}\n\nmodel = TimeForestClassifier(time_column=time_column)\n\nopt_param = env_wise_hyper_opt(training_data[features + [time_column]],\n                               training_data[TARGET],\n                               model,\n                               time_column,\n                               params_grid,\n                               cv=5,\n                               scorer=make_scorer(roc_auc_score,\n                                                  needs_proba=True))\n\n```\n\n### Make sure you have a good choice for the time column\n\nDon\'t simply use a timestamp column from the dataset, make it discrete before and guarantee there is a reasonable amount of data points in every period. Example: use year if you have 3+ years of data. Notice the choice to make it discrete becomes a modeling choice you can optimize.\n\n### Random segments\n\n#### Selecting randomly from multiple time columns\nThe user can use a list instead of a string as the `time_column` argument. The model will select randomly from it when building every estimator from the defined `n_estimators`.\n\n```python\nfrom time_robust_forest.models import TimeForestClassifier\n\nfeatures = ["x_1", "x_2"]\ntime_columns = ["periods", "periods_2"]\ntarget = "y"\n\nmodel = TimeForestClassifier(time_column=time_columns)\n\nmodel.fit(training_data[features + time_columns], training_data[target])\npredictions = model.predict_proba(test_data[features])[:, 1]\n```\n\n#### Generating random segments from a timestamp column\n\nThe user can define a maximum number of segments (`random_segments`) and the model will split the data using the time stamp information. In the following example, the model segments the data in 1, 2, 3... 10 parts. For every estimator, it picks randomly one of the ten columns representing the `time_column` and use it. In this case, the `time_column` should be the time stamp information.\n\n```python\nfrom time_robust_forest.models import TimeForestClassifier\n\nfeatures = ["x_1", "x_2"]\ntime_column = "time_stamp"\ntarget = "y"\n\nmodel = TimeForestClassifier(time_column=time_column, random_segments=10)\n\nmodel.fit(training_data[features + [time_column]], training_data[target])\npredictions = model.predict_proba(test_data[features])[:, 1]\n```\n\n## License\n\n[![License](https://img.shields.io/github/license/lgmoneda/time-robust-forest)](https://github.com/lgmoneda/time-robust-forest/blob/main/LICENSE)\n\nThis project is licensed under the terms of the `BSD-3` license. See [LICENSE](https://github.com/lgmoneda/time-robust-forest/blob/main/LICENSE) for more details.\n\n## Useful links\n\n- [Introducing the Time Robust Tree blog post](http://lgmoneda.github.io/2021/12/03/introducing-time-robust-tree.html)\n\n## Citation\n\n```\n@misc{time-robust-forest,\n  author = {Moneda, Luis},\n  title = {Time Robust Forest model},\n  year = {2021},\n  publisher = {GitHub},\n  journal = {GitHub repository},\n  howpublished = {\\url{https://github.com/lgmoneda/time-robust-forest}}\n}\n```\n',
    'author': 'lgmoneda',
    'author_email': 'lgmoneda@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lgmoneda/time-robust-forest',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9.12,<4.0.0',
}


setup(**setup_kwargs)
