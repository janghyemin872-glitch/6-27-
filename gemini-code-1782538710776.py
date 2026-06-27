import streamlit as st

# 페이지 설정
st.set_page_config(page_title="국어 서논술형 자동 채점 시스템", layout="wide")

# 세션 상태 초기화 (복습 데이터 및 리셋 기능용)
if "results" not in st.session_state:
    st.session_state.results = {}

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

# 처음부터 다시 풀기 버튼 공통 렌더링 함수
def render_reset_button(set_key):
    col1, col2 = st.columns([4, 1])
    with col1:
        st.caption("모든 문제를 제출하면 복습할 내용 탭에서 틀린 개념을 확인할 수 있어요. 답안을 초기화하고 처음부터 다시 풀고 싶다면 다음의 버튼을 누르세요.")
    with col2:
        if st.button("🔄 처음부터 다시 풀기", key=f"reset_{set_key}", use_container_width=True):
            for key in list(st.session_state.keys()):
                if key.startswith(set_key) or key == "results":
                    del st.session_state[key]
            st.rerun()

# -------------------------------------------------------------------------
# 1세트 채점 로직
# -------------------------------------------------------------------------
if set_option == "1세트 (사회적 촉진/억제)":
    st.header("🍏 [실전 적용 - 1] 과제 난이도에 따른 학습 전략")
    
    tab1, tab2, tab3, tab4 = st.tabs(["[서·논술형 1] 표 채우기", "[서·논술형 2] 설명문 작성", "[서·논술형 3] 영상 기획안", "📚 복습할 내용"])
    
    with tab1:
        st.info("""
        [자료] 사회적 촉진과 억제 요약表
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
        ans_a = st.text_input("ans_a", key="set1_ans_a", label_visibility="collapsed")
        
        st.markdown("위 요약표를 바탕으로 빈칸 (ㄴ)에 들어갈 적절한 내용을 내용을 찾아 쓰시오.")
        ans_b = st.text_input("ans_b", key="set1_ans_b", label_visibility="collapsed")
        
        st.markdown("위 요약표를 바탕으로 빈칸 (ㄷ)에 들어갈 적절한 내용을 내용을 찾아 쓰시오.")
        ans_c = st.text_input("ans_c", key="set1_ans_c", label_visibility="collapsed")
        
        if st.button("1번 문항 채점하기", key="btn_set1_1"):
            score = 0
            feedback = []
            wrong_points = []
            
            if check_keywords(ans_a, [["쉬운", "취미", "노력"]]):
                score += 1
            else:
                wrong_points.append(" (ㄱ) 과제의 특성 기술 부족 (쉬운 과제, 적은 노력 등의 조건 누락)")
                
            if check_keywords(ans_b, [["혼자", "차분"], ["집중", "연습"]]):
                score += 1
            else:
                wrong_points.append(" (ㄴ) 학습 환경 및 방법 서술 부족 (혼자, 집중, 연습 등의 핵심어 누락)")
                
            if "억제" in ans_c and "촉진" not in ans_c:
                score += 1
            else:
                wrong_points.append(" (ㄷ) 심리학 용어 오류 ('사회적 억제' 용어 미사용 혹은 혼동)")
                
            st.session_state.results["set1_1"] = {"is_perfect": score == 3, "wrong_points": wrong_points, "user_ans": f"ㄱ: {ans_a} / ㄴ: {ans_b} / ㄷ: {ans_c}"}
            
            st.write("### 최종 채점 결과")
            st.write(f"총점 {score} 점 / 3 점 만점")
            if score == 3: st.success("모든 조건을 충족했습니다!")
            else: st.error("미충족된 조건이 있습니다. 마지막 복습 탭을 확인하세요.")

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
        method1 = st.selectbox("m1", ["선택 안 함", "예시", "대조"], key="set1_m1", label_visibility="collapsed")
        sent1 = st.text_area("s1", key="set1_s1", label_visibility="collapsed")
        
        st.markdown("두 번째 문장에 사용할 설명 방법을 선택하고 해당 내용을 문장으로 이어 쓰시오.")
        method2 = st.selectbox("m2", ["선택 안 함", "예시", "대조"], key="set1_m2", label_visibility="collapsed")
        sent2 = st.text_area("s2", key="set1_s2", label_visibility="collapsed")
        
        if st.button("2번 문항 채점하기", key="btn_set1_2"):
            if method1 == "선택 안 함" or method2 == "선택 안 함" or method1 == method2:
                st.error("오류: 조건에 맞게 서로 다른 두 가지 설명 방법을 선택해야 합니다.")
            else:
                kw_m1 = f"({method1})" in sent1 or f"<{method1}>" in sent1
                kw_m2 = f"({method2})" in sent2 or f"<{method2}>" in sent2
                
                score_1 = 0
                if method1 == "예시" and check_keywords(sent1, [["예를", "예로", "도서관", "커피숍", "모임"]]): score_1 = 2 if kw_m1 else 1
                elif method1 == "대조" and check_keywords(sent1, [["반면", "달리", "반대로", "혼자", "차분"]]): score_1 = 2 if kw_m1 else 1
                
                score_2 = 0
                if method2 == "예시" and check_keywords(sent2, [["예를", "예로", "도서관", "커피숍", "모임"]]): score_2 = 2 if kw_m2 else 1
                elif method2 == "대조" and check_keywords(sent2, [["반면", "달리", "반대로", "혼자", "차분"]]): score_2 = 2 if kw_m2 else 1
                
                total_score = score_1 + score_2
                wrong_points = []
                if total_score < 4:
                    if not (kw_m1 and kw_m2): wrong_points.append(" 문장 끝에 설명 방법 명칭 괄호 표기 누락")
                    if score_1 < 1 or score_2 < 1: wrong_points.append(" 과제 난이도별 환경 내용(도서관/커피숍 혹은 혼자/차분)이나 설명 기법 적용 미흡")
                
                st.session_state.results["set1_2"] = {"is_perfect": total_score == 4, "wrong_points": wrong_points, "user_ans": f"문장1: {sent1} / 문장2: {sent2}"}
                
                st.write("### 최종 채점 결과")
                st.write(f"총점 {total_score} 점 / 4 점 만점")

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
        v_idx = st.text_area("v1", key="set1_v1", label_visibility="collapsed")
        
        st.markdown("장면 2에 들어갈 청각 요소를 기획하고 그렇게 연출했을 때 얻을 수 있는 효과를 설명하시오.")
        a_idx = st.text_area("a1", key="set1_a1", label_visibility="collapsed")
        
        if st.button("3번 문항 채점하기", key="btn_set1_3"):
            v_score = 0
            a_score = 0
            wrong_points = []
            
            if check_keywords(v_idx, [["혼자", "방", "독서실", "책상"]]) and not has_misconception(v_idx, ["도서관", "친구", "모임"]):
                v_score += 1
                if check_keywords(v_idx, [["집중", "자극 차단", "전달"]]): v_score += 1
            else:
                wrong_points.append(" 시각 요소 조건 미충족 (독립된 공간 및 집중 효과 기술 부족)")
                
            if check_keywords(a_idx, [["고요", "적막", "소음 제거", "초침", "연필"]]) and not has_misconception(a_idx, ["배경음악", "경쾌", "음악"]):
                a_score += 1
                if check_keywords(a_idx, [["차분", "분위기", "강조"]]): a_score += 1
            else:
                wrong_points.append(" 청각 요소 조건 미충족 (소음 차단이나 대조 분위기 연출 부족)")
                
            total = v_score + a_score
            st.session_state.results["set1_3"] = {"is_perfect": total == 4, "wrong_points": wrong_points, "user_ans": f"시각: {v_idx} / 청각: {a_idx}"}
            
            st.write("### 최종 채점 결과")
            st.write(f"총점 {total} 점 / 4 점 만점")

    with tab4:
        st.subheader("📝 1세트 오개념 및 조건 미충족 문제 복습")
        has_wrong = False
        
        for q_id, q_name in [("set1_1", "[서·논술형 1] 표 채우기"), ("set1_2", "[서·논술형 2] 설명문 작성"), ("set1_3", "[서·논술형 3] 영상 기획안")]:
            if q_id in st.session_state.results and not st.session_state.results[q_id]["is_perfect"]:
                has_wrong = True
                st.markdown(f"#### ❌ {q_name}")
                st.markdown(f"**💡 핵심 복습 포인트:** 과제의 특성(난이도)에 부합하는 공간 유형과 인지 심리학적 현상(사회적 촉진과 억제)의 인과 관계를 정확히 구별해야 합니다.")
                st.markdown("**⚠️ 내 답안의 부족한 부분:**")
                for wp in st.session_state.results[q_id]["wrong_points"]:
                    st.write(wp)
                st.caption(f"작성했던 답안: {st.session_state.results[q_id]['user_ans']}")
                st.markdown("---")
                
        if not has_wrong:
            st.success("틀린 문제가 없거나 아직 채전을 진행하지 않았습니다. 문제를 풀고 채점하기를 눌러주세요.")
            
        st.markdown("<br>", unsafe_allow_html=True)
        render_reset_button("set1")

# -------------------------------------------------------------------------
# 2세트 채점 로직
# -------------------------------------------------------------------------
elif set_option == "2세트 (정전기의 특징)":
    st.header("⚡ [실전 적용 - 2] 겨울철 불청객 정전기")
    
    tab1, tab2, tab3, tab4 = st.tabs(["[서·논술형 1] 표 채우기", "[서·논술형 2] 설명문 작성", "[서·논술형 3] 영상 기획안", "📚 복습할 내용"])
    
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
        ans_a = st.text_input("ans_2a", key="set2_ans_a", label_visibility="collapsed")
        
        st.markdown("본문의 비유적 설명을 바탕으로 빈칸 (ㄴ)에 들어갈 핵심 단어나 문장을 완성하시오.")
        ans_b = st.text_input("ans_2b", key="set2_ans_b", label_visibility="collapsed")
        
        st.markdown("본문의 비유적 설명을 바탕으로 빈칸 (ㄷ)에 들어갈 핵심 단어나 문장을 완성하시오.")
        ans_c = st.text_input("ans_2c", key="set2_ans_c", label_visibility="collapsed")
        
        if st.button("1번 문항 채점하기", key="btn_set2_1"):
            score = 0
            wrong_points = []
            if check_keywords(ans_a, [["고여", "멈춘"]]): score += 1
            else: wrong_points.append(" (ㄱ) 비유적 표현 불일치 (고여 있는 물의 성질 표현 누락)")
                
            if check_keywords(ans_b, [["이동하지", "머물", "정지"]]): score += 1
            else: wrong_points.append(" (ㄴ) 과학적 현상 기술 오류 (전하의 정지 및 머무름 현상 누락)")
                
            if check_keywords(ans_c, [["위험하지", "안전", "피해X", "무해"]]): score += 1
            else: wrong_points.append(" (ㄷ) 정전기의 인체 영향 오류 (전류가 미미하여 위험성이 없다는 사실 누락)")
                
            st.session_state.results["set2_1"] = {"is_perfect": score == 3, "wrong_points": wrong_points, "user_ans": f"ㄱ: {ans_a} / ㄴ: {ans_b} / ㄷ: {ans_c}"}
            
            st.write("### 최종 채점 결과")
            st.write(f"총점 {score} 점 / 3 점 만점")

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
        method1 = st.selectbox("m2_1", ["선택 안 함", "정의", "비교와 대조"], key="set2_m1", label_visibility="collapsed")
        sent1 = st.text_area("s2_1", key="set2_s1", label_visibility="collapsed")
        
        st.markdown("두 번째 문장에 사용할 설명 방법을 선택하고 정전기의 개념 혹은 비유적 특성을 이어 쓰시오.")
        method2 = st.selectbox("m2_2", ["선택 안 함", "정의", "비교와 대조"], key="set2_m2", label_visibility="collapsed")
        sent2 = st.text_area("s2_2", key="set2_s2", label_visibility="collapsed")
        
        if st.button("2번 문항 채점하기", key="btn_set2_2"):
            if method1 == "선택 안 함" or method2 == "선택 안 함" or method1 == method2:
                st.error("오류: 조건에 맞게 서로 다른 설명 방법을 매칭해야 합니다.")
            else:
                is_comp1 = "비교" in method1 or "대조" in method1
                is_comp2 = "비교" in method2 or "대조" in method2
                
                kw_m1 = "비교" in sent1 or "대조" in sent1 if is_comp1 else f"({method1})" in sent1
                kw_m2 = "비교" in sent2 or "대조" in sent2 if is_comp2 else f"({method2})" in sent2
                
                score_1 = 0
                if method1 == "정의" and check_keywords(sent1, [["전기", "뜻", "의미", "말한다"]]) and not has_misconception(sent1, ["흐르는 물"]): score_1 = 2 if kw_m1 else 1
                elif is_comp1:
                    if check_keywords(sent1, [["물", "고여", "흐르는"]]) and not has_misconception(sent1, ["시간적으로 변화하지"]): score_1 = 2 if kw_m1 else 1
                        
                score_2 = 0
                if method2 == "정의" and check_keywords(sent2, [["전기", "뜻", "의미", "말한다"]]) and not has_misconception(sent2, ["흐르는 물"]): score_2 = 2 if kw_m2 else 1
                elif is_comp2:
                    if check_keywords(sent2, [["물", "고여", "흐르는"]]) and not has_misconception(sent2, ["시간적으로 변화하지"]): score_2 = 2 if kw_m2 else 1
                        
                total = score_1 + score_2
                wrong_points = []
                if total < 4:
                    wrong_points.append(" 정의문 구성 지침 미달 또는 고여 있는 물 vs 흐르는 물의 대조 메커니즘 표현 미흡")
                
                st.session_state.results["set2_2"] = {"is_perfect": total == 4, "wrong_points": wrong_points, "user_ans": f"문장1: {sent1} / 문장2: {sent2}"}
                st.write("### 최종 채점 결과")
                st.write(f"총점 {total} 점 / 4 점 만점")

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
        v_idx = st.text_area("v2", key="set2_v1", label_visibility="collapsed")
        
        st.markdown("장면 2의 구체적인 청각 연출 계획과 그 연출을 통해 달성하려는 시청자 전달 효과를 서술하시오.")
        a_idx = st.text_area("a2", key="set2_a1", label_visibility="collapsed")
        
        if st.button("3번 문항 채점하기", key="btn_set2_3"):
            v_score = 0
            a_score = 0
            wrong_points = []
            
            if check_keywords(v_idx, [["높은", "절벽", "산"], ["고여", "댐", "저수지"]]) and not has_misconception(v_idx, ["폭포", "쏟아"]):
                v_score += 1
                if check_keywords(v_idx, [["전압", "이동하지", "시각화", "이해"]]): v_score += 1
            else:
                wrong_points.append(" 시각 요소 조건 미치달 (고여 있는 상태를 형상화하는 연출 계획 누락)")
                
            if check_keywords(a_idx, [["고요", "적막", "소리 없는"]]) and not has_misconception(a_idx, ["웅장", "물소리", "스파크"]):
                a_score += 1
                if check_keywords(a_idx, [["위험하지", "피해가 없는", "안도감", "대조"]]): a_score += 1
            else:
                wrong_points.append(" 청각 요소 조건 미치달 (무해함을 연상시키는 평온한 청각 디자인 부족)")
                
            total = v_score + a_score
            st.session_state.results["set2_3"] = {"is_perfect": total == 4, "wrong_points": wrong_points, "user_ans": f"시각: {v_idx} / 청각: {a_idx}"}
            st.write("### 최종 채점 결과")
            st.write(f"총점 {total} 점 / 4 점 만점")

    with tab4:
        st.subheader("📝 2세트 오개념 및 조건 미충족 문제 복습")
        has_wrong = False
        
        for q_id, q_name in [("set2_1", "[서·논술형 1] 표 채우기"), ("set2_2", "[서·논술형 2] 설명문 작성"), ("set2_3", "[서·논술형 3] 영상 기획안")]:
            if q_id in st.session_state.results and not st.session_state.results[q_id]["is_perfect"]:
                has_wrong = True
                st.markdown(f"#### ❌ {q_name}")
                st.markdown(f"**💡 핵심 복습 포인트:** 정전기는 일반 전류와 달리 전하가 머물러 있는 성질을 가지며 비유적으로 흐르지 않는 '고인 물'과 같다는 과학적 기본 개념을 융합해야 합니다.")
                st.markdown("**⚠️ 내 답안의 부족한 부분:**")
                for wp in st.session_state.results[q_id]["wrong_points"]:
                    st.write(wp)
                st.caption(f"작성했던 답안: {st.session_state.results[q_id]['user_ans']}")
                st.markdown("---")
                
        if not has_wrong:
            st.success("틀린 문제가 없거나 아직 채전을 진행하지 않았습니다. 문제를 풀고 채점하기를 눌러주세요.")
            
        st.markdown("<br>", unsafe_allow_html=True)
        render_reset_button("set2")

# -------------------------------------------------------------------------
# 3세트 채점 로직
# -------------------------------------------------------------------------
elif set_option == "3세트 (인간 vs AI 예술)":
    st.header("🎨 [실전 적용 - 3] 인공 지능이 그린 그림의 예술성")
    
    tab1, tab2, tab3, tab4 = st.tabs(["[서·논술형 1] 표 채우기", "[서·논술형 2] 설명문 작성", "[서·논술형 3] 영상 기획안", "📚 복습할 내용"])
    
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
        ans_a = st.text_input("ans_3a", key="set3_ans_a", label_visibility="collapsed")
        
        st.markdown("지문의 핵심 대조 항목을 고려하여 빈칸 (ㄴ)에 들어갈 알맞은 내용을 근거와 함께 채우시오.")
        ans_b = st.text_input("ans_3b", key="set3_ans_b", label_visibility="collapsed")
        
        st.markdown("지문의 핵심 대조 항목을 고려하여 빈칸 (ㄷ)에 들어갈 알맞은 가치 유형을 기술하여 채우시오.")
        ans_c = st.text_input("ans_3c", key="set3_ans_c", label_visibility="collapsed")
        
        if st.button("1번 문항 채점하기", key="btn_set3_1"):
            score = 0
            wrong_points = []
            if check_keywords(ans_a, [["로봇", "인공지능"], ["피겨", "스케이팅", "완벽"]]): score += 1
            else: wrong_points.append(" (ㄱ) 대조 비유군 설정 미흡 (기계적 매끄러움을 상징하는 로봇 연기 등 핵심 요소 누락)")
                
            if check_keywords(ans_b, [["감정", "철학", "이야기"], ["어렵다", "아니다", "부정"]]): score += 1
            else: wrong_points.append(" (ㄴ) 한계점 도출 미흡 (주체적인 감정이나 예술적 주관성이 없다는 한계 서술 누락)")
                
            if check_keywords(ans_c, [["변화", "확장", "상징"]]): score += 1
            else: wrong_points.append(" (ㄷ) 사회적 의의 분류 미진 (기존 미술계의 지평을 흔드는 상징적 가치 명시 누락)")
                
            st.session_state.results["set3_1"] = {"is_perfect": score == 3, "wrong_points": wrong_points, "user_ans": f"ㄱ: {ans_a} / ㄴ: {ans_b} / ㄷ: {ans_c}"}
            st.write("### 최종 채점 결과")
            st.write(f"총점 {score} 점 / 3 점 만점")

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
        method1 = st.selectbox("m3_1", ["선택 안 함", "분석", "대조"], key="set3_m1", label_visibility="collapsed")
        sent1 = st.text_area("s3_1", key="set3_s1", label_visibility="collapsed")
        
        st.markdown("두 번째 문장에 사용할 설명 방법을 선택하고 해당 기법에 맞춰 인간과 인공지능 작품의 차이를 서술해 이어 쓰시오.")
        method2 = st.selectbox("m3_2", ["선택 안 함", "분석", "대조"], key="set3_m2", label_visibility="collapsed")
        sent2 = st.text_area("s3_2", key="set3_s2", label_visibility="collapsed")
        
        if st.button("2번 문항 채점하기", key="btn_set3_2"):
            if method1 == "선택 안 함" or method2 == "선택 안 함" or method1 == method2:
                st.error("오류: 조건에 맞게 서로 중복되지 않는 설명 기법을 선택해야 합니다.")
            else:
                kw_m1 = f"({method1})" in sent1
                kw_m2 = f"({method2})" in sent2
                
                score_1 = 0
                if method1 == "분석" and check_keywords(sent1, [["감정", "철학", "경험", "관점", "요소"]]): score_1 = 2 if kw_m1 else 1
                elif method1 == "대조" and check_keywords(sent1, [["반면", "인공지능", "차이", "없다"]]): score_1 = 2 if kw_m1 else 1
                    
                score_2 = 0
                if method2 == "분석" and check_keywords(sent2, [["감정", "철학", "경험", "관점", "요소"]]): score_2 = 2 if kw_m2 else 1
                elif method2 == "대조" and check_keywords(sent2, [["반면", "인공지능", "차이", "없다"]]): score_2 = 2 if kw_m2 else 1
                    
                total = score_1 + score_2
                wrong_points = []
                if total < 4:
                    wrong_points.append(" 설명문 기법(분석 또는 대조) 서술 규칙 불이행 및 키워드 누락")
                
                st.session_state.results["set3_2"] = {"is_perfect": total == 4, "wrong_points": wrong_points, "user_ans": f"문장1: {sent1} / 문장2: {sent2}"}
                st.write("### 최종 채점 결과")
                st.write(f"총점 {total} 점 / 4 점 만점")

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
        v_idx = st.text_area("v3", key="set3_v1", label_visibility="collapsed")
        
        st.markdown("장면 2에 들어갈 구체적인 청각 매체 언어와 이를 통해 감상자에게 전달하고자 하는 의도를 서술하시오.")
        a_idx = st.text_area("a3", key="set3_a1", label_visibility="collapsed")
        
        if st.button("3번 문항 채점하기", key="btn_set3_3"):
            v_score = 0
            a_score = 0
            wrong_points = []
            if check_keywords(v_idx, [["인간", "선수", "예술가"], ["땀", "열정", "노력"]]) and not has_misconception(v_idx, ["로봇", "기계"]):
                v_score += 1
                if check_keywords(v_idx, [["감정", "가치", "시각적", "전달"]]): v_score += 1
            else:
                wrong_points.append(" 시각 연출 내 인간성 가치(땀방울, 노력 등) 대비 효과 미흡")
                
            if check_keywords(a_idx, [["오케스트라", "음악", "풍부"], ["환호", "박수"]]) and not has_misconception(a_idx, ["메트로놈", "기계음"]):
                a_score += 1
                if check_keywords(a_idx, [["울림", "감동", "대조", "부각"]]): a_score += 1
            else:
                wrong_points.append(" 청각 기획 내 오디토리움 대비(기계음과 대비되는 감동적인 음악 등) 미충족")
                
            total = v_score + a_score
            st.session_state.results["set3_3"] = {"is_perfect": total == 4, "wrong_points": wrong_points, "user_ans": f"시각: {v_idx} / 청각: {a_idx}"}
            st.write("### 최종 채점 결과")
            st.write(f"총점 {total} 점 / 4 점 만점")

    with tab4:
        st.subheader("📝 3세트 오개념 및 조건 미충족 문제 복습")
        has_wrong = False
        
        for q_id, q_name in [("set3_1", "[서·논술형 1] 표 채우기"), ("set3_2", "[서·논술형 2] 설명문 작성"), ("set3_3", "[서·논술형 3] 영상 기획안")]:
            if q_id in st.session_state.results and not st.session_state.results[q_id]["is_perfect"]:
                has_wrong = True
                st.markdown(f"#### ❌ {q_name}")
                st.markdown(f"**💡 핵심 복습 포인트:** 인공지능 예술은 고도의 기술적 무결성을 지니지만 인간 고유의 역사성, 감정, 예술적 고뇌가 결여되어 있다는 한계점과 상징적 교차점을 동시에 고찰해야 합니다.")
                st.markdown("**⚠️ 내 답안의 부족한 부분:**")
                for wp in st.session_state.results[q_id]["wrong_points"]:
                    st.write(wp)
                st.caption(f"작성했던 답안: {st.session_state.results[q_id]['user_ans']}")
                st.markdown("---")
                
        if not has_wrong:
            st.success("틀린 문제가 없거나 아직 채전을 진행하지 않았습니다. 문제를 풀고 채점하기를 눌러주세요.")
            
        st.markdown("<br>", unsafe_allow_html=True)
        render_reset_button("set3")
