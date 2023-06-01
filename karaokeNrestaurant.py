import requests
import xml.etree.ElementTree as ET
from tkinter import *
from tkinter import font
import tkinter.ttk
import Sggucd



query = 'portal/data/service/selectServicePage.do?page=1&rows=10&sortColumn=&sortDirection=&infId=DTG5WLA687OMHJMFRXH627862292&infSeq=3&order=&loc=&searchWord=%EB%85%B8%EB%9E%98%EB%B0%A9'

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

window = Tk()
window.title("노래방,식당")
DataList = []


# 지역리스트 삽입
def InitSearchBox():
    global SearchListBox
    ListBoxScrollbar = Scrollbar(frame1)
    ListBoxScrollbar.pack()
    ListBoxScrollbar.place(x=150, y=50)

    TempFont = font.Font(window, size=15, weight='bold', family='Consolas')
    SearchListBox = Listbox(frame1, font=TempFont, activestyle='none',
                            width=10, height=5, borderwidth=12, relief='ridge',
                            yscrollcommand=ListBoxScrollbar.set)

    for i in range(len(Sggucd.SGGUCD)):
        SearchListBox.insert(i+1, Sggucd.SGGUCD[i][1])  # 지역 리스트 삽입

    SearchListBox.pack()
    SearchListBox.place(x=10, y=50)

    ListBoxScrollbar.config(command=SearchListBox.yview)


def InitSearchButton():
    TempFont = font.Font(window, size=12, weight='bold', family='Consolas')
    SearchButton = Button(window, font=TempFont, text='검색', command=SearchButtonAction)
    SearchButton.pack()
    SearchButton.place(x=330, y=110)


def SearchButtonAction():
    global SearchListBox

    RenderText.configure(state='normal')
    RenderText.delete(0.0, END)
    iSearchIndex = SearchListBox.curselection()[0]

    sgguCd = Sggucd.SGGUCD[iSearchIndex][0]
    Search(sgguCd)

    RenderText.configure(state='disabled')


def Search(sgguCd):
    import http.client
    url = 'openapi.gg.go.kr'
    # port = 80
    conn = http.client.HTTPConnection(url)
    # conn = http.client.HTTPConnection(url, port)
    conn.request('GET', query+sgguCd)
    # conn.request('GET', '/sngrumIndutype?'+sgguCd)

    req = conn.getresponse()

    global DataList
    DataList.clear()

    if req.status == 200:
        strXml = req.read().decode('utf-8')
    tree = ET.fromstring(strXml)
    itemElements = tree.iter('row')
    for row in itemElements:
        addr = row.find('REFINE_ROADNM_ADDR')
        name = row.find('BIZPLC_NM')
        telno = row.find('LOCPLC_FACLT_TELNO')
        DataList.append((name.text, addr.text, telno.text))
    for i in range(len(DataList)):
        RenderText.insert(INSERT, '[')
        RenderText.insert(INSERT, i+1)
        RenderText.insert(INSERT, '] ')
        RenderText.insert(INSERT, ' 병원명: ')
        RenderText.insert(INSERT, DataList[i][0])
        RenderText.insert(INSERT, '\n')
        RenderText.insert(INSERT, '주소: ')
        RenderText.insert(INSERT, DataList[i][1])
        RenderText.insert(INSERT, '\n')
        RenderText.insert(INSERT, '전화번호')
        RenderText.insert(INSERT, DataList[i][2])
        RenderText.insert(INSERT, '\n\n')


def InitRenderText():
    global RenderText
    RenderTextScrollbar = Scrollbar(frame1)
    RenderTextScrollbar.pack()
    RenderTextScrollbar.place(x=375, y=200)
    TempFont = font.Font(frame1, size=10, family='Consolas')
    RenderText = Text(frame1, width=49, height=27, borderwidth=12, relief='ridge', yscrollcommand=RenderTextScrollbar.set)
    RenderText.pack()
    RenderText.place(x=10, y=215)
    RenderTextScrollbar.config(command=RenderText.yview)
    RenderTextScrollbar.pack(side=RIGHT, fill=BOTH)

    RenderText.configure(state='disabled')

# 페이지 나누기
notebook = tkinter.ttk.Notebook(window, width=800, height=600)
notebook.pack()

frame1 = Frame(window)
notebook.add(frame1, text='노래방')
Label(frame1, text='페이지1내용', fg='red', font='helvetica 48')

header = ["Name", "Addr", "TELNO"]
res_header = ["ResName", "ResAddr", "ResTel"]

# 노래방
'''
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
'''

frame2=Frame(window)
notebook.add(frame2, text='식당')
Label(frame2, text='페이지2내용', fg='blue', font='helvetica 48')
# 레스토랑
'''
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
'''
InitSearchBox()
InitSearchButton()
InitRenderText()
window.mainloop()

