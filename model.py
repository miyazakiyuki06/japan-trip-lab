"""Transparent scenario calculations. Values are assumptions, not market quotes."""
import pandas as pd

CITIES = ['도쿄', '오사카', '나고야', '후쿠오카', '삿포로', '나하']

def costs(days, room, food, transit, activities, flight, rate, reserve):
    yen = {'숙박': room * (days - 1), '식비': food * days,
           '현지 교통': transit * days, '관광·체험': activities * days}
    krw = {k: v * rate / 100 for k, v in yen.items()}
    krw['왕복 항공'] = flight
    krw['예비비'] = sum(krw.values()) * reserve / 100
    return krw

def suitability(frame, preferred, rain_limit):
    """Flag preferences rather than invent an opaque travel score."""
    result = frame.copy()
    result['선호 기온 충족'] = result.temperature_c.between(*preferred)
    result['강수량 조건 충족'] = result.precipitation_mm <= rain_limit
    result['두 조건 충족'] = result['선호 기온 충족'] & result['강수량 조건 충족']
    return result
