#!/bin/bash
python3.8 -m venv myenv
source myenv/bin/activate
pip install slack-sdk slack-bolt Flask
pip install python-dotenv
pip install langchain
pip install openai
pip install python-dotenv
pip install google-search-results
pip install tiktoken
pip install faiss-cpu==1.7.4
