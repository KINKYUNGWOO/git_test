import pandas as pd
import EquipmentDatabase as EqDb
import IngenioGLDatabse as GLDb
import CTSoftwareManagement as CTSW

def FindGLVersionCombi(eqVersion, df):

    if eqVersion[0] in df.columns:
        print(eqVersion[0])
        glVersion = df.index[df[eqVersion[0]]=='OK'].tolist()
    elif eqVersion[1] in df.columns:
        print(eqVersion[0])
        glVersion = df.index[df[eqVersion[1]]=='OK'].tolist()
    else:
        glVersion = "N/A"

    return glVersion[0]

def CheckEqType(equipment_Serial_Number):

    gl_combi_info = {'LITHIUS':'2','LITHIUSPro':'3','LITHIUSProZ':'7', 'ACT':'99'}

    if equipment_Serial_Number[0].upper() == 'Z'or equipment_Serial_Number[0].upper() == 'K':
        print(gl_combi_info['LITHIUSProZ'])
        return gl_combi_info['LITHIUSProZ']
    elif equipment_Serial_Number[0] == 'V' or equipment_Serial_Number[0] == 'v' or equipment_Serial_Number[0] == 'N' or equipment_Serial_Number[0] == 'n':
        return gl_combi_info['LITHIUSPro']
    elif equipment_Serial_Number[0] == 'G' or equipment_Serial_Number[0] == 'g':
        return gl_combi_info['LITHIUS']
    elif equipment_Serial_Number[0] == 'E' or equipment_Serial_Number[0] == 'e' or equipment_Serial_Number[0] == 'J' or equipment_Serial_Number[0] == 'J':
        return gl_combi_info['ACT']
    else:
        return gl_combi_info['ACT']

def initialize_DB():
    # CT Hompage에서 장비 정보를 불러와 csv로 저장.
    # 10 = SEC, 28 = SKH(I), 29 = SKH(C)
    cus_code = [10, 28, 29]
    EqDb.SetEqData(cus_code)

    # GLCombination Homepage에서 GL 버전 정보를 불러와 csv로 저장.
    # 2 = LITHIUS , 3 = PRO/PROV , 7 = PROZ
    eq_code_list = [2, 3, 7]
    GLDb.SetGlCombiData(eq_code_list)

######Main#######
if __name__ == '__main__':

    #DB 초기화
    #initialize_DB()

    equipment_db_path = "database/eq_data"+"[ALL].csv"
    eqdb = pd.read_csv(equipment_db_path,index_col=0)

    input_sn = input("Input Machine Number : ")
    input_sn = input_sn.upper()
    eq_list = eqdb[eqdb['EQPID'].isin([input_sn]) | eqdb['SN'].isin([input_sn])]

    if len(eq_list) == 1 :

        Customer = eq_list.iloc[0]['Customer'] # Customer열의 첫번째 값
        print(Customer)

        machine_num = eq_list["SN"].iloc[0] #'SN'열의 첫번째 값.
        machine_type_code = CheckEqType(machine_num)

        if machine_type_code != 99 or machine_type_code != "":
            GLCombi_path = "database/GLCombi" + "[" + str(machine_type_code) + "].csv"
            glCombi = pd.read_csv(GLCombi_path, index_col=0)
        else:
            print("Check Equipment Serial Number")


        eqVerList = CTSW.FindEqVersionData(machine_num)
        ColNameList = ['Customer', 'FAB', 'Machine', 'SoftVersion']
        eqVerList.columns = ColNameList
        print(eqVerList['SoftVersion'])

        select_version_index = input("Select Version Number : ")
        select_version = CTSW.GetEqVersion(eqVerList, select_version_index)

        print(FindGLVersionCombi(select_version, glCombi))

    else:
        print(eq_list)
        print("Check Equipment Serial Number")






