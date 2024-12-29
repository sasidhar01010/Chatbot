import streamlit as st
from main_app import app  # Import the workflow

# Streamlit page setup
st.set_page_config(page_title="Intelligent Q&A System", layout="centered")

# Main interface
st.title("Interactive Q&A System Powered by Self-Reflection RAG")

# User input
user_question = st.text_input(
    "Enter Your Question:",
    value="What is the passing criteria for BBA students"
)

# Submit button
if st.button("Proceed") and user_question.strip():
    # Run the RAG workflow
    inputs = {"question": user_question}
    final_generation = None

    try:
        spinner_placeholder = st.empty()
        spinner_placeholder.text("Analyzing your query...")

        # Display a loading spinner
        iteration = 1
        with st.spinner("Processing your request, please wait..."):
            for output in app.stream(inputs, {"recursion_limit": 8}):
                for key, value in output.items():
                    document_count = len(value["documents"])
                    if key == "transform_query":
                        iteration += 1
                    spinner_placeholder.text(f"Iteration: {iteration}")
        
        spinner_placeholder.empty()

        # Display the final answer
        if value.get("generation"):
            st.success("Generated Response:")
            st.markdown(value["generation"])
        else:
            st.error("Sorry, I didn't understand your question. Do you want to connect with a live agent?")
    
    except Exception as e:
        spinner_placeholder.empty()
        st.error(f"Sorry, I didn't understand your question. Do you want to connect with a live agent?")