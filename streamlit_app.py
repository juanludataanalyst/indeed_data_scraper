import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
import plotly.express as px
import altair as alt

# Cargar los datos desde el archivo CSV
data = pd.read_csv('skills_data_table.csv')

# Configuración de la barra lateral
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=[ "Skills by Role", "Contact"],
        icons=["bar-chart", "envelope"],
        menu_icon="cast",
        default_index=0,
    )


if selected == "Skills by Role":
    st.title("Top Most in Demand Skills")
    st.write("Select a role: ")

    # Crear un menú desplegable para seleccionar el rol
    roles = data['role'].unique()
    selected_role = st.selectbox("Select a role:", roles)

    # Filtrar los datos según el rol seleccionado
    df_role = data[data['role'] == selected_role]

    # Count the number of unique job IDs
    total_jobs = df_role['job_id'].nunique()

    # Count the occurrences of each skill
    skill_counts = df_role['skills'].value_counts()

    # Calculate the percentage of each skill
    skills_percentages = (skill_counts / total_jobs) * 100

    # Convertir a DataFrame para visualización
    skills_percentage_df = skills_percentages.reset_index()
    skills_percentage_df.columns = ['skill', 'percentage']
    
    # Round the 'percentage' column to one decimal place
    skills_percentage_df['percentage'] = skills_percentage_df['percentage'].round(1)
    # Formatear los porcentajes a un decimal
    #skills_percentage_df['percentage'] = skills_percentage_df['percentage'].map('{:.1f}%'.format)

    print(skills_percentage_df)


        # Ordenar las habilidades por porcentaje en orden descendente
  
# Ordenar las habilidades por porcentaje
    df = skills_percentage_df.sort_values("percentage", ascending=False).head(15)

        # Configuración de la página
    
    
        # Crear gráfica con Altair
    bars = (
        alt.Chart(df)
        .mark_bar(size=20)  # Tamaño de las barras
        .encode(
            x=alt.X("percentage:Q", title="Porcentaje (%)"),
            y=alt.Y(
                "skill:N",
                sort="-x",  # Orden descendente
                title="Habilidad"
            ),
            color=alt.Color(
                "percentage:Q",
                scale=alt.Scale(scheme="oranges"),
                legend=None
            )
        )
    )

    # Crear etiquetas con símbolo de porcentaje
    text = (
        alt.Chart(df)
        .mark_text(
            align="left",
            baseline="middle",
            dx=3,
            fontSize=20  # Tamaño del texto
        )
        .encode(
            x=alt.X("percentage:Q"),  # Mismo eje X que las barras
            y=alt.Y("skill:N", sort="-x"),  # Mismo eje Y que las barras
            text=alt.Text("percentage:Q", format=".1f")  # Mostrar valores con formato
        )
        .transform_calculate(
            percentage_label="datum.percentage + '%' "  # Añadir símbolo de porcentaje
        )
        .encode(
            text=alt.Text("percentage_label:N")  # Usar la nueva columna con el símbolo
        )
    )

    # Combinar las barras y el texto
    chart = (bars + text).properties(
        width=800,  # Ancho del gráfico
        height=600  # Altura ajustada
    ).configure_scale(
        bandPaddingInner=0.3  # Añadir espacio entre barras
    ).configure_axis(
        labelFontSize=18,  # Tamaño de las etiquetas de los ejes
        titleFontSize=20   # Tamaño del título de los ejes
    )

    # Mostrar gráfica en Streamlit
    st.altair_chart(chart, use_container_width=True)


    # Mostrar la tabla de porcentajes para el rol específico
    st.dataframe(skills_percentage_df.sort_values(by='percentage', ascending=False), use_container_width=True)
    st.markdown("""
    <style>
    .dataframe th, .dataframe td {
        border: 1px solid #dddddd;
        text-align: center;
        padding: 8px;
    }
    .dataframe th {
        background-color: #f2f2f2;
    }
    </style>
    """, unsafe_allow_html=True)


elif selected == "Contact":
    st.title("Contacta con Nosotros")
    st.write("Para cualquier consulta, puedes contactarnos a través de nuestro email.")
