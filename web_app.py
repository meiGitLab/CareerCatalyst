# web_app.py

import streamlit as st
from agents import agents_system
import json

def main():
    st.set_page_config(
        page_title="CareerCatalyst - AI-Powered Professional Development Ecosystem",
        layout="wide"
    )
    
    st.markdown("""
        <style>
        .main-title {
            color: #FF6B6B;
            font-size: 3rem;
            font-weight: bold;
            text-align: center;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .subtitle {
            text-align: center;
            color: #3498DB;
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Customized style
    st.markdown('<h1 class="main-title">✨ CareerCatalyst ✨</h1>', unsafe_allow_html=True)
    st.markdown('<h1 class="main-title">Your AI-Powered Professional Development Ecosystem</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Welcome! Get personalized help with onboarding, learning, and career development.</p>', unsafe_allow_html=True)
    
    # Initialize session state
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {}
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Sidebar for profile setup
    with st.sidebar:
        st.header("  Your Profile")
        with st.form("profile_form"):
            role = st.text_input("Your Role", 
                               placeholder="e.g., Software Engineer, Marketing Associate",
                               value=st.session_state.user_data.get('role', ''))
            interests = st.text_input("Your Career Interests",
                                    placeholder="e.g., leadership, data science, design",
                                    value=st.session_state.user_data.get('interests', ''))
            submitted = st.form_submit_button("Save Profile")
            
            if submitted:
                st.session_state.user_data = {'role': role, 'interests': interests}
                st.success("Profile saved!")
    
    # Main chat interface
    st.header("💬 Chat with CareerCatalyst")
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about onboarding, learning, or career development..."):
        # Check if profile is set
        if not st.session_state.user_data.get('role') or not st.session_state.user_data.get('interests'):
            st.warning("Please set up your profile in the sidebar first!")
            st.stop()
        
        # Add user message to chat
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response_data = agents_system.process_query(prompt, st.session_state.user_data)
                    response_text = f"**{response_data['agent_name']}:**\n\n{response_data['answer']}"
                    
                    # Add sources if available
                    if response_data['sources']:
                        sources_text = "\n\n  **Sources:**\n" + "\n".join([f"• {src}" for src in response_data['sources'][:3]])
                        if len(response_data['sources']) > 3:
                            sources_text += f"\n• ... and {len(response_data['sources']) - 3} more"
                        response_text += sources_text
                    
                    st.markdown(response_text)
                    st.session_state.chat_history.append({"role": "assistant", "content": response_text})
                    
                except Exception as e:
                    error_msg = "Sorry, I encountered an error. Please try again."
                    st.error(error_msg)
                    st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
    
    # Quick action buttons
    st.write("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("  Onboarding Help"):
            st.chat_input("What would you like to know about onboarding?", key="onboarding_prompt")
    with col2:
        if st.button("  Learning Resources"):
            st.chat_input("What skills would you like to develop?", key="learning_prompt")
    with col3:
        if st.button("  Career Guidance"):
            st.chat_input("What career advice are you looking for?", key="career_prompt")

if __name__ == "__main__":
    main()