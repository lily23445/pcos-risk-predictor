# app.py
import streamlit as st
import pandas as pd
import os
import pickle
from datetime import date

# Load model
model = pickle.load(open("pcos_model.pkl", "rb"))

st.title("🩺 PCOS 30-Day Symptom Tracker")

# File to store daily data
DATA_FILE = "user_30_day_data.csv"

# Input form
st.subheader("Day-wise Symptom Entry")
with st.form("daily_form"):
    st.markdown("### Fill today's details")

    age = st.number_input("Age (yrs)", min_value=10, max_value=60)
    bmi = st.number_input("BMI", min_value=10.0, max_value=60.0)
    tsh = st.number_input("TSH (mIU/L)", min_value=0.0)
    lh = st.number_input("LH (mIU/mL)", min_value=0.0)
    fsh = st.number_input("FSH (mIU/mL)", min_value=0.0)
    amh = st.number_input("AMH (ng/mL)", min_value=0.0)
    prl = st.number_input("PRL (ng/mL)", min_value=0.0)

    wg = st.selectbox("Weight Gain (Y/N)", ["0", "1"])
    hg = st.selectbox("Hair Growth (Y/N)", ["0", "1"])
    sd = st.selectbox("Skin Darkening (Y/N)", ["0", "1"])
    pimples = st.selectbox("Pimples (Y/N)", ["0", "1"])
    hair_loss = st.selectbox("Hair Loss (Y/N)", ["0", "1"])

    submitted = st.form_submit_button("Submit")

if submitted:
    today = str(date.today())

    entry = {
        "Date": today,
        "Age": age,
        "BMI": bmi,
        "TSH": tsh,
        "LH": lh,
        "FSH": fsh,
        "AMH": amh,
        "PRL": prl,
        "Weight gain(Y/N)": wg,
        "hair growth(Y/N)": hg,
        "Skin darkening (Y/N)": sd,
        "Pimples(Y/N)": pimples,
        "Hair loss(Y/N)": hair_loss,
    }

    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        if today in df["Date"].values:
            st.warning("You’ve already submitted data for today!")
        else:
            df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("Entry submitted successfully!")
    else:
        df = pd.DataFrame([entry])
        df.to_csv(DATA_FILE, index=False)
        st.success("Entry submitted successfully!")

if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    st.info(f"🗓️ Days logged: {df.shape[0]}/30")

    if df.shape[0] == 30:
        st.success("✅ You've completed 30 days! Generating prediction...")

        # Drop date column
        df_features = df.drop("Date", axis=1)

        # Convert all to numeric (if not already)
        df_features = df_features.apply(pd.to_numeric)

        # Option 1: Use average values across 30 days
        input_vector = df_features.mean().values.reshape(1, -1)

        prediction = model.predict(input_vector)[0]
        score = model.predict_proba(input_vector)[0][1]

        st.markdown(f"### 🧠 Model Prediction: {'Positive' if prediction == 1 else 'Negative'}")
        st.markdown(f"**Confidence Score:** {score:.2f}")

        # Risk interpretation
        if score > 0.7:
            st.error("⚠️ **High risk of PCOS. Please consult a gynecologist.**")
        elif score > 0.5:
            st.warning("🟠 **Moderate risk. Keep tracking symptoms and consider medical advice.**")
        else:
            st.success("🟢 **Low risk. PCOS is unlikely based on your data.**")

        if st.button("Clear and Restart Tracking"):
            os.remove(DATA_FILE)
            st.info("Tracker reset. You can start logging again.")
