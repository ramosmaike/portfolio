import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# ==========================
# CONFIGURAÇÃO
# ==========================

USERNAME = "ramosmaike"

st.set_page_config(
    page_title="Maike Ramos",
    page_icon="🚀",
    layout="wide"
)

# ==========================
# FUNÇÕES GITHUB
# ==========================

@st.cache_data(ttl=600)
def get_profile():

    url = f"https://api.github.com/users/{USERNAME}"

    response = requests.get(url, timeout=10)

    if response.status_code == 200:
        return response.json()

    return None


@st.cache_data(ttl=600)
def get_repos():

    url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100"

    response = requests.get(url, timeout=10)

    if response.status_code == 200:

        repos = response.json()

        repos = [
            repo
            for repo in repos
            if not repo["fork"]
        ]

        repos.sort(
            key=lambda x: x["stargazers_count"],
            reverse=True
        )

        return repos

    return []


# ==========================
# CARREGA DADOS
# ==========================

perfil = get_profile()
repos = get_repos()

# ==========================
# SIDEBAR
# ==========================

with st.sidebar:

    if perfil:

        st.image(
            perfil["avatar_url"],
            width=200
        )

        st.title(
            perfil.get("name", "Maike Ramos")
        )

        st.write(
            perfil.get(
                "bio",
                "Analista de Dados"
            )
        )

    st.divider()

    st.write("### 📬 Contato")

    st.markdown("📱 **Celular:** " 
        "[+55 (11) 96024-0070](https://wa.me)"
)


    st.markdown("📧 **Email:** "
        "[maikesystem@gmail.com](mailto:maikesystem@gmail.com)"
)

    st.markdown(
        "🔗 **LinkedIn:** "
        "[linkedin.com/in/maike-"
        "system](https://www.linkedin.com/in/maike-system)"
    )

    st.markdown(
        "🐙 **GitHub:** "
        "[github.com/ramosmaike](https://github.com/ramosmaike)"
    )

# ==========================
# TOPO
# ==========================

st.title("🚀 Maike Ramos")

st.subheader(
    "Data Science | Python | Automação"
)

# ==========================
# MÉTRICAS
# ==========================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Repos",
    perfil["public_repos"] if perfil else 0
)

col2.metric(
    "Seguidores",
    perfil["followers"] if perfil else 0
)

col3.metric(
    "Following",
    perfil["following"] if perfil else 0
)

col4.metric(
    "Projetos",
    len(repos)
)

# ==========================
# LINGUAGENS
# ==========================

st.divider()

st.header("📊 Tecnologias")

linguagens = {}

for repo in repos:

    linguagem = repo.get("language")

    if linguagem:

        linguagens[linguagem] = (
            linguagens.get(linguagem, 0) + 1
        )

if linguagens:

    df = pd.DataFrame({
        "Linguagem": list(linguagens.keys()),
        "Quantidade": list(linguagens.values())
    })

    fig = px.bar(
        df,
        x="Linguagem",
        y="Quantidade",
        color="Linguagem"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================
# MEUS PROJETOS
# ==========================

st.divider()

st.header("📂 Meus Projetos")

if repos:

    for repo in repos[:10]:

        st.subheader(repo["name"])

        st.write(
            repo.get(
                "description",
                "Sem descrição"
            )
        )

        c1, c2, c3 = st.columns(3)

        c1.write(
            f"⭐ {repo['stargazers_count']}"
        )

        c2.write(
            f"🍴 {repo['forks_count']}"
        )

        c3.write(
            repo.get(
                "language",
                "N/A"
            )
        )

        st.link_button(
            "Abrir Projeto",
            repo["html_url"]
        )

        st.divider()

else:

    st.warning(
        "Nenhum repositório encontrado."
    )

# ==========================
# SKILLS
# ==========================

st.header("🛠️ Skills")

skills = {
    "Python": 95,
    "SQL": 90,
    "Streamlit": 95,
    "Power BI": 85,
    "Pandas": 90,
    "Machine Learning": 80
}

for skill, valor in skills.items():

    st.write(skill)
    st.progress(valor)

# ==========================
# SOBRE
# ==========================

st.divider()

st.header("👨‍💻 Sobre")

st.write("""
Analista de Dados com foco em Python,
Automação, ETL, Machine Learning,
Power BI e desenvolvimento de soluções
orientadas por dados.
""")

st.divider()

st.caption(
    "Desenvolvido com Streamlit 🚀"
)
