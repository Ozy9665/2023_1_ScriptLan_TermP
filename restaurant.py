import requests
import xml.etree.ElementTree as ET
import tkinter
#
#식당 서비스 예제
url = 'https://openapi.gg.go.kr/GENRESTRT?'
# 공공데이터포털에서 발급받은 디코딩되지 않은 인증키 입력
service_key = ""
queryParams = {'KEY': service_key, 'pIndex': '1', 'pSize': '10'}


response = requests.get(url, params=queryParams)
print(response.text)
root = ET.fromstring(response.text)

window = tkinter.Tk()
window.title("식당")

frame = tkinter.Frame(window)
frame.pack()

header = ["Name", "Addr", "TELNO"]

for i, col_name in enumerate(header):
    label = tkinter.Label(frame, text=col_name, font=("Helvetica", 14, "bold"))
    label.grid(row=0, column=i)
# 현재 여까지 돌아감


row_count = 1
for item in root.iter("row"):
    BIZPLC_NM = item.findtext("BIZPLC_NM")
    REFINE_ROADNM_ADDR = item.findtext("REFINE_ROADNM_ADDR")
    LOCPLC_FACLT_TELNO = item.findtext("LOCPLC_FACLT_TELNO")

    data = [BIZPLC_NM, REFINE_ROADNM_ADDR, LOCPLC_FACLT_TELNO]
    for i, value in enumerate(data):
        label = tkinter.Label(frame, text=value, font=("Helvetica", 12))
        label.grid(row=row_count, column=i)

    row_count += 1

window.mainloop()

