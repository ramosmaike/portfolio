import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import base64

# =====================================================
# CONFIG
# =====================================================

GITHUB_USERNAME = "ramosmaike"
LINKEDIN_URL = "https://www.linkedin.com/in/maike-system"
EMAIL = "maikesystem@gmail.com"

st.set_page_config(
    page_title="Maike Ramos | Portfolio",
    page_icon="🚀",
    layout="wide"
)

# =====================================================
# CSS
# =====================================================

st.markdown("""
<style>

.main{
    background-color:#f8fafc;
}

.repo-card{
    padding:20px;
    border-radius:10px;
    background:white;
    border-left:5px solid #238636;
    margin-bottom:15px;
    box-shadow:0 2px 8px rgba(0,0,0,0.08);
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADERS
# =====================================================

def get_headers():

    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "StreamlitPortfolio"
    }

    if "GITHUB_TOKEN" in st.secrets:
        headers["Authorization"] = f"Bearer {st.secrets['GITHUB_TOKEN']}"

    return headers

# =====================================================
# GITHUB API
# =====================================================

@st.cache_data(ttl=600)
def get_profile(username):

    url = f"https://api.github.com/users/{username}"

    response = requests.get(
        url,
        headers=get_headers()
    )

    if response.status_code == 200:
        return response.json()

    return None

# =====================================================
# REPOS
# =====================================================

@st.cache_data(ttl=600)
def get_repositories(username):

    url = f"https://api.github.com/users/{username}/repos?sort=updated&per_page=100"

    response = requests.get(
        url,
        headers=get_headers()
    )

    if response.status_code == 200:

        repos = response.json()

        repos = sorted(
            repos,
            key=lambda x: x["stargazers_count"],
            reverse=True
        )

        return repos

    return []

# =====================================================
# README
# =====================================================

@st.cache_data(ttl=600)
def get_readme(owner, repo):

    url = f"https://api.github.com/repos/{owner}/{repo}/readme"

    response = requests.get(
        url,
        headers=get_headers()
    )

    if response.status_code == 200:

        content = response.json()["content"]

        return base64.b64decode(content).decode(
            "utf-8",
            errors="ignore"
        )

    return None

# =====================================================
# LOAD
# =====================================================

profile = get_profile(GITHUB_USERNAME)
repos = get_repositories(GITHUB_USERNAME)

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    if profile:

        st.image(
            profile["avatar_url"],
            width=180
        )

        st.title(
            profile.get("name", GITHUB_USERNAME)
        )

        st.write(
            profile.get(
                "bio",
                "Data Scientist"
            )
        )

    st.divider()

    st.markdown(
        f"📧 **Email:** {EMAIL}"
    )

    st.markdown(
        f"{LINKEDIN_URL}"
    )

    st.markdown(
        f"[GitHub](https://github.com/{GITHUB_USERNAME})"
    )

# =====================================================
# HEADER
