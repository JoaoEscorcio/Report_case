import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import numpy as np


def show_correlation_analyses(df):
    # **2. Convert Categorical Variables to Numeric for Analysis**
    df_encoded = df.copy()
    le = LabelEncoder()
    categorical_cols = ['Sex', 'Embarked']

    for col in categorical_cols:
        df_encoded[col] = le.fit_transform(df_encoded[col])

    # **3. Heatmap de Correlação com Triângulo Inferior**
    st.title('Correlation Analyses')
    st.write("""
    ### Correlation Heatmap
    This heatmap shows the correlation matrix of numerical variables, displayed as a lower triangle for clarity. The size of the heatmap has been adjusted for better visibility.
    """)

    corr = df_encoded[['Age', 'Fare', 'Pclass', 'Survived']].corr()

    # Criar uma máscara para a parte superior do heatmap
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # Reduzir ainda mais o tamanho da figura
    fig_heatmap = plt.figure(figsize=(5, 3))  # Ajuste para ser menor
    sns.heatmap(corr, mask=mask, annot=True, cmap='Blues', vmin=-
                1, vmax=1, center=0, linewidths=0.5, fmt='.2f')
    plt.title('Correlation Heatmap')
    st.pyplot(fig_heatmap)

    st.write("---")

    # **4. Pearson and Spearman Correlation Analysis (Coeficientes)**
    st.write("""
    ### Pearson and Spearman Correlation Analysis
    Here we present the Pearson and Spearman correlation coefficients between pairs of numerical variables.
    
    **Pearson Correlation Coefficient**:
    - Measures the strength and direction of the linear relationship between two continuous variables.
    - Ranges from -1 to 1, where:
      - **1** indicates a perfect positive linear relationship,
      - **-1** indicates a perfect negative linear relationship,
      - **0** indicates no linear relationship.
    - A higher absolute value of the coefficient indicates a stronger linear relationship.

    **Spearman's Rank Correlation Coefficient**:
    - Measures the strength and direction of the monotonic relationship between two variables.
    - Ranges from -1 to 1, where:
      - **1** indicates a perfect positive monotonic relationship,
      - **-1** indicates a perfect negative monotonic relationship,
      - **0** indicates no monotonic relationship.
    - Spearman's correlation is useful for ordinal data or when the relationship between variables is not linear but monotonic.
    """)

    # Pearson Correlation Coefficients
    pearson_corr = df_encoded[['Age', 'Fare',
                               'Pclass', 'Survived']].corr(method='pearson')
    spearman_corr = df_encoded[['Age', 'Fare',
                                'Pclass', 'Survived']].corr(method='spearman')

    pairs = [
        ('Age', 'Fare'),
        ('Age', 'Pclass'),
        ('Age', 'Survived'),
        ('Fare', 'Pclass'),
        ('Fare', 'Survived'),
        ('Pclass', 'Survived')
    ]

    def interpret_correlation(coef):
        if coef > 0.5:
            return 'Strong positive correlation', '#004b87'  # Azul forte
        elif coef > 0.2:
            return 'Moderate positive correlation', '#66b3ff'  # Azul médio
        elif coef > -0.2:
            return 'Weak correlation', '#c2c2f0'  # Azul claro
        elif coef > -0.5:
            return 'Moderate negative correlation', '#ff9999'  # Rosa claro
        else:
            return 'Strong negative correlation', '#ff4d4d'  # Rosa forte

    st.subheader('Pearson Correlation Coefficients')
    pearson_data = []
    for x, y in pairs:
        coef = pearson_corr.loc[x, y]
        interpretation, color = interpret_correlation(coef)
        pearson_data.append({
            'Pair': f'{x} vs {y}',
            'Pearson Coefficient': f'{coef:.2f}',
            'Interpretation': f'<span style="color:{color}">{interpretation}</span>'
        })

    pearson_df = pd.DataFrame(pearson_data)
    st.markdown(pearson_df.to_html(escape=False), unsafe_allow_html=True)

    st.write("---")

    st.subheader('Spearman Correlation Coefficients')
    spearman_data = []
    for x, y in pairs:
        coef = spearman_corr.loc[x, y]
        interpretation, color = interpret_correlation(coef)
        spearman_data.append({
            'Pair': f'{x} vs {y}',
            'Spearman Coefficient': f'{coef:.2f}',
            'Interpretation': f'<span style="color:{color}">{interpretation}</span>'
        })

    spearman_df = pd.DataFrame(spearman_data)
    st.markdown(spearman_df.to_html(escape=False), unsafe_allow_html=True)

    st.write("---")

    # **6. Feature Importance with Random Forest (Horizontal Bar Chart)**
    st.write("""
    ### Feature Importance with Random Forest
    This plot shows the importance of each feature in predicting survival, based on a Random Forest model. Feature importance helps us understand which features contribute most to the model's predictions.
    """)

    # Defining features and target
    X = df_encoded[['Age', 'Fare', 'Pclass', 'Sex', 'Embarked']]
    y = df_encoded['Survived']

    # Training Random Forest
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X, y)

    # Extracting feature importances
    feature_importances = rf.feature_importances_
    features = X.columns
    importance_df = pd.DataFrame(
        {'Feature': features, 'Importance': feature_importances})
    importance_df = importance_df.sort_values(by='Importance', ascending=True)

    fig_feature_importance = px.bar(importance_df, x='Importance', y='Feature',
                                    title='Feature Importance with Random Forest',
                                    orientation='h', color='Importance', color_continuous_scale='Blues')
    st.plotly_chart(fig_feature_importance)

    st.write("""
    **Insight:**
    - **Fare**: Most important feature with an importance score of 0.31, indicating that the fare paid by passengers significantly influences the prediction of survival.
    - **Age**: Important feature with a score of 0.28, suggesting that age plays a considerable role in survival predictions.
    - **Sex**: Close to age in importance with a score of 0.27, reflecting the critical role of gender in determining survival likelihood.
    - **Embarked**: Slightly less important with a score of 0.30, showing that the port of embarkation also affects survival predictions but to a lesser extent.
    - **Pclass**: Least important feature with a score of 0.09, indicating that passenger class has a smaller impact on survival prediction compared to the other features.
    """)

    st.write("---")
