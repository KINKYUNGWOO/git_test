import pandas as pd
import requests
from bs4 import BeautifulSoup
from requests_ntlm import HttpNtlmAuth

glcombi_url = 'http://tklis45249:8100/WebFormCombinationView.aspx'

def SetGlCombiData(eq_code_list):

    username = input("Input ID : ")
    password = input("Input PW : ")

    for eq_code in eq_code_list:

        #Session Open
        sess = requests.Session()
        resp = sess.get(glcombi_url, auth=HttpNtlmAuth(username, password))

        #ID/PW 검사, ID/PW가 틀리면 401 반환, 제대로 연결되면 200, OK
        if resp.status_code != 200:
            print(resp)
            print("Please check your ID/PW or if you are not authorized")
            break

        #Post에 필요한 Parameter 설정.
        soup = BeautifulSoup(resp.text, 'html.parser')

        viewstate = soup.select("#__VIEWSTATE")[0]['value']
        eventvalidation = soup.select("#__EVENTVALIDATION")[0]['value']
        params = {
            '__VIEWSTATE': viewstate,
            '__EVENTVALIDATION': eventvalidation,
            '__EVENTTARGET': 'ctl00$MainContent$DropDownListProduct',
            'ctl00$MainContent$DropDownListProduct': eq_code,
            'ctl00$MainContent$DropDownListSeries': 'ALL'
        }

        #설정된 Parameter로 Post 실행하여 WebSite 정보를 불러옴.
        resp = sess.post(glcombi_url, data=params)
        soup = BeautifulSoup(resp.text, 'html.parser')

        #Table을 찾고, 표 내부에 있는 그림을 CSV로 저장하기 위해 글자로 치환.
        all_table = soup.find('table')
        ng_table = str(all_table).replace('<font color="Black"><input alt="NG" onclick',
                                          '<font color="Black">NG<input alt="NG" onclick')
        ok_table = str(ng_table).replace('<font color="Black"><input alt="OK" onclick',
                                         '<font color="Black">OK<input alt="OK" onclick')

        #치환된 Table의 Html을 DataFrame으로 변환하여 csv로 저장.
        df_glcombidata = pd.DataFrame()
        df_glcombidata = df_glcombidata.append(pd.read_html(ok_table))
        df_glcombidata.rename(columns={"Unnamed: 0": "Version"}, inplace=True)
        df_glcombidata = df_glcombidata.set_index("Version", drop='False')

        filepath = "database/GLCombi" + "[" + str(eq_code) + "].csv"
        df_glcombidata.to_csv(filepath, mode='w')

if __name__ == '__main__':
    eq_code_list = [2,3,7]
    SetGlCombiData(eq_code_list)