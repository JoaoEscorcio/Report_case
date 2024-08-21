import streamlit as st
import plotly.express as px
import pandas as pd


def show_survival_analytics(df):
    st.title("Survival Analytics")

    # Overall Survival Rate
    survival_rate = df['Survived'].mean() * 100
    st.markdown(f"""
        <div style="padding: 15px; border-radius: 10px; background-color: #f0f0f0; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
            <h4 style="margin: 0; color: #333;">Overall Survival Rate</h4>
            <h3 style="margin: 5px 0 0; color: #1e90ff;">{survival_rate:.1f}%</h3>
        </div>
    """, unsafe_allow_html=True)

    # Spacer and line between sections
    st.markdown("""
        <hr style="border: 1px solid #e0e0e0; margin: 20px 0;">
    """, unsafe_allow_html=True)

    # Column setup
    col1, col2 = st.columns(2)

    # Survival Rate by Gender
    with col1:
        gender_survival = df.groupby('Sex')['Survived'].mean().reset_index()
        gender_survival['Survived'] = gender_survival['Survived'] * 100
        gender_survival_fig = px.pie(gender_survival, names='Sex', values='Survived',
                                     title='Survival Rate by Gender',
                                     hole=0.3,
                                     color='Sex',
                                     color_discrete_map={'male': '#004b87', 'female': '#ff6f91'})
        st.plotly_chart(gender_survival_fig, use_container_width=True)

        st.write("""
        **Insights on Survival Rate by Gender:**
        The analysis shows a significant difference in survival rates between males and females. With approximately 79.7% of women surviving compared to 20.3% of men, this reflects the prioritization of women and children in rescue operations during the disaster.
        """)

    # Survival Rate by Passenger Class
    with col2:
        class_survival = df.groupby('Pclass')['Survived'].mean().reset_index()
        class_survival['Survived'] = class_survival['Survived'] * 100
        class_survival['Pclass'] = class_survival['Pclass'].map(
            {1: 'First Class', 2: 'Second Class', 3: 'Third Class'})
        class_survival_fig = px.pie(class_survival, names='Pclass', values='Survived',
                                    title='Survival Rate by Passenger Class',
                                    hole=0.3,
                                    color='Pclass',
                                    color_discrete_map={'First Class': '#004b87', 'Second Class': '#0073b7', 'Third Class': '#00a3e0'})
        st.plotly_chart(class_survival_fig, use_container_width=True)

        st.write("""
        **Insights on Survival Rate by Passenger Class:**
        The survival rate varied significantly by passenger class. First class passengers had the highest survival rate at 46.8%, while second class passengers had a rate of 35.2%, and third class passengers had the lowest at 18%. This likely reflects better access to lifeboats and resources for first-class passengers.
        """)

    # Spacer and line between sections
    st.markdown("""
        <hr style="border: 1px solid #e0e0e0; margin: 20px 0;">
    """, unsafe_allow_html=True)

    # Survival Rate by Age Group
    age_bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    age_labels = ['0-10', '10-20', '20-30', '30-40', '40-50',
                  '50-60', '60-70', '70-80', '80-90', '90-100']
    df['AgeGroup'] = pd.cut(df['Age'], bins=age_bins, labels=age_labels)
    age_survival = df.groupby('AgeGroup')['Survived'].mean().reset_index()
    age_survival['Survived'] = age_survival['Survived'] * 100
    age_survival_fig = px.line(age_survival, x='AgeGroup', y='Survived',
                               title='Survival Rate by Age Group',
                               labels={'Survived': 'Survival Rate (%)'},
                               markers=True,
                               line_shape='linear')
    st.plotly_chart(age_survival_fig)

    st.write("""
    **Insights on Survival Rate by Age Group:**
    This line chart shows how survival rates varied across different age groups. It indicates that younger passengers generally had higher survival rates compared to older passengers.
    """)

    # Spacer and line between sections
    st.markdown("""
        <hr style="border: 1px solid #e0e0e0; margin: 20px 0;">
    """, unsafe_allow_html=True)

    # Fare Distribution by Survival Status
    df['Survived'] = df['Survived'].astype('category')
    fare_survival_fig = px.box(df, x='Survived', y='Fare',
                               title='Fare Distribution by Survival Status',
                               labels={'Survived': 'Survival Status',
                                       'Fare': 'Fare'},
                               color='Survived',
                               color_discrete_map={0: '#f75b9a', 1: '#1e90ff'})
    st.plotly_chart(fare_survival_fig)

    st.write("""
    **Insights on Fare Distribution by Survival Status:**
    This box plot illustrates how fare prices were distributed among survivors and non-survivors. It shows that survivors tended to pay higher fares, which may correlate with better access to lifeboats and safer positions on the ship.
    """)
