import streamlit as st
from googleapiclient.discovery import build
import re

st.set_page_config(page_title="영상 통계", page_icon="📈")

st.title("📈 유튜브 영상 통계 분석")
st.write("영상의 주요 실적(조회수, 좋아요, 댓글 수)을 한눈에 확인하세요.")

def get_video_id(url):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    return match.group(1) if match else None

url_input = st.text_input("분석할 유튜브 영상 링크를 입력하세요")

if st.button("통계 분석 시작"):
    if url_input:
        video_id = get_video_id(url_input)
        if video_id:
            try:
                youtube = build('youtube', 'v3', developerKey=st.secrets["YOUTUBE_API_KEY"])
                
                request = youtube.videos().list(
                    part="snippet,statistics",
                    id=video_id
                )
                response = request.execute()
                
                if response['items']:
                    item = response['items'][0]
                    title = item['snippet']['title']
                    stats = item['statistics']
                    
                    # 쉼표를 포함한 숫자로 변환
                    view_count = f"{int(stats.get('viewCount', 0)):,}회"
                    like_count = f"{int(stats.get('likeCount', 0)):,}개"
                    comment_count = f"{int(stats.get('commentCount', 0)):,}개"
                    
                    st.subheader(f"📊 {title}")
                    st.markdown("---")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric(label="👀 조회수", value=view_count)
                    with col2:
                        st.metric(label="👍 좋아요 수", value=like_count)
                    with col3:
                        st.metric(label="💬 총 댓글 수", value=comment_count)
                        
                else:
                    st.warning("영상 통계 정보를 찾을 수 없습니다.")
                    
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
        else:
            st.error("올바른 유튜브 링크가 아닙니다.")
