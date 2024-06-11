import requests,json,re,html,codecs
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim

def find_data(scripts):
    for script in scripts:
        if 'sitios.push' in script.text:
            fixed_text = codecs.decode(script.text, 'unicode_escape')
            return fixed_text

def obtener_coordenadas(direccion):
    try:
        geolocalizador = Nominatim(user_agent="app", timeout=10)
        ubicacion = geolocalizador.geocode(direccion)
        if ubicacion:
            return {'latitud': ubicacion.latitude, 'longitud': ubicacion.longitude}
        else:
            print("no encontrado: "+direccion)
            return None
    except Exception as e:
        print(e)

url = "https://beneficios.scotiabank.cl/scclubfront/categoria/platosycomida/rutagourmet"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
scripts = soup.find_all('script')
fixed_script = find_data(scripts)
matches = re.findall(r'sitios.push\((.*?)\);', fixed_script, re.DOTALL | re.MULTILINE)
cleaned_matches = [re.sub(r'[\n\r\t]', '', match) for match in matches]
sitios = [json.loads(match) for match in cleaned_matches]

for sitio in sitios:
    for key, value in sitio.items():
        if isinstance(value, str):
            sitio[key] = html.unescape(value)

data_consolidada = []

for sitio in sitios:
    lista_direcciones = sitio['direccion'].split("|")
    lista_coordenadas = []
    for direccion in lista_direcciones:
        coordenada = obtener_coordenadas(direccion)
        if coordenada:
            dict_geo_data = {
                'direccion': direccion,
                'coordenadas': coordenada
            }
            lista_coordenadas.append(dict_geo_data)
    datos = {
        'nombre': sitio['nombre'],
        'telefono': sitio['telefono'],
        'especialidad': sitio['especialidad'],
        'direcciones': lista_coordenadas
    }
    data_consolidada.append(datos)

data_map = json.dumps(data_consolidada)
with open('../app/data/food/coordinates_scotiabank.json', 'w') as archivo:
    archivo.write(data_map)
