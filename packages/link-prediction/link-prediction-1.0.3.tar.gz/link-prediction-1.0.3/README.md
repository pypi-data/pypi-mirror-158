# Link Prediction

_Link Prediction_ is a Python module that provides baseline models to predict links between the screens of smartphone applications.

1. It provides a heuristically constructed set of link data based on the [RICO dataset](https://interactionmining.org/rico).
2. It provides several heuristic and learning-based link prediction models that can be used using with hierarchical screen data.

## Requirements

Link Prediction is known to work with Python 3.10.3 and above.

## Installing

You can install the package using pip with the following command:

```Shell

pip install link-prediction

```

You can them import the necessary packages from `link_prediction`.

## Quickstart

Typically, link prediction involves (1) loading some screen data, (2) loading a pre-trained link prediction model and (3) predicting a link (or score) for a potential link from that data.

```Python
# Imports
from link_prediction.datasets import load_rico_links
import joblib

# Load some data
X = load_rico_links()

# Load a (pre-trained) model
model = "PageContainsLabel"
clf = joblib.load(f"models/{model}Classifier.joblib")

# Predict labels and scores
y_pred = clf.predict(X)
y_score = clf.decision_function(X)
```

There is also a CLI for simplified use:

```Shell
$ python3 -m link-prediction --source-screen path/to/view_hierarchy/324.json --source-element 76d99c7 --target-screen path/to/view_hierarchy/339.json --model PageContainsLabel
```

## Contributors

Christoph A. Johns
