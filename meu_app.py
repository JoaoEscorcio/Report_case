import streamlit as st
import pandas as pd
import plotly.express as px
from data_distribution import show_data_distribution
from survival_analytics import show_survival_analytics
from correlation_analyses import show_correlation_analyses
from additional_insights import show_additional_insights

# **1. Carregar e Limpar os Dados**
df = pd.read_csv("Titanic-Dataset.csv")
df['Sex'] = df['Sex'].astype('category')
df['Pclass'] = df['Pclass'].astype('category')
df['Embarked'] = df['Embarked'].astype('category')
df['Survived'] = pd.to_numeric(df['Survived'], errors='coerce')
df['Age'].fillna(df['Age'].median(), inplace=True)
df['Embarked'].fillna(df['Embarked'].mode()[0], inplace=True)
df.drop(columns=['PassengerId', 'Name', 'Ticket', 'Cabin'], inplace=True)

# **2. Cálculo das Métricas**
total_passengers = df.shape[0]
total_survivors = df['Survived'].sum()
total_non_survivors = total_passengers - total_survivors
total_female_passengers = df[df['Sex'] == 'female'].shape[0]
total_male_passengers = df[df['Sex'] == 'male'].shape[0]
average_age = df['Age'].mean()

# **3. Configurar a Página**
st.set_page_config(page_title="Titanic Dashboard", layout="wide")

# **4. Criar Abas com st.tabs**
tabs = st.tabs([
    "Start Here",
    "Overview",
    "Data Distribution",
    "Survival Analytics",
    "Correlation Analyses",
    "Additional Insights"
])

# Aba "Start Here"
with tabs[0]:
    st.title('Welcome to the Titanic Dashboard')
    
    st.write("""
    ### Start Here
    Welcome to our Titanic dataset analysis. This dashboard provides an in-depth overview of the Titanic passengers, including their survival rates, demographics, and class distribution.
    Here, you will find various visualizations and metrics to help you understand the dataset better. Start by exploring the "Overview" section for key insights and statistics.
    """)
    st.image("titanic.jpeg", caption='Titanic Ship', use_column_width=True)

# Aba "Overview"
with tabs[1]:
    st.title('Titanic Dashboard - Overview')
    with st.container():
        st.subheader("Key Metrics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
                <div style="padding: 15px; border-radius: 10px; background-color: #f0f0f0; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
                    <h4 style="margin: 0; color: #333;">Total Passengers</h4>
                    <h3 style="margin: 5px 0 0; color: #0073b7;">{total_passengers}</h3>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div style="padding: 15px; border-radius: 10px; background-color: #f0f0f0; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
                    <h4 style="margin: 0; color: #333;">Total Survivors</h4>
                    <h3 style="margin: 5px 0 0; color: #28a745;">{total_survivors}</h3>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
                <div style="padding: 15px; border-radius: 10px; background-color: #f0f0f0; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
                    <h4 style="margin: 0; color: #333;">Total Non-Survivors</h4>
                    <h3 style="margin: 5px 0 0; color: #dc3545;">{total_non_survivors}</h3>
                </div>
            """, unsafe_allow_html=True)

        col4, col5, col6 = st.columns(3)
        with col4:
            st.markdown(f"""
                <div style="padding: 15px; border-radius: 10px; background-color: #f0f0f0; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
                    <h4 style="margin: 0; color: #333;">Total Female Passengers</h4>
                    <h3 style="margin: 5px 0 0; color: #f75b9a;">{total_female_passengers}</h3>
                </div>
            """, unsafe_allow_html=True)
        with col5:
            st.markdown(f"""
                <div style="padding: 15px; border-radius: 10px; background-color: #f0f0f0; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
                    <h4 style="margin: 0; color: #333;">Total Male Passengers</h4>
                    <h3 style="margin: 5px 0 0; color: #1e73be;">{total_male_passengers}</h3>
                </div>
            """, unsafe_allow_html=True)
        with col6:
            st.markdown(f"""
                <div style="padding: 15px; border-radius: 10px; background-color: #f0f0f0; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
                    <h4 style="margin: 0; color: #333;">Average Age</h4>
                    <h3 style="margin: 5px 0 0; color: #6c757d;">{average_age:.1f}</h3>
                </div>
            """, unsafe_allow_html=True)

    # Gráficos de Rosca
    survival_dist_df = df['Survived'].value_counts().reset_index()
    survival_dist_df.columns = ['Survived', 'Count']
    survival_dist_df['Survived'] = survival_dist_df['Survived'].map(
        {0: 'Not Survived', 1: 'Survived'})
    survival_dist = px.pie(survival_dist_df, names='Survived', values='Count',
                           title='Survivors vs Non-Survivors', hole=0.3,
                           color='Survived', color_discrete_map={'Survived': '#004b87', 'Not Survived': '#ff6f91'})
    st.plotly_chart(survival_dist)
    #st.write("#### Comment:")
    #st.write("Survival rate by gender: 20.3% male; 79.7% female")

    st.write("---")

    gender_dist_df = df['Sex'].value_counts().reset_index()
    gender_dist_df.columns = ['Sex', 'Count']
    gender_dist = px.pie(gender_dist_df, names='Sex', values='Count',
                         title='Distribution by Gender', hole=0.3,
                         color='Sex', color_discrete_map={'male': '#004b87', 'female': '#ff6f91'})
    st.plotly_chart(gender_dist)
    st.write("#### Comment:")
    st.write( "Distribution by gender: 64.8% male; 35.2% female")

    st.write("---")

    class_dist_df = df['Pclass'].value_counts().reset_index()
    class_dist_df.columns = ['Pclass', 'Count']
    class_dist_df['Pclass'] = class_dist_df['Pclass'].map(
        {1: 'First Class', 2: 'Second Class', 3: 'Third Class'})
    class_dist = px.pie(class_dist_df, names='Pclass', values='Count',
                        title='Distribution by Passenger Class', hole=0.3,
                        color='Pclass', color_discrete_map={'First Class': '#004b87',
                                                            'Second Class': '#0073b7',
                                                            'Third Class': '#00a3e0'})
    st.plotly_chart(class_dist)
    st.write("#### Comment:")
    st.write( "the third class had more than 50%")

# Aba "Data Distribution"
with tabs[2]:
    show_data_distribution()

# Aba "Survival Analytics"
with tabs[3]:
    show_survival_analytics(df)

# Aba "Correlation Analyses"
with tabs[4]:
    show_correlation_analyses(df)

# Aba "Additional Insights"
with tabs[5]:
    show_additional_insights()
