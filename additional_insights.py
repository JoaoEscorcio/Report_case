import streamlit as st
import pandas as pd
import plotly.express as px


def show_additional_insights():
    # **1. Ler o Arquivo CSV Internamente**
    df = pd.read_csv("Titanic-Dataset.csv")
    df['Sex'] = df['Sex'].astype('category')
    df['Pclass'] = df['Pclass'].astype('category')
    df['Embarked'] = df['Embarked'].astype('category')
    df['Survived'] = pd.to_numeric(df['Survived'], errors='coerce')
    df['Age'].fillna(df['Age'].median(), inplace=True)
    df['Embarked'].fillna(df['Embarked'].mode()[0], inplace=True)
    df.drop(columns=['PassengerId', 'Name', 'Ticket', 'Cabin'], inplace=True)

    # **2. Distribuição da Idade por Classe de Passageiro**
    st.title('Additional Insights')

    # Gráfico de distribuição da idade por classe
    age_class_df = df.groupby('Pclass')['Age'].mean().reset_index()
    age_class_df.columns = ['Passenger Class', 'Average Age']

    fig_age_class = px.bar(age_class_df, x='Passenger Class', y='Average Age',
                           title='Average Age by Passenger Class',
                           color='Passenger Class',
                           color_discrete_map={1: '#004b87', 2: '#0073b7', 3: '#00a3e0'})  # Paleta de azuis
    st.plotly_chart(fig_age_class)

    # **3. Sobrevivência por Classe e Gênero**
    survival_class_gender_df = df.groupby(['Pclass', 'Sex'])[
        'Survived'].mean().reset_index()
    survival_class_gender_df.columns = [
        'Passenger Class', 'Gender', 'Survival Rate']

    fig_survival_class_gender = px.bar(survival_class_gender_df, x='Passenger Class', y='Survival Rate',
                                       color='Gender', barmode='group',
                                       title='Survival Rate by Passenger Class and Gender',
                                       color_discrete_map={'male': '#004b87', 'female': '#ff6f91'})  # Cores específicas para gênero
    st.plotly_chart(fig_survival_class_gender)

    # **4. Comparação da Sobrevivência com e sem Irmãos/Cônjuges a Bordo**
    # Preencher valores ausentes com 0 para a coluna SibSp
    df['SibSp'] = df['SibSp'].fillna(0)
    df['Has_SibSp'] = df['SibSp'].apply(lambda x: 'Yes' if x > 0 else 'No')

    survival_sibsp_df = df.groupby(
        'Has_SibSp')['Survived'].mean().reset_index()
    survival_sibsp_df.columns = ['Has Sibling/Spouse Aboard', 'Survival Rate']

    fig_survival_sibsp = px.bar(survival_sibsp_df, x='Has Sibling/Spouse Aboard', y='Survival Rate',
                                title='Survival Rate with and without Sibling/Spouse Aboard',
                                color='Has Sibling/Spouse Aboard',
                                color_discrete_map={'Yes': '#004b87', 'No': '#00a3e0'})  # Paleta de azuis
    st.plotly_chart(fig_survival_sibsp)

    # **5. Análise da Taxa de Sobrevivência por Faixa Etária**
    age_bins = [0, 12, 18, 30, 50, 100]
    age_labels = ['0-12', '13-18', '19-30', '31-50', '51+']
    df['AgeGroup'] = pd.cut(df['Age'], bins=age_bins,
                            labels=age_labels, right=False)

    survival_age_df = df.groupby('AgeGroup')['Survived'].mean().reset_index()
    survival_age_df.columns = ['Age Group', 'Survival Rate']

    fig_survival_age = px.bar(survival_age_df, x='Age Group', y='Survival Rate',
                              title='Survival Rate by Age Group',
                              color='Age Group',
                              color_discrete_map={'0-12': '#004b87', '13-18': '#0073b7', '19-30': '#00a3e0',
                                                  '31-50': '#1E90FF', '51+': '#ADD8E6'})  # Paleta de azuis
    st.plotly_chart(fig_survival_age)

    st.write("---")
    st.write("#### Insights:")
    st.write("1. The average age tends to increase as passenger class decreases, suggesting that younger passengers were more likely to be in lower classes.")
    st.write("2. Survival rates vary significantly between different passenger classes and genders, with female passengers having a higher survival rate.")
    st.write("3. Passengers with siblings or spouses aboard generally had a higher survival rate compared to those without.")
    st.write("4. Younger passengers (0-12) had a significantly higher survival rate compared to older age groups.")
