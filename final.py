import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

# Load real and predicted data
real_data = pd.read_excel('Company stock prices.xlsx')
predicted_data = pd.read_csv('predicted_values.csv')

# Convert the 'Date' column to datetime
real_data['Date'] = pd.to_datetime(real_data['Date'])
predicted_data['Date'] = pd.to_datetime(predicted_data['Date'])

# Creating a Streamlit app
st.title('Stock Price Prediction :chart:')
input_date = st.date_input("Enter a date:", pd.Timestamp('2023-10-17'))

# Convert the input date to a pd.Timestamp
input_date = pd.Timestamp(input_date)

# Define the date range for real data
real_data_start_date = pd.Timestamp('2020-10-19')
real_data_end_date = pd.Timestamp('2023-10-16')

# Define the date range for predicted data
predicted_data_start_date = pd.Timestamp('2023-10-17')
predicted_data_end_date = pd.Timestamp('2024-01-24')

# Plot the combined data
if real_data_start_date <= input_date <= predicted_data_end_date:
    real_data_filtered = real_data[real_data['Date'] <= input_date]
    predicted_data_filtered = predicted_data[predicted_data['Date'] <= input_date]
    
    if not real_data_filtered.empty or not predicted_data_filtered.empty:
        fig_combined = px.line(title='Combined Stock Prices')

        if not real_data_filtered.empty:
            fig_combined.add_scatter(x=real_data_filtered['Date'], y=real_data_filtered['Close'], mode='lines', name='Real Data')
            # Include the input date if it exists in real data
            if input_date in real_data['Date'].values:
                input_price_real = real_data.loc[real_data['Date'] == input_date, 'Close'].iloc[0]
                fig_combined.add_scatter(x=[input_date], y=[input_price_real], mode='markers', name='Input Date (Real Data)')
                
                # Display the stock price value for the input date in real data
                st.write(f"Stock price value on {input_date.strftime('%Y-%m-%d')} (Real Data) is: {input_price_real}")

        if not predicted_data_filtered.empty:
            fig_combined.add_scatter(x=predicted_data_filtered['Date'], y=predicted_data_filtered['Close'], mode='lines', name='Predicted Data')
            # Include the input date if it exists in predicted data
            if input_date in predicted_data['Date'].values:
                input_price_predicted = predicted_data.loc[predicted_data['Date'] == input_date, 'Close'].iloc[0]
                fig_combined.add_scatter(x=[input_date], y=[input_price_predicted], mode='markers', name='Input Date (Predicted Data)')
                
                # Display the stock price value for the input date in predicted data
                st.write(f"Stock price value on {input_date.strftime('%Y-%m-%d')} (Predicted Data) is: {input_price_predicted}")

        st.plotly_chart(fig_combined)
else:
    st.write("No data available for the selected date. Please choose a date within the range of 19-10-2020 to 24-01-2024.")
