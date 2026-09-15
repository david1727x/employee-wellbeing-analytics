# Analítica de Bienestar Laboral y Dashboard Interactivo

**Español** | [English](README.md)

Proyecto de analítica de datos enfocado en bienestar laboral, burnout, satisfacción laboral, liderazgo, riesgo psicosocial e intención de retiro.

Desarrollado con **Python, Pandas, Plotly, Streamlit, Statsmodels y Scikit-learn**.

> Este proyecto fue desarrollado como un caso académico de Ciencia de Datos en la Universidad de La Sabana. Se presenta como proyecto de portafolio para demostrar habilidades en análisis de datos, modelado estadístico, visualización, clustering y desarrollo de dashboards.

## Problema de análisis

El bienestar de los trabajadores está relacionado con múltiples factores organizacionales y psicosociales. Analizar estas variables por separado dificulta identificar grupos de empleados que pueden presentar mayores niveles de riesgo.

El objetivo del proyecto es transformar datos de una encuesta laboral en una herramienta analítica interactiva que permita explorar:

- Bienestar laboral
- Burnout y desgaste
- Satisfacción laboral
- Liderazgo
- Dimensiones de riesgo psicosocial
- Intención de retiro
- Perfiles de riesgo de los trabajadores

## Dataset

El análisis utiliza un conjunto de datos de **400 trabajadores** con información demográfica y **15 dimensiones psicosociales**.

Entre las dimensiones analizadas se encuentran bienestar, burnout, desgaste, somatización, satisfacción, intención de retiro, compromiso del líder, presión de tiempo, apoyo de compañeros, conflicto de rol, gestión del cambio, salud mental organizacional, claridad de rol y variables relacionadas con el conflicto trabajo-familia.

## Flujo de análisis

El proyecto sigue un flujo completo de analítica de datos:

1. Carga y revisión de calidad de los datos
2. Limpieza y preparación
3. Análisis Exploratorio de Datos (EDA)
4. Segmentación demográfica y psicosocial
5. Análisis de correlaciones
6. Regresión lineal
7. Clustering con K-Means
8. Interpretación de perfiles de riesgo
9. Desarrollo de un dashboard interactivo con Streamlit

## Resultados principales

### Burnout y factores relacionados

El burnout presenta relaciones positivas importantes con otras dimensiones de riesgo psicosocial:

- **Burnout ↔ Desgaste:** r = 0.658
- **Burnout ↔ Somatización:** r = 0.610
- **Desgaste ↔ Somatización:** r = 0.554

Estos resultados muestran la importancia de estudiar el burnout junto con indicadores de desgaste físico y emocional, en lugar de interpretarlo como una dimensión aislada.

### Liderazgo y experiencia laboral

El liderazgo presenta asociaciones relevantes con resultados positivos y negativos de los trabajadores:

- **Liderazgo ↔ Satisfacción laboral:** r = 0.487
- **Liderazgo ↔ Burnout:** r = -0.533

En este conjunto de datos, mayores puntuaciones de liderazgo están asociadas con mayor satisfacción laboral y menores niveles de burnout.

### Intención de retiro

Se utilizó una regresión lineal para estudiar la relación entre satisfacción laboral e intención de retiro.

- **R²:** 0.704
- **Pendiente:** -1.150
- **Intercepto:** 9.430
- **p-value:** 2.28e-107

El modelo identifica una asociación negativa fuerte: una mayor satisfacción laboral está asociada con una menor intención de retiro. Al tratarse de un análisis observacional, este resultado no debe interpretarse como evidencia causal.

### Segmentación de trabajadores

Se utilizó K-Means para identificar **tres perfiles de trabajadores**:

| Perfil | Trabajadores |
|---|---:|
| Perfil estable | 112 |
| Perfil de alto riesgo | 79 |
| Perfil de riesgo moderado | 209 |

La segmentación permite comparar grupos y establecer prioridades para análisis exploratorios de intervención.

## Dashboard interactivo

La aplicación desarrollada en Streamlit organiza el análisis en diferentes secciones interactivas:

| Sección | Análisis |
|---|---|
| Perfil demográfico | Sexo, modalidad, sector y edad |
| Ranking de riesgo | Comparación de dimensiones psicosociales |
| Bienestar por grupo | Análisis por cargo, sector y modalidad |
| Burnout y desgaste | Relaciones entre variables asociadas al burnout |
| Liderazgo | Relación con satisfacción y burnout |
| Intención de retiro | Relación estadística entre satisfacción e intención de retiro |
| Perfiles de trabajadores | Clustering K-Means y comparación de perfiles |
| Matriz de intervención | Visualización global de riesgos y priorización |

El dashboard incorpora filtros y visualizaciones interactivas para facilitar la exploración e interpretación de los resultados estadísticos.

## Tecnologías

- Python
- Pandas
- NumPy
- Plotly
- Streamlit
- Statsmodels
- Scikit-learn
- Jupyter Notebook
- OpenPyXL

## Estructura actual del repositorio

```text
.
├── README.md
├── README_ES.md
├── app.py
├── crear_app.py
├── requirements.txt
├── data/
│   └── bienestar_laboral_limpio.xlsx
└── notebook/
    └── analisis.ipynb
```

La estructura anterior representa el estado actual del repositorio. Los nombres del repositorio y de algunos archivos pueden estandarizarse posteriormente como parte de la mejora del portafolio.

## Ejecutar localmente

Clona el repositorio y entra en la carpeta del proyecto:

```bash
git clone <repository-url>
cd <repository-folder>
```

Crea un entorno virtual e instala las dependencias:

```bash
python -m venv venv
pip install -r requirements.txt
```

Ejecuta la aplicación de Streamlit:

```bash
streamlit run app.py
```

## Habilidades demostradas

`Análisis de Datos` · `Python` · `Pandas` · `Análisis Exploratorio de Datos` · `Análisis Estadístico` · `Regresión Lineal` · `K-Means Clustering` · `Visualización de Datos` · `Streamlit` · `Desarrollo de Dashboards`

## Autor

**David Santiago Cifuentes Grimaldo**  
Estudiante de Ciencia de Datos  
Universidad de La Sabana
