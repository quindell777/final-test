from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Rota principal que renderiza a página
@app.route('/')
def index():
    return render_template('index.html')

# Rota para obter o endereço a partir das coordenadas
@app.route('/get_address', methods=['POST'])
def get_address():
    data = request.get_json()
    lat = data.get('latitude')
    lon = data.get('longitude')

    if not lat or not lon:
        print('Erro: Coordenadas não fornecidas.')
        return jsonify({'error': 'Coordenadas não fornecidas.'}), 400

    try:
        lat = float(lat)
        lon = float(lon)
    except ValueError:
        print('Erro: Coordenadas inválidas.')
        return jsonify({'error': 'Coordenadas inválidas.'}), 400

    try:
        url = 'https://nominatim.openstreetmap.org/reverse'
        params = {
            'format': 'jsonv2',
            'lat': lat,
            'lon': lon,
            'zoom': 18,
            'addressdetails': 1
        }
        headers = {
            'User-Agent': 'GeolocationApp/1.0 riquelmem077@gmail.com'  # Substitua pelo seu email real
        }
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            address = data.get('display_name', 'Endereço não encontrado.')
            print('Endereço obtido:', address)
            return jsonify({'address': address})
        else:
            print(f'Erro ao obter o endereço: {response.status_code}')
            return jsonify({'error': f'Erro ao obter o endereço: {response.status_code}'}), response.status_code
    except Exception as e:
        print('Erro ao processar a requisição:', str(e))
        return jsonify({'error': f'Erro ao processar a requisição: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
