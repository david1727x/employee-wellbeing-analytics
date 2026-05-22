# 🧠 Dashboard — Bienestar Laboral

Dashboard interactivo de Análisis Exploratorio de Datos (EDA) sobre salud psicosocial y bienestar en el trabajo.  
Construido con **Python · Streamlit · Plotly**.

---

## 📁 Estructura del Proyecto

```
proyecto-dashboard/
│
├── app.py                  ← Dashboard principal (Streamlit)
├── requirements.txt        ← Dependencias para despliegue
├── README.md
│
├── data/
│   └── bienestar_laboral_limpio.xlsx   ← Dataset (reemplazar con datos reales)
│
├── assets/                 ← Logos, imágenes (opcional)
│
└── notebook/
    └── analisis.ipynb      ← Notebook original del EDA
```

---

## ⚡ Correr localmente

### 1. Clonar el repositorio
```bash
git clone https://github.com/TU_USUARIO/TU_REPO.git
cd TU_REPO
```

### 2. Crear entorno virtual (recomendado)
```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Agregar el dataset
Coloca tu archivo `bienestar_laboral_limpio.xlsx` (o `.csv`) dentro de la carpeta `data/`.

### 5. Lanzar el dashboard
```bash
streamlit run app.py
```
El navegador se abre automáticamente en `http://localhost:8501`

---

## 🚀 Despliegue en Streamlit Community Cloud

1. Sube el repositorio a GitHub (público o privado).
2. Ve a **[share.streamlit.io](https://share.streamlit.io)** e inicia sesión con GitHub.
3. Haz clic en **"New app"**.
4. Selecciona tu repositorio, rama (`main`) y archivo (`app.py`).
5. Haz clic en **"Deploy"** — Streamlit instala las dependencias automáticamente desde `requirements.txt`.
6. En 1–2 minutos tu dashboard estará en línea con una URL pública.

> ⚠️ **Dataset en repositorios públicos:** Si tu dataset es confidencial, no lo subas a un repositorio público. Usa **Streamlit Secrets** o una fuente externa (Google Sheets, S3, etc.).

---

## 📊 Secciones del Dashboard

| Tab | Análisis |
|-----|----------|
| 📊 Perfil Demográfico | Sexo, Modalidad, Sector, Edad |
| 📈 Ranking de Riesgo | Boxplots y medias de las 15 dimensiones |
| 🔬 Bienestar por Grupo | Comparativa por Cargo, Sector y Modalidad |
| 🔥 Burnout & Desgaste | Correlaciones y dispersión del síndrome |
| 🤝 Rol del Liderazgo | Impacto del liderazgo en satisfacción y burnout |
| 🎯 Predicción Retiro | Modelo OLS satisfacción → intención de retiro |
| 👥 Perfiles / Clustering | K-Means k=3 + radar de perfiles |
| 🚨 Matriz de Intervención | Heatmap global + acciones prioritarias |

---

## 🎓 Proyecto Final — Análisis de Datos

> Dataset: 400 trabajadores · 15 dimensiones psicosociales  
> Metodología: EDA + Regresión OLS + K-Means Clustering
