import streamlit as st
from codegen_api import invoke_router_agent

st.set_page_config(
    page_title="Agentic AI Code Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Agentic AI Code Assistant")

# -----------------------------
# Chat History
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        if msg["role"] == "user":
            st.markdown(msg["content"])

        else:

            response = msg["content"]

            task = response["router"]["task"]

            st.markdown(f"### 📝 Task: **{task.capitalize()}**")

            # Generated Code
            if response.get("generated_code"):

                st.markdown("### 💻 Generated Code")

                st.code(
                    response["generated_code"],
                    language=response["router"]["target_language"]
                )

            # Translated Code
            if response.get("translated_code"):

                st.markdown("### 💻 Translated Code")

                st.code(
                    response["translated_code"],
                    language=response["router"]["target_language"]
                )

            # Explanation
            if response.get("explanation"):

                st.markdown("### 📖 Explanation")

                st.write(response["explanation"])

            # Compilation
            if response.get("compilation_success") is not None:

                if response["compilation_success"]:
                    st.success("✅ Compilation Successful")
                else:
                    st.error("❌ Compilation Failed")
                    st.code(response["compiler_error"])
                    
            if response.get("pass_percentage") is not None:

                st.markdown("### 🧪 Test Results")

                st.write(f"**Pass Percentage:** {response['pass_percentage']}%")

            # Evaluation
            if response.get("evaluation"):

                with st.expander("📊 Evaluation Metrics"):

                    st.json(response["evaluation"])


# -----------------------------
# User Input
# -----------------------------
prompt = st.chat_input(
    "Ask me to generate, translate or explain code..."
)

if prompt:

    # Display user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant Response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            response = invoke_router_agent(prompt)

        st.json(response)

        task = response["router"]["task"]

        st.markdown(f"### 📝 Task: **{task.capitalize()}**")

        # Generated Code
        if response.get("generated_code"):

            st.markdown("### 💻 Generated Code")

            st.code(
                response["generated_code"],
                language=response["router"]["target_language"]
            )

        # Translated Code
        if response.get("translated_code"):

            st.markdown("### 💻 Translated Code")

            st.code(
                response["translated_code"],
                language=response["router"]["target_language"]
            )

        # Explanation
        if response.get("explanation"):

            st.markdown("### 📖 Explanation")

            st.write(response["explanation"])

        # Compilation
        if response.get("compilation_success") is not None:

            if response["compilation_success"]:
                st.success("✅ Compilation Successful")
            else:
                st.error("❌ Compilation Failed")
                st.code(response["compiler_error"])

        if response.get("pass_percentage") is not None:

            st.markdown("### 🧪 Test Results")

            st.write(f"**Pass Percentage:** {response['pass_percentage']}%")
        
        # Evaluation
        if response.get("evaluation"):

            with st.expander("📊 Evaluation Metrics"):

                st.json(response["evaluation"])

    # Save assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )