"""Reproduce the bundled JMA normals subset; no network needed at runtime."""
import csv
from pathlib import Path

SOURCE = 'https://www.data.jma.go.jp/stats/data/en/normal/normal.html'
DATA = {
    '도쿄': ('Tokyo', [5.4,6.1,9.4,14.3,18.8,21.9,25.7,26.9,23.3,18,12.5,7.7], [59.7,56.5,116,133.7,139.7,167.8,156.2,154.7,224.9,234.8,96.3,57.9]),
    '오사카': ('Osaka', [6.2,6.6,9.9,15.2,20.1,23.6,27.7,29,25.2,19.5,13.8,8.7], [47,60.5,103.1,101.9,136.5,185.1,174.4,113,152.8,136,72.5,55.5]),
    '나고야': ('Nagoya', [4.8,5.5,9.2,14.6,19.4,23,26.9,28.2,24.5,18.6,12.6,7.2], [50.8,64.7,116.2,127.5,150.3,186.5,211.4,139.5,231.6,164.7,79.1,56.6]),
    '후쿠오카': ('Fukuoka', [6.9,7.8,10.8,15.4,19.9,23.3,27.4,28.4,24.7,19.6,14.2,9.1], [74.4,69.8,103.7,118.2,133.7,249.6,299.1,210,175.1,94.5,91.4,67.5]),
    '삿포로': ('Sapporo', [-3.2,-2.7,1.1,7.3,13,17,21.1,22.3,18.6,12.1,5.2,-0.9], [108.4,91.9,77.6,54.6,55.5,60.4,90.7,126.8,142.2,109.9,113.8,114.5]),
    '나하': ('Naha', [17.3,17.5,19.1,21.5,24.2,27.2,29.1,29,27.9,25.5,22.5,19], [101.6,114.5,142.8,161,245.3,284.4,188.1,240,275.2,179.2,119.1,110]),
}
if __name__ == '__main__':
    with (Path(__file__).parent/'data/climate.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['city','station','month','temperature_c','precipitation_mm','normal_period','source'])
        for city, (station, temps, rain) in DATA.items():
            for month, (t, p) in enumerate(zip(temps, rain), 1):
                writer.writerow([city,station,month,t,p,'1991–2020',SOURCE])
