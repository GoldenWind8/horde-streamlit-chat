import streamlit as st
import requests
import json
import time

# Set up the API endpoint and headers
url = "https://api.aipowergrid.io/api/v2/generate/text/async"
headers = {
    'apikey': '0000000000',
    'Content-Type': 'application/json'
}

def generate_text(prompt):
    payload = json.dumps({
        "prompt": f"<s>[INST] {prompt} [/INST]",
        "models": [
            "aphrodite/meta-llama/Meta-Llama-3-8B-Instruct"
        ],
        "n": 1,
        "trusted_workers": False,
        "params": {
            "max_context_length": 512,
            "max_length": 100,
            "temperature": 0.7,
            "top_p": 0.9
        }
    })

    response = requests.post(url, headers=headers, data=payload)
    json_response = response.json()
    job_id = json_response["id"]
    print(json_response)

    return poll_api(job_id)

def poll_api(job_id):
    status_endpoint = f"https://api.aipowergrid.io/api/v2/generate/text/status/{job_id}"

    while True:
        time.sleep(2)

        resp = requests.get(status_endpoint, headers=headers)
        json_response = resp.json()
        print(json_response)
        if json_response["done"]:
            return json_response["generations"][0]["text"]

# Streamlit app
def main():
    st.title("AI Chat Application")

    # Chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # User input
    user_input = st.text_input("User:")

    if user_input:
        # Generate AI response
        ai_response = generate_text(user_input)

        # Update chat history
        st.session_state.chat_history.append({"User": user_input, "AI": ai_response})

    # Display chat history
    for chat in st.session_state.chat_history:
        st.write(f"User: {chat['User']}")
        st.write(f"AI: {chat['AI']}")

if __name__ == "__main__":
    main()