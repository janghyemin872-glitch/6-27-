import streamlit as st
import re

# 페이지 설정
st.set_page_config(page_title="국어 서논술형 자동 채점 시스템", layout="wide")

st.title("📝 2회고사 대비 서논술형 자동 채점 시스템")
st.markdown("---")

# 세트 선택 서브메뉴
set_option = st.sidebar.selectbox("채점할 문항 세트를 선택하세요", ["1세트 (사회적 촉진/억제)", "2세트 (정전기의 특징)", "3세트 (인간 vs AI 예술)"])

# -------------------------------------------------------------------------
# [유틸리티 함수] 키워드 및 오개념 검증 로직
# -------------------------------------------------------------------------
def check_keywords(text, keyword_lists):
    """지정된 키워드 그룹 중 하나라도 포함되어 있는지 확인 (의미 중심 허용 범위 반영)"""
    for keywords in keyword_lists:
        if any(kw in text for kw in keywords):
            continue
        return False
    return True

def has_misconception(text, error_keywords):
    """오개념 방지: 다른 개념의 특성을 가져다 썼는지 확인"""
    return any(ekw in text for ekw in error_keywords)

# -------------------------------------------------------------------------
# 1세트 채점 로직
# -------------------------------------------------------------------------
if set_option == "1세트 (사회적 촉진/억제)":
    st.header("🍏 [실전 적용 - 1] 과제 난이도에 따른 학습 전략")
    
    tab1, tab2, tab3 = st.tabs(["[서·논술형 1] 표 채우기", "[서·논술형 2] 설명문 작성", "[서·논술형 3] 영상 기획안"])
    
    with tab1:
        st.subheader("표 빈칸 저장 (각 1점, 총 3점)")
        ans_a = st.text_input("(ㄱ) 과제의 특성 (쉬운 과제 관련):", placeholder="예: 비교적 쉬운 취미 생활이나 큰 노력을 들일 필요가 없는 과제")
        ans_b = st.text_input("(ㄴ) 환경 및 방법 (어려운 과제 관련):", placeholder="예: 충분히 연습하며 익숙해질 때까지 차분하게 혼자 집중하는 시간")
        ans_c = st.text_input("(ㄷ) 관련된 심리 현상:", placeholder="예: 사회적 억제")
        
        if st.button("1번 문항 채점하기"):
            score = 0
            feedback = []
            
            # (ㄱ)번 검증: '쉬운' 혹은 '노력X' 맥락 확인
            if check_keywords(ans_a, [["쉬운", "취미", "노력"]]):
                score += 1
                feedback.append("• (ㄱ)번: 정답 (의미 통과)")
            else:
                feedback.append("• (ㄱ)번: 오답 (과제 난이도나 특성 기술 부족)")
                
            # (ㄴ)번 검증: '혼자/차분히' + '집중/연습' 맥락 확인
            if check_keywords(ans_b, [["혼자", "차분"], ["집중", "연습"]]):
                score += 1
                feedback.append("• (ㄴ)번: 정답 (핵심 맥락 일치)")
            else:
                feedback.append("• (ㄴ)번: 오답 ('혼자 집중' 또는 '연습' 핵심 표현 부족)")
                
            # (ㄷ)번 검증: 정확한 용어 확인 (오개념 차단)
            if "억제" in ans_c and "촉진" not in ans_c:
                score += 1
                feedback.append("• (ㄷ)번: 정답 (사회적 억제)")
            else:
                feedback.append("• (ㄷ)번: 오답 (촉진과 혼동했거나 오기입)")
                
            st.write("### 획득 점수")
            st.write(f"## {score} / 3 점")
            for f in feedback: st.write(f)

    with tab2:
        st.subheader("설명문 이어 쓰기 (총 4점)")
        st.info("주어진 첫 문장: 과제의 특성과 난이도에 따라 우리의 학습 효율을 높이는 방법은 다르게 적용되어야 한다.")
        
        method1 = st.selectbox("(1)번에 사용한 설명 방법", ["선택 안 함", "예시", "대조"])
        sent1 = st.text_area("(1)번 작성 문장:")
        
        method2 = st.selectbox("(2)번에 사용한 설명 방법", ["선택 안 함", "예시", "대조"])
        sent2 = st.text_area("(2)번 작성 문장:")
        
        if st.button("2번 문항 채점하기"):
            if method1 == "선택 안 함" or method2 == "선택 안 함" or method1 == method2:
                st.error("조건 위반: 서로 다른 2가지 설명 방법을 선택해야 합니다.")
            else:
                kw_m1 = f"({method1})" in sent1 or f"<{method1}>" in sent1
                kw_m2 = f"({method2})" in sent2 or f"<{method2}>" in sent2
                
                score_1 = 0
                if method1 == "예시" and check_keywords(sent1, [["예를", "예로", "도서관", "커피숍", "모임"]]):
                    score_1 = 2 if kw_m1 else 1
                elif method1 == "대조" and check_keywords(sent1, [["반면", "달리", "반대로", "혼자", "차분"]]):
                    score_1 = 2 if kw_m1 else 1
                
                score_2 = 0
                if method2 == "예시" and check_keywords(sent2, [["예를", "예로", "도서관", "커피숍", "모임"]]):
                    score_2 = 2 if kw_m2 else 1
                elif method2 == "대조" and check_keywords(sent2, [["반면", "달리", "반대로", "혼자", "차분"]]):
                    score_2 = 2 if kw_m2 else 1
                
                total_score = score_1 + score_2
                st.write("### 획득 점수")
                st.write(f"## {total_score} / 4 점")
                if not (kw_m1 and kw_m2): st.warning("힌트: 문장 끝에 사용한 설명 방법 명칭을 괄호 안에 표기했는지 확인하세요.")

    with tab3:
        st.subheader("영상 기획안 및 연출 효과 (총 4점)")
        v_idx = st.text_area("(1) 시각 요소(Ⓐ) 계획 및 효과 서술:")
        a_idx = st.text_area("(2) 청각 요소(Ⓑ) 계획 및 효과 서술:")
        
        if st.button("3번 문항 채점하기"):
            v_score = 0
            a_score = 0
            if check_keywords(v_idx, [["혼자", "방", "독서실", "책상"]]) and not has_misconception(v_idx, ["도서관", "친구", "모임"]):
                v_score += 1
                if check_keywords(v_idx, [["집중", "자극 차단", "전달"]]): v_score += 1
                
            if check_keywords(a_idx, [["고요", "적막", "소음 제거", "초침", "연필"]]) and not has_misconception(a_idx, ["배경음악", "경쾌", "음악"]):
                a_score += 1
                if check_keywords(a_idx, [["차분", "분위기", "강조"]]): a_score += 1
                
            st.write("### 획득 점수")
            st.write(f"## {v_score + a_score} / 4 점")

# -------------------------------------------------------------------------
# 2세트 채점 로직
# -------------------------------------------------------------------------
elif set_option == "2세트 (정전기의 특징)":
    st.header("⚡ [실전 적용 - 2] 겨울철 불청객 정전기")
    
    tab1, tab2, tab3 = st.tabs(["[서·논술형 1] 표 채우기", "[서·논술형 2] 설명문 작성", "[서·논술형 3] 영상 기획안"])
    
    with tab1:
        st.subheader("표 빈칸 저장 (각 1점, 총 3점)")
        ans_a = st.text_input("(ㄱ) 물의 상태에 비유:", placeholder="예: 높은 곳에 고여 있는 물")
        ans_b = st.text_input("(ㄴ) 전하의 상태:", placeholder="예: 전하가 이동하지 않고 머물러 있음")
        ans_c = st.text_input("(ㄷ) 위험성 여부:", placeholder="예: 위험하지 않음")
        
        if st.button("1번 문항 채점하기"):
            score = 0
            feedback = []
            if check_keywords(ans_a, [["고여", "멈춘"]]): 
                score += 1
                feedback.append("• (ㄱ)번: 정답")
            else: feedback.append("• (ㄱ)번: 오답")
                
            if check_keywords(ans_b, [["이동하지", "머물", "정지"]]): 
                score += 1
                feedback.append("• (ㄴ)번: 정답")
            else: feedback.append("• (ㄴ)번: 오답")
                
            if check_keywords(ans_c, [["위험하지", "안전", "피해X", "무해"]]): 
                score += 1
                feedback.append("• (ㄷ)번: 정답")
            else: feedback.append("• (ㄷ)번: 오답")
                
            st.write("### 획득 점수")
            st.write(f"## {score} / 3 점")
            for f in feedback: st.write(f)

    with tab2:
        st.subheader("설명문 이어 쓰기 (총 4점)")
        st.info("주어진 첫 문장: 겨울철에 흔히 겪는 정전기는 우리가 평소 집에서 사용하는 전기와는 다른 뚜렷한 특징이 있다.")
        
        method1 = st.selectbox("(1)번에 사용한 설명 방법", ["선택 안 함", "정의", "비교와 대조"])
        sent1 = st.text_area("(1)번 작성 문장:")
        
        method2 = st.selectbox("(2)번에 사용한 설명 방법", ["선택 안 함", "정의", "비교와 대조"])
        sent2 = st.text_area("(2)번 작성 문장:")
        
        if st.button("2번 문항 채점하기"):
            if method1 == "선택 안 함" or method2 == "선택 안 함" or method1 == method2:
                st.error("조건 위반: 서로 다른 설명 방법을 선택해야 합니다.")
            else:
                kw_m1 = f"({method1})" in sent1 or "비교" in sent1 or "대조" in sent1 if method1=="비교와 대조" else f"({method1})" in sent1
                kw_m2 = f"({method2})" in sent2 or "비교" in sent2 or "대조" in sent2 if method2=="비교와 대조" else f"({method2})" in sent2
                
                score_1 = 0
                if method1 == "정의" and check_keywords(sent1, [["전기", "뜻", "의미", "말한다"]]) and not has_misconception(sent1, ["흐르는 물"]):
                    score_1 = 2 if kw_m1 else 1
                elif "비교" in method1
