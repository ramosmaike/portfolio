import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import base64

# ==========================================
# CONFIG
# ==========================================

GITHUB_USERNAME = "ramosmaike"

NOME = "Maike Ramos"
TITULO = "Analista de Dados | Data Science"

EMAIL = "maikesystem@gmail.com"

LINKEDIN = "https://www.linkedin.com/in/maike-system"

st.set_page_config(
    page_title="Maike Ramos | Portfólio",
    page_icon="🚀",
    layout="wide"
)

# ==========================================
# CSS
# ==========================================

st.markdown("""
<style>

.block-container{
    padding-top:2rem;
}

.repo-card{
    padding:20px;
    border-radius:12px;
    background:white;
    border:1px solid #e5e7eb;
    margin-bottom:15px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# GITHUB
# ==========================================

def headers():
    return {
        "Accept": "application/vnd.github+json",
        "User-Agent": "Streamlit"
    }

@st.cache_data(ttl=600)
def get_profile():

    url = f"https://api.github.com/users/{GITHUB_USERNAME}"

    r = requests.get(url, headers=headers(), timeout=20)

    if r.status_code == 200:
        return r.json()

    return None


@st.cache_data(ttl=600)
def get_repos():

    url = (
        f"https://api.github.com/users/"
        f"{GITHUB_USERNAME}/repos?per_page=100"
    )

    r = requests.get(url, headers=headers(), timeout=20)

    if r.status_code == 200:

        repos = r.json()

        repos.sort(
            key=lambda x: x["stargazers_count"],
            reverse=True
        )

        return repos

    return []


@st.cache_data(ttl=600)
def get_readme(repo):

    url = (
        f"https://api.github.com/repos/"
        f"{GITHUB_USERNAME}/{repo}/readme"
    )

    r = requests.get(
        url,
        headers=headers(),
        timeout=20
    )

    if r.status_code == 200:

        conteudo = r.json()["content"]

        return (
            base64
            .b64decode(conteudo)
            .decode("utf-8", errors="ignore")
        )

    return None


perfil = get_profile()
repos = get_repos()

# ==========================================
# SIDEBAR
# ==========================================

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
            perfil.get("bio", TITULO)
        )

    else:

        st.title(NOME)
        st.write(TITULO)

    st.divider()

    st.write("📧", EMAIL)

    st.markdown(
        f"{LINKEDIN}"
    )

    st.markdown(
        f"[GitHub](https://github.com/{GITHUB_USERNAME})"
    )

# ==========================================
# CABEÇALHO
# ==========================================

st.title("🚀 Portfólio Data Science")

st.subheader(
    "Transformando dados em decisões"
)

# ==========================================
# MÉTRICAS
# ==========================================

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Repos",
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

# ==========================================
# ESTATÍSTICAS
# ==========================================

st.divider()

st.header("📊 Linguagens")

linguagens = {}

for repo in repos:

    linguagem = repo.get("language")

    if linguagem:

        linguagens[linguagem] = (
            linguagens.get(linguagem, 0) + 1
        )

if linguagens:

    df = pd.DataFrame({
        "Linguagem": linguagens.keys(),
        "Repos": linguagens.values()
    })

    fig = px.pie(
        df,
        names="Linguagem",
        values="Repos"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================================
# PROJETOS
# ==========================================

st.divider()

st.header("📂 Projetos")

for repo in repos[:8]:

    descricao = repo.get(
        "description",
        "Sem descrição"
    )

    st.markdown(
        f"""
        <div class='repo-card'>
        <h3>{repo['name']}</h3>

        <p>{descricao}</p>

        ⭐ {repo['stargazers_count']}
        |
        🍴 {repo['forks_count']}
        |
        💻 {repo.get('language','N/A')}
        </div>
        """,

        unsafe_allow_html=True
    )

    st.link_button(
        "Abrir Repositório",
        repo["html_url"]
    )

# ==========================================
# README
# ==========================================

st.divider()

st.header("📖 README")

if repos:

    repo_escolhido = st.selectbox(
        "Escolha um projeto",
        [r["name"] for r in repos]
    )

    readme = get_readme(
        repo_escolhido
    )

    if readme:

        with st.expander(
            "Visualizar README",
            expanded=True
        ):
            st.markdown(readme)

    else:

        st.warning(
            "README não encontrado."
        )

# ==========================================
# HABILIDADES
# ==========================================

st.divider()

st.header("🛠️ Skills")

skills = {
    "Python":95,
    "SQL":90,
    "Streamlit":95,
    "Pandas":90,
    "Power BI":85,
    "Machine Learning":80,
    "Selenium":90
}

for nome, valor in skills.items():

    st.write(nome)

    st.progress(valor)

# ==========================================
# SOBRE
# ==========================================

st.divider()

st.header("👨‍💻 Sobre")

st.write("""
Profissional focado em Data Science,
Python, automação, ETL,
Machine Learning,
dashboards e análise de dados.
""")

# ==========================================
# CONTATO
# ==========================================

st.divider()

st.header("📬 Contato")

st.write(f"Email: {EMAIL}")
st.write(f"LinkedIn: {LINKEDIN}")
st.write(f"GitHub: https://github.com/{GITHUB_USERNAME}")

st.divider()

st.caption(
    "Desenvolvido com Streamlit 🚀"
)
