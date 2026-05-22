# frontend/app.py

import streamlit as st
import requests
import uuid
import json
from pathlib import Path
from streamlit_lottie import st_lottie


#API_URL="http://127.0.0.1:8000/chat"
API_URL="http://192.168.2.213:8000/chat"


st.set_page_config(

    page_title="Agentic Customer Support",

    page_icon="",

    layout="wide"
)


# LOAD LOTTIE

BASE_DIR = Path(__file__).resolve().parent


def load_lottie():

    animation_path = (

        BASE_DIR /
        "Robot says hello.json"
    )


    with open(

        animation_path,

        "r",

        encoding="utf-8"

    ) as f:

        return json.load(f)


robot_animation=load_lottie()



# SESSION

if "messages" not in st.session_state:

    st.session_state.messages=[]


if "thread_id" not in st.session_state:

    st.session_state.thread_id=str(
        uuid.uuid4()
    )



# SIDEBAR

with st.sidebar:


    st.title(
        ":material/settings: Support Controls"
    )

    st.markdown("---")


    st.write(
        "Current Session"
    )


    st.code(
        st.session_state.thread_id[:8]
    )


    # ACTIONS FIRST

    col1,col2=st.columns(2)


    with col1:

        if st.button(

            ":material/add: New",

            use_container_width=True
        ):

            st.session_state.messages=[]

            st.session_state.thread_id=str(
                uuid.uuid4()
            )

            st.rerun()


    with col2:

        if st.button(

           ":material/delete: Clear",

            use_container_width=True
        ):

            st.session_state.messages=[]

            st.rerun()


    st.caption(
        "New Chat / Clear"
    )


    st.markdown("---")


    # BETTER STATS


    st.subheader(
        ":material/analytics: Session Stats"
    )


    total_messages=len(
        st.session_state.messages
    )


    user_count=len(

        [

            m for m in
            st.session_state.messages

            if m["role"]=="user"

        ]

    )


    st.metric(
        "Messages",
        total_messages
    )


    st.metric(
        "Conversations",
        user_count
    )


    st.markdown("---")


    st.subheader(
        ":material/bolt: Sample Queries"
    )


    if st.button(
        "Payment failed"
    ):

        st.session_state.sample_query=(
            "Payment failed and money deducted"
        )


    if st.button(
        "Forgot Password"
    ):

        st.session_state.sample_query=(
            "I forgot my password"
        )


    if st.button(
        "Fraud Complaint"
    ):

        st.session_state.sample_query=(
            "This looks like fraud"
        )


    if st.button(
        "Tracking Issue"
    ):

        st.session_state.sample_query=(
            "My order tracking link is not working"
        )


    st.markdown("---")


    if st.session_state.messages:


        transcript="\n\n".join(

            [

                f"{m['role']}:\n{m['content']}"

                for m in

                st.session_state.messages
            ]

        )


        st.download_button(

            ":material/download: Download Chat",

            transcript,

            file_name=
            f"chat_{st.session_state.thread_id[:8]}.txt",

            use_container_width=True
        )



# HEADER

col1,col2=st.columns(
    [4,1]
)


with col1:

    st.title(
        "🤖 Agentic Customer Support System"
    )


with col2:

    st_lottie(

        robot_animation,

        height=120,

        key="robot"
    )


with st.expander(
    "About System"
):


    st.info(
"""
Multi-Agent + RAG Customer Support Bot

Supported:

✔ Payment

✔ Shipping

✔ Account Issues

✔ Refunds

✔ Complaints

✔ Escalations
"""
)



# CHAT HISTORY


for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


        if message["role"]=="assistant":


            with st.expander(
                "Debug Info",
                expanded=False
            ):

                st.json(

                    {

                        "Intent":
                        message.get(
                            "intent"
                        ),

                        "Escalated":
                        message.get(
                            "escalated"
                        ),

                        "Thread":
                        message.get(
                            "thread"
                        )

                    }

                )


            if "trace" in message:

                with st.expander(

                    "Agent Execution Details",

                    expanded=False

                ):


                    for step in message[
                        "trace"
                    ]:


                        if isinstance(
                            step,
                            str
                        ):

                            st.text(
                                step
                            )

                        else:

                            with st.expander(

                                step[
                                    "agent"
                                ]

                            ):


                                for key,value in step.items():

                                    if key!="agent":

                                        st.write(

                                            f"{key.title()}: {value}"

                                        )



prompt=st.chat_input(
    "Ask your question..."
)



if "sample_query" in st.session_state:

    prompt=st.session_state.sample_query

    del st.session_state[
        "sample_query"
    ]




if prompt:


    st.session_state.messages.append(

        {

            "role":"user",

            "content":prompt
        }

    )


    with st.chat_message(
        "user"
    ):

        st.markdown(
            prompt
        )



    with st.chat_message(
        "assistant"
    ):


        with st.spinner(
            "Thinking..."
        ):


            try:


                response=requests.post(

                    API_URL,

                    json={

                        "query":
                        prompt,

                        "thread_id":
                        st.session_state.thread_id
                    }

                )


                data=response.json()


                reply=data[
                    "response"
                ]


                intent=data[
                    "intent"
                ]


                escalated=data[
                    "escalated"
                ]

                trace=data[
                    "trace"
                ]
                st.markdown(
                    reply
                )


                if escalated:


                    st.error(

                        ":material/warning: Specialist Ticket Created"
                    )


                col1,col2,col3=st.columns([1,1,4])


                with col1:

                    st.button(
                        "Helpful"
                    )


                with col2:

                    st.button(
                        "Not Helpful"
                    )


                with st.expander(
                    "Debug Info",
                    expanded=False
                ):

                    st.json(

                        {

                            "Intent":
                            intent,

                            "Escalated":
                            escalated,

                            "Thread":
                            st.session_state.thread_id[:8]

                    }

                )
                    
                with st.expander(

                    "Agent Execution Details",

                    expanded=False
                ):


                    for step in trace:


                        # supervisor logs

                        if isinstance(
                            step,
                            str
                        ):

                            st.text(
                                step
                            )


                        # agent blocks

                        else:


                            with st.expander(

                                step[
                                    "agent"
                                ]

                            ):


                                for key,value in step.items():

                                    if key!="agent":

                                        st.write(

                                            f"{key.title()}: {value}"

                                        )


                st.session_state.messages.append(

                {

                    "role":"assistant",

                    "content":reply,

                    "intent":intent,

                    "escalated":escalated,

                    "trace":trace,

                    "thread":
                    st.session_state.thread_id[:8]

                }

            )


            except Exception as e:


                st.error(

                    f"API Error: {e}"
                )