import streamlit as st
import pandas as pd
from googleapiclient.discovery import build
import re

st.set_page_config(page_title="댓글 수집기", page_icon="💬", layout="wide")

st.title("💬 유튜브 댓글 수집기")
st.write("영상에 달린 댓글을 가져와 표 형태로 보여줍니다.")

def get_video_id(url):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    return match.group(1) if match else None

url_input = st.text_input("유튜브 링크를 입력하세요")
max_comments = st.slider("가져올 댓글 수 (최대 100개)", min_value=10, max_value=100, value=30, step=10)

if st.button("댓글 가져오기"):
    if url_input:
        video_id = get_video_id(url_input)
        if video_id:
            with st.spinner("댓글을 수집하는 중입니다..."):
                try:
                    youtube = build('youtube', 'v3', developerKey=st.secrets["YOUTUBE_API_KEY"])
                    
                    # 댓글 스레드 요청
                    request = youtube.commentThreads().list(
                        part="snippet",
                        videoId=video_id,
                        maxResults=max_comments,
                        order="time" # 최신순 정렬
                    )
                    response = request.execute()
                    
                    comments_data = []
                    for item in response.get('items', []):
                        comment_info = item['snippet']['topLevelComment']['snippet']
                        comments_data.append({
                            "작성자": comment_info['authorDisplayName'],
                            "댓글 내용": comment_info['textOriginal'],
                            "좋아요 수": comment_info['likeCount'],
                            "작성일": comment_info['publishedAt'][:10]
                        })
                    
                    if comments_data:
                        df = pd.DataFrame(comments_data)
                        st.success(f"총 {len(df)}개의 댓글을 성공적으로 가져왔습니다!")
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.info("이 영상에는 댓글이 없거나, 댓글이 비활성화되어 있습니다.")
                        
                except Exception as e:
                    st.error(f"오류가 발생했습니다 (댓글 비활성화 영상일 수 있습니다): {e}")
        else:
            st.error("올바른 유튜브 링크가 아닙니다.")
    else:
        st.warning("링크를 입력해 주세요.")
      
