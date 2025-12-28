import streamlit as st
from dotenv import load_dotenv
import warnings

# Load environment variables
load_dotenv()
warnings.filterwarnings("ignore")

# Streamlit page setup
st.set_page_config(page_title="Intelligent Q&A System", layout="centered")

# --- CACHED RESOURCE INITIALIZATION ---
@st.cache_resource
def get_workflow():
    """
    Initializes the workflow. 
    Cached so we don't re-process the PDF on every interaction.
    """
    try:
        # We import here to ensure the heavy loading happens only when needed
        from main_app import build_app
        return build_app()
    except Exception as e:
        st.error(f"Failed to initialize workflow: {e}")
        return None

# Load the app
app = get_workflow()

# --- MAIN INTERFACE ---
st.title("Interactive Q&A System Powered by Self-Reflection RAG")

if app is None:
    st.error("Application failed to load. Please check console logs and ensure 'input.pdf' exists.")
    st.stop()

# User input
user_question = st.text_input(
    "Enter Your Question:",
    value="What is the passing criteria for BBA students"
)

# Submit button
if st.button("Proceed") and user_question.strip():
    inputs = {"question": user_question}
    
    # Placeholders for UI updates
    status_placeholder = st.empty()
    result_placeholder = st.empty()
    
    final_output = None
    
    try:
        with st.spinner("Processing your request..."):
            # Run the graph
            # recursion_limit prevents infinite loops if the model keeps struggling
            for output in app.stream(inputs, {"recursion_limit": 15}):
                for key, value in output.items():
                    # Update status based on which node is running
                    if key == "transform_query":
                        status_placeholder.info(f"Refining query to: '{value['question']}'...")
                    elif key == "retrieve":
                        status_placeholder.info("Retrieving relevant documents...")
                    elif key == "grade_documents":
                        status_placeholder.info("Checking document relevance...")
                    elif key == "generate":
                         status_placeholder.info("Generating answer...")
                    
                    # Keep track of the latest state
                    final_output = value

        # Clear status message
        status_placeholder.empty()

        # Display Final Result
        if final_output and "generation" in final_output:
            st.success("Generated Response:")
            st.markdown(final_output["generation"])
            
            # Optional: Show which docs were used
            with st.expander("View Source Context"):
                docs = final_output.get("documents", [])
                if docs:
                    for i, doc in enumerate(docs):
                        st.markdown(f"**Source {i+1}:**")
                        st.caption(doc.page_content[:400] + "...")
                else:
                    st.write("No specific documents were deemed relevant enough to display.")
        else:
            st.warning("The system could not generate a valid answer based on the provided documents. Please try rephrasing your question.")

    except Exception as e:
        status_placeholder.empty()
        st.error(f"An error occurred during processing: {str(e)}")