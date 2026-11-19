from pathlib import Path
import pandas as pd
from streamlit.testing.v1 import AppTest
from model import costs, suitability

ROOT=Path(__file__).parent

def test_budget_math():
    result=costs(4,8000,3500,1000,1500,300000,950,10)
    assert result['숙박']==228000
    assert sum(result.values())==831600
    assert sum(costs(2,0,0,0,0,0,950,0).values())==0

def test_data_and_conditions():
    df=pd.read_csv(ROOT/'data/climate.csv')
    assert len(df)==72 and not df.duplicated(['city','month']).any()
    assert df.notna().all().all()
    assert set(df.month)==set(range(1,13))
    flags=suitability(df,(15,25),150)
    assert flags[(flags.city=='도쿄')&(flags.month==5)]['두 조건 충족'].item()
    assert not flags[(flags.city=='도쿄')&(flags.month==10)]['두 조건 충족'].item()

def test_app_interactions():
    at=AppTest.from_file(str(ROOT/'app.py'),default_timeout=60).run()
    assert not at.exception
    assert at.metric[0].value=='4곳'
    at.sidebar.multiselect[0].set_value(['나하']).run()
    assert not at.exception and at.metric[0].value=='1곳'
    at.sidebar.select_slider[0].set_value(1).run()
    assert not at.exception and at.metric[1].value=='1월'
    at.radio[0].set_value('내 조건 충족 여부').run()
    assert not at.exception
    for control in at.number_input:
        if control.label=='총예산 (원)':
            control.set_value(0)
    at.run()
    assert not at.exception
    at.sidebar.multiselect[0].set_value([]).run()
    assert not at.exception and len(at.info)==1
