import streamlit as st
from PyPDF2 import PdfReader
import openai

# OpenAI API Key 설정
openai.api_key = st.secrets["api_key"]

# PDF 텍스트 읽기 함수
def extract_text_from_pdf(pdf_file):
    try:
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

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
    except openai.error.OpenAIError as e:
        return f"OpenAI API Error: {str(e)}"
    except Exception as e:
        return f"Unexpected Error: {str(e)}"

# Streamlit 앱 시작
st.title("PDF 기반 Q&A")

# PDF 파일 업로드
uploaded_pdf = st.file_uploader("PDF 파일을 업로드하세요", type=["pdf"])

if uploaded_pdf is not None:
    # PDF 내용 추출
    with st.spinner("PDF에서 텍스트를 추출 중입니다..."):
        pdf_text = extract_text_from_pdf(uploaded_pdf)

    if pdf_text.startswith("Error"):
        st.error(pdf_text)
    else:
        st.text_area("PDF 내용:", pdf_text, height=200)

        # 사용자 입력 프롬프트
        user_prompt = st.text_input("질문을 입력하세요:")

        if user_prompt:
            # 응답 생성
            with st.spinner("ChatGPT가 응답을 생성 중입니다..."):
                response = generate_response(user_prompt, pdf_text)

            # 결과 출력
            if response.startswith("Error"):
                st.error(response)
            else:
                st.success("응답:")
                st.write(response)

if __name__ == "__main__":
    main()





