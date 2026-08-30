import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# =========================================================
# --- CONFIGURAÇÃO DO USUÁRIO (Preencha seus dados aqui) ---
# =========================================================

GITHUB_USERNAME = "ramosmaike"  
LINKEDIN_URL = "https://linkedin.com"
EMAIL_CONTATO = "maikesystem@gmail.com"

# IMPORTANTE: Se o token expirar ou der erro, deixe vazio: GITHUB_TOKEN = ""
GITHUB_TOKEN = "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" 

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title=f"Data Portfolio | Maike Ramos", 
    page_icon="📊", 
    layout="wide"
)

# --- FUNÇÕES PARA BUSCAR DADOS DO GITHUB COM REQUESTS ---
def get_headers():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Accept': 'application/vnd.github.v3+json'
    }
    if GITHUB_TOKEN and GITHUB_TOKEN.startswith("ghp_"):
        headers['Authorization'] = f"token {GITHUB_TOKEN}"
    return headers

@st.cache_data(ttl=600)
def fetch_github_data(username):
    user_info = None
    repos_info = []
    error_msg = None
    
    try:
        # Busca dados do perfil
        user_url = f"https://github.com{username}"
        user_resp = requests.get(user_url, headers=get_headers(), timeout=10)
        
        if user_resp.status_code == 200:
            user_info = user_resp.json()
        elif user_resp.status_code == 401:
            error_msg = "Token do GitHub expirado ou inválido."
        else:
            error_msg = f"Erro ao acessar perfil: Status {user_resp.status_code}"
            
        # Busca repositórios
        repos_url = f"https://github.com{username}/repos?sort=updated&per_page=30"
        repos_resp = requests.get(repos_url, headers=get_headers(), timeout=10)
        if repos_resp.status_code == 200:
            all_repos = repos_resp.json()
            # Filtra para não pegar forks dos outros
            repos_info = [r for r in all_repos if not r.get('fork')][:6]
            if not repos_info:
                repos_info = all_repos[:6]
                
    except requests.exceptions.RequestException:
        error_msg = "Não foi possível conectar à API do GitHub (Modo Offline Local)."
        
    return user_info, repos_info, error_msg

# Executa as buscas de dados de forma segura
user_data, top_repos, network_error = fetch_github_data(GITHUB_USERNAME)

# Estilo CSS Personalizado
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .repo-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 8px;
        border-left: 5px solid #238636;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 15px;
        height: 180px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    if user_data and 'avatar_url' in user_data:
        st.image(user_data['avatar_url'], width=150)
        st.title(user_data.get('name') or user_data.get('login', 'Maike Ramos'))
        st.write(f"🎯 {user_data.get('bio') or 'Cientista de Dados | Engenheiro de Dados'}")
    else:
        # Fallback fixo se a rede cair (usa uma imagem padrão para não quebrar a tela)
        st.image("https://flaticon.com", width=150)
        st.title("Maike Ramos")
        st.write("🎯 Cientista de Dados | Engenheiro de Dados")
    
    st.write("---")
    st.markdown("### Contato")
    st.write(f"📧 {EMAIL_CONTATO}")
    st.write(f"🔗 [LinkedIn]({LINKEDIN_URL})")
    st.write(f"🐙 [GitHub](https://github.com{GITHUB_USERNAME})")

# --- CORPO PRINCIPAL DO PORTFÓLIO ---
st.title("🚀 Data Science Portfolio")
st.subheader("Transformando dados em decisões inteligentes")

# Alerta caso a API tenha falhado
if network_error:
    st.info(f"ℹ️ Nota: {network_error} Exibindo dados locais pré-configurados.")

# --- MÉTRICAS ---
col1, col2, col3, col4 = st.columns(4)

repos_publicos = str(user_data['public_repos']) if user_data else "12"
seguidores = str(user_data['followers']) if user_data else "8"

col1.metric("Repositórios", repos_publicos, "Públicos")
col2.metric("Experiência", "3 Anos", "Pleno/Sênior")
col3.metric("Seguidores", seguidores, "No GitHub")
col4.metric("NPS Médio", "9.8", "Satisfação")

st.write("---")

# --- SEÇÃO DE PROJETOS DINÂMICOS DO GITHUB ---
st.header("📂 Projetos em Destaque")

if top_repos:
    for i in range(0, len(top_repos), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(top_repos):
                repo = top_repos[i + j]
                with cols[j]:
                    desc = repo.get('description') or "Sem descrição disponível no repositório."
                    st.markdown(f"""
                    <div class="repo-card">
                        <h4>{'🍴 ' if repo.get('fork') else '⭐ '} {repo.get('name')}</h4>
                        <p style="font-size: 14px; color: #57606a;">{desc}</p>
                        <p style="font-size: 12px; font-weight: bold;">⭐ {repo.get('stargazers_count', 0)} estrelas | 🍴 {repo.get('forks_count', 0)} forks | 🛠️ {repo.get('language') or 'Python'}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.link_button("Acessar Repositório", repo.get('html_url', '#'), key=f"repo_{repo.get('id', i+j)}")
else:
    # Mostra abas fixas caso o usuário não tenha repositórios públicos ainda
    tab1, tab2 = st.tabs(["📊 Análise de Vendas", "🤖 Machine Learning"])
    
    with tab1:
        st.subheader("Dashboard de Vendas E-commerce")
        c_left, c_right = st.columns(2) 
        with c_left:
            st.write("Análise estruturada de transações comerciais e churn utilizando Python.")
            st.link_button("Ver no GitHub", f"https://github.com{GITHUB_USERNAME}")
        with c_right:
            df = pd.DataFrame({"Mês": ["Jan", "Fev", "Mar"], "Vendas": [4200, 5100, 6400]})
            st.plotly_chart(px.line(df, x="Mês", y="Vendas", template="plotly_white"), use_container_width=True)
            
    with tab2:
        st.subheader("Previsão de Preços de Imóveis")
        df_ml = px.data.iris()
        st.plotly_chart(px.scatter(df_ml, x="sepal_width", y="sepal_length", title="Modelo de Clusterização"), use_container_width=True)

# --- HABILIDADES ---
st.write("---")
st.header("🛠️ Habilidades Técnicas")
skills = {
    "Python": 90, "SQL": 85, "Streamlit": 95, "Power BI": 80, "Scikit-Learn": 75
}

cols = st.columns(len(skills))
for i, (skill, value) in enumerate(skills.items()):
    cols[i].write(f"**{skill}**")
    cols[i].progress(value)

# --- RODAPÉ ---
st.write("---")
st.caption("Desenvolvido com ❤️ usando Streamlit e Python")
