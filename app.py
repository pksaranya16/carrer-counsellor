import streamlit as st
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# 1. Download necessary NLTK data packs (with the updated punkt_tab)
@st.cache_resource
def download_nltk_data():
    try:
        nltk.download('punkt')
        nltk.download('punkt_tab')  # Fixed the latest NLTK update error
        nltk.download('stopwords')
    except Exception as e:
        st.error(f"Error downloading NLTK data: {e}")

download_nltk_data()

# 2. Career Knowledge Base (Dictionary mapping keywords to career fields)
CAREER_DATABASE = {
    "Software Engineering": ["code", "programming", "software", "developer", "python", "java", "web", "app", "coding", "git", "backend", "frontend"],
    "Data Science & AI": ["data", "analytics", "statistics", "machine learning", "ai", "maths", "sql", "graphs", "dashboard", "powerbi", "excel"],
    "Digital Marketing": ["seo", "marketing", "ads", "social media", "content", "branding", "sales", "instagram", "campaign"],
    "UI/UX Design": ["ui", "ux", "graphics", "drawing", "design", "creative", "figma", "photoshop", "wireframe", "prototype"]
}

# 3. NLP Processing Function
def process_and_predict(user_text):
    # Step A: Tokenization
    words = word_tokenize(user_text.lower())
    
    # Step B: Stopwords Removal
    stop_words = set(stopwords.words('english'))
    cleaned_words = [w for w in words if w.isalnum() and w not in stop_words]
    
    # Step C: Score Calculation
    scores = {career: 0 for career in CAREER_DATABASE.keys()}
    for word in cleaned_words:
        for career, keywords in CAREER_DATABASE.items():
            if word in keywords:
                scores[career] += 1
                
    # Step D: Best career match pick
    best_fit = max(scores, key=scores.get)
    
    if scores[best_fit] == 0:
        return None
    
    return best_fit

# 4. Streamlit UI Layout Configuration
st.set_page_config(page_title="AI Career Guide Pro", page_icon="🎓", layout="centered")

st.title("🎓 NextGen AI Career Ecosystem")
st.write("Welcome! Unga career identity-a find panna keela erukura multi-method approach-a use pannunga.")

# --- NAVIGATION TABS ---
tab1, tab2 = st.tabs(["🔮 AI Text Predictor", "🧠 Psychometric Assessment"])

# ================= TAB 1: NLP WORK =================
with tab1:
    st.subheader("Discover via Natural Language Processing")
    st.write("Unga interests, skills, illa hobbies-a paragraph-a type pannunga.")
    
    user_input = st.text_area(
        label="Describe yourself:", 
        placeholder="Example: 'I love coding in Python and building websites.'",
        height=120,
        key="nlp_input"
    )

    if st.button("Predict My Career Path ✨", use_container_width=True):
        if not user_input.strip():
            st.error("Ennachu boss? Edhavadhu typed panniட்டு click pannunga!")
        else:
            with st.spinner("Analyzing text signature..."):
                prediction = process_and_predict(user_input)
                st.divider()
                if prediction:
                    st.balloons()
                    st.success(f"### 🎉 Recommended Path: **{prediction}**")
                    
                    if prediction == "Software Engineering":
                        st.info("📌 **Next Steps:** Data Structures (DSA) padinga, JavaScript/Python master pannunga.")
                    elif prediction == "Data Science & AI":
                        st.info("📌 **Next Steps:** Statistics basics cover pannunga, Python libraries learning focus pannunga.")
                    elif prediction == "Digital Marketing":
                        st.info("📌 **Next Steps:** Google Ads certification master pannunga, SEO strategies கத்துக்கோங்க.")
                    elif prediction == "UI/UX Design":
                        st.info("📌 **Next Steps:** Figma prototyping tool layout mockups design panni practice parunga.")
                else:
                    st.warning("🤔 Keyword match aagala! Try adding specific words like 'coding', 'analytics', 'design'.")

# ================= TAB 2: PSYCHOMETRIC TEST =================
with tab2:
    st.subheader("Quick Aptitude & Interest Alignment")
    st.write("Keela irukura statements-ku ungaluku endha alavu interest iruku nu choose pannunga (1 - Dislike, 5 - Love It!)")
    
    st.divider()
    
    # Questions mapped to careers
    q1 = st.slider("1. Designing user interfaces or sketching artistic creative ideas:", 1, 5, 3)
    q2 = st.slider("2. Writing automation scripts or solving logic puzzles via code:", 1, 5, 3)
    st.write("")
    q3 = st.slider("3. Analyzing mathematical patterns, charts, or managing large spreadsheets:", 1, 5, 3)
    q4 = st.slider("4. Planning social media campaigns or analyzing target customer trends:", 1, 5, 3)
    
    if st.button("Calculate Personality Score 📊", use_container_width=True):
        personality_scores = {
            "UI/UX Design": q1,
            "Software Engineering": q2,
            "Data Science & AI": q3,
            "Digital Marketing": q4
        }
        
        top_psych_career = max(personality_scores, key=personality_scores.get)
        
        st.divider()
        st.success(f"### 🧠 Psychometric Result: **{top_psych_career}**")
        st.write("Unga test mapping profile summary metric block-la kaati erukom:")
        
        # Render clean key metrics
        cols = st.columns(4)
        for idx, (career, score) in enumerate(personality_scores.items()):
            cols[idx].metric(label=career, value=f"{score}/5")
            
        st.caption("💡 **Tip:** NLP predictor tab values kooda indha metric score higher alignment match aagudha nu double check pannunga!")