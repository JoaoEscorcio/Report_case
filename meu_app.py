import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# **1. Carregar e Limpar os Dados**
# Carregar o dataset
#df = pd.read_csv('C:/Users/Colaborador(a)/Downloads/Novapasta/Titanic-Dataset.csv')
df = pd.read_csv('Titanic-Dataset.csv')
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

# **3. Criar Gráfico de Linha do Tempo com Plotly**
def create_timeline_plot():
    # Dados da linha do tempo
    tl_dates = ["WED April 10", "SUN April 14", "MON April 15", "THU April 18"]
    tl_x = [1, 2, 6, 9]

    tl_sub_x = [1.5, 2.4, 2.9, 3.4, 3.8, 4.5, 5.0, 6.5, 7, 7.6, 8]
    tl_sub_times = ["1:30 PM", "9:00 AM", "1:42 PM", "7:15 PM", "10:00 PM", "11:30 PM", "11:40 PM", "12:20 AM", "12:45 AM", "2:00 AM", "2:20 AM"]
    tl_text = ["Titanic sets sail.", "Receive Message.", "Baltic Warns Titanic\nof icebergs.", "Smith requests the\nreturn of the message.",
               "Second Officer\nLightoller is\nrelieved from duty.", "Warning bells, iceberg\nsighting.", "Titanic hits an iceberg.",
               "Life boats are being\nlowered.", "Passengers slowly arrive\non deck.", "Rear of boat begins to\nraise.", "Titanic sinks."]

    # Criar o gráfico de linha do tempo com Plotly
    fig = go.Figure()

    # Linha da linha do tempo
    fig.add_trace(go.Scatter(x=tl_x, y=[0] * len(tl_x), mode='markers+lines', line=dict(color='#333333'), marker=dict(size=12, color='#333333', line=dict(color='black', width=1)), name='Date'))
    fig.add_trace(go.Scatter(x=tl_sub_x, y=[0] * len(tl_sub_x), mode='markers', marker=dict(size=10, color='#333333'), name='Time'))

    # Adicionar pontos de data e tempo
    for x, date in zip(tl_x, tl_dates):
        fig.add_trace(go.Scatter(x=[x], y=[0], mode='text', text=[date], textposition='bottom center', textfont=dict(size=12, color='#333333')))

    for idx, x, time, txt in zip(range(1, len(tl_sub_x)+1), tl_sub_x, tl_sub_times, tl_text):
        fig.add_trace(go.Scatter(x=[x], y=[0.5 if idx % 2 == 0 else -0.5], mode='text', text=[time], textposition='bottom center', textfont=dict(size=11, color='#333333')))
        color = '#e3120b' if txt == "Titanic sinks." else '#333333'
        fig.add_trace(go.Scatter(x=[x], y=[0.5 if idx % 2 == 0 else -0.5 - 0.2], mode='text', text=[txt], textposition='bottom center', textfont=dict(size=10, color=color)))

    # Configurações do gráfico
    fig.update_layout(
        title='Titanic Timeline',
        xaxis_title='Timeline',
        yaxis_title='',
        yaxis=dict(visible=False),
        xaxis=dict(visible=False),
        showlegend=False,
        plot_bgcolor='white'
    )

    return fig

# **4. Configurar a Página**
st.set_page_config(page_title="Titanic Dashboard", layout="wide")

# **5. Criar Abas com st.tabs**
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
    st.write("""
    ### Start Here

    Welcome to our Titanic dataset analysis. This dashboard provides an in-depth overview of the Titanic passengers, including their survival rates, demographics, and class distribution.

    Here, you will find various visualizations and metrics to help you understand the dataset better. Start by exploring the "Overview" section for key insights and statistics.
    """)

    # Exibir o gráfico de linha do tempo
    timeline_plot = create_timeline_plot()
    st.plotly_chart(timeline_plot, use_container_width=True)

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
    st.subheader("Distribution Insights")

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
