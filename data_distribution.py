import streamlit as st
import pandas as pd
import plotly.express as px


def load_data():
    # Carregar o dataset
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

    return df


def show_data_distribution():
    df = load_data()

    # Mapear os códigos de embarque para os nomes dos portos
    port_map = {'S': 'Southampton', 'C': 'Cherbourg', 'Q': 'Queenstown'}
    df['Embarked'] = df['Embarked'].map(port_map)

    # Abas
    with st.container():
        st.title("Data Distribution")

        # 1. Distribuição da Idade dos Passageiros
        st.write("""
        ### Age Distribution of Passengers
        This histogram shows the age distribution of all passengers. The density curve provides a smooth estimate of the age distribution, highlighting the age range where most passengers fall.
        """)

        # Criar histograma da distribuição de idade
        fig_age_distribution = px.histogram(df, x='Age', nbins=30, title='Age Distribution of Passengers',
                                            color_discrete_sequence=[
                                                '#003d6c'],
                                            histnorm='density')
        fig_age_distribution.update_layout(
            xaxis_title='Age', yaxis_title='Density')
        st.plotly_chart(fig_age_distribution)

        # Linha divisória
        st.markdown("""<hr style="border: 1px solid #ccc;"/>""",
                    unsafe_allow_html=True)

        # 2. Distribuição dos Passageiros por Porto de Embarque (Embarked)
        st.write("""
        ### Passenger Distribution by Embarked Port
        This bar chart illustrates the number of passengers boarding from each port. It provides an overview of the distribution of passengers across different embarkation points.
        """)
        embarked_dist_df = df['Embarked'].value_counts().reset_index()
        embarked_dist_df.columns = ['Embarked', 'Count']
        fig_embarked_distribution = px.bar(embarked_dist_df, x='Embarked', y='Count',
                                           labels={
                                               'Embarked': 'Embarked Port', 'Count': 'Count'},
                                           title='Passenger Distribution by Embarked Port',
                                           # Tons de azul mais distintos
                                           color='Embarked', color_discrete_sequence=['#003d6c', '#0063e5', '#0090f9'],
                                           text='Count')
        fig_embarked_distribution.update_layout(
            xaxis_title='Embarked Port', yaxis_title='Count')
        st.plotly_chart(fig_embarked_distribution)

        # Linha divisória
        st.markdown("""<hr style="border: 1px solid #ccc;"/>""",
                    unsafe_allow_html=True)

        # 3. Distribuição dos Passageiros por Número de Irmãos/Cônjuges a Bordo (SibSp)
        st.write("""
        ### Distribution of SibSp (Siblings/Spouses) Aboard
        This histogram depicts the number of siblings or spouses aboard the Titanic. It shows how many passengers had family members accompanying them on the journey.
        """)
        fig_sibsp_distribution = px.histogram(df, x='SibSp', title='Distribution of SibSp (Siblings/Spouses) Aboard',
                                              color_discrete_sequence=[
                                                  '#003d6c'],
                                              text_auto=True)  # Mostra contagem absoluta
        fig_sibsp_distribution.update_layout(
            xaxis_title='Number of SibSp', yaxis_title='Count')
        st.plotly_chart(fig_sibsp_distribution)

        # Linha divisória
        st.markdown("""<hr style="border: 1px solid #ccc;"/>""",
                    unsafe_allow_html=True)

        # 4. Distribuição dos Passageiros por Número de Pais/Filhos a Bordo (Parch)
        st.write("""
        ### Distribution of Parch (Parents/Children) Aboard
        This histogram illustrates the number of parents or children aboard the Titanic. It highlights how many passengers traveled with their family members.
        """)
        fig_parch_distribution = px.histogram(df, x='Parch', title='Distribution of Parch (Parents/Children) Aboard',
                                              color_discrete_sequence=[
                                                  '#003d6c'],
                                              text_auto=True)  # Mostra contagem absoluta
        fig_parch_distribution.update_layout(
            xaxis_title='Number of Parch', yaxis_title='Count')
        st.plotly_chart(fig_parch_distribution)

        # Linha divisória
        st.markdown("""<hr style="border: 1px solid #ccc;"/>""",
                    unsafe_allow_html=True)

        # 5. Distribuição da Idade por Classe (Pclass)
        st.write("""
        ### Age Distribution by Pclass
        This box plot displays the age distribution across different passenger classes. It shows the spread of ages within each class, providing insight into the age profile of passengers in each class.
        """)
        fig_age_by_class = px.box(df, x='Pclass', y='Age', title='Age Distribution by Pclass',
                                  color='Pclass',
                                  color_discrete_map={1: '#004b87', 2: '#0073b7', 3: '#00a3e0'})  # Cores distintas para cada classe
        fig_age_by_class.update_layout(xaxis_title='Pclass', yaxis_title='Age')
        st.plotly_chart(fig_age_by_class)

        # Linha divisória
        st.markdown("""<hr style="border: 1px solid #ccc;"/>""",
                    unsafe_allow_html=True)

        # 6. Distribuição da Tarifa por Classe (Pclass)
        st.write("""
        ### Fare Distribution by Pclass
        This box plot shows the distribution of fare prices across different passenger classes. It highlights how fare prices vary between classes, reflecting the differences in ticket pricing.
        """)
        fig_fare_by_class = px.box(df, x='Pclass', y='Fare', title='Fare Distribution by Pclass',
                                   color='Pclass',
                                   color_discrete_map={1: '#004b87', 2: '#0073b7', 3: '#00a3e0'})  # Cores distintas para cada classe
        fig_fare_by_class.update_layout(
            xaxis_title='Pclass', yaxis_title='Fare')
        st.plotly_chart(fig_fare_by_class)

        # Linha divisória
        st.markdown("""<hr style="border: 1px solid #ccc;"/>""",
                    unsafe_allow_html=True)

        # 7. Distribuição da Idade por Gênero (Sex)
        st.write("""
        ### Age Distribution by Gender
        This box plot illustrates the age distribution by gender. It provides insights into the age profile of male and female passengers.
        """)
        fig_age_by_gender = px.box(df, x='Sex', y='Age', title='Age Distribution by Gender',
                                   color='Sex',
                                   color_discrete_map={'male': '#004b87', 'female': '#ff6f91'})  # Cores distintas para gênero
        fig_age_by_gender.update_layout(
            xaxis_title='Gender', yaxis_title='Age')
        st.plotly_chart(fig_age_by_gender)
