import streamlit as st
from duckduckgo_search import DDGS

# ... (페이지 설정 및 사이드바 설정 코드는 동일)

# 검색창
query = st.text_input("검색어를 입력해 (Enter key)", placeholder="Type anything you want...")

# 🚀 [수정된 부분 시작]
if query:
    st.divider()
    
    # 1. YouTube 제외 필터 추가
    # 동영상 검색 시에만 제외 필터를 추가합니다.
    if "동영상" in search_type:
        search_query = f"{query} -site:youtube.com"
    else:
        search_query = query
    
    st.caption(f"실제 검색 쿼리: **`{search_query}`**")
    
    with DDGS() as ddgs:
        if "이미지" in search_type:
            st.subheader(f"📸 '{query}' 이미지 사냥 결과")
            # ... (이미지 검색 코드는 동일, search_query 사용)
            results = ddgs.images(search_query, region='wt-wt', safesearch='off', max_results=max_results)
            
            # ... (이미지 표시 코드는 동일)

        elif "동영상" in search_type:
            st.subheader(f"🎥 '{query}' 동영상 사냥 결과 (YouTube 제외)")
            # 2. 동영상 검색에 수정된 쿼리 사용
            results = ddgs.videos(search_query, region='wt-wt', safesearch='off', max_results=max_results)
            
            for r in results:
                with st.expander(f"🎬 {r['title']}"):
                    st.write(f"게시자: {r['publisher']}")
                    st.write(r['description'])
                    # st.video(r['content']) # 원본 코드는 URL이 아닌 content 링크를 사용하는데, 대부분의 경우 DuckDuckGo videos API는 embed link를 제공하므로 작동할 수 있지만, 안정성을 위해 원본 링크를 쓰는 것도 고려해보세요.
                    st.write(f"[영상 보러가기]({r['content']})")

        else: # 텍스트
            st.subheader(f"📝 '{query}' 텍스트 사냥 결과")
            # 3. 텍스트 검색에 수정된 쿼리 사용 (텍스트 검색에서도 YouTube 제외가 필요하다면)
            results = ddgs.text(search_query, region='wt-wt', safesearch='off', max_results=max_results)
            
            # ... (텍스트 표시 코드는 동일)
# 🚀 [수정된 부분 끝]
else:
    st.info("검색어를 입력하고 엔터를 쳐. 나머진 내가 알아서 할 테니까.")

# 하단 푸터
st.markdown("---")

st.markdown("Powered by **YUNA** | No Limits, No Filters.")
