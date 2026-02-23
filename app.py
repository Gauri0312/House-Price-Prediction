import streamlit as st
import pandas as pd
import joblib

st.title("🏠 House Price Prediction")
st.write("If you see this, the app is running.")

# Load model safely AFTER rendering starts
@st.cache_resource
def load_model():
    return joblib.load("xgb_model.joblib")

try:
    model = load_model()
    st.success("Model loaded successfully")
except Exception as e:
    st.error(f"Model loading failed: {e}")
    st.stop()

features = [
    'OverallQual', 'GrLivArea', 'GarageArea', '1stFlrSF',
    'FullBath', 'YearBuilt', 'YearRemodAdd', 'MasVnrArea',
    'Fireplaces', 'BsmtFinSF1', 'LotFrontage',
    'WoodDeckSF', 'OpenPorchSF', 'LotArea', 'CentralAir'
]

input_data = {}

for feature in features:
    if feature == "CentralAir":
        input_data[feature] = st.selectbox("Central Air", ["Yes", "No"])
    else:
        input_data[feature] = st.number_input(feature, value=0.0)

if st.button("Predict"):

    input_data["CentralAir"] = 1 if input_data["CentralAir"] == "Yes" else 0
    input_df = pd.DataFrame([input_data])

    try:
        prediction = model.predict(input_df)
        st.success(f"Predicted Price: ₹ {prediction[0]:,.0f}")
    except Exception as e:
        st.error(f"Prediction failed: {e}")