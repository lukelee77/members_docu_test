import streamlit as st
from openai import OpenAI

# Show title and description.
st.set_page_config(page_title="Document ASK GPT", page_icon="📖", layout="wide")
st.title('''Luke's AI Doc. ASK 프로그램 테스트_Ver1😏''')
st.subheader('※ 배포금지. 개인용 유료 API key 사용 (해외시장 전용)')    
st.text('''Instruction - txt 형식의 불량 증상 파일 업로드 후 AI 질문 (최대 100줄 이하)''')    
st.markdown('---')

apikey = st.secrets["openai"]["apikey"]  # 환경변수나 Streamlit secrets에서 가져오기

# OpenAI Client 초기화 (api_key를 설정)
client = OpenAI(api_key=apikey)

# Let the user upload a file via `st.file_uploader`.
uploaded_file = st.file_uploader(
    "Upload a document (.txt or .md)", type=("txt", "md")
)

# Ask the user for a question via `st.text_area`.
question = st.text_area(
    "Now ask a question about the document!",
    placeholder="Can you give me a short summary?",
    disabled=not uploaded_file,
)

if uploaded_file and question:
    # Process the uploaded file and question.
    document = uploaded_file.read().decode()
    messages = [
        {
            "role": "user",
            "content": f"Here's a document: {document} \n\n---\n\n {question}",
        }
    ]

    # Generate an answer using the OpenAI API.
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        stream=True,
    )

    # Stream the response to the app using `st.write_stream`.
    st.write_stream(stream)