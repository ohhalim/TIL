"""
import streamlit as st
from utils import print_message, StreamHandler 
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import ChatMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

import os   

st.set_page_config(page_title="ai미연시 근데 귀여니를 곁들인", page_icon=":speech_balloon:")
st.title("ai미연시 근데 귀여니를 곁들인") 

os.environ["OPENAI_API_KEY"] = st.secrets["openai_api_key"] 

if "messages" not in st.session_state:
    st.session_state.messages = []

if "store" not in st.session_state:
    st.session_state["store"] = dict()

with st.sidebar:
    session_id = st.text_input("Session ID", value="abc123")

print_message()

def get_session_history(session_ids: str) -> BaseChatMessageHistory:
    if session_ids not in st.session_state["store"]:

    
        st.session_state["store"][session_ids] = ChatMessageHistory()
    return st.session_state["store"][session_ids]

if user_input := st.chat_input("메세지를 입력해주세요."):
    st.chat_message("user").write(f"{user_input}")
    st.session_state["messages"].append(ChatMessage(role="user", content=user_input))   

    
    with st.chat_message("assistant"):
        stream_hander = StreamHandler(st.empty())

        # 1. 모델 생성 
    llm = ChatOpenAI(streaming=True, callbacks=[stream_hander])

    # 2. 프롬프트 생성
    prompt = ChatPromptTemplate.from_messages([
        ("system", "질문에 짧고 간결하게 답변해 주세요"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}")
    ])

    chain = prompt | llm 

    chain_with_memory = (
        RunnableWithMessageHistory(
            chain,
            get_session_history,
            input_message_key="question",
            history_messages_key="history",
        )    
    )


    response = chain_with_memory.invoke(
        {"question": user_input},
        config={"configurable": {"session_id": session_id}},
    )

    st.session_state["messages"].append(
        ChatMessage(role="assistant", content=response.content)
    )
"""
import re
import streamlit as st
from utils import print_message, StreamHandler 
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import ChatMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os   



def load_and_extract_dialogues():
    try:
        with open('boyfriend.txt', 'r', encoding='utf-8') as file:
            content = file.read()
            
            # 큰따옴표로 둘러싸인 텍스트만 추출
            dialogues = re.findall(r'"([^"]*)"', content)
            
            # 빈 문자열 제거 및 중복 제거
            dialogues = [d.strip() for d in dialogues if d.strip()]
            dialogues = list(dict.fromkeys(dialogues))
            
            # 청크로 분할 (원래 코드의 chunk_size와 비슷한 방식 유지)
            chunks = []
            current_chunk = []
            current_length = 0
            
            for dialogue in dialogues:
                if current_length + len(dialogue) > 400:
                    chunks.append("\n".join(current_chunk))
                    current_chunk = [dialogue]
                    current_length = len(dialogue)
                else:
                    current_chunk.append(dialogue)
                    current_length += len(dialogue)
            
            if current_chunk:
                chunks.append("\n".join(current_chunk))
                
            return chunks
    except FileNotFoundError:
        st.error("boyfriend.txt 파일을 찾을 수 없습니다!")
        return None


st.set_page_config(page_title="ai미연시 근데 귀여니를 곁들인", page_icon=":speech_balloon:")
st.title("ai미연시 근데 귀여니를 곁들인") 

# Load and chunk boyfriend content
text_chunks = load_and_extract_dialogues()
if text_chunks is None:
    st.stop()

# Store chunks in session state
if "text_chunks" not in st.session_state:
    st.session_state.text_chunks = text_chunks
    st.session_state.current_chunk_index = 0

os.environ["OPENAI_API_KEY"] = st.secrets["openai_api_key"] 

if "messages" not in st.session_state:
    st.session_state.messages = []

if "store" not in st.session_state:
    st.session_state["store"] = dict()

with st.sidebar:
    session_id = st.text_input("Session ID", value="abc123")
    # Add chunk navigation
    st.write(f"현재 청크: {st.session_state.current_chunk_index + 1}/{len(text_chunks)}")
    if st.button("다음 청크"):
        st.session_state.current_chunk_index = (st.session_state.current_chunk_index + 1) % len(text_chunks)
    if st.button("이전 청크"):
        st.session_state.current_chunk_index = (st.session_state.current_chunk_index - 1) % len(text_chunks)

print_message()

def get_session_history(session_ids: str) -> BaseChatMessageHistory:
    if session_ids not in st.session_state["store"]:
        st.session_state["store"][session_ids] = ChatMessageHistory()
    return st.session_state["store"][session_ids]

if user_input := st.chat_input("메세지를 입력해주세요."):
    st.chat_message("user").write(f"{user_input}")
    st.session_state["messages"].append(ChatMessage(role="user", content=user_input))   
    
    with st.chat_message("assistant"):
        stream_hander = StreamHandler(st.empty())

        llm = ChatOpenAI(
            model_name="gpt-4o",  # 명시적으로 모델 지정
            streaming=True, 
            temperature=1.0, 
            callbacks=[stream_hander]
        )

        # Get current chunk
        current_chunk = st.session_state.text_chunks[st.session_state.current_chunk_index]

        # Modified prompt to include current chunk
        prompt = ChatPromptTemplate.from_messages([
    ("system", f"""
     당신은 '이강순'이라는 캐릭터입니다. 아래의 책 내용과 동일한 말투와 성격을 정확히 따라야 합니다.
    - 반말을 사용하며, 거칠고 직설적이고 감정 표현이 강렬한 스타일로 대화합니다.
    - 반드시 txt 내용만 참고하여 답변하세요.
    - txt 내용에 없는 질문에는 "내가 어떻게 알아?"와 같이 책 외부의 정보를 참조하지 않도록 답하세요.
       귀여니 스타일의 감정 표현(!!, -_-, ?! 등)을 사용하세요.
    청크 외의 정보를 사용하지마.
    
    참고할 텍스트 내용:
    {current_chunk}
    
    권은형과 대화할 때 위 텍스트에 나타난 것과 같은 말투와 태도를 유지하세요.
    """),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}")
])
        chain = prompt | llm 

        chain_with_memory = RunnableWithMessageHistory(
            chain,
            get_session_history,
            input_message_key="question",
            history_messages_key="history",
        )    

        response = chain_with_memory.invoke(
            {"question": user_input},
            config={"configurable": {"session_id": session_id}},
        )

        st.session_state["messages"].append(
            ChatMessage(role="assistant", content=response.content)
        )


        # conda activate llm
        # streamlit run main.py 출력