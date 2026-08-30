import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import base64

# =====================================
# CONFIGURAÇÃO
# =====================================

GITHUB_USERNAME = "ramosmaike"

EMAIL = "maikesystem@gmail.com"

LINKEDIN = "https://www.linkedin.com/in/maike-system"

st.set_page_config(
    page_title="Maike Ramos | Portfólio",
    page_icon="🚀",
    layout="wide"
)

# =====================================
# ESTILO
# =====================================

st.markdown("""readme
<style>

.repo-card{
    background:#ffffff;
    padding:20px;
    border-radius:12px;
    border:1px solid #e5e7eb;
    margin-bottom:15px;
}

.metric-container{
    text-align:center;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# GITHUB API
# =====================================

def github_headers():

    headers = {
        "Accept":"application/vnd.github+json",
        "User-Agent":"StreamlitPortfolio"
    }

    if "GITHUB_TOKEN" in st.secrets:
        headers["Authorization"] = (
            f"Bearer {st.secrets['GITHUB_TOKEN']}"
        )

    return headers

# =====================================
# PERFIL
# =====================================

@st.cache_data(ttl=600)
def get_profile():

    url = (
        f"https://api.github.com/users/"
        f"{GITHUB_USERNAME}"
    )

    response = requests.get(
        url,
        headers=github_headers(),
        timeout=20
    )

    if response.status_code == 200:
        return response.json()

    return None

# =====================================
# REPOSITÓRIOS
# =====================================

@st.cache_data(ttl=600)
def get_repositories():

    url = (
        f"https://api.github.com/users/"
        f"{GITHUB_USERNAME}/repos?per_page=100"
    )

    response = requests.get(
        url,
        headers=github_headers(),
        timeout=20
    )

    if response.status_code != 200:
        return []

    repos = response.json()

    # Apenas reposit
