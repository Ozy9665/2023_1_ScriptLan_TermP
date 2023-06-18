import tkinter as tk
import tkinter.ttk as ttk
import requests
import xml.etree.ElementTree as ET
from PIL import Image, ImageTk
import io
from googlemaps import Client
from tkinter import font

zoom = 13

# 공공데이터 API 키
api_key_k = "bffbc47cb864414c97e2ec2f249a364d"
api_key_r = "446f9523547c4323b5a529e9f553c2b5"
# url
Kurl = 'https://openapi.gg.go.kr/sngrumIndutype?'
Rurl = 'https://openapi.gg.go.kr/GENRESTRT?'


r_params = {
    "KEY": api_key_k,
    "pSize": 350,  #
    "sgguCd": 41390,  # 코드
}


response = requests.get(Rurl, params=r_params)
root = ET.fromstring(response.content)
items = root.findall(".//row")


restaurants = []
for item in items:
    restaurant = {
        "name": item.findtext("BIZPLC_NM"),  # 식당 이름
        "address": item.findtext("REFINE_ROADNM_ADDR"),  # 식당 주소
        "lat": item.findtext("REFINE_WGS84_LAT"),  # 위도
        "lng": item.findtext("REFINE_WGS84_LOGT"),  # 경도
        "emplies": item.findtext("TOT_EMPLY_CNT"),  # 총 종업원 수
    }
    restaurants.append(restaurant)

# Google Maps API 클라이언트 생성
Google_API_Key = 'AIzaSyC-Rg20B0vglH9DSOor7uTyXFtBtKSvIWk'
gmaps = Client(key=Google_API_Key)

# 지도 생성
center = gmaps.geocode("경기도 시흥시 정왕동 876-207")[0]['geometry']['location']
map_url = f"https://maps.googleapis.com/maps/api/staticmap?center={center['lat']},{center['lng']}&zoom={zoom}&size=400x400&maptype=roadmap"

# 음식점별 병원 위치 마커 추가
for restaurant in restaurants:
    if restaurant['lat'] and restaurant['lng']:
        lat, lng = float(restaurant['lat']), float(restaurant['lng'])
        marker_url = f"&markers=color:red%7C{lat},{lng}"
        map_url += marker_url

# tkinter GUI 생성
root = tk.Tk()
root.title("식당 정보")

# 지역 선택 콤보박스 생성
selected_gu = tk.StringVar()
selected_gu.set("시흥시")  # 초기값 설정

gu_options = set()
for restaurant in restaurants:
    try:
        address_parts = restaurant['address'].split()
        if len(address_parts) >= 2:
            gu_name = address_parts[1]
            gu_options.add(gu_name)
    except (TypeError, IndexError) as e:
        print(f"Error processing restaurant: {restaurant}")
        print(f"Error message: {str(e)}")
gu_combo = ttk.Combobox(root, textvariable=selected_gu, values=list(gu_options))
gu_combo.pack()


# 식당 목록 표시 함수
def show_restaurant():
    restaurant_list.delete(0, tk.END)

    gu_name = selected_gu.get()
    restaurants_in_gu = [restaurant for restaurant in restaurants if len(restaurant['address'].split()) >= 2 and restaurant['address'].split()[1] == gu_name]

    restaurant_names = [restaurant['name'] for restaurant in restaurants_in_gu]
    emply_counts = [restaurant['emplies'] for restaurant in restaurants_in_gu]

    # 캔버스 초기화
    canvas.delete('all')

    # # 막대그래프 생성
    # max_emply_count = max(emply_counts)
    # bar_width = 20
    # x_gap = 30
    # x0 = 60
    # y0 = 250
    # for i in range(len(restaurant_names)):
    #     x1 = x0 + i * (bar_width + x_gap)
    #     y1 = y0 - 200 * emply_counts[i] / max_emply_count
    #     canvas.create_rectangle(x1, y1, x1 + bar_width, y0, fill='blue')
    #     canvas.create_text(x1 + bar_width / 2, y0 + 100, text=restaurant_names[i], anchor='n', angle=90)
    #     canvas.create_text(x1 + bar_width / 2, y1 -10, text=emply_counts[i], anchor='s')

    # 병원 목록에 추가
    for restaurant in restaurants_in_gu:
        restaurant_list.insert(tk.END, f"{restaurant['name']} ({restaurant['emplies']} emplies)")


#지도 이미지 업데이트 함수
def update_map():
    global zoom
    gu_name = selected_gu.get()
    gu_center = gmaps.geocode(f"{gu_name}")[0]['geometry']['location']
    gu_map_url = f"https://maps.googleapis.com/maps/api/staticmap?center={gu_center['lat']},{gu_center['lng']}&zoom={zoom}&size=400x400&maptype=roadmap"

    # 선택한 구의 병원 위치 마커 추가
    restaurants_in_gu = [restaurant for restaurant in restaurants if len(restaurant['address'].split()) >= 2 and restaurant['address'].split()[1] == gu_name]

    for restaurant in restaurants_in_gu:
        if restaurant['lat'] and restaurant['lng']:
            lat, lng = float(restaurant['lat']), float(restaurant['lng'])
            marker_url = f"&markers=color:red%7C{lat},{lng}"
            gu_map_url += marker_url

    # 지도 이미지 업데이트
    response = requests.get(gu_map_url+'&key='+Google_API_Key)
    image = Image.open(io.BytesIO(response.content))
    photo = ImageTk.PhotoImage(image)
    map_label.configure(image=photo)
    map_label.image = photo

    # 식당 목록 업데이트
    show_restaurant()


def on_gu_select(event):
    update_map()


def zoom_in():
    global zoom
    zoom += 1
    update_map()


def zoom_out():
    global zoom
    if zoom > 1:
        zoom -= 1
    update_map()


# 캔버스 생성
canvas = tk.Canvas(root, width=800, height=400)
canvas.pack()

# 병원 목록 리스트박스 생성
restaurant_list = tk.Listbox(root, width=60)
restaurant_list.pack(side=tk.LEFT, fill=tk.BOTH)

# 스크롤바 생성
scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# 스크롤바와 병원 목록 연결
restaurant_list.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=restaurant_list.yview)


#지도 이미지 다운로드
response = requests.get(map_url+'&key='+Google_API_Key)
image = Image.open(io.BytesIO(response.content))
photo = ImageTk.PhotoImage(image)

#지도 이미지 라벨 생성
map_label = tk.Label(root, image=photo)
map_label.pack()

# 확대/축소 버튼 생성
zoom_in_button = tk.Button(root, text="확대(+)", command=zoom_in)
zoom_in_button.pack(side=tk.LEFT)

zoom_out_button = tk.Button(root, text="축소(-)", command=zoom_out)
zoom_out_button.pack(side=tk.LEFT)


update_map()


root.mainloop()
