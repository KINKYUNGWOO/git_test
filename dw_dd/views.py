from django.http import HttpResponse
from django.shortcuts import render

from bs4 import BeautifulSoup
import requests
import pandas as pd

import EquipmentDatabase as EqDb
import IngenioGLDatabse as GLDb
import CTSoftwareManagement as CTSW
import CT_GL_Version_Project_Rev3 as CTGL3
import GLStatus as GLSt

global glCombi

def refreshBTN(request): #로그인 이후 버튼이벤트 생성 임시
            return render(request,'login.html')

def login_next(request): #로그인 입력 성공시
    return render(request,"login_next.html")

def Base(request):
    return render(request,"result.html")


def main(request):
    return render(request,"main.html")


def GL_Result(request):
    EQ_Version = request.GET.get('EQ_Version')

    select_version = CTSW.SplitEqVersion(EQ_Version)
    GL_Version = CTGL3.FindGLVersionCombi(select_version, glCombi)
    fulltext = request.GET.get('fulltext')
    return render(request,"result.html",{"GLfulltext":GL_Version,'data':data,'label':label,'combo':combo, 'EQ_Version':EQ_Version,"fulltext":fulltext})



def Search_EQ(request):
    global glCombi
    global label
    global data
    global combo
    fulltext = request.GET.get('fulltext')

    equipment_db_path = "database/eq_data"+"[ALL].csv"
    eqdb = pd.read_csv(equipment_db_path,index_col=0)

    input_sn = fulltext.upper()
    eq_list = eqdb[eqdb['EQPID'].isin([input_sn]) | eqdb['SN'].isin([input_sn])]


    if len(eq_list) == 1 :
        customer_name = eq_list.iloc[0]['Customer'] # Customer열의 첫번째 값
        label , data = GLSt.GetGLStatusData(customer_name)

        machine_num = eq_list["SN"].iloc[0] #'SN'열의 첫번째 값.
        machine_type_code = CTGL3.CheckEqType(machine_num)

        if machine_type_code != 99 or machine_type_code != "":
            GLCombi_path = "database/GLCombi" + "[" + str(machine_type_code) + "].csv"
            glCombi = pd.read_csv(GLCombi_path, index_col=0)
        else:
            print("Check Equipment Serial Number")

        eqVerList = CTSW.FindEqVersionData(machine_num)
        ColNameList = ['Customer', 'FAB', 'Machine', 'SoftVersion']
        eqVerList.columns = ColNameList

        combo = eqVerList['SoftVersion']
        return render(request, 'result.html', {'data':data,'combo':combo,'label':label,'fulltext':fulltext})

    else:
    #except:
        Errortxt = 'There is no machine s/n. Please check Machine S/N'
        return render(request, 'main.html', {'Errortext': Errortxt})

def login(request):
    return render(request,"login.html")
