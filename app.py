import pickle
import streamlit as st
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import seaborn as sns
import io

# Load diabetes_model.pkl file
diabetes_model = pickle.load(open('diabetes_model.pkl', 'rb'))

# Initialize session state for diabetic status
if 'diabetic' not in st.session_state:
    st.session_state['diabetic'] = False
    st.session_state['features'] = None  # To store the input features
    st.session_state['feature_importance'] = None  # To store the importance of features

# Function to save plot as image
def save_plot_as_image(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    return buf

# Sidebar for navigation
with st.sidebar:
    selected = option_menu('Diabetes Prediction System',
                          ['Diabetes Prediction', 'Graphs/Charts'],
                          icons=['activity', 'bar-chart'],
                          default_index=0)

# Function to set title with color
def colored_title(title, color):
    st.markdown(f"<h1 style='color:{color};'>{title}</h1>", unsafe_allow_html=True)

# Diabetes Prediction Page
if selected == 'Diabetes Prediction':
    
    # Page title
    st.title('Predicting Diabetes Onset using ML')
    
    # Getting the input data from the user
    col1, col2, col3 = st.columns(3)
    
    with col1:
        Pregnancies = st.text_input('Number of Pregnancies', help="Enter the number of times the patient has been pregnant.")
        
    with col2:
        Glucose = st.text_input('Glucose Level', help="Enter the plasma glucose concentration measured two hours after an oral glucose tolerance test.")
    
    with col3:
        BloodPressure = st.text_input('Blood Pressure value', help="Enter the diastolic blood pressure value in mm Hg. This is the blood pressure when the heart is resting between beats.")
    
    with col1:
        SkinThickness = st.text_input('Skin Thickness value', help="Enter the thickness of the triceps skin fold in mm. This value helps in estimating body fat.")
    
    with col2:
        Insulin = st.text_input('Insulin Level', help="Enter the 2-hour serum insulin level in mu U/ml. This helps in assessing insulin production and resistance.")
    
    with col3:
        BMI = st.text_input('BMI value', help="Enter the Body Mass Index (BMI) value, calculated as weight in kg divided by the square of height in meters. It indicates body fat and health risk.")
    
    with col1:
        DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function value', help="Enter the diabetes pedigree function value, a measure of the genetic risk of diabetes based on family history.")
    
    with col2:
        Age = st.text_input('Age of the Person', help="Enter the age of the patient in years. This value should be a whole number.")
    
    # Code for Prediction
    diab_diagnosis = ''

    # Creating a button for Prediction
    if st.button('Diabetes Test Result'):
        with st.spinner('Predicting...'):
            # Check if all fields are filled
            if Pregnancies == '' or Glucose == '' or BloodPressure == '' or SkinThickness == '' or Insulin == '' or BMI == '' or DiabetesPedigreeFunction == '' or Age == '':
                st.warning('Please fill in all the input fields to get an accurate prediction.')
            else:
                # Perform prediction
                diab_prediction = diabetes_model.predict([[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]])
                st.session_state['features'] = {
                    'Pregnancies': float(Pregnancies),
                    'Glucose': float(Glucose),
                    'Blood Pressure': float(BloodPressure),
                    'Skin Thickness': float(SkinThickness),
                    'Insulin': float(Insulin),
                    'BMI': float(BMI),
                    'Diabetes Pedigree Function': float(DiabetesPedigreeFunction),
                    'Age': float(Age)
                }
                st.session_state['diabetic'] = (diab_prediction[0] == 1)
                if st.session_state['diabetic']:
                    diab_diagnosis = 'The person is diabetic'
                else:
                    diab_diagnosis = 'The person is not diabetic'
    st.write(diab_diagnosis)
    st.info('Please fill in all the input fields with the appropriate values to get an accurate prediction.', icon="ℹ️")

# Graphs/Charts Page
if selected == 'Graphs/Charts':
    
    # Page title with color
    colored_title('Diabetes Predictions Charts/Graphs', '#007bff')  # Adjust color as needed
    
    # Warning to make predictions first
    st.warning('Please make a prediction on the Diabetes Prediction page before viewing charts here.')
    
    # Check if the user has made predictions
    if st.session_state['features']:
        features = st.session_state['features']
        feature_names = list(features.keys())
        feature_values = list(features.values())
        
        # Calculate feature importance based on input values (for demonstration)
        feature_importance = dict(zip(feature_names, feature_values))
        
        # Sort features by their importance (in this case, just their values)
        sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
        sorted_feature_names, sorted_feature_values = zip(*sorted_features)

        # Display charts in single column layout
        st.write("### Feature Charts")

        # Bar chart for all features
        fig, ax = plt.subplots(figsize=(12, 8))
        color = 'red' if st.session_state['diabetic'] else 'green'
        ax.barh(sorted_feature_names, sorted_feature_values, color=color)
        ax.set_title('Feature Values' if st.session_state['diabetic'] else 'Feature Values for Non-Diabetic Case')
        ax.set_xlabel('Value')
        ax.set_ylabel('Feature')
        plt.tight_layout()  # Ensure layout is tight
        st.pyplot(fig)  # Display the chart
        
        # Save bar chart as image
        bar_chart_image = save_plot_as_image(fig)
        st.download_button(label='Download Bar Chart', data=bar_chart_image, file_name='bar_chart.png', mime='image/png')

        # Pie chart for feature distribution with improved readability
        fig, ax = plt.subplots(figsize=(12, 12))
        explode = [0.1] * len(sorted_feature_values)  # Highlight all slices equally
        wedges, texts, autotexts = ax.pie(
            sorted_feature_values, 
            labels=sorted_feature_names, 
            autopct='%1.1f%%', 
            colors=sns.color_palette('pastel'),
            startangle=140,
            explode=explode
        )
        
        # Improve readability
        plt.setp(autotexts, size=10, weight="bold")
        plt.setp(texts, size=12)
        ax.set_title('Feature Distribution' if st.session_state['diabetic'] else 'Feature Distribution for Non-Diabetic Case')
        plt.tight_layout()  # Ensure layout is tight
        st.pyplot(fig)  # Display the pie chart
        
        # Save pie chart as image
        pie_chart_image = save_plot_as_image(fig)
        st.download_button(label='Download Pie Chart', data=pie_chart_image, file_name='pie_chart.png', mime='image/png')

        # Display detailed feature values below the charts
        st.write("### Detailed Feature Values:")
        for name, value in zip(sorted_feature_names, sorted_feature_values):
            st.write(f"- {name}: {value:.2f}")

        # Social media sharing with icons
        st.markdown("""
            ### Share your results!
            <a href="https://twitter.com/intent/tweet?text=Check%20out%20my%20diabetes%20prediction%20results%20with%20Streamlit%20app!%20%23DiabetesPrediction%20%23Streamlit" target="_blank">
            <img src="https://img.icons8.com/ios-filled/50/000000/twitter.png" alt="Twitter" style="vertical-align:middle; width: 30px; height: 30px;"/></a>
            <a href="https://www.facebook.com/sharer/sharer.php?u=your_app_url" target="_blank">
            <img src="https://img.icons8.com/ios-filled/50/000000/facebook.png" alt="Facebook" style="vertical-align:middle; width: 30px; height: 30px;"/></a>
            <a href="https://www.linkedin.com/sharing/share-offsite/?url=your_app_url" target="_blank">
            <img src="https://img.icons8.com/ios-filled/50/000000/linkedin.png" alt="LinkedIn" style="vertical-align:middle; width: 30px; height: 30px;"/></a>
            <a href="https://wa.me/?text=Check%20out%20my%20diabetes%20prediction%20results%20with%20Streamlit%20app!%20%23DiabetesPrediction%20%23Streamlit" target="_blank">
            <img src="https://img.icons8.com/ios-filled/50/000000/whatsapp.png" alt="WhatsApp" style="vertical-align:middle; width: 30px; height: 30px;"/></a>
        """, unsafe_allow_html=True)
        
    else:
        st.warning('No prediction data available. Please make a prediction first.')
