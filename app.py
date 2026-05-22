# =============================================================================
# DASHBOARD: BIENESTAR LABORAL — EDA INTERACTIVO
# =============================================================================

import glob
import warnings
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import statsmodels.api as sm
import streamlit as st
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")
np.random.seed(42)

# ── Paleta corporativa (Cool Tech) ────────────────────────────────────────────
C_PRIMARY   = "#1e3d59"
C_SECONDARY = "#17b978"
C_NEUTRAL   = "#90b4ce"
C_WARN      = "#ff6b6b"
C_ACCENT    = "#e056fd"
C_DARK      = "#112233"

# =============================================================================
# CONFIGURACIÓN DE PÁGINA
# =============================================================================
st.set_page_config(
    page_title="Bienestar Laboral | Dashboard EDA",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS global
st.markdown("""
<style>
    /* Tipografía base */
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;700&family=Space+Grotesk:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    h1, h2, h3 { font-family: 'Space Grotesk', sans-serif; }

    /* Header principal */
    .main-header {
        background: linear-gradient(135deg, #1e3d59 0%, #17b978 100%);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        color: white;
    }
    .main-header h1 { color: white; font-size: 2rem; margin: 0; }
    .main-header p  { color: rgba(255,255,255,0.85); margin: 0.4rem 0 0; font-size: 1rem; }

    /* KPI cards */
    .kpi-card {
        background: white;
        border-radius: 12px;
        padding: 1.2rem 1.4rem;
        border-left: 4px solid #17b978;
        box-shadow: 0 2px 12px rgba(30,61,89,0.08);
    }
    .kpi-label { font-size: 0.78rem; color: #6b7280; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; }
    .kpi-value { font-size: 2rem; font-weight: 700; color: #1e3d59; line-height: 1.2; }
    .kpi-delta { font-size: 0.82rem; color: #17b978; font-weight: 500; }

    /* Sección de análisis */
    .section-header {
        background: #f8fafc;
        border-left: 4px solid #1e3d59;
        padding: 0.7rem 1rem;
        border-radius: 0 8px 8px 0;
        margin: 1.2rem 0 0.8rem;
    }
    .section-header p { margin: 0; font-weight: 600; color: #1e3d59; font-size: 0.95rem; }

    /* Insight box */
    .insight-box {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-radius: 10px;
        padding: 0.9rem 1.1rem;
        font-size: 0.87rem;
        color: #166534;
        margin: 0.5rem 0;
    }

    /* Alert box */
    .alert-box {
        background: #fff1f2;
        border: 1px solid #fecdd3;
        border-radius: 10px;
        padding: 0.9rem 1.1rem;
        font-size: 0.87rem;
        color: #9f1239;
        margin: 0.5rem 0;
    }

    /* Sidebar refinements */
    section[data-testid="stSidebar"] { background: #f8fafc; }
    section[data-testid="stSidebar"] .stMarkdown h3 { color: #1e3d59; }

    /* Tab styling */
    .stTabs [data-baseweb="tab"] { font-weight: 600; font-size: 0.85rem; }
    .stTabs [aria-selected="true"] { color: #1e3d59 !important; }

    /* Remove default padding on main */
    .block-container { padding-top: 1.5rem; }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# CARGA Y LIMPIEZA DE DATOS
# =============================================================================
@st.cache_data
def load_data():
    import os
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    paths = glob.glob(os.path.join(BASE_DIR, "data", "bienestar_laboral_limpio*"))
    if not paths:
        raise FileNotFoundError(
            "No se encontró el dataset en la carpeta data/. "
            "Añade el archivo 'bienestar_laboral_limpio.xlsx' o '.csv'."
        )
    path = paths[0]
    df = pd.read_excel(path) if path.endswith((".xlsx", ".xls")) else pd.read_csv(path)
    df = df.loc[:, ~df.columns.duplicated(keep="first")].copy()
    df.columns = df.columns.str.strip()
    return df


@st.cache_data
def map_cols(df):
    """Devuelve el nombre real de cada dimensión (con o sin .1)."""
    def _col(name):
        return f"{name}.1" if f"{name}.1" in df.columns else name
    return {
        "bienestar":         _col("BIENESTAR"),
        "burnout":           _col("BURNOUT"),
        "desgaste":          _col("DESGASTE"),
        "somatizacion":      _col("SOMATIZACION"),
        "satisfaccion":      _col("SATISFACCION"),
        "retiro":            _col("INTENCION_RETIRO"),
        "lider":             _col("COMPROMISO_LIDER"),
        "presion":           _col("PRESION_TIEMPO"),
        "apoyo":             _col("APOYO_COMP"),
        "conflicto":         _col("CONFLICTO_ROL"),
        "cambio":            _col("GESTION_CAMBIO"),
        "salud_mental":      _col("SALUD_MENTAL_ORG"),
        "claridad":          _col("CLARIDAD_ROL"),
        "conf_fam_trab":     _col("CONF_FAM_TRAB"),
        "conf_trab_fam":     _col("CONF_TRAB_FAM"),
    }


# --- Intentar cargar ---
try:
    df_original = load_data()
except FileNotFoundError as e:
    st.error(str(e))
    st.stop()

C = map_cols(df_original)

DIMS_TODAS = [
    C["presion"], C["lider"], C["apoyo"], C["conflicto"],
    C["cambio"], C["salud_mental"], C["claridad"], C["satisfaccion"],
    C["retiro"], C["conf_fam_trab"], C["conf_trab_fam"],
    C["burnout"], C["bienestar"], C["somatizacion"], C["desgaste"],
]
DIMS_ETIQUETAS = {
    C["presion"]:      "Presión de Tiempo",
    C["lider"]:        "Compromiso del Líder",
    C["apoyo"]:        "Apoyo de Compañeros",
    C["conflicto"]:    "Conflicto de Rol",
    C["cambio"]:       "Gestión del Cambio",
    C["salud_mental"]: "Salud Mental Org.",
    C["claridad"]:     "Claridad de Rol",
    C["satisfaccion"]: "Satisfacción Laboral",
    C["retiro"]:       "Intención de Retiro",
    C["conf_fam_trab"]:"Conflicto Fam→Trab",
    C["conf_trab_fam"]:"Conflicto Trab→Fam",
    C["burnout"]:      "Burnout",
    C["bienestar"]:    "Bienestar",
    C["somatizacion"]: "Somatización",
    C["desgaste"]:     "Desgaste",
}


# =============================================================================
# SIDEBAR — FILTROS GLOBALES
# =============================================================================
with st.sidebar:
    st.markdown("### 🧭 Filtros del Dashboard")
    st.markdown("---")

    sectores   = st.multiselect("Sector", df_original["Sector"].unique().tolist(),
                                default=df_original["Sector"].unique().tolist())
    modalidades = st.multiselect("Modalidad", df_original["Modalidad"].unique().tolist(),
                                 default=df_original["Modalidad"].unique().tolist())
    sexos = st.multiselect("Sexo", df_original["Sexo"].unique().tolist(),
                           default=df_original["Sexo"].unique().tolist())
    edad_rng = st.slider("Rango de Edad", int(df_original["Edad"].min()),
                         int(df_original["Edad"].max()),
                         (int(df_original["Edad"].min()), int(df_original["Edad"].max())))

    st.markdown("---")
    st.caption("📊 Bienestar Laboral EDA · v1.0")
    st.caption("🎓 Proyecto Final Análisis de Datos")

# Aplicar filtros globales
df = df_original[
    df_original["Sector"].isin(sectores) &
    df_original["Modalidad"].isin(modalidades) &
    df_original["Sexo"].isin(sexos) &
    df_original["Edad"].between(edad_rng[0], edad_rng[1])
].copy()

# =============================================================================
# HEADER PRINCIPAL
# =============================================================================
st.markdown(f"""
<div class="main-header">
    <h1>🧠 Dashboard · Bienestar Laboral</h1>
    <p>Análisis Exploratorio de Datos · Salud Psicosocial en el Trabajo &nbsp;|&nbsp;
       <strong>n = {len(df)}</strong> trabajadores seleccionados</p>
</div>
""", unsafe_allow_html=True)


# =============================================================================
# KPIs GLOBALES
# =============================================================================
def kpi(label, value, delta="", color="#17b978"):
    return f"""
    <div class="kpi-card" style="border-left-color:{color}">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-delta">{delta}</div>
    </div>"""


k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.markdown(kpi("Trabajadores", f"{len(df):,}", "muestra filtrada"), unsafe_allow_html=True)
with k2:
    bien_media = df[C["bienestar"]].mean()
    st.markdown(kpi("Bienestar Promedio", f"{bien_media:.2f}", "escala 1–10", C_SECONDARY), unsafe_allow_html=True)
with k3:
    burn_media = df[C["burnout"]].mean()
    color = C_WARN if burn_media > 6 else C_PRIMARY
    st.markdown(kpi("Burnout Promedio", f"{burn_media:.2f}", "escala 1–10", color), unsafe_allow_html=True)
with k4:
    sat_media = df[C["satisfaccion"]].mean()
    st.markdown(kpi("Satisfacción Laboral", f"{sat_media:.2f}", "escala 1–10", C_NEUTRAL), unsafe_allow_html=True)
with k5:
    ret_media = df[C["retiro"]].mean()
    color = C_WARN if ret_media > 5.5 else C_PRIMARY
    st.markdown(kpi("Intención de Retiro", f"{ret_media:.2f}", "escala 1–10", color), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# =============================================================================
# TABS DE ANÁLISIS
# =============================================================================
tabs = st.tabs([
    "📊 Perfil Demográfico",
    "📈 Ranking de Riesgo",
    "🔬 Bienestar por Grupo",
    "🔥 Burnout & Desgaste",
    "🤝 Rol del Liderazgo",
    "🎯 Predicción Retiro",
    "👥 Perfiles / Clustering",
    "🚨 Matriz de Intervención",
])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — PERFIL SOCIODEMOGRÁFICO
# ══════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown('<div class="section-header"><p>Pregunta 1 · ¿Cuál es el perfil sociodemográfico predominante de la muestra?</p></div>',
                unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    col_c, col_d = st.columns(2)

    # Sexo — Donut
    with col_a:
        counts = df["Sexo"].value_counts()
        fig = px.pie(values=counts.values, names=counts.index, hole=0.55,
                     color_discrete_sequence=[C_PRIMARY, C_NEUTRAL, C_SECONDARY])
        fig.update_traces(textposition="inside", textinfo="percent+label")
        fig.update_layout(title="Distribución por Sexo", title_font_color=C_PRIMARY,
                          showlegend=True, margin=dict(t=50, b=10), height=320)
        st.plotly_chart(fig, use_container_width=True)

    # Modalidad — Bar
    with col_b:
        counts = df["Modalidad"].value_counts().reset_index()
        counts.columns = ["Modalidad", "N"]
        fig = px.bar(counts, x="Modalidad", y="N", text="N",
                     color_discrete_sequence=[C_NEUTRAL])
        fig.update_traces(textposition="outside", marker_line_color=C_DARK, marker_line_width=1)
        fig.update_layout(title="Modalidad de Trabajo", title_font_color=C_PRIMARY,
                          yaxis_title="Trabajadores", xaxis_title="",
                          plot_bgcolor="white", margin=dict(t=50, b=10), height=320)
        st.plotly_chart(fig, use_container_width=True)

    # Sector — Bar horizontal
    with col_c:
        counts = df["Sector"].value_counts().reset_index()
        counts.columns = ["Sector", "N"]
        fig = px.bar(counts, y="Sector", x="N", text="N", orientation="h",
                     color_discrete_sequence=[C_PRIMARY])
        fig.update_traces(textposition="outside", marker_line_color=C_DARK, marker_line_width=1)
        fig.update_layout(title="Sector Organizacional", title_font_color=C_PRIMARY,
                          xaxis_title="N", yaxis_title="",
                          plot_bgcolor="white", margin=dict(t=50, b=10), height=320)
        st.plotly_chart(fig, use_container_width=True)

    # Edad — Histograma + KDE
    with col_d:
        fig = px.histogram(df, x="Edad", nbins=20, marginal="violin",
                           color_discrete_sequence=[C_PRIMARY])
        fig.update_traces(marker_line_color=C_DARK, marker_line_width=0.8)
        fig.update_layout(title="Distribución de Edad", title_font_color=C_PRIMARY,
                          bargap=0.05, plot_bgcolor="white",
                          margin=dict(t=50, b=10), height=320)
        st.plotly_chart(fig, use_container_width=True)

    # Tabla resumen
    with st.expander("📋 Tablas de frecuencia completas"):
        for col in ["Sexo", "Nivel_Educativo", "Sector", "Modalidad", "Estado_Civil"]:
            if col in df.columns:
                freq = df[col].value_counts().rename_axis(col).reset_index()
                freq.columns = [col, "N"]
                freq["%"] = (freq["N"] / freq["N"].sum() * 100).round(1).astype(str) + "%"
                st.dataframe(freq, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — RANKING DE RIESGO
# ══════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown('<div class="section-header"><p>Pregunta 2 · ¿Cuál es la distribución de las dimensiones y su priorización de riesgo?</p></div>',
                unsafe_allow_html=True)

    dims_presentes = [d for d in DIMS_TODAS if d in df.columns]
    df_desc = df[dims_presentes].describe().T
    df_desc["Asimetría"] = df[dims_presentes].skew()
    df_desc["Curtosis"]  = df[dims_presentes].kurt()
    df_desc.index = [DIMS_ETIQUETAS.get(i, i) for i in df_desc.index]
    df_ranking = df_desc.sort_values("mean", ascending=False)[["mean","50%","std","Asimetría","Curtosis"]]
    df_ranking.columns = ["Media","Mediana","Desv. Est.","Asimetría","Curtosis"]
    df_ranking = df_ranking.round(3)

    col_left, col_right = st.columns([1.2, 1])

    with col_left:
        # Boxplot horizontal
        fig = go.Figure()
        for i, dim in enumerate(reversed(dims_presentes)):
            label = DIMS_ETIQUETAS.get(dim, dim)
            fig.add_trace(go.Box(
                x=df[dim], name=label,
                orientation="h",
                marker_color=px.colors.sequential.Blues_r[i % 9],
                line_width=1.5, boxmean=True,
            ))
        fig.update_layout(
            title="Distribución Psicosocial — Priorización de Riesgo",
            title_font_color=C_PRIMARY,
            xaxis_title="Puntaje (1–10)", yaxis_title="",
            plot_bgcolor="white", showlegend=False,
            margin=dict(t=50, b=10), height=540,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        # Ranking bar chart
        df_rank_plot = df_ranking.reset_index().rename(columns={"index": "Dimensión"})
        fig2 = px.bar(df_rank_plot.sort_values("Media"), y="Dimensión", x="Media",
                      orientation="h", text=df_rank_plot.sort_values("Media")["Media"].round(2),
                      color="Media", color_continuous_scale=["#90b4ce","#1e3d59"],
                      title="Media por Dimensión (Mayor → Mayor Riesgo)")
        fig2.update_traces(textposition="outside")
        fig2.update_layout(coloraxis_showscale=False, plot_bgcolor="white",
                           title_font_color=C_PRIMARY,
                           margin=dict(t=50, b=10), height=540)
        st.plotly_chart(fig2, use_container_width=True)

    # Tabla de ranking
    st.markdown("**Tabla Estadística Completa**")
    st.dataframe(df_ranking,
                 use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — BIENESTAR POR GRUPO
# ══════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown('<div class="section-header"><p>Pregunta 3 · ¿Existen diferencias en el bienestar según cargo, sector o modalidad?</p></div>',
                unsafe_allow_html=True)

    factores_disponibles = [f for f in ["Tipo_Cargo", "Sector", "Modalidad"] if f in df.columns]
    factor_sel = st.radio("Comparar Bienestar por:", factores_disponibles, horizontal=True)

    col_box, col_violin = st.columns(2)

    with col_box:
        fig = px.box(df, x=factor_sel, y=C["bienestar"],
                     color=factor_sel,
                     color_discrete_sequence=[C_PRIMARY, C_NEUTRAL, C_SECONDARY, C_WARN],
                     title=f"Bienestar por {factor_sel.replace('_',' ')}")
        fig.update_layout(showlegend=False, plot_bgcolor="white",
                          title_font_color=C_PRIMARY, yaxis_title="Puntaje Bienestar",
                          margin=dict(t=50, b=10), height=380)
        st.plotly_chart(fig, use_container_width=True)

    with col_violin:
        fig = px.violin(df, x=factor_sel, y=C["bienestar"],
                        color=factor_sel, box=True, points="outliers",
                        color_discrete_sequence=[C_PRIMARY, C_NEUTRAL, C_SECONDARY, C_WARN],
                        title=f"Distribución de Bienestar (Violín)")
        fig.update_layout(showlegend=False, plot_bgcolor="white",
                          title_font_color=C_PRIMARY, yaxis_title="Puntaje Bienestar",
                          margin=dict(t=50, b=10), height=380)
        st.plotly_chart(fig, use_container_width=True)

    # Tabla descriptiva
    resumen = df.groupby(factor_sel)[C["bienestar"]].agg(
        N="count", Media="mean", Mediana="median",
        Desv_Est="std", Mínimo="min", Máximo="max"
    ).round(3)
    st.markdown(f"**Estadísticos descriptivos de Bienestar por {factor_sel.replace('_',' ')}**")
    st.dataframe(resumen,
                 use_container_width=True)

    # Comparación adicional: Bienestar vs Burnout por modalidad
    st.markdown("**Mapa de Dispersión: Bienestar vs Burnout segmentado**")
    fig3 = px.scatter(df, x=C["burnout"], y=C["bienestar"],
                      color=factor_sel, size=C["desgaste"], opacity=0.7,
                      color_discrete_sequence=[C_PRIMARY, C_NEUTRAL, C_SECONDARY, C_WARN],
                      labels={C["burnout"]: "Burnout", C["bienestar"]: "Bienestar",
                              C["desgaste"]: "Desgaste"},
                      title=f"Bienestar vs Burnout | color = {factor_sel.replace('_',' ')} | tamaño = Desgaste")
    fig3.update_layout(plot_bgcolor="white", title_font_color=C_PRIMARY, height=380,
                       margin=dict(t=50, b=10))
    st.plotly_chart(fig3, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — BURNOUT, DESGASTE & SOMATIZACIÓN
# ══════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown('<div class="section-header"><p>Pregunta 4 · ¿Cuál es la relación entre Burnout, Desgaste y Somatización?</p></div>',
                unsafe_allow_html=True)

    trio = [C["burnout"], C["desgaste"], C["somatizacion"]]
    labels_trio = ["Burnout", "Desgaste", "Somatización"]

    col_heat, col_scatter = st.columns([1, 1.5])

    with col_heat:
        corr_m = df[trio].corr().round(3)
        corr_m.index   = labels_trio
        corr_m.columns = labels_trio
        fig = px.imshow(corr_m, text_auto=True, color_continuous_scale="Blues",
                        zmin=-1, zmax=1, aspect="auto",
                        title="Correlación de Pearson")
        fig.update_layout(title_font_color=C_PRIMARY, margin=dict(t=50, b=10), height=360)
        st.plotly_chart(fig, use_container_width=True)

        corr_bd = df[C["burnout"]].corr(df[C["desgaste"]])
        corr_bs = df[C["burnout"]].corr(df[C["somatizacion"]])
        corr_ds = df[C["desgaste"]].corr(df[C["somatizacion"]])
        st.markdown(f"""
        <div class="insight-box">
        📌 <b>Correlaciones clave:</b><br>
        Burnout ↔ Desgaste: <b>r = {corr_bd:.3f}</b><br>
        Burnout ↔ Somatización: <b>r = {corr_bs:.3f}</b><br>
        Desgaste ↔ Somatización: <b>r = {corr_ds:.3f}</b>
        </div>
        """, unsafe_allow_html=True)

    with col_scatter:
        # Scatter matrix
        fig2 = px.scatter_matrix(df, dimensions=trio, color=C["burnout"],
                                 color_continuous_scale=["#90b4ce","#1e3d59"],
                                 labels={t: l for t, l in zip(trio, labels_trio)},
                                 title="Matriz de Dispersión — Síndrome Psicosomático")
        fig2.update_traces(diagonal_visible=False, showupperhalf=False, marker_size=4)
        fig2.update_layout(plot_bgcolor="white", title_font_color=C_PRIMARY,
                           coloraxis_showscale=False, height=360, margin=dict(t=50, b=10))
        st.plotly_chart(fig2, use_container_width=True)

    # Regplots interactivos
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        fig3 = px.scatter(df, x=C["desgaste"], y=C["burnout"], trendline="ols",
                          opacity=0.6, color_discrete_sequence=[C_NEUTRAL],
                          labels={C["desgaste"]: "Desgaste", C["burnout"]: "Burnout"},
                          title="Desgaste vs. Burnout (con regresión)")
        fig3.update_traces(marker_size=5)
        fig3.data[1].line.color = C_PRIMARY
        fig3.data[1].line.width = 2.5
        fig3.update_layout(plot_bgcolor="white", title_font_color=C_PRIMARY,
                           height=340, margin=dict(t=50, b=10))
        st.plotly_chart(fig3, use_container_width=True)

    with col_r2:
        fig4 = px.scatter(df, x=C["desgaste"], y=C["somatizacion"], trendline="ols",
                          opacity=0.6, color_discrete_sequence=[C_NEUTRAL],
                          labels={C["desgaste"]: "Desgaste", C["somatizacion"]: "Somatización"},
                          title="Desgaste vs. Somatización (con regresión)")
        fig4.update_traces(marker_size=5)
        fig4.data[1].line.color = C_SECONDARY
        fig4.data[1].line.width = 2.5
        fig4.update_layout(plot_bgcolor="white", title_font_color=C_PRIMARY,
                           height=340, margin=dict(t=50, b=10))
        st.plotly_chart(fig4, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — ROL DEL LIDERAZGO
# ══════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown('<div class="section-header"><p>Pregunta 5 · ¿Cuál es el rol del liderazgo en la satisfacción y el burnout?</p></div>',
                unsafe_allow_html=True)

    corr_sat  = df[C["lider"]].corr(df[C["satisfaccion"]])
    corr_burn = df[C["lider"]].corr(df[C["burnout"]])

    m1, m2, m3 = st.columns(3)
    m1.metric("r: Liderazgo → Satisfacción", f"{corr_sat:.3f}",
              "Relación positiva ✅" if corr_sat > 0 else "Relación negativa ⚠️")
    m2.metric("r: Liderazgo → Burnout", f"{corr_burn:.3f}",
              "Protector ✅" if corr_burn < 0 else "Factor de riesgo ⚠️")
    m3.metric("Media Compromiso Líder", f"{df[C['lider']].mean():.2f}",
              "escala 1–10")

    col_l, col_r = st.columns(2)
    with col_l:
        fig = px.scatter(df, x=C["lider"], y=C["satisfaccion"], trendline="ols",
                         opacity=0.55, color_discrete_sequence=[C_NEUTRAL],
                         labels={C["lider"]: "Compromiso del Líder",
                                 C["satisfaccion"]: "Satisfacción Laboral"},
                         title=f"Impacto en Satisfacción (r = {corr_sat:.3f})")
        fig.update_traces(marker_size=5, selector=dict(mode="markers"))
        fig.data[1].line.color = C_PRIMARY
        fig.data[1].line.width = 2.5
        fig.update_layout(plot_bgcolor="white", title_font_color=C_PRIMARY,
                          height=380, margin=dict(t=50, b=10))
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        fig2 = px.scatter(df, x=C["lider"], y=C["burnout"], trendline="ols",
                          opacity=0.55, color_discrete_sequence=[C_NEUTRAL],
                          labels={C["lider"]: "Compromiso del Líder",
                                  C["burnout"]: "Burnout"},
                          title=f"Mitigación del Burnout (r = {corr_burn:.3f})")
        fig2.update_traces(marker_size=5, selector=dict(mode="markers"))
        fig2.data[1].line.color = C_WARN
        fig2.data[1].line.width = 2.5
        fig2.update_layout(plot_bgcolor="white", title_font_color=C_PRIMARY,
                           height=380, margin=dict(t=50, b=10))
        st.plotly_chart(fig2, use_container_width=True)

    # Correlaciones del líder con todas las dimensiones
    st.markdown("**Correlaciones del Compromiso del Líder con todas las dimensiones**")
    corrs_lider = {DIMS_ETIQUETAS.get(d, d): df[C["lider"]].corr(df[d])
                   for d in dims_presentes if d in df.columns}
    df_corrs = pd.DataFrame.from_dict(corrs_lider, orient="index", columns=["Correlación"]).round(3)
    df_corrs = df_corrs.sort_values("Correlación")
    fig3 = px.bar(df_corrs.reset_index(), y="index", x="Correlación", orientation="h",
                  color="Correlación", color_continuous_scale=["#ff6b6b","white","#17b978"],
                  color_continuous_midpoint=0, text="Correlación",
                  title="Correlaciones del Liderazgo con Dimensiones Organizacionales")
    fig3.update_traces(textposition="outside")
    fig3.update_layout(yaxis_title="", xaxis_title="Correlación de Pearson (r)",
                       coloraxis_showscale=False, plot_bgcolor="white",
                       title_font_color=C_PRIMARY, height=420, margin=dict(t=50, b=10))
    st.plotly_chart(fig3, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 6 — MODELO PREDICTIVO DE RETIRO
# ══════════════════════════════════════════════════════════════════════════════
with tabs[5]:
    st.markdown('<div class="section-header"><p>Pregunta 6 · ¿Puede la satisfacción laboral predecir la intención de retiro?</p></div>',
                unsafe_allow_html=True)

    # OLS
    X_ols = sm.add_constant(df[C["satisfaccion"]])
    modelo = sm.OLS(df[C["retiro"]], X_ols).fit()

    r2     = modelo.rsquared
    pval   = modelo.pvalues[C["satisfaccion"]]
    beta   = modelo.params[C["satisfaccion"]]
    intercepto = modelo.params["const"]

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("R² del Modelo", f"{r2:.3f}", f"{r2*100:.1f}% varianza explicada")
    m2.metric("p-valor", f"{pval:.2e}", "Significativo ✅" if pval < 0.05 else "No significativo ⚠️")
    m3.metric("Pendiente (β)", f"{beta:.3f}", "Dirección del efecto")
    m4.metric("Intercepto", f"{intercepto:.3f}", "")

    col_s, col_r2 = st.columns([1.5, 1])

    with col_s:
        fig = px.scatter(df, x=C["satisfaccion"], y=C["retiro"], trendline="ols",
                         opacity=0.55, color_discrete_sequence=[C_NEUTRAL],
                         labels={C["satisfaccion"]: "Satisfacción Laboral",
                                 C["retiro"]: "Intención de Retiro"},
                         title=f"Satisfacción → Intención de Retiro (R² = {r2:.3f})")
        fig.update_traces(marker_size=5, selector=dict(mode="markers"))
        fig.data[1].line.color = C_ACCENT
        fig.data[1].line.width = 3
        fig.update_layout(plot_bgcolor="white", title_font_color=C_PRIMARY,
                          height=400, margin=dict(t=50, b=10))
        st.plotly_chart(fig, use_container_width=True)

    with col_r2:
        # Residuos
        residuos = modelo.resid
        fig2 = px.histogram(pd.DataFrame({"Residuos": residuos}), x="Residuos",
                            nbins=25, color_discrete_sequence=[C_PRIMARY],
                            title="Distribución de Residuos")
        fig2.update_traces(marker_line_color=C_DARK, marker_line_width=0.8)
        fig2.update_layout(plot_bgcolor="white", title_font_color=C_PRIMARY,
                           height=400, margin=dict(t=50, b=10))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown(f"""
    <div class="insight-box">
    📐 <b>Ecuación del modelo:</b>&nbsp;
    Intención de Retiro = {intercepto:.3f} + ({beta:.3f}) × Satisfacción Laboral<br>
    🔍 <b>Interpretación:</b> Por cada punto que sube la satisfacción, la intención de retiro
    {'<b>baja</b>' if beta < 0 else '<b>sube</b>'} <b>{abs(beta):.3f}</b> puntos.
    El modelo explica el <b>{r2*100:.1f}%</b> de la variabilidad en retiro.
    </div>
    """, unsafe_allow_html=True)

    with st.expander("Ver resumen completo del modelo OLS"):
        st.text(str(modelo.summary()))


# ══════════════════════════════════════════════════════════════════════════════
# TAB 7 — CLUSTERING K-MEANS
# ══════════════════════════════════════════════════════════════════════════════
with tabs[6]:
    st.markdown('<div class="section-header"><p>Pregunta 7 · ¿Es posible identificar perfiles diferenciados de trabajadores?</p></div>',
                unsafe_allow_html=True)

    features_clust = [C["bienestar"], C["burnout"], C["satisfaccion"], C["desgaste"]]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[features_clust])

    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df["Cluster"] = kmeans.fit_predict(X_scaled).astype(str)

    LABELS_CLUST = {"0": "Perfil A · Estable", "1": "Perfil B · En Riesgo Alto", "2": "Perfil C · Riesgo Moderado"}
    df["Perfil"] = df["Cluster"].map(LABELS_CLUST)

    col_s, col_b = st.columns([1.5, 1])

    with col_s:
        fig = px.scatter(df, x=C["burnout"], y=C["bienestar"],
                         color="Perfil", symbol="Perfil", opacity=0.8,
                         color_discrete_sequence=[C_SECONDARY, C_WARN, C_NEUTRAL],
                         labels={C["burnout"]: "Burnout", C["bienestar"]: "Bienestar"},
                         title="Segmentación K-Means (k=3): Perfiles de Salud Laboral")
        fig.update_traces(marker_size=8, marker_line_width=0.5, marker_line_color="white")
        fig.update_layout(plot_bgcolor="white", title_font_color=C_PRIMARY,
                          height=420, margin=dict(t=50, b=10))
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        # Medias por cluster
        df_perfiles = df.groupby("Perfil")[features_clust].mean().round(2)
        df_perfiles.columns = ["Bienestar","Burnout","Satisfacción","Desgaste"]
        df_perfiles["N"] = df["Perfil"].value_counts()

        fig2 = px.bar(df_perfiles.reset_index().melt(id_vars="Perfil", value_vars=["Bienestar","Burnout","Satisfacción","Desgaste"]),
                      x="variable", y="value", color="Perfil", barmode="group",
                      color_discrete_sequence=[C_SECONDARY, C_WARN, C_NEUTRAL],
                      title="Medias por Dimensión y Perfil",
                      labels={"variable": "Dimensión", "value": "Media"})
        fig2.update_layout(plot_bgcolor="white", title_font_color=C_PRIMARY,
                           height=420, margin=dict(t=50, b=10))
        st.plotly_chart(fig2, use_container_width=True)

    # Tabla de perfiles
    st.markdown("**Caracterización de Perfiles**")
    st.dataframe(df_perfiles,
                 use_container_width=True)

    # Radar chart
    df_radar = df.groupby("Perfil")[features_clust].mean()
    df_radar.columns = ["Bienestar","Burnout","Satisfacción","Desgaste"]
    categorias = df_radar.columns.tolist()

    fig3 = go.Figure()
    colores_radar = [C_SECONDARY, C_WARN, C_NEUTRAL]
    for (perfil, row), color in zip(df_radar.iterrows(), colores_radar):
        vals = row.tolist() + [row.tolist()[0]]
        cats = categorias + [categorias[0]]
        fig3.add_trace(go.Scatterpolar(r=vals, theta=cats, fill="toself",
                                       name=perfil, line_color=color,
                                       fillcolor=color + "44"))
    fig3.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,10])),
                       title="Radar de Perfiles Psicosociales", title_font_color=C_PRIMARY,
                       showlegend=True, height=420, margin=dict(t=60, b=20))
    st.plotly_chart(fig3, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 8 — MATRIZ DE INTERVENCIÓN
# ══════════════════════════════════════════════════════════════════════════════
with tabs[7]:
    st.markdown('<div class="section-header"><p>Pregunta 8 · Matriz Ejecutiva de Intervención Prioritaria</p></div>',
                unsafe_allow_html=True)

    # Calcular métricas actuales para el resumen ejecutivo
    burn_mean = df[C["burnout"]].mean()
    desg_mean = df[C["desgaste"]].mean()
    pres_mean = df[C["presion"]].mean()
    sat_mean  = df[C["satisfaccion"]].mean()
    ret_mean  = df[C["retiro"]].mean()
    lider_mean= df[C["lider"]].mean()

    # KPIs de riesgo
    st.markdown("#### 📊 Estado Actual de Indicadores Críticos")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🔴 Burnout", f"{burn_mean:.2f}/10",
              "CRÍTICO ⚠️" if burn_mean > 6 else "Moderado")
    c2.metric("🟠 Presión de Tiempo", f"{pres_mean:.2f}/10",
              "ALTO ⚠️" if pres_mean > 6 else "Moderado")
    c3.metric("🟡 Satisfacción", f"{sat_mean:.2f}/10",
              "BAJO ⚠️" if sat_mean < 5 else "Aceptable")
    c4.metric("🟢 Compromiso Líder", f"{lider_mean:.2f}/10",
              "BAJO ⚠️" if lider_mean < 5 else "Aceptable")

    st.markdown("---")
    st.markdown("#### 🚨 Matriz de Intervención Prioritaria")

    datos_intervencion = {
        "Dimensión": [
            "1. BURNOUT / DESGASTE",
            "2. PRESIÓN DE TIEMPO",
            "3. SATISFACCIÓN LABORAL",
        ],
        "Nivel de Urgencia": [
            "🔴 CRÍTICO (Prioridad 1)",
            "🟠 ALTO (Prioridad 2)",
            "🟠 ALTO (Prioridad 3)",
        ],
        "Sustento Estadístico": [
            f"Media Burnout = {burn_mean:.2f} | Correlación alta con Somatización (r > 0.65)",
            f"Media Presión = {pres_mean:.2f} | Primer detonante del desgaste diario",
            f"Media Satisfacción = {sat_mean:.2f} | Predictor directo de Intención de Retiro (r = {df[C['satisfaccion']].corr(df[C['retiro']]):.3f})",
        ],
        "Acción Mitigadora Recomendada": [
            "Implementar programas de primeros auxilios psicológicos y canales de descompresión emocional.",
            "Revisión de cargas de trabajo, metas y flexibilización de cronogramas/entregables.",
            "Fortalecer el Compromiso del Líder como recurso protector y revisar esquemas de reconocimiento.",
        ],
    }

    df_interv = pd.DataFrame(datos_intervencion)
    st.dataframe(df_interv, use_container_width=True, hide_index=True)

    st.markdown("---")

    # Heatmap de correlaciones globales
    st.markdown("#### 🔥 Heatmap de Correlaciones — Todas las Dimensiones")
    dims_hm = [d for d in DIMS_TODAS if d in df.columns]
    corr_global = df[dims_hm].corr().round(3)
    corr_global.index   = [DIMS_ETIQUETAS.get(i, i) for i in corr_global.index]
    corr_global.columns = [DIMS_ETIQUETAS.get(c, c) for c in corr_global.columns]

    fig = px.imshow(corr_global, text_auto=".2f", aspect="auto",
                    color_continuous_scale="RdBu_r", zmin=-1, zmax=1,
                    title="Correlaciones entre todas las dimensiones psicosociales")
    fig.update_layout(title_font_color=C_PRIMARY, height=560,
                      margin=dict(t=60, b=10),
                      coloraxis_colorbar=dict(title="r"))
    st.plotly_chart(fig, use_container_width=True)

    # Descargar datos filtrados
    st.markdown("---")
    st.markdown("#### 💾 Exportar Datos Filtrados")
    csv = df.drop(columns=["Cluster","Perfil"], errors="ignore").to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Descargar dataset filtrado (.csv)",
        data=csv,
        file_name="bienestar_laboral_filtrado.csv",
        mime="text/csv",
    )
