from app.models.predictor import predict_from_csv

def process_prediction(df):
    return predict_from_csv(df)
