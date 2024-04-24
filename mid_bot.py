import streamlit as st
import openai

def ask_gpt(question, model, api_key):
    openai.api_key = api_key
    response = openai.Completion.create(
        engine=model,
        prompt=question,
        temperature=0.7,
        max_tokens=150
    )
    return response.choices[0].text.strip()

def main():
    st.set_page_config(
        page_title="MY GPT",
        layout="wide"
    )
    st.header("MY GPT")
    st.markdown("---")
    with st.expander("ABOUT MY GPT", expanded=True):
        st.write(
            """
            - 채팅을 통해 GPT에게 질문할 수 있습니다.
            - 궁금한 것을 MY GPT에게 물어보세요.
            """
        )
        st.markdown("")
    if "chat" not in st.session_state:
        st.session_state["chat"] = []
    if "OPENAI_API" not in st.session_state:
        st.session_state["OPENAI_API"] = ""
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "system", "content": "You are a thoughful assistant. Respond to all input in 25 words and answer in korea"}]
    with st.sidebar:
        st.session_state["OPENAI_API"] = st.text_input(label="OPENAI API 키", placeholder="Enter Your API Key", value="", type="password")

        st.markdown("---")
        model = st.radio(label="GPT 모델", options=["gpt-4", "gpt-3.5-turbo"])
        st.markdown("---")

        if st.button(label="초기화"):
            st.session_state["chat"] = []
            st.session_state["messages"] = [{"role": "system", "content": "You are a thoughtful assistant. Respond to all input in 25 words and answer in korea"}]
            st.session_state["check_reset"] = True

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("질문하기")
        user_question = st.text_input(label="Type your question here:", value="", max_chars=100)
        if st.button("질문하기"):
            if user_question.strip() != "":
                st.session_state["chat"].append(("user", "current_time", user_question))
                response = ask_gpt(user_question, model, st.session_state["OPENAI_API"])
                st.session_state["messages"].append({"role": "user", "content": user_question})
                st.session_state["messages"].append({"role": "GPT", "content": response})

    with col2:
        st.subheader("질문/답변")
        for message in st.session_state["messages"]:
            if message["role"] == "user":
                st.write(f'<div style="display:flex;align-items:center;"><div style="background-color:#007AFF;color:white;border-radius:12px;padding:8px 12px;margin-right:8px;">{message["content"]}</div><div style="font-size:0.8rem;color:gray;">{message["time"]}</div></div>', unsafe_allow_html=True)
                st.write("")
            elif message["role"] == "GPT":
                st.write(f'<div style="display:flex;align-items:center;justify-content:flex-end;"><div style="background-color:lightgray;border-radius:12px;padding:8px 12px;margin-left:8px;">{message["content"]}</div><div style="font-size:0.8rem;color:gray;">{message["time"]}</div></div>', unsafe_allow_html=True)
                st.write("")

if __name__ == "__main__":
    main()
