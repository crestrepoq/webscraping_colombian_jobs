import requests
from bs4 import BeautifulSoup
import re
from re import search
import numpy as np
import pandas as pd
import json
import html2text

def parser_html(html_file):
    '''
    Obtener url y parsearla
    input y outputs
    '''
    with open(html_file, 'r') as f:
        contents = f.read()

    soup = BeautifulSoup(contents, 'lxml')
    split_html = list(soup.children)
    return split_html[0]

def parser_url(url):
    '''
    Obtener url y parsearla
    input y outputs
    '''
    url = requests.get(url)
    soup = BeautifulSoup(url.content, 'html.parser')
    split_html = list(soup.children)
    return split_html[1]

#Obtener la lista de urls correspondientes a cada trabajo en una pagina
def url_jobs(url_parser):
    urls_jobs = list()
    for link in url_parser.find_all(class_="base-card__full-link"):
    #for link in jobs.find_all(class_="result-card__full-card-link"):
        link_job = link.get('href')
        urls_jobs.append(link_job)
    return urls_jobs


#Para un solo enlace de vacates
def list_url_jobs(url_job):
    jobs_urls = list()
    link_parser = parser_url(url_job)
    links_jobs = url_jobs(link_parser)
    for i in range(len(links_jobs)):
        jobs_urls.append(links_jobs[i])
        print(len(jobs_urls))
    return jobs_urls

# Para varios enlaces de vacates
def list_urls_jobs(list_urls_searchs):
    jobs_urls = list()
    for i in range(len(list_urls_searchs)):
        link_parser = parser_url(list_urls_searchs[i])
        links_jobs = url_jobs(link_parser)
        for i in range(len(links_jobs)):
            jobs_urls.append(links_jobs[i])
    
    return jobs_urls

def cargos(list_links_jobs):
    cargos = []
    for i in range(len(list_links_jobs)):
        url = list_links_jobs[i]
        job = parser_url(url)
        #Extraer los nombres de los cargos o vacantes
        try:
            cargo = (json.loads(job.find(type="application/ld+json").text)).get('title')
            #cargo = (json.loads(job.findall(type="application/ld+json").text)).get('title')
            print(cargo)
            cargos.append(cargo)
        except:
            cargos.append('')
            continue
    return cargos

def descripciones(list_links_jobs):
    descripciones = []
    for i in range(len(list_links_jobs)):
        url = list_links_jobs[i]
        job = parser_url(url)
        #Extraer los nombres de los cargos o vacantes
        try:
            descripcion = (json.loads(job.find(type="application/ld+json").text)).get('description')
            descripcion1 = BeautifulSoup(descripcion, "lxml").text
            descripciones.append(descripcion1)
            print(descripcion1)
        except: 
            descripciones.append('')
            continue
    return descripciones

def df_vacantes(lst_cargos,lst_descripciones):
    vacantes = pd.DataFrame.from_dict({#'Id_vacante':ids_vacantes},
                            'Cargo':lst_cargos,
                            'Descripcion':lst_descripciones
                            #'Habilidades':skills,
                            #'Nivel experiencia':experiencia,
                            #'Tipo empleo':tipos_empleo,
                            #'# Solicitudes':num_solicitudes,
                            #'Empresa':empresas,
                            #'Sector':sectores,
                            #'Fecha publicacion':fechas,
                            #'Ubicacion':ubicaciones,
                            #'Ciudad':ciudades,
                            #'Pais':paises,
                            #'url_vacante':link_vacante
                            })
    return vacantes

#url = open('jobs.html')

#link = requests.get(url)

#html = parser_html('jobs.html')
html = parser_html('prueba.html')
list_jobs = url_jobs(html)
roles = cargos(list_jobs)
desc_roles = descripciones(list_jobs)
set_vacantes = df_vacantes(roles,desc_roles)
set_vacantes.to_excel('vacantes.xlsx',encoding='utf8',index=False)
print(len(roles))

# Muchas solicitudes, mirar enlace
# https://stackoverflow.com/questions/23013220/max-retries-exceeded-with-url-in-requests

#html_vacante_especifica = str(parser_url(list_jobs[2]))
#print(html_vacante_especifica)
#h = html2text.HTML2Text()
#tml_vacante_especifica = h.handle(html_vacante_especifica)


#file = open('html_vacante_especifica.txt', 'w')
#file.write(html_vacante_especifica)
#file.close()
#print(len(vacantes))

#return split_html[1]




#jobs = parser_url(url)
#jobs_urls = url_jobs(jobs)
#vacantes = cargos(jobs_urls)

#print(jobs_urls)
#print(len(jobs_urls))
# def elements_job(list_links_jobs):




#     cargos = []
#     empresas = []
#     ubicaciones = []
#     ciudades = []
#     paises = []
#     fechas = []
#     sectores = []
#     experiencia = []
#     tipos_empleo = []
#     descripciones = []
#     ids_vacantes = []
#     skills = []
#     num_solicitudes = []
#     link_vacante = []

#     for i in range(len(list_links_jobs)):
#         '''
#         <script type="application/ld+json">
#         {"@context":"http://schema.org",
#         "@type":"JobPosting",
#         "datePosted":"2021-04-27T16:48:22.000Z",
#         "description":"Trabajamos de la mano con el equipo comercial de importante entidad bancaria con más de 60 años en el mercado. Actualmente nos encontramos en búsqueda de nuevos miembros para el equipo administrativo. Si eres técnico o tecnólogo en carreras administrativas, tienes manejo intermedio de excel y cuentas con experiencia mínima de 6 meses como apoyo operativo o auxiliar administrativo de sedes bancarias, te invitamos a aplicar a esta oferta.Horario: L-V 8:00 am a 6:00 pmSalario: SMLV** Se requiere disponibilidad inmediata**",
#         "employmentType":"FULL_TIME",
#         "experienceRequirements":"Sin experiencia",
#         "hiringOrganization":{"@type":"Organization","name":"Gobernación de Santander","sameAs":"https://co.linkedin.com/company/gobernacionsantander",
#         "logo":"https://media-exp1.licdn.com/dms/image/C560BAQHLOzIzR_tqLg/company-logo_200_200/0/1519883317393?e=1628121600&v=beta&t=LH4FmBmIe05CI6qoydG7OEYN6hkBdw_rNMb5QHKejRc"},
#         "identifier":{"@type":"PropertyValue","name":"Gobernación de Santander","value":"45-TRAUDX878834Y1"}
#         ,"image":"https://media-exp1.licdn.com/dms/image/C560BAQHLOzIzR_tqLg/company-logo_100_100/0/1519883317393?e=1628121600&v=beta&t=_rjv4o6O_JCqwNfE2MhWKAsw0MIy6S3nqJKegwdDECQ",
#         "industry":"Administración gubernamental",
#         "jobLocation":{"@type":"Place","address":{"@type":"PostalAddress","streetAddress":null,"addressLocality":"Nariño","addressRegion":null,"postalCode":"252837","addressCountry":"CO"}},
#         "skills":"",
#         "title":"Auxiliar administrativo","validThrough":"2021-05-27T16:48:39.000Z"}</script>
#         '''
#         url = list_links_jobs[i]
#         job = parser_url(url)
        
#         #Extraer los nombres de los cargos o vacantes
#         cargo = (json.loads(job.find(type="application/ld+json").text)).get('title')
#         cargos.append(cargo)
        
#         #Extraer la empresa de cada vacate
#         empresa = (json.loads(job.find(type="application/ld+json").text)).get('hiringOrganization').get('name')
#         empresas.append(empresa)

#         #Extraer la ubicacion completa de cada vacante
#         ubicacion = job.find(class_="topcard__flavor topcard__flavor--bullet").text
#         ubicaciones.append(ubicacion)

#         #Extraer la ciudad y el pais de cada vacante
#         ciudad = (json.loads(job.find(type="application/ld+json").text)).get('jobLocation').get('address').get('addressLocality')
#         ciudades.append(ciudad)
#         pais = (json.loads(job.find(type="application/ld+json").text)).get('jobLocation').get('address').get('addressCountry')
#         paises.append(pais)

#         #Extraer fecha de publicacion de cada vacante
#         #fecha = prueba.find(class_="topcard__flavor--metadata posted-time-ago__text").text
#         fecha = (json.loads(job.find(type="application/ld+json").text)).get('datePosted')
#         fechas.append(fecha)

#         #Extraer sectores de cada vacante
#         sector = (json.loads(job.find(type="application/ld+json").text)).get('industry')
#         sectores.append(sector)

#         #Extraer nivel de experiencia de cada vacante
#         experience = (json.loads(job.find(type="application/ld+json").text)).get('experienceRequirements')
#         experiencia.append(experience)

#         #Extraer el tipo de empleo de cada vacante
#         tipo_empleo = (json.loads(job.find(type="application/ld+json").text)).get('employmentType')
#         tipos_empleo.append(tipo_empleo)

#         #Extraer descripciones de cada vacante
#         descripcion = (json.loads(job.find(type="application/ld+json").text)).get('description')
#         descripcion1 = BeautifulSoup(descripcion, "lxml").text
#         descripciones.append(descripcion1)

#         #Extraer los ids de cada vacante
#         id_vacante = (json.loads(job.find(type="application/ld+json").text)).get('identifier').get('value')
#         ids_vacantes.append(id_vacante)

#         #Extraer las skills de cada vacante
#         skill = (json.loads(job.find(type="application/ld+json").text)).get('identifier').get('skills')
#         skills.append(skill)

#         #Extraer el numero de solicitudes de cada vacante sin el texto adicional
#         #solicitudes = re.findall(r'\b\d+\b',job.find(class_="topcard__flavor--metadata topcard__flavor--bullet num-applicants__caption").text)[0]
#         solicitudes = job.find(class_="topcard__flavor--metadata topcard__flavor--bullet num-applicants__caption")
#         num_solicitudes.append(solicitudes)

#         link_vacante.append(url)

#     print(cargos)

#     vacantes = pd.DataFrame({'Id_vacante':ids_vacantes,
#                             'Cargo':cargos,
#                             'Descripcion':descripciones,
#                             'Habilidades':skills,
#                             'Nivel experiencia':experiencia,
#                             'Tipo empleo':tipos_empleo,
#                             '# Solicitudes':num_solicitudes,
#                             'Empresa':empresas,
#                             'Sector':sectores,
#                             'Fecha publicacion':fechas,
#                             'Ubicacion':ubicaciones,
#                             'Ciudad':ciudades,
#                             'Pais':paises,
#                             'url_vacante':link_vacante})

#     return vacantes

# jobs = get_urls_jobs(url)
# jobs_urls = list_urls_jobs(jobs)
# vacantes = elements_job(jobs_urls)

# print(vacantes)
# vacantes.to_excel('vacantes.xlsx',encoding='utf8',index=False)

