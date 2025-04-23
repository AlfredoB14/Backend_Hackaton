from flask import Flask, jsonify, Response, request
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Habilitar CORS para permitir solicitudes desde el frontend

# Configuración de Orthanc
ORTHANC_URL = "https://orthancpinguland-production.up.railway.app/"  # Cambia esto a la URL de tu servidor Orthanc

# Función para realizar solicitudes a Orthanc
def orthanc_request(path, method="GET", data=None, params=None):
    url = f"{ORTHANC_URL}{path}"
    try:
        response = requests.request(
            method=method,
            url=url,
            json=data,
            params=params
        )
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud a Orthanc: {e}")
        return None

# Endpoint para obtener todas las URLs de imágenes renderizadas de un estudio
@app.route('/api/studies/<study_id>/images', methods=['GET'])
def get_study_images(study_id):
    try:
        # Obtener calidad deseada para las imágenes (por defecto 90)
        quality = request.args.get('quality', 90, type=int)
        
        # Obtener lista de instancias del estudio
        response = orthanc_request(f"/studies/{study_id}/instances")
        if not response:
            return jsonify({"error": "No se pudo obtener las instancias del estudio"}), 500
        
        instances = response.json()
        
        # Crear lista de URLs para renderizar cada instancia
        image_urls = []
        for instance in instances:
            instance_id = instance['ID'] if isinstance(instance, dict) else instance
            # Crear URL relativa para esta imagen
            image_url = f"https://orthancpinguland-production.up.railway.app/instances/{instance_id}/frames/0/rendered?quality={quality}"
            image_urls.append({
                "instanceId": instance_id,
                "imageUrl": image_url
            })
        
        return jsonify({
            "studyId": study_id,
            "imageCount": len(image_urls),
            "images": image_urls
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint para obtener una imagen renderizada específica
@app.route('/api/instances/<instance_id>/rendered', methods=['GET'])
def get_rendered_instance(instance_id):
    try:
        # Obtener calidad deseada para la imagen
        quality = request.args.get('quality', 90, type=int)
        
        # Obtener la imagen renderizada de Orthanc
        response = orthanc_request(f"/instances/{instance_id}/rendered", params={"quality": quality})
        if not response:
            return jsonify({"error": "No se pudo obtener la imagen"}), 500
        
        # Devolver la imagen como respuesta binaria
        return Response(
            response.content,
            mimetype="image/jpeg",
            headers={
                "Content-Disposition": f"inline; filename=instance-{instance_id}.jpg",
                "Cache-Control": "public, max-age=86400"  # Caché por 24 horas
            }
        )
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint adicional para obtener metadatos del estudio
@app.route('/api/studies/<study_id>/metadata', methods=['GET'])
def get_study_metadata(study_id):
    try:
        response = orthanc_request(f"/studies/{study_id}")
        if not response:
            return jsonify({"error": "No se pudo obtener los metadatos del estudio"}), 500
        
        # Obtener etiquetas DICOM compartidas para información adicional
        shared_tags_response = orthanc_request(f"/studies/{study_id}/shared-tags")
        shared_tags = shared_tags_response.json() if shared_tags_response else {}
        
        # Extraer información relevante
        metadata = response.json()
        metadata["SharedTags"] = shared_tags
        
        return jsonify(metadata)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint para listar todos los estudios disponibles
@app.route('/api/studies', methods=['GET'])
def get_all_studies():
    try:
        response = orthanc_request("/studies")
        if not response:
            return jsonify({"error": "No se pudo obtener la lista de estudios"}), 500
        
        studies = response.json()
        
        # Opcional: Obtener más información para cada estudio
        if request.args.get('expand', 'false').lower() == 'true':
            detailed_studies = []
            for study_id in studies:
                study_info_response = orthanc_request(f"/studies/{study_id}")
                if study_info_response:
                    detailed_studies.append(study_info_response.json())
            return jsonify(detailed_studies)
        
        return jsonify(studies)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)