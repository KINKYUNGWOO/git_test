import pandas as pd

def GetGLStatusData(Customer):

    GLStatusDB = pd.read_csv("database/GL_Source_Data.csv")
    is_Customer = GLStatusDB['Customer'] == Customer
    FilteredDB = GLStatusDB[is_Customer]
    Line_list = FilteredDB['Line'].values.tolist()
    Versoin_list = FilteredDB['Version'].values.tolist()

    formatted_list = []
    for v in Versoin_list:
        formatted_list.append(v.split('.')[2])

    return Line_list, formatted_list


x,y = GetGLStatusData("Samsung")
print(x)
print(y)
