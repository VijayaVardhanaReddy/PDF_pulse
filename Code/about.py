import streamlit as st
import time
def about():
    st.header("About Us")
    st.markdown("### Features")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Extract Key Points 🔑**\n\nSummarize lengthy passages, extract key information, and quickly locate what you need. Say hello to an efficient and hassle-free document comprehension journey.")
    
    with col2:
        st.markdown("**Answer Questions about PDF Documents 📃**\n\nPDF Pulse thoroughly analyzes your PDFs, providing insightful answers based on document content. Pdf Pulse ensures effective analysis of PDFs in diverse languages.")
    
    with col3:
        st.markdown("**Interact with your Personal AI 🤖**\n\n Here, you can engage with a sophisticated AI system designed to assist you in answering questions, solving problems, and providing insights on a wide range of topics. Whether you're looking for quick answers, detailed explanations, or simply a conversational partner, your personal AI is here to help.")

    # User Sections
    st.markdown("### Who Can Benefit?")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Students 👨‍💻**\n\nSummarize long textbooks, clarify concepts, get new ideas, and more. Ideal for enhancing learning experiences.")
    
    with col2:
        st.markdown("**Researchers 🕵️**\n\nAnalyze industry reports and professional documents easily. Improve speed, accuracy, and efficiency.")
    
    with col3:
        st.markdown("**Professionals 👨‍🎓**\n\nExplain business reports, analyze financial data, and do market research. Raise work productivity and optimize performance.")

    st.markdown("### How to Chat with PDF Online?")
    st.markdown("""
    1. **Upload A PDF File**: Upload or drag-and-drop the PDF file onto HiPDF's Chat with PDF Page.
    2. **AI Analyzes PDF**: Upon uploading, HiPDF will start analyzing your PDF, extracting its key information.
    3. **Chat with PDF**: Chat with the PDF by asking your questions and receiving answers. Easily copy and paste the answers as needed.
    """)

    # FAQ Section
    with st.expander("FAQs about chatting with PDF online"):
        st.markdown("""
        - **How can I chat with my PDF?** Simply upload your PDF and start chatting using the AI interface.
        - **Do I need to sign up for an account for a chat?** No, you can use the service without signing up.
        - **How many times can I chat with PDF?** There is no limit to the number of times you can chat with your PDFs.
        - **Is there a way to summarize a PDF?** Yes, ChatGPT can summarize a PDF file for you.
        """)
