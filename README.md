# 일본 여행, 몇 월에 가면 좋을까?

도쿄·오사카·삿포로의 기온과 강수량을 비교하는 간단한 Streamlit 과제입니다.

앱: https://japan-trip-lab-miyazaki.streamlit.app/

## 화면 구성
1. 도시를 선택하면 그 도시의 월별 평균기온을 선 그래프로 표시합니다.
2. 여행할 달을 선택하면 세 도시의 월 강수량을 막대그래프로 비교합니다.
3. 선택한 도시의 12개월 데이터 표와 출처를 표시합니다.

## 코드 이해하기
- pd.read_csv: CSV 파일을 읽습니다.
- st.selectbox, st.slider: 도시와 월을 선택합니다.
- data[조건]: 선택한 도시 또는 월의 행만 가져옵니다.
- px.line, px.bar: 선 그래프와 막대그래프를 만듭니다.
- idxmax, idxmin: 가장 따뜻한 달과 강수량이 가장 적은 도시를 찾습니다.
- st.dataframe: 데이터 표를 보여줍니다.

앱 실행에는 app.py, requirements.txt, data/climate.csv가 필요합니다.
.streamlit/config.toml은 화면 색상을 설정합니다.
build_data.py는 CSV 재생성용이며 실행할 필요가 없습니다.
기존 model.py는 이전 버전의 예산 계산용 파일로 현재 앱에서 사용하지 않습니다.

## 실행과 배포
Python 3.13에서 검증했습니다.

```bash
pip install -r requirements.txt
streamlit run app.py
```

Streamlit Community Cloud에서 저장소 miyazakiyuki06/japan-trip-lab, 브랜치 main, 실행 파일 app.py를 사용합니다.

## 데이터 출처
일본 기상청(JMA)의 1991–2020년 평년값:
https://www.data.jma.go.jp/stats/data/en/normal/normal.html

기존 CSV의 6개 도시 중 도쿄·오사카·삿포로의 36행을 사용합니다.
평균기온의 단위는 °C, 월 강수량의 단위는 mm입니다.
평년값은 실제 여행 날짜의 예보가 아니며 강수량은 강수확률이 아닙니다.

AI의 도움을 받아 코드와 화면을 구성했습니다.
