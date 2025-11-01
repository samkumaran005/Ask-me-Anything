import streamlit as st
from transformers import pipeline
import wikipedia

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Ask Me Anything 🤖",
    page_icon="❓",
    layout="centered"
)

# -----------------------------
# Load Model
# -----------------------------
@st.cache_resource
def load_qa_model():
    return pipeline("question-answering", model="deepset/roberta-base-squad2")

qa_pipeline = load_qa_model()

# -----------------------------
# App Header
# -----------------------------
st.markdown(
    """
    <h1 style='text-align:center; color:#1f77b4;'>🧠 Ask Me Anything</h1>
    <p style='text-align:center;'>A Hugging Face powered Question Answering System</p>
    <hr>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Input Mode Selection
# -----------------------------
mode = st.radio("📚 Choose Context Source:", ["Manual Input", "Wikipedia"])

context = ""

if mode == "Manual Input":
    context = st.text_area("📄 Enter your context paragraph:", height=200)
else:
    topic = st.text_input("🔎 Enter a Wikipedia topic:")
    if topic:
        try:
            context = wikipedia.summary(topic, sentences=5)
            st.success(f"Fetched context for **{topic}** ✅")
            st.write(context)
        except Exception as e:
            st.error("⚠️ Unable to fetch Wikipedia summary. Try another topic.")

# -----------------------------
# Question Input
# -----------------------------
question = st.text_input("❓ Ask your question:")

# -----------------------------
# Answer Button
# -----------------------------
if st.button("💬 Get Answer"):
    if context.strip() and question.strip():
        with st.spinner("Finding the best answer... 🔍"):
            result = qa_pipeline(question=question, context=context)

        st.subheader("✅ Answer:")
        st.success(result["answer"])

        st.progress(result["score"])
        st.caption(f"Confidence: {round(result['score'] * 100, 2)}%")
    else:
        st.warning("Please provide both context and question before submitting.")

# -----------------------------
# Footer
# -----------------------------
st.markdown(
    """
    <hr>
    <div style='text-align:center;'>
        <p>Built with ❤️ using <b>Hugging Face Transformers</b> & <b>Streamlit</b></p>
        <p style='color:gray;'>AI-Powered Question Answering Assistant</p>
    </div>
    """,
    unsafe_allow_html=True
)
