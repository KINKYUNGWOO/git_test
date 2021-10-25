import pandas as pd
import requests
import EquipmentDatabase as EqDb
import IngenioGLDatabse as GLDb
from urllib.request import urlopen
from bs4 import BeautifulSoup
from requests_ntlm import HttpNtlmAuth

eqverinfo_url = ['http://tekis1244/TEKCTSVM/Board/list.aspx?gn=S&ccd=All&lcd=All&t=&s=','&ty=All&send=&work=&ncdr=&sv=&con=']

username ="administrator"
password = "123qwe!@#"

def SplitEqVersion(eqVer):
    eqVerSplit = eqVer.split('+')[0].split('.')

    eqVer1 = '.'.join(eqVerSplit[0:4])
    eqVer2 = '.'.join(eqVerSplit[0:3])

    eqVerList = [eqVer1, eqVer2]
    return eqVerList

def FindEqVersionData(machine_num):
    url = eqverinfo_url[0] + machine_num + eqverinfo_url[1]

    req = requests.get(url, auth=HttpNtlmAuth(username, password))
    soup = BeautifulSoup(req.text, 'html.parser')

    html_table = soup.find('table')
    df_table = pd.DataFrame()
    df_table = pd.read_html(str(html_table))

    eq_version_data = df_table[0].iloc[:, [1, 2, 3, 5]]

    return eq_version_data

def GetEqVersion(eq_version_data, index):

    select_ver = eq_version_data.loc[int(index)]
    eq_ver = select_ver[3]

    return SplitEqVersion(eq_ver)

