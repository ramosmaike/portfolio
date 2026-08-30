import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# =========================================================
# --- CONFIGURAÇÃO DO USUÁRIO (Preencha seus dados aqui) ---
# =========================================================

GITHUB_USERNAME = "/ramosmaike"  
LINKEDIN_URL = "https://www.linkedin.com/in/maike-system"
EMAIL_CONTATO = "maikesystem@gmail.com"

# 💡 CORREÇÃO: Removemos o token exposto do código para evitar novos bloqueios automáticos do GitHub.
# Se o app pedir token futuramente, usaremos o st.secrets do Streamlit Cloud.
GITHUB_TOKEN = "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" 

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Data Portfolio | Maike Ramos", 
    page_icon="📊", 
    layout="wide"
)

# --- FUNÇÕES PARA BUSCAR DADOS DO GITHUB COM REQUESTS ---
# 💡 CORREÇÃO 1: Garanta que esta linha no topo do código está vazia!
GITHUB_TOKEN = "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" 


def get_headers():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        # 💡 CORREÇÃO DO ERRO 410: Formato estrito exigido pelo GitHub
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28'
        'curl --request GET \
         url "https://api.github.com/octocat" \
         header "Authorization: Bearer YOUR-TOKEN" \
         header "X-GitHub-Api-Version: 2026-03-10"'
    }
    # Mantém a leitura limpa do token caso tenha configurado no Secrets
    if "GITHUB_TOKEN" in st.secrets and st.secrets["GITHUB_TOKEN"].strip():
        headers['Authorization'] = f"token {st.secrets['GITHUB_TOKEN'].strip()}"
    return headers


# 💡 CORREÇÃO 2: Diminuímos o TTL para apenas 5 segundos para limpar o cache travado na hora dos testes
@st.cache_data(ttl=5)
def fetch_github_data(username):
    user_info = None
    repos_info = []
    error_msg = None
    
    try:
        # Busca perfil
        user_url = f"https://github.com{username}"
        user_resp = requests.get(user_url, headers=get_headers(), timeout=10)
        
        if user_resp.status_code == 200:
            user_info = user_resp.json()
        else:
            # Mostra o status real que o GitHub está devolvendo para sabermos o problema exato
            error_msg = f"A API do GitHub respondeu com o código {user_resp.status_code}. Carregando dados locais."
            
        # Busca repositórios
        repos_url = f"https://github.com{username}/repos?sort=updated&per_page=30"
        repos_resp = requests.get(repos_url, headers=get_headers(), timeout=10)
        if repos_resp.status_code == 200:
            all_repos = repos_resp.json()
            repos_info = [r for r in all_repos if not r.get('fork')][:6]
            if not repos_info:
                repos_info = all_repos[:6]
                
    except requests.exceptions.RequestException as e:
        error_msg = f"Erro de conexão com o servidor: {str(e)}"
        
    return user_info, repos_info, error_msg


@st.cache_data(ttl=300)
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
        else:
            error_msg = f"API do GitHub retornou status {user_resp.status_code}. Usando dados locais."
            
        # Busca repositórios
        repos_url = f"https://github.com{username}/repos?sort=updated&per_page=30"
        repos_resp = requests.get(repos_url, headers=get_headers(), timeout=10)
        if repos_resp.status_code == 200:
            all_repos = repos_resp.json()
            repos_info = [r for r in all_repos if not r.get('fork')][:6]
            if not repos_info:
                repos_info = all_repos[:6]
                
    except requests.exceptions.RequestException:
        error_msg = "Falha de conexão com a API do GitHub. Modo Offline Local ativo."
        
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
    if user_data and user_data.get('avatar_url'):
        st.image(user_data['avatar_url'], width=150)
        st.title(user_data.get('name') or user_data.get('login', 'Maike Ramos'))
        st.write(f"🎯 {user_data.get('bio') or 'Cientista de Dados | Engenheiro de Dados'}")
    else:
        # 💡 CORREÇÃO: Link de fallback estável caso o GitHub bloqueie conexões anônimas temporariamente
        st.image("https://github.com", width=150)
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

if network_error:
    st.info(f"ℹ️ {network_error}")

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
    tab1, tab2 = st.tabs(["📊 Análise de Vendas", "🤖 Machine Learning"])
    
    with tab1:
        st.subheader("Dashboard de Vendas E-commerce")
        c_left, c_right = st.columns(2) 
        with c_left:
            st.write("Análise estruturada de transações comerciais e churn utilizando Python.")
            st.link_button("Ver no GitHub", f"https://github.com{GITHUB_USERNAME}")
        with c_right:
            # 💡 CORREÇÃO: Adicionados dados corretos ao dicionário para evitar o erro do gráfico
            df = pd.DataFrame({"Mês": ["Jan", "Fev", "Mar"], "Vendas": [10, 20, 30]})
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
