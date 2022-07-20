import requests
from bs4 import BeautifulSoup

def parse_horizontal_table(table, row_names=[]):
    out_dict = {}
    rows = table.find_all("tr")

    for i in range(len(rows)):
        data = rows[i].find_all("td")
        if i < len(row_names):
            name = row_names[i]
        else:
            name = data[0].get_text(strip=True)
        out_dict[name] = [val.get_text(strip=True) for val in data[1:]]

    return out_dict




def parse_vertical_table(table, col_names=[]):
    out_dict = {}
    rows = table.find_all("tr")

    names=[]

    for i in range(len(rows)):
        data = rows[i].find_all("td")
        if i == 0:
            for j in range(len(data)):
                if j < len(col_names):
                    names.append(col_names[j])
                else:
                    names.append(data[j].get_text(strip=True))

                out_dict[names[j]] = []
        else:
            for j in range(len(data)):
                out_dict[names[j]].append(data[j].get_text(strip=True))

    return out_dict 




URL = "https://uspdigital.usp.br/jupiterweb/obterTurma?nomdis=&sgldis=PCS3559"
page = requests.get(URL)

#print(page.text)

soup = BeautifulSoup(page.content, "html.parser")

class_infos_attr = {
    "style" : "border: 2px solid #658CCF; padding: 5px; border-radius: 5px;"
}

class_infos = soup.find_all("div", attrs=class_infos_attr)
row_names = ['cod_turma', 'inicio', 'fim', 'tipo', 'obs']
col_names = ['dia_semana', 'hora_inicio', 'hora_fim', 'prof']

for c_info in class_infos:

    infos = c_info.find_all("table")

    #print(parse_horizontal_table(infos[0], row_names))
    print(parse_vertical_table(infos[1], col_names))




    