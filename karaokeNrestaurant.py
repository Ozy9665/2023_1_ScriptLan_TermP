import requests
import xml.etree.ElementTree as ET
from tkinter import *
import tkinter.ttk


#
#노래방 서비스 예제
karaoke_url = 'https://openapi.gg.go.kr/sngrumIndutype?'
restaurant_url = 'https://openapi.gg.go.kr/GENRESTRT?'
# 공공데이터포털에서 발급받은 디코딩되지 않은 인증키 입력
karaoke_service_key = ""
karaoke_queryParams = {'KEY': karaoke_service_key, 'pIndex': '1', 'pSize': '10'}
restaurant_service_key = ""
restaurant_queryParams = {'KEY': restaurant_service_key, 'pIndex': '1', 'pSize': '10'}

karaoke_response = requests.get(karaoke_url, params=karaoke_queryParams)
print(karaoke_response.text)
karaoke_root = ET.fromstring(karaoke_response.text)

restaurant_response = requests.get(restaurant_url, params=restaurant_queryParams)
print(restaurant_response.text)
restaurant_root = ET.fromstring(restaurant_response.text)

window = tkinter.Tk()
window.title("노래방,식당")

# 페이지 나누기
notebook = tkinter.ttk.Notebook(window, width=800, height=600)
notebook.pack()

frame1 = Frame(window)
notebook.add(frame1, text='노래방')
Label(frame1, text='페이지1내용', fg='red', font='helvetica 48')

header = ["Name", "Addr", "TELNO"]
res_header = ["ResName", "ResAddr", "ResTel"]

# 노래방
for i, col_name in enumerate(header):
    label = Label(frame1, text=col_name, font=("Helvetica", 14, "bold"))
    label.grid(row=0, column=i)


row_count = 1
for item in karaoke_root.iter("row"):
    BIZPLC_NM = item.findtext("BIZPLC_NM")
    REFINE_ROADNM_ADDR = item.findtext("REFINE_ROADNM_ADDR")
    LOCPLC_FACLT_TELNO = item.findtext("LOCPLC_FACLT_TELNO")

    data = [BIZPLC_NM, REFINE_ROADNM_ADDR, LOCPLC_FACLT_TELNO]
    for i, value in enumerate(data):
        label = tkinter.Label(frame1, text=value, font=("Helvetica", 12))
        label.grid(row=row_count, column=i)

    row_count += 1


frame2=Frame(window)
notebook.add(frame2, text='식당')
Label(frame2, text='페이지2내용', fg='blue', font='helvetica 48')
# 레스토랑
for i, col_name in enumerate(res_header):
    label = tkinter.Label(frame2, text=col_name, font=("Helvetica", 14, "bold"))
    label.grid(row=row_count, column=i)

row_count += 1

for item in restaurant_root.iter("row"):
    BIZPLC_NM = item.findtext("BIZPLC_NM")
    REFINE_ROADNM_ADDR = item.findtext("REFINE_ROADNM_ADDR")
    LOCPLC_FACLT_TELNO = item.findtext("LOCPLC_FACLT_TELNO")

    data = [BIZPLC_NM, REFINE_ROADNM_ADDR, LOCPLC_FACLT_TELNO]
    for i, value in enumerate(data):
        label = Label(frame2, text=value, font=("Helvetica", 12))
        label.grid(row=row_count, column=i)

    row_count += 1

window.mainloop()

