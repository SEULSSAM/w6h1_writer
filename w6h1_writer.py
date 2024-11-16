import streamlit as st
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI

def generate_writing_prompt(writing_type, w5h1_info):
    prompts = {
        "시": f"""다음 정보를 바탕으로 시를 작성해주세요:
            {w5h1_info}
            한국어로 서정적이고 감성적인 시를 작성해주세요.""",
        
        "수필": f"""다음 정보를 바탕으로 수필을 작성해주세요:
            {w5h1_info}
            개인적인 경험과 생각을 담아 수필 형식으로 작성해주세요.""",
        
        "소설": f"""다음 정보를 바탕으로 단편 소설을 작성해주세요:
            {w5h1_info}
            등장인물, 배경, 사건을 포함한 이야기를 전개해주세요.""",
        
        "보고서": f"""다음 정보를 바탕으로 보고서를 작성해주세요:
            {w5h1_info}
            객관적인 사실과 분석을 포함한 공식적인 보고서 형식으로 작성해주세요."""
    }
    return prompts.get(writing_type, "")

def main():
    st.title("육하원칙 작문 생성기")

    # 세션 상태 초기화
    if 'generated_text' not in st.session_state:
        st.session_state.generated_text = ""

    # API 키 입력
    api_key = st.text_input("API 키:", type="password")

    # 작문 종류 선택
    writing_type = st.selectbox(
        "작문 종류:",
        ["시", "수필", "소설", "보고서"]
    )

    # 육하원칙 입력 필드들
    col1, col2 = st.columns(2)
    with col1:
        who = st.text_input("누가:")
        when = st.text_input("언제:")
        where = st.text_input("어디서:")
        what = st.text_input("무엇을:")
    
    with col2:
        how = st.text_input("어떻게:")
        why = st.text_input("왜:")
        who_with = st.text_input("누구와:")

    # 작문 생성 버튼
    if st.button("작문 생성"):
        if not api_key:
            st.error("API 키를 입력해주세요.")
            return

        # 육하원칙 정보 수집
        w5h1_info = {
            "누가": who,
            "언제": when,
            "어디서": where,
            "무엇을": what,
            "어떻게": how,
            "왜": why,
            "누구와": who_with
        }

        # 빈 필드 확인
        if not all(w5h1_info.values()):
            st.error("모든 필드를 입력해주세요.")
            return

        try:
            # Gemini 모델 설정
            genai.configure(api_key=api_key)
            llm = ChatGoogleGenerativeAI(
                google_api_key=api_key,
                model="gemini-1.0-pro",
                temperature=0.7
            )

            # 프롬프트 생성 및 작문 생성
            prompt = generate_writing_prompt(writing_type, w5h1_info)
            response = llm.invoke(prompt)
            
            # 결과 저장 및 표시
            st.session_state.generated_text = response.content
            st.text_area("생성된 작문:", value=st.session_state.generated_text, height=300)

        except Exception as e:
            st.error(f"오류가 발생했습니다: {str(e)}")

    # 수정사항 입력
    if st.session_state.generated_text:
        feedback = st.text_area("수정사항:", height=100)
        
        # 수정하여 재생성 버튼
        if st.button("수정하여 재생성"):
            if not api_key:
                st.error("API 키를 입력해주세요.")
                return

            if not feedback:
                st.error("수정사항을 입력해주세요.")
                return

            try:
                # Gemini 모델 설정
                genai.configure(api_key=api_key)
                llm = ChatGoogleGenerativeAI(
                    google_api_key=api_key,
                    model="gemini-1.0-pro",
                    temperature=0.7
                )

                # 수정 요청 프롬프트 생성
                revision_prompt = f"""다음 작문을 수정사항을 반영하여 새로 작성해주세요:

원본 작문:
{st.session_state.generated_text}

수정사항:
{feedback}

위의 수정사항을 반영하여 전체 작문을 새로 작성해주세요."""

                # 수정된 작문 생성
                response = llm.invoke(revision_prompt)
                
                # 결과 저장 및 표시
                st.session_state.generated_text = response.content
                st.text_area("수정된 작문:", value=st.session_state.generated_text, height=300)

            except Exception as e:
                st.error(f"오류가 발생했습니다: {str(e)}")

if __name__ == "__main__":
    main()
