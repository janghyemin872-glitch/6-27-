import streamlit as st

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
    for keywords in keyword_lists:
        if any(kw in text for kw in keywords):
            continue
        return False
    return True

def has_misconception(text, error_keywords):
    return any(ekw in text for ekw in error_keywords)

# -------------------------------------------------------------------------
# 1세트 채점 로직
# -------------------------------------------------------------------------
if set_option == "1세트 (사회적 촉진/억제)":
    st.header("🍏 [실전 적용 - 1] 과제 난이도에 따른 학습 전략")
    
    tab1, tab2, tab3 = st.tabs(["[서·논술형 1] 표 채우기", "[서·논술형 2] 설명문 작성", "[서·논술형 3] 영상 기획안"])
    
    with tab1:
        st.info("""
        [자료] 사회적 촉진과 억제 요약표
        - 쉬운 과제 처리 시: 타인의 존재가 수행 능력을 높임 (사회적 촉진)
        - 어려운 과제 처리 시: 타인의 존재가 수행 능력을 떨어뜨림 (사회적 억제)
        - (ㄱ) 과제의 특성 ──> 커피숍이나 도서관 등 개방된 공간 활용
        - (ㄴ) 환경 및 방법 ──> 충분히 연습하며 익숙해질 때까지 차분하게 혼자 집중하는 시간 필요
        - 관련된 심리 현상 ──> (ㄷ)
        """)
        
        st.code("""
        📌 조건 1: 지문에 제시된 핵심 내용을 바탕으로 문맥에 맞게 작성할 것
        📌 조건 2: (ㄷ)은 정확한 심리학 용어를 사용할 것
        """, language="text")
        
        st.markdown("위 요약표를 바탕으로 빈칸 (ㄱ)에 들어갈 적절한 내용을 내용을 찾아 쓰시오.")
        ans_a = st.text_input("ans_a", label_visibility="collapsed")
        
        st.markdown("위 요약표를 바탕으로 빈칸 (ㄴ)에 들어갈 적절한 내용을 내용을 찾아 쓰시오.")
        ans_b = st.text_input("ans_b", label_visibility="collapsed")
        
        st.markdown("위 요약표를 바탕으로 빈칸 (ㄷ)에 들어갈 적절한 내용을 내용을 찾아 쓰시오.")
        ans_c = st.text_input("ans_c", label_visibility="collapsed")
        
        if st.button("1번 문항 채점하기"):
            score = 0
            feedback = []
            
            if check_keywords(ans_a, [["쉬운", "취미", "노력"]]):
                score += 1
                feedback.append("ㄱ번 항목은 정답입니다. 의미가 올바르게 통합니다.")
            else:
                feedback.append("ㄱ번 항목은 오답입니다. 과제의 난이도나 특성 기술이 부족합니다.")
                
            if check_keywords(ans_b, [["혼자", "차분"], ["집중", "연습"]]):
                score += 1
                feedback.append("ㄴ번 항목은 정답입니다. 핵심 맥락이 일치합니다.")
            else:
                feedback.append("ㄴ번 항목은 오답입니다. 혼자 집중 또는 연습이라는 핵심 표현이 부족합니다.")
                
            if "억제" in ans_c and "촉진" not in ans_c:
                score += 1
                feedback.append("ㄷ번 항목은 정답입니다. 사회적 억제 용어가 정확합니다.")
            else:
                feedback.append("ㄷ번 항목은 오답입니다. 사회적 촉진 현상과 혼동했거나 잘못 기입되었습니다.")
                
            st.write("### 최종 채점 결과")
            st.write(f"총점 {score} 점 / 3 점 만점")
            for f in feedback: st.write(f)

    with tab2:
        st.info("""
        [자료] 첫 문장 제시
        과제의 특성과 난이도에 따라 우리의 학습 효율을 높이는 방법은 다르게 적용되어야 한다.
        """)
        
        st.code("""
        ⚠️ 조건 1: 서로 다른 두 가지 설명 방법을 사용하여 두 문장으로 작성할 것
        ⚠️ 조건 2: 각 문장 끝에 자신이 사용한 설명 방법의 명칭을 괄호에 넣어 표기할 것
        ⚠️ 조건 3: 지문에 제시된 과제 난이도별 환경 구축 내용을 모두 포함할 것
        """, language="text")
        
        st.markdown("첫 번째 문장에 사용할 설명 방법을 선택하고 해당 내용을 문장으로 이어 쓰시오.")
        method1 = st.selectbox("m1", ["선택 안 함", "예시", "대조"], label_visibility="collapsed")
        sent1 = st.text_area("s1", label_visibility="collapsed")
        
        st.markdown("두 번째 문장에 사용할 설명 방법을 선택하고 해당 내용을 문장으로 이어 쓰시오.")
        method2 = st.selectbox("m2", ["선택 안 함", "예시", "대조"], label_visibility="collapsed")
        sent2 = st.text_area("s2", label_visibility="collapsed")
        
        if st.button("2번 문항 채점하기"):
            if method1 == "선택 안 함" or method2 == "선택 안 함" or method1 == method2:
                st.error("오류: 조건에 맞게 서로 다른 두 가지 설명 방법을 선택해야 합니다.")
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
                st.write("### 최종 채점 결과")
                st.write(f"총점 {total_score} 점 / 4 점 만점")
                if not (kw_m1 and kw_m2): 
                    st.warning("안내: 문장 끝에 설명 방법 명칭을 괄호 안에 올바르게 표기하지 않아 감점 요소가 있습니다.")

    with tab3:
        st.info("""
        [자료] 영상 제작 상황
        장면 1: 경쾌한 음악이 흐르며 친구들과 도서관에서 쉬운 퀴즈 과제를 함께 해결하는 모습 (사회적 촉진 시각화)
        장면 2: 어려운 과제를 해결해야 하는 상황에 알맞은 시각 및 청각 연출 계획 (사회적 억제 대응)
        """)
        
        st.code("""
        📢 조건 1: 어려운 과제를 해결할 때 필요한 환경의 특성이 시각과 청각에 모두 드러날 것
        📢 조건 2: 장면 1의 연출 분위기와 대조를 이룰 수 있도록 구상할 것
        """, language="text")
        
        st.markdown("장면 2에 들어갈 시각 요소를 기획하고 그렇게 연출했을 때 얻을 수 있는 효과를 설명하시오.")
        v_idx = st.text_area("v1", label_visibility="collapsed")
        
        st.markdown("장면 2에 들어갈 청각 요소를 기획하고 그렇게 연출했을 때 얻을 수 있는 효과를 설명하시오.")
        a_idx = st.text_area("a1", label_visibility="collapsed")
        
        if st.button("3번 문항 채점하기"):
            v_score = 0
            a_score = 0
            if check_keywords(v_idx, [["혼자", "방", "독서실", "책상"]]) and not has_misconception(v_idx, ["도서관", "친구", "모임"]):
                v_score += 1
                if check_keywords(v_idx, [["집중", "자극 차단", "전달"]]): v_score += 1
                
            if check_keywords(a_idx, [["고요", "적막", "소음 제거", "초침", "연필"]]) and not has_misconception(a_idx, ["배경음악", "경쾌", "음악"]):
                a_score += 1
                if check_keywords(a_idx, [["차분", "분위기", "강조"]]): a_score += 1
                
            st.write("### 최종 채점 결과")
            st.write(f"총점 {v_score + a_score} 점 / 4 점 만점")

# -------------------------------------------------------------------------
# 2세트 채점 로직
# -------------------------------------------------------------------------
elif set_option == "2세트 (정전기의 특징)":
    st.header("⚡ [실전 적용 - 2] 겨울철 불청객 정전기")
    
    tab1, tab2, tab3 = st.tabs(["[서·논술형 1] 표 채우기", "[서·논술형 2] 설명문 작성", "[서·논술형 3] 영상 기획안"])
    
    with tab1:
        st.info("""
        [자료] 실생활 전기와 정전기 비교표
        - 실생활 전기 ──> 흐르는 물에 비유 ──> 전하가 계속 이동함 ──> 전압은 낮으나 감전 위험 있음
        - 정전기 ──> (ㄱ)에 비유 ──> (ㄴ) ──> 전압은 매우 높으나 (ㄷ)
        """)
        
        st.code("""
        📌 조건 1: 본문에 제시된 비유 표현과 과학적 사실을 정확히 근거로 삼을 것
        📌 조건 2: 흐르는 전기와 정전기의 차이점이 명확히 부각되도록 단어를 선택할 것
        """, language="text")
        
        st.markdown("본문의 비유적 설명을 바탕으로 빈칸 (ㄱ)에 들어갈 핵심 단어나 문장을 완성하시오.")
        ans_a = st.text_input("ans_2a", label_visibility="collapsed")
        
        st.markdown("본문의 비유적 설명을 바탕으로 빈칸 (ㄴ)에 들어갈 핵심 단어나 문장을 완성하시오.")
        ans_b = st.text_input("ans_2b", label_visibility="collapsed")
        
        st.markdown("본문의 비유적 설명을 바탕으로 빈칸 (ㄷ)에 들어갈 핵심 단어나 문장을 완성하시오.")
        ans_c = st.text_input("ans_2c", label_visibility="collapsed")
        
        if st.button("1번 문항 채점하기"):
            score = 0
            feedback = []
            if check_keywords(ans_a, [["고여", "멈춘"]]): 
                score += 1
                feedback.append("ㄱ번 항목은 정답입니다. 고여 있는 물의 특성을 잘 파악했습니다.")
            else: feedback.append("ㄱ번 항목은 오답입니다. 물의 상태 비유가 적절하지 않습니다.")
                
            if check_keywords(ans_b, [["이동하지", "머물", "정지"]]): 
                score += 1
                feedback.append("ㄴ번 항목은 정답입니다. 전하의 정지 상태를 잘 설명했습니다.")
            else: feedback.append("ㄴ번 항목은 오답입니다. 전하의 이동 여부를 다시 확인해 주세요.")
                
            if check_keywords(ans_c, [["위험하지", "안전", "피해X", "무해"]]): 
                score += 1
                feedback.append("ㄷ번 항목은 정답입니다. 위험성이 없음을 명확히 짚어냈습니다.")
            else: feedback.append("ㄷ번 항목은 오답입니다. 인체 영향이나 위험성 결론이 잘못되었습니다.")
                
            st.write("### 최종 채점 결과")
            st.write(f"총점 {score} 점 / 3 점 만점")
            for f in feedback: st.write(f)

    with tab2:
        st.info("""
        [자료] 첫 문장 제시
        겨울철에 흔히 겪는 정전기는 우리가 평소 집에서 사용하는 전기와는 다른 뚜렷한 특징이 있다.
        """)
        
        st.code("""
        ⚠️ 조건 1: 정의의 설명 방법과 비교와 대조의 설명 방법을 각각 한 번씩 사용할 것
        ⚠️ 조건 2: 문장 간 인과 관계나 논리적 흐름이 자연스럽게 이어지도록 서술할 것
        """, language="text")
        
        st.markdown("첫 번째 문장에 사용할 설명 방법을 선택하고 정전기의 개념 혹은 비유적 특성을 이어 쓰시오.")
        method1 = st.selectbox("m2_1", ["선택 안 함", "정의", "비교와 대조"], label_visibility="collapsed")
        sent1 = st.text_area("s2_1", label_visibility="collapsed")
        
        st.markdown("두 번째 문장에 사용할 설명 방법을 선택하고 정전기의 개념 혹은 비유적 특성을 이어 쓰시오.")
        method2 = st.selectbox("m2_2", ["선택 안 함", "정의", "비교와 대조"], label_visibility="collapsed")
        sent2 = st.text_area("s2_2", label_visibility="collapsed")
        
        if st.button("2번 문항 채점하기"):
            if method1 == "선택 안 함" or method2 == "선택 안 함" or method1 == method2:
                st.error("오류: 조건에 맞게 서로 다른 설명 방법을 매칭해야 합니다.")
            else:
                is_comp1 = "비교" in method1 or "대조" in method1
                is_comp2 = "비교" in method2 or "대조" in method2
                
                kw_m1 = "비교" in sent1 or "대조" in sent1 if is_comp1 else f"({method1})" in sent1
                kw_m2 = "비교" in sent2 or "대조" in sent2 if is_comp2 else f"({method2})" in sent2
                
                score_1 = 0
                if method1 == "정의" and check_keywords(sent1, [["전기", "뜻", "의미", "말한다"]]) and not has_misconception(sent1, ["흐르는 물"]):
                    score_1 = 2 if kw_m1 else 1
                elif is_comp1:
                    if check_keywords(sent1, [["물", "고여", "흐르는"]]) and not has_misconception(sent1, ["시간적으로 변화하지"]):
                        score_1 = 2 if kw_m1 else 1
                        
                score_2 = 0
                if method2 == "정의" and check_keywords(sent2, [["전기", "뜻", "의미", "말한다"]]) and not has_misconception(sent2, ["흐르는 물"]):
                    score_2 = 2 if kw_m2 else 1
                elif is_comp2:
                    if check_keywords(sent2, [["물", "고여", "흐르는"]]) and not has_misconception(sent2, ["시간적으로 변화하지"]):
                        score_2 = 2 if kw_m2 else 1
                        
                st.write("### 최종 채점 결과")
                st.write(f"총점 {score_1 + score_2} 점 / 4 점 만점")

    with tab3:
        st.info("""
        [자료] 영상 화면 구성안
        - 장면 1: 웅장하게 흐르는 폭포와 거센 물소리를 보여주며 우리가 쓰는 전기를 설명함
        - 장면 2: 정전기의 과학적 원리(고여 있는 물, 위험하지 않음)를 전달하기 위한 시각 및 청각 계획
        """)
        
        st.code("""
        📢 조건 1: 반드시 본문 속 높은 곳에 고여 있는 물이라는 근거가 시각 연출에 반영될 것
        📢 조건 2: 정전기가 인체에 위험하지 않다는 결론적 메시지가 청각적 분위기로 형상화될 것
        """, language="text")
        
        st.markdown("장면 2의 구체적인 시각 연출 계획과 그 연출을 통해 달성하려는 시청자 전달 효과를 서술하시오.")
        v_idx = st.text_area("v2", label_visibility="collapsed")
        
        st.markdown("장면 2의 구체적인 청각 연출 계획과 그 연출을 통해 달성하려는 시청자 전달 효과를 서술하시오.")
        a_idx = st.text_area("a2", label_visibility="collapsed")
        
        if st.button("3번 문항 채점하기"):
            v_score = 0
            a_score = 0
            if check_keywords(v_idx, [["높은", "절벽", "산"], ["고여", "댐", "저수지"]]) and not has_misconception(v_idx, ["폭포", "쏟아"]):
                v_score += 1
                if check_keywords(v_idx, [["전압", "이동하지", "시각화", "이해"]]): v_score += 1
                
            if check_keywords(a_idx, [["고요", "적막", "소리 없는"]]) and not has_misconception(a_idx, ["웅장", "물소리", "스파크"]):
                a_score += 1
                if check_keywords(a_idx, [["위험하지", "피해가 없는", "안도감", "대조"]]): a_score += 1
                
            st.write("### 최종 채점 결과")
            st.write(f"총점 {v_score + a_score} 점 / 4 점 만점")

# -------------------------------------------------------------------------
# 3세트 채점 로직
# -------------------------------------------------------------------------
elif set_option == "3세트 (인간 vs AI 예술)":
    st.header("🎨 [실전 적용 - 3] 인공 지능이 그린 그림의 예술성")
    
    tab1, tab2, tab3 = st.tabs(["[서·논술형 1] 표 채우기", "[서·논술형 2] 설명문 작성", "[서·논술형 3] 영상 기획안"])
    
    with tab1:
        st.info("""
        [자료] 인간의 예술성과 인공지능 그림의 대조표
        - 인간의 예술 ──> 선수들의 노력과 열정이 담긴 올림픽 경기 ──> 작가의 철학이 담겨 예술임 ──> 남다른 감동을 줌
        - AI 그림 ──> (ㄱ) ──> (ㄴ) ──> 미술계 변화 및 예술 범주를 확장하는 (ㄷ)
        """)
        
        st.code("""
        📌 조건 1: (ㄴ)은 인공지능 작품이 예술로 인정받기 어려운 이유를 논리적 근거와 함께 쓸 것
        📌 조건 2: (ㄷ)은 본문에서 인정한 인공지능 그림만의 가치 유형을 명시할 것
        """, language="text")
        
        st.markdown("지문의 핵심 대조 항목을 고려하여 빈칸 (ㄱ)에 들어갈 알맞은 내용을 비유적으로 표현해 채우시오.")
        ans_a = st.text_input("ans_3a", label_visibility="collapsed")
        
        st.markdown("지문의 핵심 대조 항목을 고려하여 빈칸 (ㄴ)에 들어갈 알맞은 내용을 근거와 함께 채우시오.")
        ans_b = st.text_input("ans_3b", label_visibility="collapsed")
        
        st.markdown("지문의 핵심 대조 항목을 고려하여 빈칸 (ㄷ)에 들어갈 알맞은 가치 유형을 기술하여 채우시오.")
        ans_c = st.text_input("ans_3c", label_visibility="collapsed")
        
        if st.button("1번 문항 채점하기"):
            score = 0
            feedback = []
            if check_keywords(ans_a, [["로봇", "인공지능"], ["피겨", "스케이팅", "완벽"]]): 
                score += 1
                feedback.append("ㄱ번 항목은 정답입니다. 기계적 완벽함 비유를 정확히 포착했습니다.")
            else: feedback.append("ㄱ번 항목은 오답입니다. 올림픽 경기 비유 대상을 다시 찾아보세요.")
                
            if check_keywords(ans_b, [["감정", "철학", "이야기"], ["어렵다", "아니다", "부정"]]): 
                score += 1
                feedback.append("ㄴ번 항목은 정답입니다. 한계점과 부정이 명확히 연결되었습니다.")
            else: feedback.append("ㄴ번 항목은 오답입니다. 예술로 보기 어려운 근거와 판단 결론이 부족합니다.")
                
            if check_keywords(ans_c, [["변화", "확장", "상징"]]): 
                score += 1
                feedback.append("ㄷ번 항목은 정답입니다. 상징적 가치와 범주 확장의 의의를 잘 짚었습니다.")
            else: feedback.append("ㄷ번 항목은 오답입니다. 본문 마지막 단락에 제시된 가치 내용을 확인하세요.")
                
            st.write("### 최종 채점 결과")
            st.write(f"총점 {score} 점 / 3 점 만점")
            for f in feedback: st.write(f)

    with tab2:
        st.info("""
        [자료] 첫 문장 제시
        인공 지능이 그린 그림이 늘어나는 요즘, 우리는 이 작품들을 어떤 눈으로 바라봐야 할지 올바르게 생각해야 한다.
        """)
        
        st.code("""
        ⚠️ 조건 1: 인간 예술의 구성 요소를 쪼개어 설명하는 분석 방법을 사용할 것
        ⚠️ 조건 2: 인간과 인공지능의 차이점을 극명히 드러내는 대조 방법을 사용할 것
        """, language="text")
        
        st.markdown("첫 번째 문장에 사용할 설명 방법을 선택하고 해당 기법에 맞춰 인간 예술의 구성 요소를 서술해 이어 쓰시오.")
        method1 = st.selectbox("m3_1", ["선택 안 함", "분석", "대조"], label_visibility="collapsed")
        sent1 = st.text_area("s3_1", label_visibility="collapsed")
        
        st.markdown("두 번째 문장에 사용할 설명 방법을 선택하고 해당 기법에 맞춰 인간과 인공지능 작품의 차이를 서술해 이어 쓰시오.")
        method2 = st.selectbox("m3_2", ["선택 안 함", "분석", "대조"], label_visibility="collapsed")
        sent2 = st.text_area("s3_2", label_visibility="collapsed")
        
        if st.button("2번 문항 채점하기"):
            if method1 == "선택 안 함" or method2 == "선택 안 함" or method1 == method2:
                st.error("오류: 조건에 맞게 서로 중복되지 않는 설명 기법을 선택해야 합니다.")
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
                    
                st.write("### 최종 채점 결과")
                st.write(f"총점 {score_1 + score_2} 점 / 4 점 만점")

    with tab3:
        st.info("""
        [자료] 공익 광고 영상 콘티
        - 장면 1: 일정한 기계음(메트로놈)에 맞추어 자로 잰 듯 완벽하게 움직이는 로봇 선수의 피겨 연기
        - 장면 2: 인간 예술만이 줄 수 있는 진정한 울림과 가치를 강조하기 위한 시각 및 청각 계획
        """)
        
        st.code("""
        📢 조건 1: 기계적 완벽함과 대비되는 인간의 땀방울, 노력, 열정 등의 가치가 시각화될 것
        📢 조건 2: 장면 1의 단조로운 기계음과 대조를 이루며 관객의 마음을 움직이는 소리 요소가 들어갈 것
        """, language="text")
        
        st.markdown("장면 2에 들어갈 구체적인 시각 매체 언어와 이를 통해 감상자에게 전달하고자 하는 의도를 서술하시오.")
        v_idx = st.text_area("v3", label_visibility="collapsed")
        
        st.markdown("장면 2에 들어갈 구체적인 청각 매체 언어와 이를 통해 감상자에게 전달하고자 하는 의도를 서술하시오.")
        a_idx = st.text_area("a3", label_visibility="collapsed")
        
        if st.button("3번 문항 채점하기"):
            v_score = 0
            a_score = 0
            if check_keywords(v_idx, [["인간", "선수", "예술가"], ["땀", "열정", "노력"]]) and not has_misconception(v_idx, ["로봇", "기계"]):
                v_score += 1
                if check_keywords(v_idx, [["감정", "가치", "시각적", "전달"]]): v_score += 1
                
            if check_keywords(a_idx, [["오케스트라", "음악", "풍부"], ["환호", "박수"]]) and not has_misconception(a_idx, ["메트로놈", "기계음"]):
                a_score += 1
                if check_keywords(a_idx, [["울림", "감동", "대조", "부각"]]): a_score += 1
                
            st.write("### 최종 채점 결과")
            st.write(f"총점 {v_score + a_score} 점 / 4 점 만점")
