from pathlib import Path
from streamlit.testing.v1 import AppTest


def test_city_and_month_selection():
    app = AppTest.from_file(str(Path(__file__).parent / "app.py"), default_timeout=60).run()
    assert not app.exception
    assert app.selectbox[0].options == ["도쿄", "오사카", "삿포로"]
    assert len(app.dataframe[0].value) == 12
    app.selectbox[0].set_value("삿포로").run()
    assert not app.exception
    assert app.dataframe[0].value.iloc[0]["평균기온 (°C)"] == -3.2
    app.slider[0].set_value(1).run()
    assert not app.exception
    assert any("오사카" in item.value and "47.0" in item.value for item in app.markdown)
