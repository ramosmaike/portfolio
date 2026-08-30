import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# =========================================================
# CONFIGURAÇÕES
# =========================================================

GITHUB_USERNAME = "ramosmaike"
LINKEDIN_URL = "https://www.linkedin.com/in/maike-system"
EMAIL_CONTATO = "maikesystem@gmail.com"

st.set_page_config(
    page_title="Data Portfolio | Maike Ramos",
    page_icon="📊",
    layout="wide"
)

# =========================================================
# GITHUB API
# =========================================================

def get_headers():
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "Streamlit-Portfolio"
    }

    if "GITHUB_TOKEN" in st.secrets:
        headers["Authorization"] = f"Bearer {st.secrets['GITHUB_TOKEN']}"

    return headers


@st.cache_data(ttl=300)
def fetch_github_data(username):

    user_info = None
    repos_info = []
    error_msg = None

    try:
        user_url = f"https://api.github.com/users/{username}"

        repos_url = (
            f"https://api.github.com/users/"
            f"{username}/repos?sort=updated&per_page=30"
        )

        user_resp = requests.get(
            user_url,
            headers=get_headers(),
            timeout=10
        )

        repos_resp = requests.get(
            repos_url,
            headers=get_headers(),
            timeout=10
        )

        if user_resp.status_code == 200:
            user_info = user_resp.json()
        else:
            error_msg = (
                f"API do GitHub retornou status "
                f"{user_resp.status_code}"
            )

        if repos_resp.status_code == 200:
            all_repos = repos_resp.json()

            repos_info = [
                repo
                for repo in all_repos
                if not repo.get("fork")
            ][:6]

            if not repos_info:
                repos_info = all_repos[:6]

    except requests.exceptions.RequestException as e:
        error_msg = f"Erro de conexão: {e}"

    return user_info, repos_info, error_msg


user_data, top_repos, network_error = fetch_github_data(
    GITHUB_USERNAME
)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    if user_data and user_data.get("avatar_url"):

        st.image(
            user_data["avatar_url"],
            width=150
        )

        st.title(
            user_data.get(
                "name",
                "Maike Ramos"
            )
        )

        st.write(
            user_data.get(
                "bio",
                "Cientista de Dados"
            )
        )

    else:

        st.title("Maike Ramos")
        st.write("Cientista de Dados")

    st.divider()

    st.markdown("### Contato")

    st.write(f"📧 {EMAIL_CONTATO}")

    st.markdown(
        f"{LINKEDIN_URL}"
    )

    st.markdown(
        f"[GitHub](https://github.com/{GITHUB_USERNAME})"
    )

# =========================================================
# CONTEÚDO
# =========================================================

st.title("🚀 Data Science Portfolio")
st.subheader(
    "Transformando dados em decisões inteligentes"
)

if network_error:
    st.info(network_error)

col1, col2, col3, col4 = st.columns(4)

repos_publicos = (
    user_data["public_repos"]
    if user_data
    else 0
)

seguidores = (
    user_data["followers"]
    if user_data
    else 0
)

col1.metric("Repositórios", repos_publicos)
col2.metric("Experiência", "3 anos")
col3.metric("Seguidores", seguidores)
col4.metric("NPS Médio", "9.8")

st.divider()

st.header("📂 Projetos em Destaque")

if top_repos:

    for repo in top_repos:

        with st.container():

            st.subheader(repo["name"])

            st.write(
                repo.get(
                    "description",
                    "Sem descrição."
                )
            )

            st.write(
                f"⭐ {repo['stargazers_count']} | "
                f"🍴 {repo['forks_count']} | "
                f"🛠️ {repo.get('language', 'N/A')}"
            )

            st.link_button(
                "Abrir repositório",
                repo["html_url"]
            )

            st.divider()

else:

    st.warning(
        "Nenhum repositório encontrado."
    )

# =========================================================
# HABILIDADES
# =========================================================

st.header("🛠️ Habilidades")

skills = {
    "Python": 90,
    "SQL": 85,
    "Streamlit": 95,
    "Power BI": 80,
    "Scikit-Learn": 75
}

for skill, value in skills.items():
    st.write(skill)
    st.progress(value)

st.divider()
st.caption(
    "Desenvolvido com ❤️ usando Streamlit"
)