import streamlit as st, json
import pandas as pd
from utils import predict_price, get_currency, CURRENCY_MAPPING

# Page Config
st.set_page_config(
    page_title="Laptop Price Prediction",
    page_icon="💻",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.title("Laptop Price Prediction 🖥️")
st.write("This app predicts the price of a laptop based on its specifications.")

# Sidebar
st.sidebar.header("⚙️ Options")
data_input_method = st.sidebar.radio("Select data input method", options=["Manual", "Upload JSON"])
currency = st.sidebar.selectbox("Select Currency", options=[f"{k} - {v}" for k,v in CURRENCY_MAPPING.items()], index=0)

# Author Details
st.sidebar.markdown("---")
st.sidebar.markdown("## Author Details")
st.sidebar.markdown("**Name: Bhallamudi Sai Narasimha Abhiram**")
st.sidebar.markdown("Email: abhirambsn@gmail.com")
st.sidebar.markdown("GitHub: [@abhirambsn](https://github.com/abhirambsn)")
st.sidebar.markdown("LinkedIn: [@bhallamudi-sai-narasimha-abhiram](https://www.linkedin.com/in/bhallamudi-sai-narasimha-abhiram/)")

# Change Page by data_input_method
if data_input_method == "Manual":
    st.write("You have selected manual data input method.")
    
    data = {
        "Product Name": "", 
        "Processor Brand": "", 
        "Processor Speed": 0.0,
        "Processor Count": 0, 
        "RAM Size": 0, 
        "Memory Clock Speed": 0.0, 
        "Hard Drive Size": 0,
        "Operating System": "",
        "GraphicsCardRAM": 0.0,
        "Number of HDMI Ports": 0,
        "BatteryLife": 0.0,
        "Display Type": "",
        "is_SSD": 0,
        "HeadphoneJack": 0,
        "DedicatedGraphics": 0,
        "Fingerprint": 0,
        "BacklitKeyboard": 0,
        "RGBKeyboard": 0,
        "SoftwareIncluded": 0,
        "AdditionalInput": 0,
        "USB_Ports": 0,
        "Resolution Type": ""
    }
    
    # Create Inputs for all features as above
    # Example:
    product_name = st.text_input("Product Name")
    processor_brand = st.selectbox("Processor Brand", options=["Intel", "AMD", "Other"], index=0)
    processor_speed = st.number_input("Processor Speed (in GHz)", min_value=0.0, max_value=5.0)
    processor_count = st.number_input("Processor Count", min_value=0, max_value=64)
    ram = st.number_input("RAM Size (in GB)", min_value=0, step=1, max_value=64)
    memory_clock_speed = st.number_input("Memory Clock Speed (in GHz)", min_value=0.0, step=0.1, max_value=5.0)
    storage = st.number_input("Hard Drive Size", min_value=0, max_value=2048)
    operating_system = st.selectbox("Operating System", options=["Windows", "MacOS", "Linux", "ChromeOS"], index=0)
    graphics_card = st.number_input("Graphics Card RAM (in GB)", min_value=0.0, step=0.1, max_value=32.0)
    hdmi_ports = st.number_input("Number of HDMI Ports", min_value=0, step=1, max_value=32)
    battery_life = st.number_input("Battery Life (in Hours)", min_value=0.0, step=0.5, max_value=24.0)
    display_type = st.selectbox("Display Type", options=["LCD", "LED", "OLED", "AMOLED"], index=0)
    is_ssd = st.checkbox("Is SSD?")
    headphone_jack = st.checkbox("Headphone Jack?")
    dedicated_graphics = st.checkbox("Dedicated Graphics?")
    fingerprint = st.checkbox("Fingerprint?")
    backlit_keyboard = st.checkbox("Backlit Keyboard?")
    rgb_keyboard = st.checkbox("RGB Keyboard?")
    software_included = st.checkbox("Software Included?")
    additional_input = st.checkbox("Additional Input?")
    usb_ports = st.number_input("USB Ports", min_value=0, step=1, max_value=32)
    resolution_type = st.selectbox("Resolution Type", options=["HD", "FHD", "2k", "4k", "8k"], index=0)

    submit_button = st.button("Submit")

    if submit_button:
        # Add all features to data dictionary as above
        # Example:
        data["Product Name"] = product_name
        data["Processor Brand"] = processor_brand
        data["Processor Speed"] = processor_speed
        data["Processor Count"] = processor_count
        data["RAM Size"] = ram
        data["Memory Clock Speed"] = memory_clock_speed
        data["Hard Drive Size"] = storage
        data["Operating System"] = operating_system
        data["GraphicsCardRAM"] = graphics_card
        data["Number of HDMI Ports"] = hdmi_ports
        data["BatteryLife"] = battery_life
        data["Display Type"] = display_type
        data["is_SSD"] = int(is_ssd)
        data["HeadphoneJack"] = int(headphone_jack)
        data["DedicatedGraphics"] = int(dedicated_graphics)
        data["Fingerprint"] = int(fingerprint)
        data["BacklitKeyboard"] = int(backlit_keyboard)
        data["RGBKeyboard"] = int(rgb_keyboard)
        data["SoftwareIncluded"] = int(software_included)
        data["AdditionalInput"] = int(additional_input)
        data["USB_Ports"] = usb_ports
        data["Resolution Type"] = resolution_type
        
        prediction = predict_price(data, get_currency(currency))
        markdown_price_template = """#### Predicted Price: {} {}"""
        st.markdown(markdown_price_template.format(get_currency(currency), prediction))

elif data_input_method == "Upload JSON":
    st.write("You have selected JSON file upload data input method.")
    # Add your code here for JSON file upload data input method
    # Code to upload json file
    file = st.file_uploader("Upload JSON", type=["json"])
    if file is not None:
        fileData = json.loads(file.read())
        st.markdown("#### Uploaded Data")

        if isinstance(fileData, list):
            st.table(pd.DataFrame(fileData))
        else:
            st.table(pd.DataFrame([fileData]).T)

        submit = st.button("Predict Price")
        if submit:
            prediction = predict_price(fileData, get_currency(currency))
            markdown_price_template = """#### Predicted Price: {} {}"""
            st.markdown(markdown_price_template.format(get_currency(currency), prediction))
else:
    st.write("Invalid data input method selected.")
