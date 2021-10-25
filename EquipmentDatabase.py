import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup

eqinfo_url =['http://tekis1244.asia.tel.com/TEKCTSPS/maclist/mac_board.asp?page=',
           '&order_arrange=111&s_machine_no=&s_machine_name=&s_code_no=&s_customer_name=',
           '&s_fab_name=&s_process=&s_scan_maker=&s_scan_model=&s_scan_model2=&s_thc=&s_move_in_year=&s_move_in_month=&s_warranty_in=&s_warranty_out=&s_comment=&s_exception=0']
#http://tekis1244/TEKCTSVM/Board/list.aspx?gn=S&ccd=All&lcd=All&t=&s=G240114&ty=All&send=&work=&ncdr=&sv=&con=

def GetLastPage(cus_code):

    url = eqinfo_url[0] + '1' + eqinfo_url[1] +  str(cus_code) + eqinfo_url[2]

    with urlopen(url) as doc:
        html = BeautifulSoup(doc,'lxml')
        table_array = html.find_all('table')
        href_array = table_array[-1].find_all('a')

    tmp = href_array[-1].attrs["href"]
    tmp = tmp.split('=')
    tmp = tmp[1].split('&')

    last_page = tmp[0]

    return last_page

def SetEqData(cus_code_list):
    df_eqdata = pd.DataFrame()

    for cus_code in cus_code_list:
        lastPage = GetLastPage(cus_code)
        for i in range(1, int(lastPage) + 1):
            url = eqinfo_url[0] + str(i) + eqinfo_url[1] + str(cus_code) + eqinfo_url[2]

            with urlopen(url) as doc:
                html = BeautifulSoup(doc, 'lxml')
                table_array = html.find_all('table')

            df_eqdata = df_eqdata.append(pd.read_html(str(table_array[-2])))

    df_eqdata = df_eqdata.drop(0)
    df_eqdata = df_eqdata.iloc[:, [1, 2, 3, 4]]
    df_eqdata.columns = ["Customer", "FAB", "EQPID", "SN"]
    df_eqdata = df_eqdata.reset_index(drop=True)

    filepath = "database/eq_data[ALL].csv"
    df_eqdata.to_csv(filepath, mode='w')

if __name__ == '__main__':
    cus_code = [10, 28, 29]
    SetEqData(cus_code)