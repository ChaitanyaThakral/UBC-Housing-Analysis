from flask import Flask, request, render_template
import joblib
import os
import pandas as pd
import xgboost as xgb

app = Flask(__name__)

model_trend = "models/linear_trend_model.pkl"
model_residual = "models/xgb_residual_model.pkl"
model_features = "models/feature_names.pkl"

list_model = [model_trend, model_residual , model_features] 

for file in list_model :
    if os.path.exists(file):
        continue
    else:
        print(file,"Does not exist")
        exit()

model_trend_loaded = joblib.load(model_trend)
model_residual_loaded = joblib.load(model_residual)
model_features_loaded = joblib.load(model_features)

def make_input_frame(year, room_type, zone, features):
    
    df = pd.DataFrame(columns=features)  
    df.loc[0, "year"] = year  

    
    room_col = f"room_type_{room_type}"
    if room_col in features:
        df.loc[0, room_col] = 1

    
    zone_col = f"zone_{zone}"
    if zone_col in features:
        df.loc[0, zone_col] = 1

    
    df = df.fillna(0).astype("float64")
    return df


@app.route("/",methods = ["GET","POST"])
def predict():
    predicted_rent = None
    if request.method == "POST":
        year = int(request.form["Year"])
        room_type = request.form["RoomType"]
        zone = request.form["Zone"]

        input = make_input_frame(year , room_type , zone , model_features_loaded)

        linear_prediction = model_trend_loaded.predict(input)[0]

        matrix_xgb = xgb.DMatrix(input)
        xgb_residual_prediction = model_residual_loaded.predict(matrix_xgb)[0]

        final_prediction = linear_prediction + xgb_residual_prediction
        predicted_rent = round(float(final_prediction), 3)

       
    return render_template("index.html", predicted_rent=predicted_rent)

@app.route("/about")
def about():
    return render_template("aboutRentWise.html")

@app.route("/how-it-works")
def how():
    return render_template("HowItWorks.html")


if __name__ == "__main__":
    app.run(debug=True)

