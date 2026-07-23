import joblib

from src.train import MODEL_PATH, main as train


def test_trained_model_predicts_a_valid_class() -> None:
    train()
    model = joblib.load(MODEL_PATH)
    assert model.predict([[5.1, 3.5, 1.4, 0.2]])[0] in (0, 1, 2)
