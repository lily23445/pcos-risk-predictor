import streamlit as st
import pandas as pd
import pickle
import sklearn

st.title("PCOS Risk Input Form")

model = pickle.load(open("pcos_model.pkl", "rb"))

age = st.number_input("Age (years)", min_value=10, max_value=60, value=25)
bmi = st.number_input("BMI", min_value=10.0, max_value=50.0, value=22.0)
cycle_length = st.number_input("Cycle Length (days)", min_value=15, max_value=60, value=28)

weight_gain = st.radio("Weight gain", ["No", "Yes"])
hair_growth = st.radio("Hair growth", ["No", "Yes"])
skin_darkening = st.radio("Skin darkening", ["No", "Yes"])
pimples = st.radio("Pimples", ["No", "Yes"])
hair_loss = st.radio("Hair loss", ["No", "Yes"])

fast_food = st.radio("Fast food consumption", ["No", "Yes"])
exercise = st.radio("Regular Exercise", ["No", "Yes"])

tsh = st.number_input("TSH (mIU/L)", min_value=0.0, max_value=10.0, value=2.0)
lh = st.number_input("LH (mIU/mL)", min_value=0.0, max_value=50.0, value=5.0)
fsh = st.number_input("FSH (mIU/mL)", min_value=0.0, max_value=50.0, value=6.0)
amh = st.number_input("AMH (ng/mL)", min_value=0.0, max_value=15.0, value=3.0)
prl = st.number_input("PRL (ng/mL)", min_value=0.0, max_value=100.0, value=20.0)

def yn_to_num(val):
    return 1 if val == "Yes" else 0

if st.button("Predict Risk"):
    data = {
        " Age (yrs)": age,
        "BMI": bmi,
        "TSH (mIU/L)": tsh,
        "LH(mIU/mL)": lh,
        "FSH(mIU/mL)": fsh,
        "AMH(ng/mL)": amh,
        "PRL(ng/mL)": prl,
        "Weight gain(Y/N)": yn_to_num(weight_gain),
        "hair growth(Y/N)": yn_to_num(hair_growth),  # note lowercase "hair"
        "Skin darkening (Y/N)": yn_to_num(skin_darkening),
        "Pimples(Y/N)": yn_to_num(pimples),
        "Hair loss(Y/N)": yn_to_num(hair_loss)
    }

    input_df = pd.DataFrame([data])

    input_df = pd.DataFrame([data])

    risk = model.predict_proba(input_df)[:, 1][0]
    st.write(f"PCOS Risk Score: {risk*100:.2f}%")

    if risk > 0.7:
        st.error("High Risk – Consult a doctor.")
    elif risk > 0.4:
        st.warning("Moderate Risk – Monitor symptoms.")
    else:
        st.success("Low Risk – Maintain healthy habits.")
