import requests
import json
import contador
import utils
import bd_layer.storage_class as storage_class
import os

class Sla_month_extrator():
  def __init__(self, usuarios_fabrica, feriados, paginas, mes, ano, user_login, file_name, off_set):
    self.usuarios_fabrica = usuarios_fabrica
    self.feriados = feriados
    self.paginas = paginas
    self.mes = mes
    self.ano = ano
    self.user_login = user_login
    self.file_name = file_name
    self.off_set = off_set

  def execute(self):
    offset_numero = self.off_set
    issues_resolved_list = []

    # percorre por 10 paginas com 50 issues cada
    percorre_quantas_paginas = self.paginas

    url_login = 'https://redmine.iphan.gov.br/issues.json' 

    auth_user = self.user_login

    qual_mes = self.mes

    qual_ano = self.ano

    dias_feriados = self.feriados

    url_base = 'https://redmine.iphan.gov.br'
    projects = '/projects.json'
    issues = '/issues.json'
    issue7400 = "/issues/7400.json"
    notas = 'include=journals'
    sustentacao = 'tracker_id=49'
    status_closed = 'status_id=closed'
    add_filtro = '&'
    iniciarFiltro = '?'
    # 100 sao muitos dados, esbarrou no limite de json de itens (5000)
    limit = 'limit=50'
    offset = 'offset='+ str(offset_numero)

    url_request = url_base + issues + iniciarFiltro + \
      status_closed + add_filtro + limit + add_filtro + offset

    response = requests.get(url_request, auth=auth_user, verify="certicate.pem")

    dicionario = response.text

    dicionario_deconding = json.loads(dicionario)

    # criar um arquivo resultado mostrando a resposta de cada pagina
    """
    json_object = json.dumps(dicionario_deconding, indent=4, ensure_ascii=False)

    with open("resultado.json", "w", encoding='utf-8') as outfile:
        outfile.write(json_object)
    """

    # all_issues_list = dicionario["issues"]

    for tarefa in dicionario_deconding["issues"]:
      closed_on = tarefa["closed_on"]
      mes_closed = closed_on[5:7]
      ano_closed = closed_on[0:4]

      status = tarefa["status"]["name"]
      tipo = tarefa["tracker"]["name"]
      if (status == "Resolvida") & (mes_closed == str(qual_mes)) & (ano_closed == str(qual_ano)) & (tipo == "Sustentação"):
        issues_resolved_list.append(tarefa["id"])

    list_of_results = []

    # leandro, rhoxanna, mauricio, cristiano, romao, gestor fabrica, desenvolvedor fabrica, sabino, michel, henrique, testador fabrica, valter, domingos, vinicius
    usuarios_da_fabrica = self.usuarios_fabrica

    for issue in issues_resolved_list:
        list_of_results.append(contador.execute(issue, dias_feriados, auth_user, usuarios_da_fabrica))
    
    # Resultados em json
    saving_in_temp = utils.result_to_json(issues_resolved_list, list_of_results)

    #saving_in_temp = utils.result_to_csv(issues_resolved_list, list_of_results, self.file_name)
    
    """if saving_in_temp[0] == 200:
      blob_name = self.file_name.split("\\")
      storage_class.upload_blob_from_file("redmine-bd.appspot.com", self.file_name, blob_name[-1])

      if os.path.exists(self.file_name):
        os.remove(self.file_name) """

    return saving_in_temp

