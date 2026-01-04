import numpy as np
import joblib
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from src.train_pipeline import save_pipeline, load_pipeline  # Updated import


def test_pipeline_predict_shape(tmp_path):
    X = np.array([[0, 1], [1, 0], [1, 1]])
    y = np.array([0, 1, 1])

    pipe = Pipeline([("clf", LogisticRegression(max_iter=200))])
    pipe.fit(X, y)

    model_path = tmp_path / "model.pkl"
    save_pipeline(pipe, model_path)  # Use new function

    loaded = load_pipeline(model_path)  # Use new function
    preds = loaded.predict(X)

    assert len(preds) == len(X)