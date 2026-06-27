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
        st.subheader("표 빈칸 채우기 (각 1점, 총 3점)")
        ans1 = st.text_input("(1) 과제의 특성 (쉬운 과제 관련):", placeholder="예: 비교적 쉬운 취미 생활이나 큰 노력을 들일 필요가 없는 과제")
        ans2 = st.text_input("(2) 환경 및 방법 (어려운 과제 관련):", placeholder="예: 충분히 연습하며 익숙해질 때까지 차분하게 혼자 집중하는 시간")
        ans3 = st.text_input("(3) 관련된 심리 현상:", placeholder="예: 사회적 억제")
        
        if st.button("1번 문항 채점하기"):
            score = 0
            feedback = []
            
            # (1)번 검증: '쉬운' 혹은 '노력X' 맥락 확인
            if check_keywords(ans1, [["쉬운", "취미", "노력"]]):
                score += 1
                feedback.append("• (1)번: 정답 (의미 통과)")
            else:
                feedback.append("• (1)번: 오답 (과제 난이도나 특성 기술 부족)")
                
            # (2)번 검증: '혼자/차분히' + '집중/연습' 맥락 확인
            if check_keywords(ans2, [["혼자", "차분"], ["집중", "연습"]]):
                score += 1
                feedback.append("• (2)번: 정답 (핵심 맥락 일치)")
            else:
                feedback.append("• (2)번: 오답 ('혼자 집중' 또는 '연습' 핵심 표현 부족)")
                
            # (3)번 검증: 정확한 용어 확인 (오개념 차단)
            if "억제" in ans3 and "촉진" not in ans3:
                score += 1
                feedback.append("• (3)번: 정답 (사회적 억제)")
            else:
                feedback.append("• (3)번: 오답 (촉진과 혼동했거나 오기입)")
                
            st.metric(label="획득 점수", value=f"{score} / 3 점")
            for f in feedback: st.write(f)

    with tab2:
        st.subheader("설명문 이어 쓰기 (총 4점)")
        st.info("주어진 첫 문장: 과제의 특성과 난이도에 따라 우리의 학습 효율을 높이는 방법은 다르게 적용되어야 한다.")
        
        method1 = st.selectbox("(1)번에 사용한 설명 방법", ["선택 안 함", "예시", "대조"])
        sent1 = st.text_area("(1)번 작성 문장:")
        
        method2 = st.selectbox("(2)번에 사용한 설명 방법", ["선택 안 함", "예시", "대조"])
        sent2 = st.text_area("(2)번 작성 문장:")
        
        if st.button("2번 문항 채점하기"):
            score = 0
            feedback = []
            
            if method1 == "선택 안 함" or method2 == "선택 안 함" or method1 == method2:
                st.error("조건 위반: 서로 다른 2가지 설명 방법을 선택해야 합니다.")
            else:
                # 괄호 표기 조건 검사
                kw_m1 = f"({method1})" in sent1 or f"<{method1}>" in sent1
                kw_m2 = f"({method2})" in sent2 or f"<{method2}>" in sent2
                
                # (1)번 선택지별 특성 및 결론 방향 검증
                score_1 = 0
                if method1 == "예시" and check_keywords(sent1, [["예를", "예로", "도서관", "커피숍", "모임"]]):
                    score_1 = 2 if kw_m1 else 1
                elif method1 == "대조" and check_keywords(sent1, [["반면", "달리", "반대로", "혼자", "차분"]]):
                    score_1 = 2 if kw_m1 else 1
                
                # (2)번 선택지별 특성 및 결론 방향 검증
                score_2 = 0
                if method2 == "예시" and check_keywords(sent2, [["예를", "예로", "도서관", "커피숍", "모임"]]):
                    score_2 = 2 if kw_m2 else 1
                elif method2 == "대조" and check_keywords(sent2, [["반면", "달리", "반대로", "혼자", "차분"]]):
                    score_2 = 2 if kw_m2 else 1
                
                total_score = score_1 + score_2
                st.metric(label="획득 점수", value=f"{total_score} / 4 점")
                if not (kw_m1 and kw_m2): st.warning("힌트: 문장 끝에 사용한 설명 방법 명칭을 괄호 안에 표기했는지 확인하세요.")

    with tab3:
        st.subheader("영상 기획안 및 연출 효과 (총 4점)")
        v_idx = st.text_area("(1) 시각 요소(Ⓐ) 계획 및 효과 서술:")
        a_idx = st.text_area("(2) 청각 요소(Ⓑ) 계획 및 효과 서술:")
        
        if st.button("3번 문항 채점하기"):
            v_score = 0
            a_score = 0
            
            # 시각 요소 결론 및 오개념 검증
            if check_keywords(v_idx, [["혼자", "방", "독서실", "책상"]]) and not has_misconception(v_idx, ["도서관", "친구", "모임"]):
                v_score += 1 # 연출 인정
                if check_keywords(v_idx, [["집중", "자극 차단", "전달"]]): v_score += 1 # 효과 인정
                
            # 청각 요소 결론 및 오개념 검증
            if check_keywords(a_idx, [["고요", "적막", "소음 제거", "초침", "연필"]]) and not has_misconception(a_idx, ["배경음악", "경쾌", "음악"]):
                a_score += 1 # 연출 인정
                if check_keywords(a_idx, [["차분", "분위기", "강조"]]): a_score += 1 # 효과 인정
                
            st.metric(label="획득 점수", value=f"{v_score + a_score} / 4 점")

# -------------------------------------------------------------------------
# 2세트 채점 로직
# -------------------------------------------------------------------------
elif set_option == "2세트 (정전기의 특징)":
    st.header("⚡ [실전 적용 - 2] 겨울철 불청객 정전기")
    
    tab1, tab2, tab3 = st.tabs(["[서·논술형 1] 표 채우기", "[서·논술형 2] 설명문 작성", "[서·논술형 3] 영상 기획안"])
    
    with tab1:
        st.subheader("표 빈칸 채우기 (각 1점, 총 3점)")
        ans1 = st.text_input("(1) 물의 상태에 비유:", placeholder="예: 높은 곳에 고여 있는 물")
        ans2 = st.text_input("(2) 전하의 상태:", placeholder="예: 전하가 이동하지 않고 머물러 있음")
        ans3 = st.text_input("(3) 위험성 여부:", placeholder="예: 위험하지 않음")
        
        if st.button("1번 문항 채점하기"):
            score = 0
            if check_keywords(ans1, [["고여", "멈춘"]]): score += 1
            if check_keywords(ans2, [["이동하지", "머물", "정지"]]): score += 1
            if check_keywords(ans3, [["위험하지", "안전", "피해X", "무해"]]): score += 1
            st.metric(label="획득 점수", value=f"{score} / 3 점")

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
                elif "비교" in method1 or "대조" in method1:
                    if check_keywords(sent1, [["물", "고여", "흐르는"]]) and not has_misconception(sent1, ["시간적으로 변화하지"]):
                        score_1 = 2 if kw_m1 else 1
                        
                score_2 = 0
                if method2 == "정의" and check_keywords(sent2, [["전기", "뜻", "의미", "말한다"]]) and not has_misconception(sent2, ["흐르는 물"]):
                    score_2 = 2 if kw_m2 else 1
                elif "비교" in method2 or "대조" in method2:
                    if check_keywords(sent2, [["물", "고여", "흐르는"]]) and not has_misconception(sent2, ["시간적으로 변화하지"]):
                        score_2 = 2 if kw_m2 else 1
                        
                st.metric(label="획득 점수", value=f"{score_1 + score_2} / 4 점")

    with tab3:
        st.subheader("영상 기획안 및 연출 효과 (총 4점)")
        v_idx = st.text_area("(1) 시각 요소(Ⓐ) 및 효과 (높은 곳에 고여 있는 물 관련):")
        a_idx = st.text_area("(2) 청각 요소(Ⓑ) 및 효과 (위험하지 않은 특성 관련):")
        
        if st.button("3번 문항 채점하기"):
            v_score = 0
            a_score = 0
            
            # 시각 요소 검증 (높은 곳 + 고여있는 물 필수)
            if check_keywords(v_idx, [["높은", "절벽", "산"], ["고여", "댐", "저수지"]]) and not has_misconception(v_idx, ["폭포", "쏟아"]):
                v_score += 1
                if check_keywords(v_idx, [["전압", "이동하지", "시각화", "이해"]]): v_score += 1
                
            # 청각 요소 검증 (고요함 -> 위험하지 않음 연결 결론 확인)
            if check_keywords(a_idx, [["고요", "적막", "소리 없는"]]) and not has_misconception(a_idx, ["웅장", "물소리", "스파크"]):
                a_score += 1
                if check_keywords(a_idx, [["위험하지", "피해가 없는", "안도감", "대조"]]): a_score += 1
                
            st.metric(label="획득 점수", value=f"{v_score + a_score} / 4 점")

# -------------------------------------------------------------------------
# 3세트 채점 로직
# -------------------------------------------------------------------------
elif set_option == "3세트 (인간 vs AI 예술)":
    st.header("🎨 [실전 적용 - 3] 인공 지능이 그린 그림의 예술성")
    
    tab1, tab2, tab3 = st.tabs(["[서·논술형 1] 표 채우기", "[서·논술형 2] 설명문 작성", "[서·논술형 3] 영상 기획안"])
    
    with tab1:
        st.subheader("표 빈칸 채우기 (각 1점, 총 3점)")
        ans1 = st.text_input("(1) 올림픽 경기에 비유:", placeholder="예: 로봇이 한 번의 실수 없이 완벽하게 피겨 스케이팅을 해내는 경기")
        ans2 = st.text_input("(2) 예술로 볼 수 있는가(근거 포함):", placeholder="예: 감정이 없고 독자적인 철학이 없으므로 예술이 아니다")
        ans3 = st.text_input("(3) 예술로서의 가치:", placeholder="예: 미술계 변화를 가져오고 예술의 범주를 확장하는 상징적 가치")
        
        if st.button("1번 문항 채점하기"):
            score = 0
            if check_keywords(ans1, [["로봇", "인공지능"], ["피겨", "스케이팅", "완벽"]]): score += 1
            if check_keywords(ans2, [["감정", "철학", "이야기"], ["어렵다", "아니다", "부정"]]): score += 1 # 결론 방향 확인
            if check_keywords(ans3, [["변화", "확장", "상징"]]): score += 1
            st.metric(label="획득 점수", value=f"{score} / 3 점")

    with tab2:
        st.subheader("설명문 이어 쓰기 (총 4점)")
        st.info("주어진 첫 문장: 인공 지능이 그린 그림이 늘어나는 요즘, 우리는 이 작품들을 어떤 눈으로 바라봐야 할지 올바르게 생각해야 한다.")
        
        method1 = st.selectbox("(1)번에 사용한 설명 방법", ["선택 안 함", "분석", "대조"])
        sent1 = st.text_area("(1)번 작성 문장:")
        
        method2 = st.selectbox("(2)번에 사용한 설명 방법", ["선택 안 함", "분석", "대조"])
        sent2 = st.text_area("(2)번 작성 문장:")
        
        if st.button("2번 문항 채점하기"):
            if method1 == "선택 안 함" or method2 == "선택 안 함" or method1 == method2:
                st.error("조건 위반: 서로 다른 설명 방법을 선택해야 합니다.")
            else:
                kw_m1 = f"({method1})" in sent1
                kw_m2 = f"({method2})" in sent2
                
                score_1 = 0
                if method1 == "분석" and check_keywords(sent1, [["감정", "철학", "경험", "관점", "요소"]]):
                    score_1 = 2 if kw_m1 else 1
                elif method1 == "대조" and check_keywords(sent1, [["반면", "인공지능", "차이", "없다"]]):
                    score_1 = 2 if kw_m1 else 1
                    
                score_2 = 0
                if method2 == "분석" and check_keywords(sent2, [["감정", "철학", "경험", "관점", "요소"]]):
                    score_2 = 2 if kw_m2 else 1
                elif method2 == "대조" and check_keywords(sent2, [["반면", "인공지능", "차이", "없다"]]):
                    score_2 = 2 if kw_m2 else 1
                    
                st.metric(label="획득 점수", value=f"{score_1 + score_2} / 4 점")

    with tab3:
        st.subheader("영상 기획안 및 연출 효과 (총 4점)")
        v_idx = st.text_area("(1) 시각 요소(Ⓐ) 및 효과 (인간의 열정/노력 관련):")
        a_idx = st.text_area("(2) 청각 요소(Ⓑ) 및 효과 (마음의 울림/박수 관련):")
        
        if st.button("3번 문항 채점하기"):
            v_score = 0
            a_score = 0
            
            # 시각 요소 (인간의 피겨 연기 혹은 인간 예술가 매칭)
            if check_keywords(v_idx, [["인간", "선수", "예술가"], ["땀", "열정", "노력"]]) and not has_misconception(v_idx, ["로봇", "기계"]):
                v_score += 1
                if check_keywords(v_idx, [["감정", "가치", "시각적", "전달"]]): v_score += 1
                
            # 청각 요소 (풍부한 음악 및 환호성 매칭 -> 감동/울림 결론 확인)
            if check_keywords(a_idx, [["오케스트라", "음악", "풍부"], ["환호", "박수"]]) and not has_misconception(a_idx, ["메트로놈", "기계음"]):
                a_score += 1
                if check_keywords(a_idx, [["울림", "감동", "대조", "부각"]]): a_score += 1
                
            st.metric(label="획득 점수", value=f"{v_score + a_score} / 4 점")
