#PINGULAND - Ibero Puebla
#Hackathon TalentLand 2025 - Track SaludDigna
# API de Imágenes Médicas DICOM

## Descripción
Este proyecto es una API RESTful desarrollada en Flask que sirve como intermediario entre aplicaciones cliente y un servidor Orthanc (servidor PACS para imágenes médicas DICOM). La API proporciona endpoints para acceder, visualizar y gestionar estudios médicos en formato DICOM, facilitando la integración con aplicaciones web de visualización médica.

## Características principales
- Recuperación y listado de estudios médicos DICOM
- Obtención de imágenes de estudios específicos con ordenamiento correcto por serie e instancia
- Renderizado de imágenes DICOM en formato JPEG con calidad ajustable
- Acceso a los metadatos de estudios para obtener información clínica relevante
- Soporte para diferentes modalidades: Tomografía, Rayos X, Mastografía y Estudios generales

## Estructura del proyecto
```
├── app.py                     # Aplicación principal de Flask
├── Procfile                   # Configuración para despliegue en plataformas como Heroku
├── requirements.txt           # Dependencias del proyecto
├── Estudios/                  # Directorio con estudios médicos generales
├── Mastografias/              # Directorio con estudios de mastografía
├── Rayos X/                   # Directorio con estudios de rayos X
└── Tomografia/                # Directorio con estudios de tomografía
```

## Requisitos
- Python 3.8+
- Flask
- Flask-CORS
- Requests
- PyDICOM
- numpy
- pillow
- gunicorn (para producción)

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/tu-usuario/backend-imagenes-medicas.git
cd backend-imagenes-medicas
```

2. Crear y activar un entorno virtual:
```bash
python -m venv venv
# En Windows
venv\Scripts\activate
# En macOS/Linux
source venv/bin/activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar la URL del servidor Orthanc:
Editar la variable `ORTHANC_URL` en `app.py` para que apunte a tu servidor Orthanc.

## Uso

### Iniciar el servidor en desarrollo:
```bash
python app.py
```

### Endpoints disponibles:

#### Obtener todos los estudios
```
GET /api/studies
```
Parámetros opcionales:
- `expand=true` - Devuelve información detallada de cada estudio

#### Obtener metadatos de un estudio
```
GET /api/studies/{study_id}/metadata
```

#### Obtener imágenes de un estudio
```
GET /api/studies/{study_id}/images
```
Parámetros opcionales:
- `quality` - Calidad de imagen (1-100), por defecto 90

#### Obtener una imagen renderizada
```
GET /api/instances/{instance_id}/rendered
```
Parámetros opcionales:
- `quality` - Calidad de imagen (1-100), por defecto 90

## Despliegue
El proyecto incluye un archivo `Procfile` para facilitar el despliegue en plataformas como Heroku o Railway. Para desplegar en producción:

1. Asegúrate de tener instalado gunicorn:
```bash
pip install gunicorn
```

2. Despliega usando el Procfile incluido que configura gunicorn como servidor WSGI.

## Notas importantes
- Las imágenes se devuelven en formato JPEG con una caché configurada para 24 horas.
- La API ordena las imágenes por número de serie y número de instancia para asegurar una visualización correcta.
- Se habilita CORS para permitir solicitudes desde aplicaciones frontend.

## Licencia
[Incluir información de licencia aquí]

---
## Contacto
[Información de contacto del equipo o desarrollador]
