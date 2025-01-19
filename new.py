import streamlit as st
from PyPDF2 import PdfReader
import openai

api_key = st.secrets["api_key"]

# PDF 텍스트 읽기 함수
def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# OpenAI ChatGPT를 이용한 응답 생성 함수
def generate_response(prompt, context):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that can answer questions based on the provided PDF content."},
                {"role": "user", "content": context},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error generating response: {str(e)}"

# Streamlit 앱 인터페이스
def main():
    st.title("PDF 기반 챗봇")
    st.write("PDF 파일을 업로드하고 내용을 기반으로 질문하세요.")

    # PDF 업로드 위젯
    uploaded_file = st.file_uploader("PDF 파일 업로드", type="pdf")

    if uploaded_file is not None:
        # PDF 텍스트 추출
        with st.spinner("PDF에서 텍스트를 추출 중입니다..."):
            pdf_text = extract_text_from_pdf(uploaded_file)

        st.success("텍스트 추출 완료!")
        st.write("PDF 내용 미리보기:")
        st.text_area("추출된 텍스트", pdf_text, height=200)

        # 챗봇 인터페이스
        st.write("### 질문을 입력하세요:")
        user_input = st.text_input("질문")

        if user_input:
            with st.spinner("답변 생성 중..."):
                response = generate_response(user_input, pdf_text)

            st.write("### 답변:")
            st.write(response)

if __name__ == "__main__":
    main()





