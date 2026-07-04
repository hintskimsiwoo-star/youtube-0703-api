import streamlit as st

st.set_page_config(page_title="유튜브 데이터 추출기", page_icon="▶️", layout="centered")

st.title("▶️ 유튜브 데이터 자동 추출기")
st.subheader("YouTube Data API v3 활용 대시보드")

st.markdown("---")
st.markdown("""
### 👋 환영합니다!
이 앱은 유튜브 링크(URL)만 입력하면 원하는 데이터를 자동으로 수집해주는 툴입니다.
왼쪽 메뉴에서 원하는 기능을 선택해 보세요.

* **🖼️ 썸네일 추출기**: 영상의 썸네일 이미지와 기본 정보를 확인합니다.
* **💬 댓글 수집기**: 영상에 달린 최신 댓글들을 모아서 표(데이터프레임) 형태로 보여줍니다.
* **📈 영상 통계**: 조회수, 좋아요 수 등 수치화된 데이터를 분석합니다.

---
**💡 사용 전 필수 확인 (API Key 설정)**
이 앱이 정상 작동하려면 Streamlit 클라우드 설정(Settings) -> **Secrets** 메뉴에 아래와 같이 API 키가 입력되어 있어야 합니다.
```toml
YOUTUBE_API_KEY = "여기에_발급받은_API_키_입력"
