import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

# Load saved assets
model = joblib.load('Models/battery_soh_model.pkl')
scaler = joblib.load('Models/scaler.pkl')

st.title("EV Battery Health Advisor")
st.markdown("Use this tool to predict the state of health for lithium-ion packs.")

# Sidebar inputs
st.sidebar.header("Input Sensor Data")
cycle = st.sidebar.number_input("Cycle Number", 0)
voltage = st.sidebar.number_input("Voltage (V)", 0.0)
current = st.sidebar.number_input("Current (A)", 0.0)
temp = st.sidebar.number_input("Temperature (°C)", 0.0)

# Prediction Logic
if st.button("Calculate SOH"):
    input_data = pd.DataFrame([[cycle, voltage, current, temp]], 
                              columns=['cycle_number', 'voltage', 'current', 'temperature'])
    
    # Scale and predict
    input_scaled = scaler.transform(input_data)
    prediction = model.predict(input_scaled)[0]
    
    # Display results
    st.metric("Predicted SOH", f"{prediction:.2f}%")
    
    if prediction < 80:
        st.error("Battery performance below threshold. Recommend: Second-life transition.")
    else:
        st.success("Battery is within operational limits.")
# show context
st.subheader("Degradation Trend")
# Create a dummy dataframe representing the expected degradation curve
trend_data = pd.DataFrame({
    'Cycle': range(0, 1000, 50),
    'Expected_SOH': [100 - (i * 0.05) for i in range(0, 1000, 50)]
})

# Highlight where the current prediction sits on that curve
fig = px.line(trend_data, x='Cycle', y='Expected_SOH', title="Battery Life Degradation Curve")
fig.add_scatter(x=[cycle], y=[prediction], mode='markers', name='Your Battery', marker=dict(size=12, color='red'))

st.plotly_chart(fig)
