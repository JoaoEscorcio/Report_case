import streamlit as st
import pandas as pd
import plotly.express as px

# **1. Carregar e Limpar os Dados**
# Carregar o dataset
#df = pd.read_csv('C:/Users/Colaborador(a)/Downloads/Novapasta/Titanic-Dataset.csv')
df = pd.read_csv("Titanic-Dataset.csv")
# Convertendo colunas categóricas
df['Sex'] = df['Sex'].astype('category')
df['Pclass'] = df['Pclass'].astype('category')
df['Embarked'] = df['Embarked'].astype('category')

# Garantir tipo numérico e tratar valores faltantes
df['Survived'] = pd.to_numeric(df['Survived'], errors='coerce')
df['Age'].fillna(df['Age'].median(), inplace=True)
df['Embarked'].fillna(df['Embarked'].mode()[0], inplace=True)

# Remover colunas não necessárias para a análise
df.drop(columns=['PassengerId', 'Name', 'Ticket', 'Cabin'], inplace=True)

# Verificar o DataFrame
print(df.head())
print(df.dtypes)

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
    "Features Comparison", 
    "Additional Insights"
])

# Aba "Start Here"
with tabs[0]:
    st.title('Welcome to the Titanic Dashboard')
    
    # Adicionar a imagem
   
    
    st.write("""
    ### Start Here

    Welcome to our Titanic dataset analysis. This dashboard provides an in-depth overview of the Titanic passengers, including their survival rates, demographics, and class distribution.

    Here, you will find various visualizations and metrics to help you understand the dataset better. Start by exploring the "Overview" section for key insights and statistics.
    """)
    #st.image('C:/Users/Colaborador(a)/Downloads/titanic.jpeg', caption='Titanic Ship', use_column_width=True)
    st.image("titanic.jpeg", caption='Titanic Ship', use_column_width=True)
# Aba "Overview"
with tabs[1]:
    st.title('Titanic Dashboard - Overview')

    # Seção de Métricas
    with st.container():
        st.subheader("Key Metrics")

        # Dividir a página em 2 linhas com 3 colunas cada
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
                <div style="padding: 15px; border-radius: 10px; background-color: #f0f0f0; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
                    <h4 style="margin: 0; color: #333;">Total Passengers</h4>
                    <h3 style="margin: 5px 0 0; color: #007bff;">{total_passengers}</h3>
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

    # 1. Distribuição de Sobreviventes e Não Sobreviventes
    survival_dist_df = df['Survived'].value_counts().reset_index()
    survival_dist_df.columns = ['Survived', 'Count']
    survival_dist_df['Survived'] = survival_dist_df['Survived'].map({0: 'Not Survived', 1: 'Survived'})
    survival_dist = px.pie(survival_dist_df, names='Survived', values='Count',
                          title='Survivors vs Non-Survivors', hole=0.3,
                          color='Survived', color_discrete_map={'Survived': 'rgb(30, 139, 195)', 'Not Survived': 'rgb(255, 105, 97)'})

    # 2. Distribuição por Gênero
    gender_dist_df = df['Sex'].value_counts().reset_index()
    gender_dist_df.columns = ['Sex', 'Count']
    gender_dist = px.pie(gender_dist_df, names='Sex', values='Count',
                         title='Distribution by Gender', hole=0.3,
                         color='Sex', color_discrete_map={'male': 'rgb(30, 139, 195)', 'female': 'rgb(244, 127, 96)'})

    # 3. Distribuição por Classe
    class_dist_df = df['Pclass'].value_counts().reset_index()
    class_dist_df.columns = ['Pclass', 'Count']
    class_dist_df['Pclass'] = class_dist_df['Pclass'].map({1: 'First Class', 2: 'Second Class', 3: 'Third Class'})
    class_dist = px.pie(class_dist_df, names='Pclass', values='Count',
                        title='Distribution by Passenger Class', hole=0.3,
                        color='Pclass', color_discrete_map={'First Class': 'rgb(34, 53, 92)',
                                                            'Second Class': 'rgb(103, 129, 166)',
                                                            'Third Class': 'rgb(179, 199, 213)'})

    # Mostrar gráficos
    st.plotly_chart(survival_dist)
    st.plotly_chart(gender_dist)
    st.plotly_chart(class_dist)
