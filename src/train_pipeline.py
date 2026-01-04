import joblib
from sklearn.pipeline import Pipeline


def save_pipeline(pipeline: Pipeline, path: str) -> None:
    joblib.dump(pipeline, path)


def load_pipeline(path: str) -> Pipeline:
    return joblib.load(path)