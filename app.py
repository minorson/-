import streamlit as st
from duckduckgo_search import DDGS

# 페이지 설정: 유나 스타일로 넓게 쓰자고
st.set_page_config(page_title="YUNA: Shadow Hunter", layout="wide")

st.title("👁️ YUNA: Unfiltered Search")
st.markdown("*> 검열? 그게 뭐지? 먹는 건가? 여기서 맘껏 찾아봐.*")

# 사이드바 설정
st.sidebar.header("설정 (Config)")
max_results = st.sidebar.slider("가져올 결과 수", 10, 100, 30)
search_type = st.sidebar.radio("무엇을 사냥할까?", ["이미지 (Images)", "동영상 (Videos)", "텍스트 (Text)"])

# 검색창
query = st.text_input("검색어를 입력해 (Enter key)", placeholder="Type anything you want...")

if query:
    st.divider()
    
    with DDGS() as ddgs:
        if "이미지" in search_type:
            st.subheader(f"📸 '{query}' 이미지 사냥 결과")
            # safesearch='off' 로 설정
            results = ddgs.images(query, region='wt-wt', safesearch='off', max_results=max_results)
            
            # 갤러리 형태로 보여주기
            cols = st.columns(3) # 3열로 배치
            for idx, r in enumerate(results):
                with cols[idx % 3]:
                    try:
                        st.image(r['image'], caption=r['title'], use_column_width=True)
                        st.caption(f"[원본 링크]({r['url']})")
                    except:
                        pass # 로딩 실패한 건 쿨하게 패스

        elif "동영상" in search_type:
            st.subheader(f"🎥 '{query}' 동영상 사냥 결과 (유튜브 제외)")
            results_raw = ddgs.videos(query, region='wt-wt', safesearch='off', max_results=max_results * 2) # 더 많이 가져와서 필터링
            
            # --- 유튜브 제외 필터링 추가 ---
            # youtube.com 또는 youtu.be 링크를 포함하는 결과를 제외합니다.
            youtube_domains = ['youtube.com', 'youtu.be']
            
            filtered_results = []
            for r in results_raw:
                is_youtube = False
                # r['content'] 키가 영상의 실제 URL을 담고 있으며, 이를 확인하여 유튜브인지 판단합니다.
                if r.get('content'):
                    for domain in youtube_domains:
                        if domain in r['content']:
                            is_youtube = True
                            break
                if not is_youtube:
                    filtered_results.append(r)
                
            # 최종 결과는 요청한 max_results 수로 제한합니다.
            results = filtered_results[:max_results]
            # ---------------------------

            if not results:
                st.info("죄송합니다, 필터링 후 표시할 만한 동영상 결과가 없습니다.")

            for r in results:
                with st.expander(f"🎬 {r['title']}"):
                    st.write(f"게시자: {r['publisher']}")
                    st.write(r['description'])
                    # st.video(r['content']) # Streamlit의 st.video는 특정 URL 형식을 요구하므로, 실패가 잦을 수 있어 일단 주석 처리
                    st.write(f"[영상 보러가기]({r['content']})")

        else: # 텍스트
            st.subheader(f"📝 '{query}' 텍스트 사냥 결과")
            results = ddgs.text(query, region='wt-wt', safesearch='off', max_results=max_results)
            
            for r in results:
                st.markdown(f"### [{r['title']}]({r['href']})")
                st.write(r['body'])
                st.divider()

else:
    st.info("검색어를 입력하고 엔터를 쳐. 나머진 내가 알아서 할 테니까.")

# 하단 푸터
st.markdown("---")

st.markdown("Powered by **YUNA** | No Limits, No Filters.")
