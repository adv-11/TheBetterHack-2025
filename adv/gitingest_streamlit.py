import streamlit as st
from gitingest import ingest
import asyncio
import sys

# Fix for Windows subprocess issue
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

def main():
    st.title("GitHub Repository Ingestor")
    st.write("Enter a GitHub repository URL to fetch its summary, tree, and content.")
    
    repo_url = st.text_input("GitHub Repository URL", "https://github.com/adv-11/RAG_from_scratch")
    
    if st.button("Ingest Repository"):
        with st.spinner("Fetching repository data..."):
            try:
                # Directly call the ingest function (NO asyncio.run needed)
                summary, tree, content = ingest(repo_url)
                
                st.subheader("Repository Summary")
                st.write(summary)
                
                st.subheader("Repository Tree")
                st.text(tree)  # Use text instead of json for better formatting
                
                st.subheader("Repository Content")
                st.text(content)  # Use text instead of json for readability
                
            except Exception as e:
                st.error(f"Error fetching repository: {e}")

if __name__ == "__main__":
    main()
