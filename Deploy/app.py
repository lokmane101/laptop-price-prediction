import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load your model
model = joblib.load('model.joblib')

# Define the options for the checkboxes
laptop_types = ["_Acer","_Apple","_Asus","_Dell","_Lenovo","_MSI","_Toshiba" ,"_Hp"]
graphique_types = ["Grapihque_AMD Graphique","Grapihque_Intel HD Graphics","Grapihque_Intel HD Graphics 400","Grapihque_Intel HD Graphics 520","Grapihque_Intel HD Graphics 530","Grapihque_Intel HD Graphics 620","Grapihque_Intel Iris","Grapihque_Nvidia  GTX","Grapihque_Nvidia  M","Grapihque_Nvidia  MX","Grapihque_Nvidia GeForce 920","Grapihque_Intel HD Graphiques","Grapihque_Intel UHD Graphics 620","Grapihque_Nvidia  Quadro","Grapihque_carte graphiques intégré"]

# Create a form
with st.form(key='my_form'):
    st.image('1_ejs8uD5aFnJaiDLwOO-khQ.jpg', use_column_width=True)
    st.title('Laptop Price Prediction')
    st.markdown('**Enter the specifications of your laptop below:**')
    ram = st.number_input('Enter the size of RAM (in GB)', step=1)
    weight = st.number_input('Enter WEIGHT (in KG)', step=1.0)
    stockage_ssd = st.number_input('Enter STOCKAGESSD (in GB)', step=1)
    stockage_hdd = st.number_input('Enter STOCKAGEHDD (in GB)', step=1)
    stockage_flash = st.number_input('Enter STOCKAGEFlash (in GB)', step=1)
    laptop_type = st.selectbox('Select Laptop Type', laptop_types)
    cpu_modifier = st.number_input('Enter CPU Modifier', step=1)
    cpu_generation = st.number_input('Enter CPU Generation', step=1)
    cpu_amd = st.checkbox('CPU_AMD')
    cpu_intel = not cpu_amd if cpu_amd else st.checkbox('CPU_Intel')
    graphique_type = st.selectbox('Select type of GPU', graphique_types)
    submit_button = st.form_submit_button(label='Predict')

# Make a prediction
if submit_button:
    data = {
        'RAM': [ram],
        'WEIGHT': [weight],
        'STOCKAGESSD': [stockage_ssd],
        'STOCKAGEHDD': [stockage_hdd],
        'STOCKAGEFlash': [stockage_flash]
    }
    data.update({type: [1] if type == laptop_type else [0] for type in laptop_types})
    data.update({
        'CPU_Modifier': [cpu_modifier],
        'CPU_Generation': [cpu_generation],
        'CPU_AMD': [cpu_amd],
        'CPU_Intel': [cpu_intel]
    })
    data.update({type: [1] if type == graphique_type else [0] for type in graphique_types})
    data_df = pd.DataFrame(data, columns=['RAM', 'WEIGHT', 'STOCKAGESSD', 'STOCKAGEHDD', 'STOCKAGEFlash', '_Acer', '_Apple', '_Asus', '_Dell', '_Lenovo', '_MSI', '_Toshiba', 'CPU_Modifier', 'CPU_Generation', 'CPU_AMD', 'CPU_Intel', 'Grapihque_AMD Graphique', 'Grapihque_Intel HD Graphics', 'Grapihque_Intel HD Graphics 400', 'Grapihque_Intel HD Graphics 520', 'Grapihque_Intel HD Graphics 530', 'Grapihque_Intel HD Graphics 620', 'Grapihque_Intel Iris', 'Grapihque_Nvidia  GTX', 'Grapihque_Nvidia  M', 'Grapihque_Nvidia  MX', 'Grapihque_Nvidia GeForce 920',  '_Hp', 'Grapihque_Intel HD Graphiques', 'Grapihque_Intel UHD Graphics 620', 'Grapihque_Nvidia  Quadro', 'Grapihque_carte graphiques intégré'])
    prediction = model.predict(data_df)
    st.success(f"The predicted price for the laptop with the given specifications is **{prediction[0]:.2f}MAD**  !")
