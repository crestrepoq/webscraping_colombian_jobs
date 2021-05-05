import requests
from bs4 import BeautifulSoup
import re
from re import search
import numpy as np
import pandas as pd
import json

#url = 'https://www.linkedin.com/jobs/search/?geoId=100876405&location=Colombia'

#Url de las vacantes de la ultima semana ordenada por fecha de publicacion mas reciente
#url = 'https://www.linkedin.com/jobs/search/?geoId=100876405&location=Colombia&f_TPR=r604800&sortBy=DD&position=1&pageNum=0'
url = 'https://www.linkedin.com/jobs/search/?f_TPR=r604800&geoId=100876405&location=Colombia&sortBy=DD'
######'https://www.linkedin.com/jobs/search/?f_TPR=r604800&geoId=100876405&location=Colombia&sortBy=DD&start=25'
#Obtener url y parsearla jajaja
def parser_url(url):
    url = requests.get(url)
    soup = BeautifulSoup(url.content, 'html.parser')
    split_html = list(soup.children)
    return split_html[1]

#Obtener la lista de urls correspondientes a cada trabajo en una pagina
def url_jobs(url_parser):
    urls_jobs = list()
    for link in url_parser.find_all(class_="result-card__full-card-link"):
    #for link in jobs.find_all(class_="result-card__full-card-link"):
        link_job = link.get('href')
        urls_jobs.append(link_job)
    return urls_jobs

def get_urls_jobs(url):
    list_urls = list()
    count = 0
    times = 0
    while times <= 5:
        url_search = url + '&start=' + str(count)
        list_urls.append(url_search)
        count = count + 25
        times = times + 1

    return list_urls


def list_urls_jobs(list_urls_searchs):
    jobs_urls = list()
    for i in range(len(list_urls_searchs)):
        link_parser = parser_url(list_urls_searchs[i])
        links_jobs = url_jobs(link_parser)
        for i in range(len(links_jobs)):
            jobs_urls.append(links_jobs[i])
    
    return jobs_urls

jobs = get_urls_jobs(url)
jobs_urls = list_urls_jobs(jobs)

cargos = []
empresas = []
ubicaciones = []
ciudades = []
paises = []
fechas = []
sectores = []
experiencia = []
tipos_empleo = []
descripciones = []
ids_vacantes = []
skills = []
num_solicitudes = []
link_vacante = []

for i in range(len(jobs_urls)):
    '''
    <script type="application/ld+json">
    {"@context":"http://schema.org",
    "@type":"JobPosting",
    "datePosted":"2021-04-27T16:48:22.000Z",
    "description":"Trabajamos de la mano con el equipo comercial de importante entidad bancaria con más de 60 años en el mercado. Actualmente nos encontramos en búsqueda de nuevos miembros para el equipo administrativo. Si eres técnico o tecnólogo en carreras administrativas, tienes manejo intermedio de excel y cuentas con experiencia mínima de 6 meses como apoyo operativo o auxiliar administrativo de sedes bancarias, te invitamos a aplicar a esta oferta.Horario: L-V 8:00 am a 6:00 pmSalario: SMLV** Se requiere disponibilidad inmediata**",
    "employmentType":"FULL_TIME",
    "experienceRequirements":"Sin experiencia",
    "hiringOrganization":{"@type":"Organization","name":"Gobernación de Santander","sameAs":"https://co.linkedin.com/company/gobernacionsantander",
    "logo":"https://media-exp1.licdn.com/dms/image/C560BAQHLOzIzR_tqLg/company-logo_200_200/0/1519883317393?e=1628121600&v=beta&t=LH4FmBmIe05CI6qoydG7OEYN6hkBdw_rNMb5QHKejRc"},
    "identifier":{"@type":"PropertyValue","name":"Gobernación de Santander","value":"45-TRAUDX878834Y1"}
    ,"image":"https://media-exp1.licdn.com/dms/image/C560BAQHLOzIzR_tqLg/company-logo_100_100/0/1519883317393?e=1628121600&v=beta&t=_rjv4o6O_JCqwNfE2MhWKAsw0MIy6S3nqJKegwdDECQ",
    "industry":"Administración gubernamental",
    "jobLocation":{"@type":"Place","address":{"@type":"PostalAddress","streetAddress":null,"addressLocality":"Nariño","addressRegion":null,"postalCode":"252837","addressCountry":"CO"}},
    "skills":"",
    "title":"Auxiliar administrativo","validThrough":"2021-05-27T16:48:39.000Z"}</script>
    '''
    url = jobs_urls[i]
    job = parser_url(url)
    
    #Extraer los nombres de los cargos o vacantes
    cargo = (json.loads(job.find(type="application/ld+json").text)).get('title')
    cargos.append(cargo)
    
    #Extraer la empresa de cada vacate
    empresa = (json.loads(job.find(type="application/ld+json").text)).get('hiringOrganization').get('name')
    empresas.append(empresa)

    #Extraer la ubicacion completa de cada vacante
    ubicacion = job.find(class_="topcard__flavor topcard__flavor--bullet").text
    ubicaciones.append(ubicacion)

    #Extraer la ciudad y el pais de cada vacante
    ciudad = (json.loads(job.find(type="application/ld+json").text)).get('jobLocation').get('address').get('addressLocality')
    ciudades.append(ciudad)
    pais = (json.loads(job.find(type="application/ld+json").text)).get('jobLocation').get('address').get('addressCountry')
    paises.append(pais)

    #Extraer fecha de publicacion de cada vacante
    #fecha = prueba.find(class_="topcard__flavor--metadata posted-time-ago__text").text
    fecha = (json.loads(job.find(type="application/ld+json").text)).get('datePosted')
    fechas.append(fecha)

    #Extraer sectores de cada vacante
    sector = (json.loads(job.find(type="application/ld+json").text)).get('industry')
    sectores.append(sector)

    #Extraer nivel de experiencia de cada vacante
    experience = (json.loads(job.find(type="application/ld+json").text)).get('experienceRequirements')
    experiencia.append(experience)

    #Extraer el tipo de empleo de cada vacante
    tipo_empleo = (json.loads(job.find(type="application/ld+json").text)).get('employmentType')
    tipos_empleo.append(tipo_empleo)

    #Extraer descripciones de cada vacante
    descripcion = (json.loads(job.find(type="application/ld+json").text)).get('description')
    descripcion1 = BeautifulSoup(descripcion, "lxml").text
    descripciones.append(descripcion1)

    #Extraer los ids de cada vacante
    id_vacante = (json.loads(job.find(type="application/ld+json").text)).get('identifier').get('value')
    ids_vacantes.append(id_vacante)

    #Extraer las skills de cada vacante
    skill = (json.loads(job.find(type="application/ld+json").text)).get('identifier').get('skills')
    skills.append(skill)

    #Extraer el numero de solicitudes de cada vacante sin el texto adicional
    #solicitudes = re.findall(r'\b\d+\b',job.find(class_="topcard__flavor--metadata topcard__flavor--bullet num-applicants__caption").text)[0]
    solicitudes = job.find(class_="topcard__flavor--metadata topcard__flavor--bullet num-applicants__caption")
    num_solicitudes.append(solicitudes)

    link_vacante.append(url)

print(cargos)

vacantes = pd.DataFrame({'Id_vacante':ids_vacantes,
                        'Cargo':cargos,
                        'Descripcion':descripciones,
                        'Habilidades':skills,
                        'Nivel experiencia':experiencia,
                        'Tipo empleo':tipos_empleo,
                        '# Solicitudes':num_solicitudes,
                        'Empresa':empresas,
                        'Sector':sectores,
                        'Fecha publicacion':fechas,
                        'Ubicacion':ubicaciones,
                        'Ciudad':ciudades,
                        'Pais':paises,
                        'url_vacante':link_vacante})

print(vacantes)
vacantes.to_excel('vacantes.xlsx',encoding='utf8',index=False)


# prueba = parser_url(jobs_urls[1])
# #cargo = prueba.find(class_="topcard__title").text
# cargo = (json.loads(prueba.find(type="application/ld+json").text)).get('title')
# #empresa = prueba.find(class_="topcard__org-name-link").text
# empresa = (json.loads(prueba.find(type="application/ld+json").text)).get('hiringOrganization').get('name')
# ubicacion = prueba.find(class_="topcard__flavor topcard__flavor--bullet").text
# ciudad = (json.loads(prueba.find(type="application/ld+json").text)).get('jobLocation').get('address').get('addressLocality')
# pais = (json.loads(prueba.find(type="application/ld+json").text)).get('jobLocation').get('address').get('addressCountry')
# #fecha = prueba.find(class_="topcard__flavor--metadata posted-time-ago__text").text
# fecha = (json.loads(prueba.find(type="application/ld+json").text)).get('datePosted')
# sector = (json.loads(prueba.find(type="application/ld+json").text)).get('industry')
# experience = (json.loads(prueba.find(type="application/ld+json").text)).get('experienceRequirements')
# tipo_empleo = (json.loads(prueba.find(type="application/ld+json").text)).get('employmentType')
# descripcion = (json.loads(prueba.find(type="application/ld+json").text)).get('description')
# id_vacante = (json.loads(prueba.find(type="application/ld+json").text)).get('identifier').get('value')
# skills = (json.loads(prueba.find(type="application/ld+json").text)).get('identifier').get('skills')
# #Me trae solo el numero de solicitudes sin texto
# solicitudes = re.findall(r'\b\d+\b',prueba.find(class_="topcard__flavor--metadata topcard__flavor--bullet num-applicants__caption").text)[0]
#re.findall(r'\b\d+\b', 'he33llo 42 I\'m a 32 string 30')
#class="topcard__flavor--metadata topcard__flavor--bullet num-applicants__caption"
# print("id_vacante:",id_vacante)
# print("Cargo:",cargo)
# print("Nivel experiencia:",experience)
# print("Tipo empleo:",tipo_empleo)
# print("Descripcion cargo:",descripcion)
# print("# Solicitudes:",solicitudes)
# print("Empresa:",empresa)
# print("Ubicacion:",ubicacion)
# print("Ciudad:",ciudad)
# print("Pais:",pais)
# print("Fecha publicacion:",fecha)
# print("Sector",sector)


'''
<script type="application/ld+json">
{"@context":"http://schema.org",
"@type":"JobPosting",
"datePosted":"2021-04-27T16:48:22.000Z",
"description":"Trabajamos de la mano con el equipo comercial de importante entidad bancaria con más de 60 años en el mercado. Actualmente nos encontramos en búsqueda de nuevos miembros para el equipo administrativo. Si eres técnico o tecnólogo en carreras administrativas, tienes manejo intermedio de excel y cuentas con experiencia mínima de 6 meses como apoyo operativo o auxiliar administrativo de sedes bancarias, te invitamos a aplicar a esta oferta.Horario: L-V 8:00 am a 6:00 pmSalario: SMLV** Se requiere disponibilidad inmediata**",
"employmentType":"FULL_TIME",
"experienceRequirements":"Sin experiencia",
"hiringOrganization":{"@type":"Organization","name":"Gobernación de Santander","sameAs":"https://co.linkedin.com/company/gobernacionsantander",
"logo":"https://media-exp1.licdn.com/dms/image/C560BAQHLOzIzR_tqLg/company-logo_200_200/0/1519883317393?e=1628121600&v=beta&t=LH4FmBmIe05CI6qoydG7OEYN6hkBdw_rNMb5QHKejRc"},
"identifier":{"@type":"PropertyValue","name":"Gobernación de Santander","value":"45-TRAUDX878834Y1"}
,"image":"https://media-exp1.licdn.com/dms/image/C560BAQHLOzIzR_tqLg/company-logo_100_100/0/1519883317393?e=1628121600&v=beta&t=_rjv4o6O_JCqwNfE2MhWKAsw0MIy6S3nqJKegwdDECQ",
"industry":"Administración gubernamental",
"jobLocation":{"@type":"Place","address":{"@type":"PostalAddress","streetAddress":null,"addressLocality":"Nariño","addressRegion":null,"postalCode":"252837","addressCountry":"CO"}},
"skills":"",
"title":"Auxiliar administrativo","validThrough":"2021-05-27T16:48:39.000Z"}</script>
'''


#class="topcard__flavor--metadata posted-time-ago__text"





# conteo = 0
# for i in jobs_urls:
#     conteo = conteo + 1

# print(conteo)

# vacantes = pd.DataFrame({'jobs':jobs_urls})
# print(vacantes)
# vacantes.to_excel('vacantes.xlsx',encoding='utf8',index=False)


# f= open("prueba.txt","w+")
# f.write(str(prueba))
# f.close()