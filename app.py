import streamlit as st

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
# 4️⃣ CHATBOT MODERNE
# --------------------------------------------------------
st.subheader("🤖 Chatbot intelligent")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

prompt = st.chat_input("Posez une question financière…")

def chatbot_reply(question):

    question = question.lower()

    if "profil" in question:
        if st.session_state.profil:
            return f"Votre profil est *{st.session_state.profil}*."
        else:
            return "Veuillez d'abord analyser votre profil."

    if "allocation" in question:
        if st.session_state.allocation:
            allocation = st.session_state.allocation
            return (
                f"Votre allocation actuelle est :\n"
                f"- Actions : {allocation['Actions']}%\n"
                f"- Obligations : {allocation['Obligations']}%\n"
                f"- Liquidités : {allocation['Liquidités']}%"
            )
        else:
            return "Veuillez analyser votre profil d'abord."



    if "risque" in question:
        if st.session_state.profil:
            return {
                "Prudent": "Faible risque, placements sûrs.",
                "Équilibré": "Équilibre entre risque et rendement.",
                "Dynamique": "Risque élevé, rendement potentiel élevé."
            }[st.session_state.profil]
        else:
            return "Votre profil n'est pas encore analysé."

    if "bonjour" in question:
        return "Bonjour 👋 ! Comment puis-je vous aider ?"

    return "Je n'ai pas compris votre question. Essayez : 'profil', 'allocation', 'risque'."

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = chatbot_reply(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
fonts.googleapis.com
