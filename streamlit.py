import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Configuração da página
st.set_page_config(page_title="Dashboard de Focos de Incêndio", layout="wide")

# Caminho do arquivo conforme sua estrutura
DATA_PATH = "data/processed/focos_br_2024_sample.csv"

@st.cache_data
def load_data(path):
    if not os.path.exists(path):
        st.error(f"Arquivo não encontrado em: {path}")
        return pd.DataFrame()
    df = pd.read_csv(path)
    # Converter data para datetime para facilitar filtros
    df['data'] = pd.to_datetime(df['data'])
    return df

# Carregamento dos dados
df = load_data(DATA_PATH)

if not df.empty:
    st.title("🔥 Monitoramento de Focos de Incêndio - Brasil 2024")

    # --- SIDEBAR (FILTROS) ---
    st.sidebar.header("Filtros")
    
    # Filtro de Estado
    estados = sorted(df['estado'].unique())
    selected_estados = st.sidebar.multiselect("Selecione os Estados", estados, default=[])

    # Filtro de Bioma
    biomas = sorted(df['bioma'].unique())
    selected_biomas = st.sidebar.multiselect("Selecione os Biomas", biomas, default=biomas)

    # Filtro de Mês
    meses = sorted(df['mes'].unique())
    selected_meses = st.sidebar.multiselect("Selecione os Meses", meses, default=meses)

    # Aplicando os filtros
    df_filtered = df.copy()
    if selected_estados:
        df_filtered = df_filtered[df_filtered['estado'].isin(selected_estados)]
    if selected_biomas:
        df_filtered = df_filtered[df_filtered['bioma'].isin(selected_biomas)]
    if selected_meses:
        df_filtered = df_filtered[df_filtered['mes'].isin(selected_meses)]

    # --- DASHBOARD PRINCIPAL ---
    
    # Indicadores Rápidos
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Focos", f"{len(df_filtered):,}")
    col2.metric("Média Risco de Fogo", f"{df_filtered['risco_fogo'].mean():.2f}")
    col3.metric("Municípios Afetados", df_filtered['municipio'].nunique())

    # Gráficos
    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        st.subheader("Focos por Estado")
        focos_estado = df_filtered['estado'].value_counts().reset_index()
        fig_estado = px.bar(focos_estado, x='count', y='estado', orientation='h', 
                           title="Quantidade de Focos por Estado", color='count',
                           color_continuous_scale='Reds')
        st.plotly_chart(fig_estado, use_container_width=True)

    with row1_col2:
        st.subheader("Evolução Mensal")
        focos_mes = df_filtered.groupby('mes').size().reset_index(name='quantidade')
        fig_mes = px.line(focos_mes, x='mes', y='quantidade', markers=True,
                         title="Tendência de Focos ao Longo dos Meses")
        st.plotly_chart(fig_mes, use_container_width=True)

    # Mapa de Calor (Amostra para performance se o dado for muito grande)
    st.subheader("Distribuição Geográfica (Amostra de 10k pontos)")
    map_sample = df_filtered.sample(n=min(10000, len(df_filtered)))
    st.map(map_sample[['lat', 'lon']])

    # Tabela de Dados
    if st.checkbox("Mostrar dados brutos (Filtrados)"):
        st.dataframe(df_filtered.head(100))

else:
    st.info("Aguardando carregamento dos dados ou arquivo não encontrado.")