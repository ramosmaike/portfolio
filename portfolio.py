import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import base64

# =====================================================
# CONFIGURAÇÃO
# =====================================================

GITHUB_USERNAME = "ramosmaike"

NOME = "Maike Ramos"
CARGO = "Analista de Dados | Data Science | Automação Python"

EMAIL = "maikesystem@gmail.com"

LINKEDIN = "https://www.linkedin.com/in/maike-system"

# =====================================================
# STREAMLIT
# =====================================================

st.set_page_config(
    page_title="Maike Ramos | Portfólio",
    page_icon="🚀",
    layout="wide"
)

# =====================================================
# CSS
# =====================================================

st.markdown("""
<style>

.main {
    background-color: #f8fafc;
}

.block-container{
    padding-top:2rem;
}

.metric-card{
    background:white;
    padding:20px;
    border-radius:12px;
    box-shadow:0px 2px 8px rgba(0,0,0,0.08);
}

.repo-card{
    background:white;
    padding:20px;
    border-radius:12px;
    box-shadow:0px 2px 8px rgba(0,0,0,0.08);
    margin-bottom:15px;
}

.hero-title{
    font-size:42px;
    font-weight:bold;
}

.hero-subtitle{
    font-size:20px;
    color:#666;
}

</style>
""",
unsafe_allow_html=True)

# =====================================================
# HEADERS
# =====================================================

def get_headers():

    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "Portfolio-App"
    }

    if "GITHUB_TOKEN" in st.secrets:
        headers["Authorization"] = (
            f"Bearer {st.secrets['GITHUB_TOKEN']}"
        )

    return headers

# =====================================================
# PERFIL
# =====================================================

@st.cache_data(ttl=600)
def get_profile(username):

    url = f"https://api.github.com/users/{username}"

    response = requests.get(
        url,
        headers=get_headers(),
        timeout=20
    )

    if response.status_code == 200:
        return response.json()

    return None

# =====================================================
# REPOSITÓRIOS
# =====================================================

@st.cache_data(ttl=600)
def get_repositories(username):

    url = (
        f"https://api.github.com/users/"
        f"{username}/repos?per_page=100"
    )

    response = requests.get(
        url,
        headers=get_headers(),
        timeout=20
    )

    if response.status_code == 200:

        repos = response.json()

        repos.sort(
            key=lambda x: x["stargazers_count"],
            reverse=True
        )

        return repos

    return []

# =====================================================
# README
# =====================================================

@st.cache_data(ttl=600)
def get_readme(user, repo):

    url = (
        f"https://api.github.com/repos/"
        f"{user}/{repo}/readme"
    )

    response = requests.get(
        url,
        headers=get_headers(),
        timeout=20
    )

    if response.status_code == 200:

        content = response.json()["content"]

        try:
            return base64.b64decode(content).decode(
                "utf-8",
                errors="ignore"
            )
        except:
            return None

    return None

# =====================================================
# DADOS
# =====================================================

perfil = get_profile(GITHUB_USERNAME)
repos = get_repositories(GITHUB_USERNAME)

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    if perfil:

        st.image(
            perfil["avatar_url"],
            width=220
        )

        st.title(
            perfil.get("name", NOME)
        )

        st.write(
            perfil.get(
                "bio",
                CARGO
            )
        )

    else:

        st.title(NOME)
        st.write(CARGO)

    st.divider()

    st.markdown(f"📧 **{EMAIL}**")

    st.markdown(
        f"{LINKEDIN}"
    )

    st.markdown(
        f"[GitHub](https://github.com/{GITHUB_USERNAME})"
    )

# =====================================================
# HERO
# =====================================================

st.markdown(
    f"""
    <div class="hero-title">
    🚀 {NOME}
    </div>

    <div class="hero-subtitle">
    {CARGO}
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")

# =====================================================
# MÉTRICAS
# =====================================================

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Repos Públicos",
    perfil["public_repos"] if perfil else 0
)

c2.metric(
    "Seguidores",
    perfil["followers"] if perfil else 0
)

c3.metric(
    "Following",
    perfil["following"] if perfil else 0
)

c4.metric(
    "Projetos",
    len(repos)
)

st.divider()

# =====================================================
# GRÁFICOS
# =====================================================

st.header("📊 Analytics")

linguagens = {}

for repo in repos:

    linguagem = repo.get("language")

    if linguagem:

        linguagens[linguagem] = (
            linguagens.get(linguagem, 0) + 1
        )

if linguagens:

    df_lang = pd.DataFrame({
        "Linguagem": linguagens.keys(),
        "Repos": linguagens.values()
    })

    col1, col2 = st.columns(2)

    with col1:

        fig = px.pie(
            df_lang,
            names="Linguagem",
            values="Repos",
            title="Linguagens Utilizadas"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        fig2 = px.bar(
            df_lang,
            x="Linguagem",
            y="Repos",
            title="Quantidade por Linguagem"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

# =====================================================
# ESTATÍSTICAS GITHUB
# =====================================================

st.header("📈 GitHub Stats")

col1, col2 = st.columns(2)

with col1:

    st.image(
        f"https://github-readme-stats.vercel.app/api?username={GITHUB_USERNAME}&show_icons=true"
    )

with col2:

    st.image(
        f"https://github-readme-stats.vercel.app/api/top-langs/?username={GITHUB_USERNAME}&layout=compact"
    )

st.subheader
