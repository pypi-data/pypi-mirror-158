# wj_common library

Exeption library for backend in Whale and Jaguar

## Description 

Esta libreria tiene como objetivo brindar al desarrollador un método para responder desde el backend cuando ocurra un error, de acuerdo al [estándar](https://whaleandjaguar.atlassian.net/wiki/spaces/~62165c0271554c0069553da0/pages/1822883841/Estandarizaci+n+de+Respuestas+en+el+Backend) propuesto en W&J.

Por otro lado se han dispuesto funcionalidades que son utiles en los diferentes micro servicios desarrollados en W&J. Esto con el fin de centralizar las funciones comunes y evitar la duplicación de código.

## Getting started
### Requirements 

- Docker
- GNU make 
- Git

Actualmente se ha construido la librería en el repositorio para paquetes de prueba python [TestPyPI](https://test.pypi.org/) por lo que se puede instalar este paquet vía pip.

### Install

```
pip3 install -i https://test.pypi.org/simple/ wj-common
```
## Usage 

La librería cuenta con dos paquetes: 

- [wj_common](docs/commons_functions/commons_functions.md): 
Aquí se encuentran las funcionalidades útiles que se pueden emplear para el desarrollo de nuevas funcionalides en los servicios ofrecidos.

- [wj_exception](docs/exceptions/exceptions.md): 
Aquí se encuentran las excepciones personalizadas para el manejo de los errores de acuerdo al [estándar](https://whaleandjaguar.atlassian.net/wiki/spaces/~62165c0271554c0069553da0/pages/1822883841/Estandarizaci+n+de+Respuestas+en+el+Backend).

Para obtener las respuestas de acuaerdo a lo planteado se deben usar ambos paquetes como se muestra en el siguiente ejemplo.

```
from wj_exception.exception.no_data import ItemNotFound
from wj_common.utils import utils

try:
    raise ItemNotFound()
except Exception as e:
    exception_resp = utils.get_response_error(exception=e)
    status = e.status

print(f"response error = {exception_resp}\nstatus = {status}")
``` 

Respuesta obtenida:

```
response error = {'error': {'code': 'itemNotFound', 'message': 'data not found','location': '<stdin> in line 2'}}
status = 404
```
## License
GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007

