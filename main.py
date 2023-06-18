import tkinter as tk
import tkinter.ttk as ttk
import requests
import xml.etree.ElementTree as ET
from PIL import Image, ImageTk
import io
from googlemaps import Client

zoom = 13

# 공공데이터 API 키
api_key_k = "bffbc47cb864414c97e2ec2f249a364d"
api_key_r = "446f9523547c4323b5a529e9f553c2b5"

# Google Maps API 키
Google_API_Key = 'AIzaSyC-Rg20B0vglH9DSOor7uTyXFtBtKSvIWk'

# url
Kurl = 'https://openapi.gg.go.kr/restprod?'
Rurl = 'https://openapi.gg.go.kr/GENRESTRT?'

# 공공데이터 API 요청 파라미터
r_params = {
    "KEY": api_key_k,
    "pSize": 350,
    "sgguCd": 41390,
}

response = requests.get(Rurl, params=r_params)
root = ET.fromstring(response.content)
items = root.findall(".//row")

restaurants = []
for item in items:
    restaurant = {
        "name": item.findtext("BIZPLC_NM"),
        "address": item.findtext("REFINE_ROADNM_ADDR"),
        "lat": item.findtext("REFINE_WGS84_LAT"),
        "lng": item.findtext("REFINE_WGS84_LOGT"),
        "emplies": item.findtext("TOT_EMPLY_CNT"),
    }
    restaurants.append(restaurant)

# 노래방 데이터 가져오기
k_params = {
    "KEY": api_key_k,
    "pSize": 350,
    "sgguCd": 41390,
}

response = requests.get(Kurl, params=k_params)
root = ET.fromstring(response.content)
items = root.findall(".//row")

karaoke_rooms = []
for item in items:
    karaoke_room = {
        "name": item.findtext("BIZPLC_NM"),
        "address": item.findtext("REFINE_ROADNM_ADDR"),
        "lat": item.findtext("REFINE_WGS84_LAT"),
        "lng": item.findtext("REFINE_WGS84_LOGT"),
        "rooms": item.findtext("ROOM_CNT"),
    }
    karaoke_rooms.append(karaoke_room)

# Google Maps API 클라이언트 생성
gmaps = Client(key=Google_API_Key)


def show_karaoke_list():
    # 팝업 창 생성
    popup = tk.Toplevel(root)
    popup.title("노래방 목록")

    # 노래방 목록 라벨
    karaoke_label = tk.Label(popup, text="노래방 목록")
    karaoke_label.pack()

    # 노래방 목록 리스트박스
    karaoke_listbox = tk.Listbox(popup)
    karaoke_listbox.pack()

    # 노래방 데이터 추가
    for karaoke in karaoke_rooms:
        karaoke_listbox.insert(tk.END, karaoke["name"])

    # 팝업 창 닫기 버튼
    close_button = tk.Button(popup, text="닫기", command=popup.destroy)
    close_button.pack()

# tkinter GUI 생성
root = tk.Tk()
root.title("식당 및 노래방 정보")

selected_gu = tk.StringVar()
selected_gu.set("시흥시")

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


def show_restaurant():
    restaurant_list.delete(0, tk.END)

    gu_name = selected_gu.get()
    restaurants_in_gu = [restaurant for restaurant in restaurants if len(restaurant['address'].split()) >= 2 and
                         restaurant['address'].split()[1] == gu_name]

    for restaurant in restaurants_in_gu:
        restaurant_list.insert(tk.END, f"{restaurant['name']} ({restaurant['emplies']} employees)")


def show_karaoke():
    karaoke_list.delete(0, tk.END)

    gu_name = selected_gu.get()
    karaoke_in_gu = [karaoke for karaoke in karaoke_rooms if len(karaoke['address'].split()) >= 2 and
                     karaoke['address'].split()[1] == gu_name]

    for karaoke in karaoke_in_gu:
        karaoke_list.insert(tk.END, f"{karaoke['name']} ({karaoke['rooms']} rooms)")


def update_map():
    global zoom
    gu_name = selected_gu.get()
    gu_center = gmaps.geocode(f"{gu_name}")[0]['geometry']['location']
    gu_map_url = f"https://maps.googleapis.com/maps/api/staticmap?center={gu_center['lat']},{gu_center['lng']}&zoom={zoom}&size=400x400&maptype=roadmap"

    restaurants_in_gu = [restaurant for restaurant in restaurants if len(restaurant['address'].split()) >= 2 and
                         restaurant['address'].split()[1] == gu_name]

    for restaurant in restaurants_in_gu:
        if restaurant['lat'] and restaurant['lng']:
            lat, lng = float(restaurant['lat']), float(restaurant['lng'])
            marker_url = f"&markers=color:red%7C{lat},{lng}"
            gu_map_url += marker_url

    karaoke_in_gu = [karaoke for karaoke in karaoke_rooms if len(karaoke['address'].split()) >= 2 and
                     karaoke['address'].split()[1] == gu_name]

    for karaoke in karaoke_in_gu:
        if karaoke['lat'] and karaoke['lng']:
            lat, lng = float(karaoke['lat']), float(karaoke['lng'])
            marker_url = f"&markers=color:blue%7C{lat},{lng}"
            gu_map_url += marker_url

    response = requests.get(gu_map_url + '&key=' + Google_API_Key)
    image = Image.open(io.BytesIO(response.content))
    photo = ImageTk.PhotoImage(image)
    map_label.configure(image=photo)
    map_label.image = photo

    show_restaurant()
    show_karaoke()


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


# 식당 페이지 프레임 생성
restaurant_frame = tk.Frame(root)
restaurant_frame.pack(side=tk.LEFT, padx=10)

# 식당 목록 라벨 생성
restaurant_label = tk.Label(restaurant_frame, text="식당 목록", font=("Arial", 12, "bold"))
restaurant_label.pack()

# 식당 목록 스크롤바 생성
restaurant_scrollbar = tk.Scrollbar(restaurant_frame)
restaurant_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# 식당 목록 리스트박스 생성
restaurant_list = tk.Listbox(restaurant_frame, width=40, yscrollcommand=restaurant_scrollbar.set)
restaurant_list.pack(fill=tk.BOTH, expand=True)

# 식당 목록 스크롤바와 리스트박스 연결
restaurant_scrollbar.config(command=restaurant_list.yview)

# 노래방 페이지 프레임 생성
karaoke_frame = tk.Frame(root)
karaoke_frame.pack(side=tk.LEFT, padx=10)

# 노래방 목록 라벨 생성
karaoke_label = tk.Label(karaoke_frame, text="노래방 목록", font=("Arial", 12, "bold"))
karaoke_label.pack()

# 노래방 목록 스크롤바 생성
karaoke_scrollbar = tk.Scrollbar(karaoke_frame)
karaoke_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# 노래방 목록 리스트박스 생성
karaoke_list = tk.Listbox(karaoke_frame, width=40, yscrollcommand=karaoke_scrollbar.set)
karaoke_list.pack(fill=tk.BOTH, expand=True)

# 노래방 목록 스크롤바와 리스트박스 연결
karaoke_scrollbar.config(command=karaoke_list.yview)

# 맵 이미지 프레임 생성
map_frame = tk.Frame(root)
map_frame.pack(side=tk.LEFT, padx=10)

# 맵 이미지 라벨 생성
map_label = tk.Label(map_frame)
map_label.pack()

# 지도 조작 버튼 프레임 생성
zoom_frame = tk.Frame(root)
zoom_frame.pack(side=tk.LEFT, padx=10)

# 지도 확대 버튼 생성
zoom_in_button = tk.Button(zoom_frame, text="확대", command=zoom_in)
zoom_in_button.pack()

# 지도 축소 버튼 생성
zoom_out_button = tk.Button(zoom_frame, text="축소", command=zoom_out)
zoom_out_button.pack()

# 이벤트 바인딩
gu_combo.bind("<<ComboboxSelected>>", on_gu_select)

# 초기 지도 업데이트
update_map()


# GUI 실행
root.mainloop()
