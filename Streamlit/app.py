import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

# Load your saved assets (ensure these are in a folder named 'model_files')
model = joblib.load('Models/battery_soh_model.pkl')
scaler = joblib.load('Models/scaler.pkl')

st.set_page_config(page_title="EV Battery Health Advisor", layout="wide")

st.title("🔋 EV Battery Health Advisor")
st.markdown("### Prototyping Circular Economy Solutions for Automotive")

# Sidebar for User Inputs
st.sidebar.header("Input Sensor Data")
cycle = st.sidebar.number_input("Cycle Number", min_value=0, value=100)
voltage = st.sidebar.number_input("Voltage (V)", min_value=0.0, value=3.7)
current = st.sidebar.number_input("Current (A)", min_value=0.0, value=1.5)
temp = st.sidebar.number_input("Temperature (°C)", min_value=0.0, value=25.0)

# Prediction Logic
if st.button("Calculate State of Health (SOH)"):
    # Create DataFrame for prediction
    input_data = pd.DataFrame([[cycle, voltage, current, temp]], 
                              columns=['cycle_number', 'voltage', 'current', 'temperature'])
    
    # Scale and predict
    input_scaled = scaler.transform(input_data)
    prediction = model.predict(input_scaled)[0]
    
    # Display Result
    col1, col2 = st.columns(2)
    col1.metric("Predicted SOH", f"{prediction:.2f}%")
    
    if prediction < 80:
        col2.error("Status: Degraded (Repurpose for Storage)")
    else:
        col2.success("Status: Healthy (Vehicle Use)")

    # Data Visualization
    st.subheader("Battery Degradation Analysis")
    
    # Create dummy trend data for visualization purposes
    trend_data = pd.DataFrame({
        'Cycle': range(0, 1000, 50),
        'Expected_SOH': [100 - (i * 0.05) for i in range(0, 1000, 50)]
    })
    
    # Generate the line chart
    fig = px.line(trend_data, x='Cycle', y='Expected_SOH', title="Degradation Trend Line")
    
    # Add the current battery's position
    fig.add_scatter(x=[cycle], y=[prediction], mode='markers', 
                    name='Current Battery State', marker=dict(size=14, color='red'))
    
    st.plotly_chart(fig, use_container_width=True)
