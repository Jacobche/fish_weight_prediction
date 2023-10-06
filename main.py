import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb
import numpy as np

# load data
@st.cache()
def load_data():
  data = pd.read_csv("https://raw.githubusercontent.com/Jacobche/fish_weight_prediction/main/Fish.csv")
  return data

# load label encoder
@st.cache()
def load_encoder():
  encoder = LabelEncoder()
  encoder.classes_ = np.load('classes.npy',allow_pickle=True)
  return encoder

# load model
@st.cache()
def load_model():
  best_xgboost_model = xgb.XGBRegressor()
  best_xgboost_model.load_model("best_model.json")
  return best_xgboost_model

# main app code
st.title("Fish Weight Prediction App")
st.text_input("Enter your Name: ", key="name")

data = load_data()
encoder = load_encoder()
best_xgboost_model = load_model()

if st.checkbox('Show Training Dataframe'):
  data

st.subheader("Please select relevant features of your fish!")
left_column, right_column = st.columns(2)
with left_column:
  inp_species = st.radio(
    'Name of the fish:',
    np.unique(data['Species']))


input_Length1 = st.slider('Vertical length(cm)', 0.0, max(data["Length1"]), 1.0)
input_Length2 = st.slider('Diagonal length(cm)', 0.0, max(data["Length2"]), 1.0)
input_Length3 = st.slider('Cross length(cm)', 0.0, max(data["Length3"]), 1.0)
input_Height = st.slider('Height(cm)', 0.0, max(data["Height"]), 1.0)
input_Width = st.slider('Diagonal width(cm)', 0.0, max(data["Width"]), 1.0)


if st.button('Make Prediction'):
  input_species = encoder.transform(np.expand_dims(inp_species, -1))
  inputs = np.expand_dims(
    [int(input_species), input_Length1, input_Length2, input_Length3, input_Height, input_Width], 0)
  prediction = best_xgboost_model.predict(inputs)
  print("final pred", np.squeeze(prediction, -1))
  st.write(f"Your fish weight is: {np.squeeze(prediction, -1):.2f}g")

  st.write(f"Thank you {st.session_state.name}! I hope you liked it.")
