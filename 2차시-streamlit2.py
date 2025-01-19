import streamlit as st
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import LLMResult

# 실시간으로 대답을 스트리밍하는 핸들러 클래스
class StreamHandler(BaseCallbackHandler):
    def __init__(self, container):
        super().__init__()
        self.container = container
        self.text = ""  # 스트리밍 중인 텍스트

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        # 새로운 토큰이 생성될 때마다 호출
        self.text += token
        self.container.markdown(self.text)  # Streamlit의 마크다운 컨테이너 업데이트

    def on_llm_end(self, response: LLMResult, **kwargs) -> None:
        # LLM 처리가 완료되었을 때 호출
        self.container.markdown(self.text)  # 최종 텍스트 출력

# Streamlit 설정
st.title("아라리요")

# Streamlit 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# 예제 질문 및 응답
st.chat_message("user").write("안녕하세요!")
st.chat_message("assistant").write("질문이 있으신가요?")

# 사용자 입력 처리
if prompt := st.chat_input("질문을 적어주세요."):
    # 사용자 메시지를 기록하고 출력
    st.chat_message("user").write(prompt)

    # 스트리밍 출력 컨테이너 생성
    with st.chat_message("assistant"):
        container = st.empty()
        stream_handler = StreamHandler(container)

        # OpenAI API 호출 예제 (stream=True 가정)
        from langchain.chat_models import ChatOpenAI
        from langchain.chains import RetrievalQA
        from langchain.embeddings import OpenAIEmbeddings
        from langchain.vectorstores import FAISS

        # OpenAI 설정
        api_key = st.secrets["default"]["api_key"]
        embeddings = OpenAIEmbeddings(api_key=api_key)
        vectors = FAISS.load_local("your-vectorstore-path", embeddings)

        # LLM 초기화
        llm = ChatOpenAI(
            streaming=True,
            callbacks=[stream_handler],
            temperature=0.0,
            model_name="gpt-4-0125-preview",
            openai_api_key=api_key
        )

        # 질의 응답 체인 생성 및 실행
        qa = RetrievalQA.from_llm(llm=llm, retriever=vectors.as_retriever())
        qa(prompt)

        # 최종 답변을 세션 상태에 저장
        st.session_state["messages"].append(("user", prompt))
        st.session_state["messages"].append(("assistant", stream_handler.text))




