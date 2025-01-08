import hashlib
import json
import hmac
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

# Hardcoded keys for HMAC signing based on the first character of the UID
keys = {
    '0': 'ef55032bcaed111c7449cb9fd6f3ccd5e2529c241c24f248e2476e00499b309b',
    '1': '1e33fcedd16e26f7a0a7ce8b981174bb555e7a4de0be9e6bfecdbc7518da2e33',
    '2': 'b82199e25dca75744992dcacfa3b3bc912c98f72fb021e3a88b832b5fa60befa',
    '3': '13a099941cccb9d8f5577488b0bf08201b5df23991fe8e0e3dc0a9938acce7ea',
    '4': '4516447f4b46ac8eff3c111f05054f154630750734f27a88eec3a72679a998df',
    '5': 'a01cfd643d81e125d35afee4985e14f3a5cb87fee81a3f9215c9292d89048152',
    '6': 'eb06b18693bacfc8b74dbd5cf29f9fce9f97678fc4a551cde75031e0d901923e',
    '7': '0df82ae6b8fa95be0fd6d50e3edcc4b7cde3c8e42a1205a715c82e2fd2805d44',
    '8': 'be95f803d250c1681af8a35db71d99d621d56e92967a956fa13a1e9336df0abd'
}
# Static conformity certificate structure
conformity_certificate_template = {   
    "device_id": "LOWEND_1",
    "domain_id": "QUBITECH",
    "integrity": "1",
    "access_control": "1"
                                   }


def hash_with_key(data, key, data_is_hex):
    """Hash the data with the provided key using HMAC-SHA256."""
    key_bytes = bytes.fromhex(key)
    if data_is_hex:
        data_bytes = bytes.fromhex(data)
    else:
        data_bytes = data.encode('utf-8')

    hmac_result = hmac.new(key_bytes,data_bytes, hashlib.sha256)
    return hmac_result.hexdigest()

@app.route('/lowenddevice_verification', methods=['POST'])
def lowenddevice_verification():
    try:
        verify_start =time.time()
        data = request.json
        nonce = data.get('nonce')
        uid = data.get('uid')

        if not nonce or not uid:
            return jsonify({'error': 'Nonce or UID missing'}), 400

        # Determine the key based on the first character of the UID
        key_index = uid[0]
        key = keys.get(key_index)

        if not key:
            return jsonify({'error': 'Invalid UID format'}), 400


        # Generate the signed nonce
        signed_nonce = hash_with_key(nonce, key, data_is_hex = True)
        verify_end =time.time()
        print("[TIMING] DEVICE VERIFICATION = ", verify_end-verify_start)

        # Respond with the signed nonce
        return jsonify({'signednonce': signed_nonce}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/lowenddevice_cc', methods=['POST'])
def lowenddevice_cc():
    try:
        cc_start =time.time()
        data = request.json
        uid = data.get('uid')

        if not uid:
            return jsonify({'error': 'UID missing'}), 400

        # Determine the key based on the first character of the UID
        key_index = uid[0]
        key = keys.get(key_index)

        if not key:
            return jsonify({'error': 'Invalid UID format'}), 400

        conformity_certificate_json = json.dumps(conformity_certificate_template)
        # Generate the conformity certificate HMAC without nonce
        conformity_certificate_hmac = hash_with_key(conformity_certificate_json, key, data_is_hex = False)

        # Format the JSON data to include conformity certificate and UID
        cc_data = {
            "cc": conformity_certificate_template,
            "evidence": {
                "signature": conformity_certificate_hmac,
                "uid": uid
            }
        }
        cc_json_bytes = json.dumps(cc_data).encode('utf-8')
        
        response_data = {
            "conformity_certificate" : cc_json_bytes.hex()
        }
        cc_end =time.time()
        print("[TIMING] CONFORMITY CERTIFICATE = ", cc_end-cc_start)

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
