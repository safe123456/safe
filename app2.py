import streamlit as st
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import HuggingFaceHub
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import os

# --------------------------------------------------------
# CONFIGURATION DE LA PAGE
# --------------------------------------------------------
st.set_page_config(
    page_title="Assistant Investissement",
    page_icon="Briefcase",
    layout="wide",
)
# --------------------------------------------------------
# CONFIGURATION DE LA PAGE
# --------------------------------------------------------
st.set_page_config(
    page_title="Assistant Investissement",
    page_icon="💼",
    layout="wide",
)

# --------------------------------------------------------
# CSS POUR DESIGN MODERNE ET ANIMATIONS
# --------------------------------------------------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.title {
    font-size: 42px;
    font-weight: 600;
    color: #4A90E2;
    text-align: center;
    animation: fadein 2s ease-in-out;
}

.card {
    padding: 20px;
    border-radius: 15px;
    background-color: #F7F9FC;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    animation: slideIn 1s ease;
}

@keyframes fadein {
    from {opacity: 0;}
    to {opacity: 1;}
}

@keyframes slideIn {
    from {transform: translateY(10px); opacity: 0;}
    to {transform: translateY(0); opacity: 1;}
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------------
# TITRE ANIMÉ
# --------------------------------------------------------
st.markdown('<h1 class="title">💼 Assistant Intelligent d’Investissement</h1>', unsafe_allow_html=True)
st.write("### Optimisez votre stratégie financière en quelques clics ✔️")

# --------------------------------------------------------
# INITIALISATION SESSION STATE
# --------------------------------------------------------
if "profil" not in st.session_state:
    st.session_state.profil = None

if "allocation" not in st.session_state:
    st.session_state.allocation = None

# --------------------------------------------------------
# 1️⃣ COLLECTE DES INFORMATIONS UTILISATEUR
# --------------------------------------------------------
st.subheader("📝 Informations utilisateur")

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Âge", 18, 100)
    annual_income = st.number_input("Revenu Annuel (€)", min_value=0.0)

with col2:
    investment_horizon = st.selectbox("Horizon d'investissement", ["court", "moyen", "long"])
    risk_tolerance = st.selectbox("Tolérance au risque", ["faible", "modéré", "élevé"])

investment_goals = st.text_input("Objectifs d'investissement")

user_data = {
    "Âge": age,
    "Revenu Annuel": annual_income,
    "Horizon d'Investissement": investment_horizon,
    "Tolérance au Risque": risk_tolerance,
    "Objectifs d'Investissement": investment_goals,
}

# --------------------------------------------------------
# 2️⃣ CALCUL DU SCORE DE RISQUE ET PROFIL
# --------------------------------------------------------
def calculate_risk_score(user_data):
    score = 0

    if user_data['Âge'] < 30:
        score += 3
    elif user_data['Âge'] <= 50:
        score += 2
    else:
        score += 1

    horizon = user_data["Horizon d'Investissement"].lower()
    score += {"court": 1, "moyen": 2, "long": 3}[horizon]

    tol = user_data["Tolérance au Risque"].lower()
    score += {"faible": 1, "modéré": 2, "élevé": 3}[tol]

    return score


def get_risk_profile(risk_score):
    if risk_score <= 4:
        return "Prudent"
    elif risk_score <= 6:
        return "Équilibré"
    return "Dynamique"


# --------------------------------------------------------
# BOUTON ANALYSER
# --------------------------------------------------------
if st.button("Analyser mon profil"):
    risk_score = calculate_risk_score(user_data)
    profil = get_risk_profile(risk_score)

    # 🔥 STOCKAGE DANS SESSION STATE
    st.session_state.profil = profil
    st.session_state.allocation = {
        "Actions": 20 if profil == "Prudent" else (50 if profil == "Équilibré" else 80),
        "Obligations": 60 if profil == "Prudent" else (40 if profil == "Équilibré" else 15),
        "Liquidités": 20 if profil == "Prudent" else (10 if profil == "Équilibré" else 5)
    }

    st.markdown("### 🎯 Résultat")
    st.markdown(f"""
    <div class="card">
        <h3>Profil d'investisseur : {profil}</h3>
        <p><b>Score :</b> {risk_score}</p>
    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------------
# 3️⃣ AFFICHAGE ALLOCATION SI PROFIL EXISTE
# --------------------------------------------------------
if st.session_state.profil:
    st.subheader("📊 Allocation de portefeuille recommandée")

    allocation = st.session_state.allocation

    colA, colB, colC = st.columns(3)
    colA.metric("📈 Actions", f"{allocation['Actions']}%")
    colB.metric("💵 Obligations", f"{allocation['Obligations']}%")
    colC.metric("🏦 Liquidités", f"{allocation['Liquidités']}%")

    capital = st.number_input("Montant du capital à investir (€)", min_value=0.0)

    if capital > 0:
        st.markdown("### 💰 Allocation en montants")

        st.write(f"- Actions : *{capital * allocation['Actions'] / 100:.2f} €*")
        st.write(f"- Obligations : *{capital * allocation['Obligations'] / 100:.2f} €*")
        st.write(f"- Liquidités : *{capital * allocation['Liquidités'] / 100:.2f} €*")
     # --------------------------------------------------------
# --------------------------------------------------------
#4 AI-POWERED ROBO-ADVISOR – Vraie IA qui lit tes PDFs
# --------------------------------------------------------
st.markdown("<h2 style='text-align:center;color:#636efb;margin-top:50px;'>AI-Powered Robo-Advisor</h2>", unsafe_allow_html=True)
st.write("Posez n’importe quelle question sur vos documents (frais, duration, stratégie, risques…)")

# Charge l’IA une seule fois
if "robo" not in st.session_state:
    with st.spinner("L'IA lit tous vos documents PDF… (30-60 secondes la première fois)"):
        loader = PyPDFDirectoryLoader("docs")  # dossier "docs" à côté de app.py
        docs = loader.load()
        texts = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(docs)
        db = Chroma.from_documents(texts, HuggingFaceBgeEmbeddings(model_name="BAAI/bge-small-en-v1.5"))
        llm = HuggingFaceHub(repo_id="mistralai/Mistral-7B-Instruct-v0.3",
                             model_kwargs={"temperature": 0.3, "max_length": 1024})
        template = """Tu es un robo-advisor expert en finance.
Réponds en français, de façon claire et professionnelle, uniquement avec les informations des documents.

Contexte :
{context}

Question : {question}

Réponse détaillée :"""
        prompt = PromptTemplate(template=template, input_variables=["context", "question"])
        st.session_state.robo = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=db.as_retriever(search_kwargs={"k": 5}),
            chain_type_kwargs={"prompt": prompt}
        )
    st.balloons()
    st.success("Robo-Advisor IA activé ! Posez votre question")

# Chat intelligent
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if question := st.chat_input("Ex : Quels sont les frais ? Quelle est la duration ? Stratégie actions émergentes ?"):
    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message("user").write(question)

    with st.chat_message("assistant"):
        with st.spinner("Recherche dans les documents..."):
            result = st.session_state.robo.invoke({"query": question})
            reponse = result["result"]
        st.markdown(reponse)
        st.session_state.messages.append({"role": "assistant", "content": reponse})
