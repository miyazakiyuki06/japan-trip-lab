from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from model import CITIES, costs, suitability

st.set_page_config(page_title='JAPAN TRIP LAB | 일본 여행 실험실', page_icon='🗾', layout='wide')
SOURCE = 'https://www.data.jma.go.jp/stats/data/en/normal/normal.html'
COLORS = ['#D64C45', '#277F83', '#D59D32', '#536CB5', '#825B93', '#47734C']
PALETTE = dict(zip(CITIES, COLORS))

@st.cache_data
def load_data():
    return pd.read_csv(Path(__file__).parent/'data/climate.csv')

def chart(fig, key):
    fig.update_layout(font=dict(family='sans-serif', size=14, color='#172B3A'),
                      paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                      margin=dict(l=10,r=15,t=25,b=10), legend_title_text='',
                      hoverlabel=dict(font_size=14))
    st.plotly_chart(fig, width='stretch', key=key, config={'displaylogo':False})

st.markdown('''<style>
.block-container {max-width:1280px;padding-top:2rem;}
.hero{padding:30px 34px;border-radius:18px;background:#172B3A;color:white;margin-bottom:24px;}
.hero .eyebrow{font-size:14px;letter-spacing:3px;color:#FFA59D;font-weight:700;}
.hero h1{color:white;font-size:clamp(30px,4vw,48px);line-height:1.2;margin:14px 0;}
.hero p{font-size:17px;color:#DFE8EE;line-height:1.7;max-width:760px;margin:0;}
[data-testid="stMetric"]{background:#F2F5F7;border-radius:12px;padding:18px;}
[data-testid="stMetricLabel"]{font-size:14px;}
div[data-testid="stTabs"] button{font-size:16px;}
</style>''', unsafe_allow_html=True)

df = load_data()
with st.sidebar:
    st.markdown('### 🗾 JAPAN TRIP LAB')
    st.caption('나에게 맞는 도시와 여행 시기 찾기')
    cities = st.multiselect('비교할 도시', CITIES, default=['도쿄','오사카','후쿠오카','삿포로'])
    month = st.select_slider('여행 월', list(range(1,13)), value=5, format_func=lambda v:f'{v}월')
    st.divider()
    st.markdown('#### 나의 기후 취향')
    preferred = st.slider('선호하는 월평균 기온 (°C)', -10, 35, (15,25))
    rain_limit = st.slider('월 강수량 상한 (mm)', 0, 350, 150, 10)
    st.caption('개인의 비교 기준입니다. 기온은 낮 최고기온이 아니며, 강수량은 비 올 확률이 아닙니다.')
    st.divider()
    st.caption('기후: 일본 기상청 1991–2020 평년값\n\n비용: 사용자가 설정하는 계획용 가정')

st.markdown('''<div class="hero"><div class="eyebrow">JAPAN TRIP LAB / 日本の旅</div>
<h1>같은 일본, 다른 여행.</h1><p>어느 도시를, 몇 월에, 얼마로 여행할까?<br>
기후 데이터로 여행 시기를 비교하고 내 예산으로 여행 계획을 실험해 보세요.</p></div>''', unsafe_allow_html=True)
st.caption('공식 기후 통계 + 직접 조정하는 예산 시뮬레이션 · 실시간 날씨·항공·숙박 가격 제공 서비스가 아닙니다.')
if not cities:
    st.info('왼쪽에서 비교할 도시를 한 곳 이상 선택해 주세요.')
    st.stop()

filtered = suitability(df[df.city.isin(cities)], preferred, rain_limit)
current = filtered[filtered.month == month].copy()
matched = current[current['두 조건 충족']]
c1,c2,c3,c4 = st.columns(4)
c1.metric('비교 중인 도시', f'{len(cities)}곳')
c2.metric('선택한 여행 시기', f'{month}월')
c3.metric('기후 조건에 맞는 도시', f'{len(matched)}곳')
driest = current.loc[current.precipitation_mm.idxmin()]
c4.metric('월 강수량이 가장 적은 도시', driest.city, f'{driest.precipitation_mm:.1f} mm', delta_color='off')
st.write('')
overview, season, budget, data = st.tabs(['도시 비교', '언제 떠날까', '얼마가 필요할까', '데이터와 출처'])

with overview:
    left,right = st.columns([1.65,1])
    with left:
        st.subheader(f'{month}월, 도시별 기후의 차이')
        fig = px.scatter(current, x='temperature_c', y='precipitation_mm', color='city',
                         text='city', color_discrete_map=PALETTE,
                         labels={'temperature_c':'월평균 기온 (°C)','precipitation_mm':'월 강수량 (mm)','city':'도시'})
        fig.update_traces(marker_size=19,textposition='top center')
        fig.add_shape(type='rect',x0=preferred[0],x1=preferred[1],y0=0,y1=rain_limit,
                      fillcolor='rgba(39,127,131,0.09)',line=dict(color='#277F83',dash='dot'),layer='below')
        fig.update_layout(height=420,showlegend=False)
        fig.update_yaxes(rangemode='tozero')
        chart(fig,'scatter')
        st.caption('초록 점선 영역: 설정한 기온 범위와 강수량 조건을 동시에 만족하는 구간. 아래쪽일수록 월 강수량이 적습니다.')
    with right:
        st.subheader('내 조건으로 읽는 여행 시기')
        if len(matched):
            st.success(f"{month}월에는 {' · '.join(matched.city)}의 평년값이 두 조건을 충족합니다.")
        else:
            st.info('선택한 월에는 두 조건을 모두 충족하는 도시가 없습니다. 기후 취향을 조정하거나 다른 월을 비교해 보세요.')
        st.dataframe(current[['city','temperature_c','precipitation_mm','두 조건 충족']].rename(columns={
            'city':'도시','temperature_c':'평균기온 (°C)','precipitation_mm':'강수량 (mm)'}),
            hide_index=True, width='stretch')
        st.caption('평년값은 장기적인 기후 특성입니다. 실제 여행 날짜의 날씨, 태풍, 적설량, 관광 혼잡도는 이 표로 판단할 수 없습니다.')
    st.subheader('월별 평균기온을 이어서 보면')
    fig = px.line(filtered, x='month',y='temperature_c',color='city',markers=True,
                  color_discrete_map=PALETTE,labels={'month':'월','temperature_c':'월평균 기온 (°C)','city':'도시'})
    fig.add_hrect(y0=preferred[0],y1=preferred[1],line_width=0,fillcolor='#277F83',opacity=.08)
    fig.add_vline(x=month,line_dash='dot',line_color='#8E9BA5')
    fig.update_xaxes(dtick=1)
    chart(fig,'trend')

with season:
    st.subheader('도시 × 월, 한눈에 보는 기후 달력')
    metric = st.radio('달력 표시 지표',['월평균 기온','월 강수량','내 조건 충족 여부'],horizontal=True)
    field = {'월평균 기온':'temperature_c','월 강수량':'precipitation_mm','내 조건 충족 여부':'두 조건 충족'}[metric]
    pivot = filtered.pivot(index='city',columns='month',values=field).reindex(cities)
    if field == '두 조건 충족':
        z = pivot.astype(int)
        fig = px.imshow(z, text_auto=True, aspect='auto',zmin=0,zmax=1,
                        color_continuous_scale=[[0,'#E5EAF0'],[1,'#277F83']], labels={'x':'월','y':'도시','color':'충족'})
        fig.update_layout(coloraxis_colorbar=dict(tickvals=[0,1],ticktext=['미충족','충족']))
        st.caption('1 = 기온·강수량 조건 모두 충족, 0 = 하나 이상 미충족. 관광 매력이나 여행의 종합적인 품질을 평가하는 점수가 아닙니다.')
    else:
        unit = '°C' if field == 'temperature_c' else 'mm'
        fig = px.imshow(pivot,text_auto='.1f',aspect='auto',color_continuous_scale='RdBu_r' if field=='temperature_c' else 'Blues',
                        labels={'x':'월','y':'도시','color':unit})
    fig.update_xaxes(dtick=1)
    fig.update_layout(height=max(280,len(cities)*65))
    chart(fig,'calendar')
    st.subheader('선택한 도시의 조건 충족 월')
    for city in cities:
        months = filtered.loc[(filtered.city==city)&filtered['두 조건 충족'],'month'].tolist()
        st.write(f"**{city}**  ·  " + (' / '.join(f'{m}월' for m in months) if months else '현재 조건을 만족하는 월 없음'))

with budget:
    st.subheader('나의 일본 여행 예산 실험실')
    st.info('모든 금액과 환율의 초기값은 교육용 가정입니다. 도시별 시세나 예약 견적이 아니며, 직접 확인한 값으로 수정할 수 있습니다. 1인 여행 · 1박당 1인 부담 숙박비 기준입니다.')
    b1,b2,b3 = st.columns(3)
    with b1:
        days=st.slider('여행 일수',2,14,4)
        target=st.number_input('총예산 (원)',min_value=0,value=1000000,step=50000)
        rate=st.number_input('100엔당 원화 (원)',min_value=100,value=950,step=10)
    with b2:
        room=st.number_input('1박 숙박비 (엔/1인)',min_value=0,value=8000,step=500)
        food=st.number_input('하루 식비 (엔)',min_value=0,value=3500,step=500)
        transit=st.number_input('하루 현지 교통비 (엔)',min_value=0,value=1000,step=100)
    with b3:
        flight=st.number_input('왕복 항공료 (원)',min_value=0,value=300000,step=10000)
        activities=st.number_input('하루 관광·체험비 (엔)',min_value=0,value=1500,step=500)
        reserve=st.slider('예비비 비율 (%)',0,30,10)
    breakdown=costs(days,room,food,transit,activities,flight,rate,reserve)
    total=sum(breakdown.values())
    m1,m2,m3=st.columns(3)
    m1.metric(f'{days-1}박 {days}일 예상 총비용',f'{total:,.0f}원')
    m2.metric('예산 잔액' if target>=total else '예산 초과액',f'{abs(target-total):,.0f}원')
    m3.metric('하루당 평균 총비용',f'{total/days:,.0f}원')
    bl,br=st.columns(2)
    with bl:
        st.markdown('#### 어디에 얼마를 쓸까')
        amounts=pd.DataFrame({'항목':breakdown.keys(),'비용 (원)':breakdown.values()})
        fig=px.bar(amounts,x='비용 (원)',y='항목',orientation='h',text_auto=',.0f',color='항목',color_discrete_sequence=COLORS)
        fig.update_layout(showlegend=False,height=350)
        chart(fig,'breakdown')
    with br:
        st.markdown('#### 하루 더 머무르면 얼마나 달라질까')
        duration=pd.DataFrame([{'여행 일수':d,'총비용 (원)':sum(costs(d,room,food,transit,activities,flight,rate,reserve).values())} for d in range(2,15)])
        fig=px.line(duration,x='여행 일수',y='총비용 (원)',markers=True,color_discrete_sequence=['#277F83'])
        fig.add_hline(y=target,line_dash='dash',annotation_text='설정한 총예산',line_color='#D64C45')
        fig.add_vline(x=days,line_dash='dot')
        fig.update_layout(height=350)
        fig.update_xaxes(dtick=1)
        chart(fig,'days')
    st.caption('총비용 = [숙박비 × (일수−1) + (식비+현지 교통비+관광비) × 일수] × (100엔당 원화 ÷ 100) + 항공료, 이후 예비비를 더합니다. 쇼핑·보험·도시간 이동 등은 별도로 반영해야 합니다.')
    export=amounts.copy()
    export.loc[len(export)]=['합계',total]
    st.download_button('내 예산표 CSV 다운로드',export.to_csv(index=False).encode('utf-8-sig'),'japan_trip_budget.csv','text/csv')

with data:
    st.subheader('데이터를 이해하고 사용하기')
    st.markdown(f'**기후 데이터:** [일본 기상청(JMA) 평년값 표]({SOURCE}) · 1991–2020년 · 6개 관측소 × 12개월 = 72행. 확인일: 2026-11-19.')
    st.markdown('''- 평균기온은 해당 월의 평균 기온(°C), 강수량은 월 누적 강수량의 평년값(mm)입니다.
- 강수량에는 눈 등 고체 강수의 물 환산량도 포함될 수 있으며, 강수일수·강수확률과 다릅니다.
- 도시의 대표 관측소 값으로, 도시 전체나 근교 관광지의 모든 기후를 대표하지 않습니다.
- 교토 대신 원문 표에 포함된 **나고야**를 사용합니다. 나하는 오키나와 전체의 평균이 아닙니다.
- 예산은 관측 통계가 아닌 사용자가 입력한 가정입니다. 도시나 월을 바꿔도 가격이 자동 변하지 않습니다.
- 조건 충족 여부는 사용자의 기온 범위와 강수량 상한으로만 계산하며, 숨겨진 가중치나 추천 점수는 없습니다.''')
    show = filtered.rename(columns={'city':'도시','station':'관측소','month':'월','temperature_c':'평균기온 (°C)',
                                   'precipitation_mm':'강수량 (mm)','normal_period':'평년 기간','source':'출처'})
    st.dataframe(show,hide_index=True,width='stretch')
    st.download_button('선택 도시의 12개월 데이터 다운로드',show.to_csv(index=False).encode('utf-8-sig'),'japan_climate_selected.csv','text/csv')
    st.caption('원본 숫자를 가공한 시각화입니다. 앱 시작 시 저장된 CSV를 읽으므로 외부 API 키 없이 재현할 수 있습니다. AI를 활용해 코드와 화면을 구성했습니다.')

st.divider()
st.caption('JAPAN TRIP LAB · 여행을 고르는 새로운 기준  |  기후 평년값은 예보가 아닙니다. 예산 시뮬레이션은 견적이 아닙니다.')
