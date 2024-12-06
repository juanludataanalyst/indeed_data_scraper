import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import altair as alt
import json

# Cargar los datos desde el archivo CSV
data = pd.read_csv('output_data/skills_data_table.csv')

# Cargar datos reglas de asociacion

import pandas as pd
import json

# Leer el archivo JSON
with open("output_data/summary_association_rules.json", "r") as file:
    rules = json.load(file)

# Convertirlo a un DataFrame
association_rules_data = pd.DataFrame([
    {
        "antecedent": rule["antecedents"][0],
        "consequent": rule["consequents"][0],
        "support": rule["support"],
        "confidence": rule["confidence"],
        "lift": rule["lift"]
    } for rule in rules
])





# Configuración de la barra lateral
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=[ "Skills by Role", "Skills to learn","Contact"],
        icons=["bar-chart","book" ,"envelope"],
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
            x=alt.X("percentage:Q", title="Proportion of offers where appears (%)"),
            y=alt.Y(
                "skill:N",
                sort="-x",  # Orden descendente
                title="Skill"
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


elif selected == "Skills to learn":


    # Título de la aplicación
    st.title("Skills to Learn")



    # Selector de antecedente
    #selected_antecedent = st.selectbox("Select a skill (antecedent):", association_rules_data ["antecedent"].unique())

    # Crear botones para cada antecedente
    selected_antecedent = st.radio("Elige una habilidad:", association_rules_data ["antecedent"].unique())

    # Filtrar los datos para mostrar el consecuente correspondiente
    filtered_data = association_rules_data [association_rules_data ["antecedent"] == selected_antecedent]

        # Mostrar los resultados en texto
    if not filtered_data.empty:
        for _, row in filtered_data.iterrows():
            st.write(
    f"""
    ## Recomendación personalizada para tu desarrollo profesional

    Basándonos en tus conocimientos actuales y en el análisis de miles de ofertas de trabajo, te sugerimos que complementes tu perfil con  **{row['consequent']}**. 

    **¿Por qué esta recomendación?**

    * **Alta correlación:** El {row['confidence']:.1%} de las veces que aparece '{row['antecedent']}' en una oferta de trabajo, también aparece '{row['consequent']}'.
    * **Frecuencia conjunta:** Ambas habilidades, '{row['antecedent']}' y '{row['consequent']}', aparecen juntas en un {row['support']:.2%} de las ofertas de trabajo analizadas.
    * **Impacto en tu empleabilidad:** Al adquirir la habilidad de {row['consequent']}, tus posibilidades de encontrar un empleo que se ajuste a tu perfil se m ultiplicaran por un factor de {row['lift']:.1f}x

    """
)
    else:
        st.write("No hay datos disponibles para la habilidad seleccionada.")

elif selected == "Contact":
    st.title("Contacta con Nosotros")
    st.write("Para cualquier consulta, puedes contactarnos a través de nuestro email.")
