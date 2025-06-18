import streamlit as st
import pandas as pd
import numpy as np
import pickle
import warnings
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
warnings.filterwarnings('ignore')

# Konfigurasi halaman
st.set_page_config(
    page_title="Student Dropout Prediction",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS untuk styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .prediction-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 1rem;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .stSelectbox > div > div > select {
        background-color: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model_safe():
    """Load model dengan berbagai metode untuk mengatasi pickle error"""
    model_path = 'saved_models/best_model.pkl'
    scaler_path = 'saved_models/scaler.pkl'
    class_names_path = 'saved_models/class_names.pkl'
    
    try:
        # Method 1: Normal pickle load
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        with open(scaler_path, 'rb') as f:
            scaler = pickle.load(f)
        with open(class_names_path, 'rb') as f:
            class_names = pickle.load(f)
        st.success("✅ Model loaded successfully with pickle")
        return model, scaler, class_names
        
    except Exception as e1:
        try:
            # Method 2: Load dengan encoding
            with open(model_path, 'rb') as f:
                model = pickle.load(f, encoding='latin-1')
            with open(scaler_path, 'rb') as f:
                scaler = pickle.load(f, encoding='latin-1')
            with open(class_names_path, 'rb') as f:
                class_names = pickle.load(f, encoding='latin-1')
            st.success("✅ Model loaded successfully with encoding")
            return model, scaler, class_names
            
        except Exception as e2:
            try:
                # Method 3: Load dengan joblib
                import joblib
                model = joblib.load(model_path)
                scaler = joblib.load(scaler_path)
                class_names = joblib.load(class_names_path)
                st.success("✅ Model loaded successfully with joblib")
                return model, scaler, class_names
                
            except Exception as e3:
                st.error(f"❌ Failed to load model: {e3}")
                return None, None, None

def predict_student(data_dict, model, scaler, class_names):
    """Prediksi dropout status mahasiswa"""
    try:
        # Buat DataFrame dari input
        df_input = pd.DataFrame([data_dict])
        
        # Scaling features
        df_scaled = scaler.transform(df_input)
        
        # Prediksi
        prediction = model.predict(df_scaled)[0]
        probabilities = model.predict_proba(df_scaled)[0]
        
        # Hasil
        predicted_label = class_names[prediction]
        confidence = probabilities[prediction]
        
        # Buat dictionary hasil
        result = {
            'prediction': predicted_label,
            'confidence': confidence,
            'probabilities': {}
        }
        
        # Tambahkan probabilitas semua kelas
        for i, class_name in enumerate(class_names):
            result['probabilities'][class_name] = probabilities[i]
        
        return result
        
    except Exception as e:
        st.error(f"❌ Error dalam prediksi: {e}")
        return None

def create_probability_chart(probabilities):
    """Buat chart probabilitas"""
    classes = list(probabilities.keys())
    probs = list(probabilities.values())
    
    fig = go.Figure(data=[
        go.Bar(
            x=classes,
            y=probs,
            text=[f'{p:.1%}' for p in probs],
            textposition='auto',
            marker_color=['#ff6b6b' if 'Dropout' in c else '#4ecdc4' for c in classes]
        )
    ])
    
    fig.update_layout(
        title="Probabilitas Prediksi",
        xaxis_title="Status",
        yaxis_title="Probabilitas",
        yaxis=dict(tickformat='.0%'),
        height=400
    )
    
    return fig

def create_gauge_chart(confidence, prediction):
    """Buat gauge chart untuk confidence"""
    color = '#ff6b6b' if 'Dropout' in prediction else '#4ecdc4'
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = confidence * 100,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': f"Confidence Level<br>{prediction}"},
        delta = {'reference': 50},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 80], 'color': "gray"},
                {'range': [80, 100], 'color': "darkgray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(height=300)
    return fig

def main():
    """Main Streamlit app"""
    
    # Header
    st.markdown('<h1 class="main-header">🎓 Student Dropout Prediction</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Load model
    with st.spinner("Loading prediction model..."):
        model, scaler, class_names = load_model_safe()
    
    if model is None:
        st.error("❌ Gagal memuat model. Pastikan file model ada di folder 'saved_models/'")
        st.stop()
    
    # Sidebar untuk input
    st.sidebar.header("📊 Input Data Mahasiswa")
    
    # Tab untuk berbagai mode input
    tab1, tab2, tab3 = st.tabs(["🔍 Single Prediction", "📁 Batch Prediction", "📈 Model Info"])
    
    with tab1:
        # Input form dalam sidebar
        with st.sidebar:
            st.subheader("Data Demografis")
            col1, col2 = st.columns(2)
            
            with col1:
                age = st.number_input("Umur saat mendaftar", min_value=16, max_value=50, value=18)
                gender = st.selectbox("Gender", options=[1, 2], format_func=lambda x: "Female" if x == 1 else "Male")
                marital_status = st.selectbox("Status Pernikahan", options=[1, 2, 3, 4, 5, 6], 
                                            format_func=lambda x: ["Single", "Married", "Widower", "Divorced", "Facto union", "Legally separated"][x-1])
            
            with col2:
                nationality = st.number_input("Kewarganegaraan (ID)", min_value=1, max_value=100, value=1)
                international = st.selectbox("Mahasiswa Internasional", options=[0, 1],
                                           format_func=lambda x: "No" if x == 0 else "Yes")
                displaced = st.selectbox("Status Pengungsi", options=[0, 1],
                                       format_func=lambda x: "No" if x == 0 else "Yes")
            
            st.subheader("Data Akademik")
            admission_grade = st.number_input("Nilai Masuk", min_value=0.0, max_value=200.0, value=127.0)
            prev_qualification_grade = st.number_input("Nilai Kualifikasi Sebelumnya", min_value=0.0, max_value=200.0, value=160.0)
            
            course = st.number_input("ID Course", min_value=1, max_value=200, value=33)
            daytime_attendance = st.selectbox("Waktu Kuliah", options=[1, 0],
                                            format_func=lambda x: "Siang" if x == 1 else "Malam")
            
            st.subheader("Data Finansial & Beasiswa")
            tuition_up_to_date = st.selectbox("SPP Up to Date", options=[0, 1],
                                            format_func=lambda x: "No" if x == 0 else "Yes")
            debtor = st.selectbox("Status Debitur", options=[0, 1],
                                format_func=lambda x: "No" if x == 0 else "Yes")
            scholarship = st.selectbox("Penerima Beasiswa", options=[0, 1],
                                     format_func=lambda x: "No" if x == 0 else "Yes")
            
            st.subheader("Performa Semester 1")
            sem1_enrolled = st.number_input("Unit Semester 1 Terdaftar", min_value=0, max_value=30, value=0)
            sem1_approved = st.number_input("Unit Semester 1 Lulus", min_value=0, max_value=30, value=0)
            sem1_grade = st.number_input("Nilai Rata-rata Semester 1", min_value=0.0, max_value=20.0, value=0.0)
            
            st.subheader("Performa Semester 2")
            sem2_enrolled = st.number_input("Unit Semester 2 Terdaftar", min_value=0, max_value=30, value=0)
            sem2_approved = st.number_input("Unit Semester 2 Lulus", min_value=0, max_value=30, value=0)
            sem2_grade = st.number_input("Nilai Rata-rata Semester 2", min_value=0.0, max_value=20.0, value=0.0)
            
            st.subheader("Data Ekonomi")
            unemployment_rate = st.number_input("Tingkat Pengangguran (%)", min_value=0.0, max_value=50.0, value=10.8)
            inflation_rate = st.number_input("Tingkat Inflasi (%)", min_value=-10.0, max_value=20.0, value=1.4)
            gdp = st.number_input("GDP", min_value=-5.0, max_value=10.0, value=1.74)
        
        # Tombol prediksi
        if st.sidebar.button("🔮 Prediksi Sekarang!", type="primary"):
            # Buat dictionary data
            student_data = {
                'Marital_status': marital_status,
                'Application_mode': 1,
                'Application_order': 1,
                'Course': course,
                'Daytime_evening_attendance': daytime_attendance,
                'Previous_qualification': 1,
                'Previous_qualification_grade': prev_qualification_grade,
                'Nacionality': nationality,
                'Mothers_qualification': 19,
                'Fathers_qualification': 13,
                'Mothers_occupation': 4,
                'Fathers_occupation': 10,
                'Admission_grade': admission_grade,
                'Displaced': displaced,
                'Educational_special_needs': 0,
                'Debtor': debtor,
                'Tuition_fees_up_to_date': tuition_up_to_date,
                'Gender': gender,
                'Scholarship_holder': scholarship,
                'Age_at_enrollment': age,
                'International': international,
                'Curricular_units_1st_sem_credited': 0,
                'Curricular_units_1st_sem_enrolled': sem1_enrolled,
                'Curricular_units_1st_sem_evaluations': sem1_enrolled,
                'Curricular_units_1st_sem_approved': sem1_approved,
                'Curricular_units_1st_sem_grade': sem1_grade,
                'Curricular_units_1st_sem_without_evaluations': 0,
                'Curricular_units_2nd_sem_credited': 0,
                'Curricular_units_2nd_sem_enrolled': sem2_enrolled,
                'Curricular_units_2nd_sem_evaluations': sem2_enrolled,
                'Curricular_units_2nd_sem_approved': sem2_approved,
                'Curricular_units_2nd_sem_grade': sem2_grade,
                'Curricular_units_2nd_sem_without_evaluations': 0,
                'Unemployment_rate': unemployment_rate,
                'Inflation_rate': inflation_rate,
                'GDP': gdp
            }
            
            # Prediksi
            with st.spinner("Sedang melakukan prediksi..."):
                result = predict_student(student_data, model, scaler, class_names)
            
            if result:
                # Hasil prediksi
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # Card hasil utama
                    if result['prediction'] == 'Dropout':
                        st.markdown(f"""
                        <div class="prediction-card" style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);">
                            <h2>⚠️ RISIKO TINGGI</h2>
                            <h3>Prediksi: {result['prediction']}</h3>
                            <p>Confidence: {result['confidence']:.1%}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.warning("🚨 **Perhatian!** Mahasiswa ini memiliki risiko dropout yang tinggi. "
                                 "Disarankan untuk memberikan dukungan akademik dan konseling.")
                    else:
                        st.markdown(f"""
                        <div class="prediction-card" style="background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);">
                            <h2>✅ RISIKO RENDAH</h2>
                            <h3>Prediksi: {result['prediction']}</h3>
                            <p>Confidence: {result['confidence']:.1%}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.success("🎉 **Bagus!** Mahasiswa ini memiliki kemungkinan tinggi untuk "
                                 "menyelesaikan studinya dengan baik.")
                
                with col2:
                    # Gauge chart
                    gauge_fig = create_gauge_chart(result['confidence'], result['prediction'])
                    st.plotly_chart(gauge_fig, use_container_width=True)
                
                # Detail probabilitas
                st.subheader("📊 Detail Probabilitas")
                prob_fig = create_probability_chart(result['probabilities'])
                st.plotly_chart(prob_fig, use_container_width=True)
                
                # Rekomendasi
                st.subheader("💡 Rekomendasi")
                if result['prediction'] == 'Dropout':
                    st.markdown("""
                    **Langkah-langkah yang dapat diambil:**
                    - 🎯 Konseling akademik intensif
                    - 📚 Program tutorial atau mentoring
                    - 💰 Bantuan finansial jika diperlukan
                    - 🤝 Dukungan psikologis dan motivasi
                    - 📈 Monitoring progress secara berkala
                    """)
                else:
                    st.markdown("""
                    **Dukungan yang dapat diberikan:**
                    - 🌟 Pertahankan motivasi belajar
                    - 🏆 Program pengembangan bakat
                    - 🤝 Peer mentoring sebagai tutor
                    - 📈 Challenge akademik yang lebih tinggi
                    """)
    
    with tab2:
        st.subheader("📁 Batch Prediction dari CSV")
        
        uploaded_file = st.file_uploader("Upload file CSV", type=['csv'])
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.write("Preview data:", df.head())
                
                if st.button("🚀 Jalankan Batch Prediction"):
                    with st.spinner("Processing batch prediction..."):
                        # Scaling
                        df_scaled = scaler.transform(df)
                        
                        # Prediksi
                        predictions = model.predict(df_scaled)
                        probabilities = model.predict_proba(df_scaled)
                        
                        # Buat hasil DataFrame
                        results = pd.DataFrame({
                            'prediction': [class_names[pred] for pred in predictions],
                            'confidence': [max(prob) for prob in probabilities]
                        })
                        
                        # Tambahkan probabilitas untuk setiap kelas
                        for i, class_name in enumerate(class_names):
                            results[f'prob_{class_name}'] = probabilities[:, i]
                        
                        st.write("Hasil Prediksi:", results)
                        
                        # Download hasil
                        csv = results.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Hasil CSV",
                            data=csv,
                            file_name='prediction_results.csv',
                            mime='text/csv'
                        )
                        
                        # Visualisasi hasil batch
                        dropout_count = (results['prediction'] == 'Dropout').sum()
                        total_count = len(results)
                        
                        fig = go.Figure(data=[
                            go.Pie(
                                labels=['Non-Dropout', 'Dropout'],
                                values=[total_count - dropout_count, dropout_count],
                                hole=0.4,
                                marker_colors=['#4ecdc4', '#ff6b6b']
                            )
                        ])
                        fig.update_layout(title="Distribusi Prediksi Batch")
                        st.plotly_chart(fig)
                        
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
    
    with tab3:
        st.subheader("🔍 Informasi Model")
        
        if class_names is not None:
            st.write("**Target Classes:**", class_names)
        
        st.write("**Features yang digunakan:**")
        feature_info = {
            "Demografis": ["Age_at_enrollment", "Gender", "Marital_status", "Nationality"],
            "Akademik": ["Admission_grade", "Previous_qualification_grade", "Course"],
            "Performa": ["Curricular_units_1st_sem_*", "Curricular_units_2nd_sem_*"],
            "Finansial": ["Tuition_fees_up_to_date", "Debtor", "Scholarship_holder"],
            "Ekonomi": ["Unemployment_rate", "Inflation_rate", "GDP"]
        }
        
        for category, features in feature_info.items():
            with st.expander(f"📋 {category}"):
                for feature in features:
                    st.write(f"• {feature}")
        
        st.markdown("---")
        st.markdown("**Developed with ❤️ using Streamlit**")

if __name__ == "__main__":
    main()