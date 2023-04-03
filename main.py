from email.mime import base
from pickle import PUT
from fastapi import FastAPI, Response, status, Header, Depends, HTTPException
import bases_models
import login_class
from fastapi.middleware.cors import CORSMiddleware
import bd_layer.crud_class as crud_class
import auth_layer.jwt_class as auth_class
from service_layer.params_formater import Params_formater as Params
from service_layer.sla_month_extractor import Sla_month_extrator as Extractor
from typing import Union
import datetime
import os
from auth_layer.auth_bearer import JWTBearer

app = FastAPI()

#origins = ["*"]
origins = ["http://localhost:8080", "https://esr-front.vercel.app" , "https://esr-web.vercel.app"]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

@app.get("/")
async def root():
  return {"message" : "ESR_backend server is online"}

#login
@app.post("/login/", status_code=200)
async def create_login(login: bases_models.Login, response: Response ):
  login_dict = login.dict()
  response_login = login_class.login_auth(login_dict=login_dict)
  if  response_login[0] != 200:
    response.status_code = status.HTTP_401_UNAUTHORIZED
  else:
    token = auth_class.verify_and_decode_jwt(response_login[1]) 
    token_expires_time_stamp = token["exp"]
    token_expires = datetime.datetime.fromtimestamp(token_expires_time_stamp)
    response.set_cookie(key="Authorization",value=f"Bearer {response_login[1]}", httponly=True , expires=token_expires.strftime("%a, %d %b %Y %H:%M:%S GMT"), samesite="none", secure=True)
  return  [{"redmine_status_response": response_login[0]}]

#create configurações
@app.post("/configuracoes/usuariosFabrica/", status_code=201, dependencies=[Depends(JWTBearer())])
async def create_usuarios_fabrica(usuario: bases_models.Usuario_fabrica, response: Response ):
  usuario_dict = usuario.dict()
  response_crud = crud_class.create_usuarios_fabrica_BD(id=usuario_dict["id"],login=usuario_dict["login"])
  if response_crud[0] != 201:
    response.status_code = status.HTTP_400_BAD_REQUEST
  return [{"redmine_status_response": response_crud[0]}, response_crud[1]]

@app.post("/configuracoes/feriadosEDatas/", status_code=201, dependencies=[Depends(JWTBearer())])
async def create_feriados_e_datas(ferido_e_datas: bases_models.Feriados_e_datas , response: Response):
  feriados_e_datas_dict= ferido_e_datas.dict()
  response_crud = crud_class.create_feriados_e_datas_DB(dia=feriados_e_datas_dict["dia"],periodo=feriados_e_datas_dict["periodo"])
  if response_crud[0] != 201:
    response.status_code = status.HTTP_400_BAD_REQUEST
  return [{"redmine_status_response": response_crud[0]}, response_crud[1]]

@app.post("/configuracoes/paginasDeDados/perfil/", status_code=201, dependencies=[Depends(JWTBearer())])
async def create_paginas_de_dados(paginas_de_dados: bases_models.Pagina_de_dados, response: Response, Authorization: Union [str, None] = Header(default=None)):
  token_list = Authorization.split(" ")
  token = token_list[1]
  user_login_decoded = auth_class.verify_and_decode_jwt(token)
  paginas_de_dados_dict = paginas_de_dados.dict()
  response_crud = crud_class.create_paginas_de_dados_BD(login=user_login_decoded["usuario"],quantas_paginas=paginas_de_dados_dict["quantas_paginas"])
  if response_crud[0] != 201:
    response.status_code = status.HTTP_400_BAD_REQUEST
  return [{"redmine_status_response": response_crud[0]}, response_crud[1]]

#update
@app.put("/configuracoes/paginasDeDados/perfil/", status_code=200, dependencies=[Depends(JWTBearer())])
async def update_pagina_de_dados(paginas_de_dados: bases_models.Pagina_de_dados, response: Response, Authorization: Union [str, None] = Header(default=None)):
  token_list = Authorization.split(" ")
  token = token_list[1]
  user_login_decoded = auth_class.verify_and_decode_jwt(token)
  paginas_de_dados_dict = paginas_de_dados.dict()
  response_crud = crud_class.update_paginas_de_dados_BD(login=user_login_decoded["usuario"],quantas_paginas=paginas_de_dados_dict["quantas_paginas"])
  if response_crud[0] != 200:
    response.status_code = status.HTTP_404_NOT_FOUND
    response_crud = crud_class.create_paginas_de_dados_BD(login=user_login_decoded["usuario"],quantas_paginas=paginas_de_dados_dict["quantas_paginas"])
    if response_crud[0] != 201:
      response.status_code = status.HTTP_400_BAD_REQUEST
  return [{"redmine_status_response": response_crud [0]}, response_crud[1]]

#delete
@app.delete("/configuracoes/usuariosFabrica/{usuario_id}", status_code=200, dependencies=[Depends(JWTBearer())])
async def delete_usuarios_fabrica(usuario_id: str, response: Response ):
  response_crud = crud_class.delete_usuarios_fabrica_BD(id=usuario_id)
  if response_crud[0] != 200:
    response.status_code = status.HTTP_404_NOT_FOUND
  return [{"redmine_status_response": response_crud [0]}, response_crud[1]]

@app.delete("/configuracoes/feriadosEDatas/{dia}", status_code=200, dependencies=[Depends(JWTBearer())])
async def delete_feriados_e_datas(dia: str, response: Response ):
  response_crud = crud_class.delete_feriados_e_datas_DB(dia=dia)
  if response_crud[0] != 200:
    response.status_code = status.HTTP_404_NOT_FOUND
  return [{"redmine_status_response": response_crud [0]}, response_crud[1]]

#read by id
@app.get("/configuracoes/usuariosFabrica/{usuario_id}", status_code=200, dependencies=[Depends(JWTBearer())])
async def read_usuarios_fabrica_by_id(usuario_id: str, response: Response ):
  response_crud = crud_class.read_usuarios_fabrica_BD_by_id(id=usuario_id)
  if response_crud[0] != 200:
    response.status_code = status.HTTP_404_NOT_FOUND
  return [{"redmine_status_response": response_crud[0]}, response_crud[1]] 

@app.get("/configuracoes/feriadosEDatas/{dia}", status_code=200, dependencies=[Depends(JWTBearer())])
async def read_feriados_e_datas_by_id(dia: str, response: Response ):
  response_crud = crud_class.read_feriados_e_datas_DB_by_id(dia=dia)
  if response_crud[0] != 200:
    response.status_code = status.HTTP_404_NOT_FOUND
  return [{"redmine_status_response": response_crud[0]}, response_crud[1]] 

@app.get("/configuracoes/paginasDeDados/perfil/", status_code=200, dependencies=[Depends(JWTBearer())])
async def read_paginas_de_dados_by_id(response: Response, Authorization: Union [str, None] = Header(default=None)):
  token_list = Authorization.split(" ")
  token = token_list[1]
  user_login_decoded = auth_class.verify_and_decode_jwt(token)
  response_crud = crud_class.read_paginas_de_dados_BD_by_id(login=user_login_decoded["usuario"])
  if response_crud[0] != 200:
    response.status_code = status.HTTP_404_NOT_FOUND
  return [{"redmine_status_response": response_crud[0]}, response_crud[1]] 

#read all
@app.get("/configuracoes/usuariosFabrica/", status_code=200, dependencies=[Depends(JWTBearer())])
async def read_usuarios_fabrica_all(response: Response):
  response_crud = crud_class.read_usuarios_fabrica_BD_all()
  if response_crud[0] != 200:
    response.status_code = status.HTTP_404_NOT_FOUND
  return [{"redmine_status_response": response_crud[0]}, response_crud[1]] 

@app.get("/configuracoes/feriadosEDatas/", status_code=200, dependencies=[Depends(JWTBearer())])
async def read_feriados_e_datas_all(response: Response ):
  response_crud = crud_class.read_feriados_e_datas_DB_all()
  if response_crud[0] != 200:
    response.status_code = status.HTTP_404_NOT_FOUND
  return [{"redmine_status_response": response_crud[0]}, response_crud[1]] 

@app.get("/configuracoes/paginasDeDados/", status_code=200, dependencies=[Depends(JWTBearer())])
async def read_paginas_de_dados_all(response: Response ):
  response_crud = crud_class.read_paginas_de_dados_BD_all()
  if response_crud[0] != 200:
    response.status_code = status.HTTP_404_NOT_FOUND
  return [{"redmine_status_response": response_crud[0]}, response_crud[1]] 

@app.get("/configuracoes/allRedmineUsers/", status_code=200, dependencies=[Depends(JWTBearer())])
async def read_all_readmine_users(response: Response , Authorization: Union [str, None] = Header(default=None)):
  token_list = Authorization.split(" ")
  token = token_list[1]
  try:
    response_crud = crud_class.read_all_users_readmine(jwt=token)
    if response_crud[0] != 200:
      response.status_code = status.HTTP_404_NOT_FOUND
    return [{"redmine_status_response": response_crud[0]}, response_crud[1]] 
  except:
    raise HTTPException(status_code=401, detail="Redmine Authentication problem")

@app.post("/extratorSlaMensal/", status_code=200, dependencies=[Depends(JWTBearer())])
async def extract_Month_Sla(extract_body: bases_models.Extract_body, response: Response, Authorization: Union [str, None] = Header(default=None)):
  token_list = Authorization.split(" ")
  token = token_list[1]

  user_login_decoded = auth_class.verify_and_decode_jwt(token)

  params_formated = Params(
    crud_class.read_usuarios_fabrica_BD_all(), 
    crud_class.read_feriados_e_datas_DB_all(),
    crud_class.read_paginas_de_dados_BD_by_id(login=user_login_decoded["usuario"]),
    token
  )
    
  if not params_formated.validar_todas_entradas_do_banco():
    response.status_code = status.HTTP_424_FAILED_DEPENDENCY
    return [{"Problema com a chamada de dados do banco de dados": 424}]

  #num_int_randomico = random.randint(0, 10000)

  dirname = os.path.dirname(__file__)
  #filename = os.path.join(dirname,f"temp\\{params_formated.user_login_out()[0]}-{num_int_randomico}.csv")
  filename = os.path.join(dirname,f"temp\\{params_formated.user_login_out()[0]}.csv")

  extract_body_dict = extract_body.dict()

  sla_month_extractor = Extractor(
    usuarios_fabrica=params_formated.usuarios_fabrica_lista_out(),
    feriados=params_formated.feriados_lista_out(),
    paginas=params_formated.quantidade_de_paginas_out(),
    mes=extract_body_dict["mes"],
    ano=extract_body_dict["ano"],
    user_login=params_formated.user_login_out(),
    file_name=filename,
    off_set=extract_body_dict["off_set"]
    )
  
  response_executer = sla_month_extractor.execute()

  if response_executer[0] != 200:
    response.status_code = status.HTTP_424_FAILED_DEPENDENCY
  return [{"Sla_month_extractor_executer": response_executer[0]}, response_executer[1]] 
   

@app.get("/extratorSlaMensal/pegarDados", status_code=200, dependencies=[Depends(JWTBearer())])
async def extract_Month_Sla_pegar_dados(extract_body: bases_models.Extract_body, response: Response, Authorization: Union [str, None] = Header(default=None)):
  token_list = Authorization.split(" ")
  token = token_list[1]

  user_login_decoded = auth_class.verify_and_decode_jwt(token)

  params_formated = Params(
    crud_class.read_usuarios_fabrica_BD_all(), 
    crud_class.read_feriados_e_datas_DB_all(),
    crud_class.read_paginas_de_dados_BD_by_id(login=user_login_decoded["usuario"]),
    token
  )
    
  if not params_formated.validar_todas_entradas_do_banco():
    response.status_code = status.HTTP_424_FAILED_DEPENDENCY
    return [{"Problema com a chamada de dados do banco de dados": 424}]

  #num_int_randomico = random.randint(0, 10000)

  dirname = os.path.dirname(__file__)
  #filename = os.path.join(dirname,f"temp\\{params_formated.user_login_out()[0]}-{num_int_randomico}.csv")
  filename = os.path.join(dirname,f"temp\\{params_formated.user_login_out()[0]}.csv")

  extract_body_dict = extract_body.dict()

  sla_month_extractor = Extractor(
    usuarios_fabrica=params_formated.usuarios_fabrica_lista_out(),
    feriados=params_formated.feriados_lista_out(),
    paginas=params_formated.quantidade_de_paginas_out(),
    mes=extract_body_dict["mes"],
    ano=extract_body_dict["ano"],
    user_login=params_formated.user_login_out(),
    file_name=filename,
    off_set=extract_body["off_set"]
    )
  
  response_executer = sla_month_extractor.execute()

  if response_executer[0] != 200:
    response.status_code = status.HTTP_424_FAILED_DEPENDENCY
  return [{"Sla_month_extractor_executer": response_executer[0]}, response_executer[1]] 