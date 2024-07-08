from flask import Flask, request, jsonify
import rsa
import base64

app = Flask(__name__)

@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.json
    message = data.get('message')
    if not message:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        # Generate RSA keys
        (public_key, private_key) = rsa.newkeys(1024)
        encrypted_message = rsa.encrypt(message.encode('utf-8'), public_key)
        
        # Serialize the private key to PEM format and then encode it with base64
        private_key_pem = private_key.save_pkcs1().decode('utf-8')
        encoded_private_key = base64.b64encode(private_key_pem.encode('utf-8')).decode('utf-8')
        
        return jsonify({'encrypted_message': encrypted_message.hex(), 'key': encoded_private_key})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/decrypt', methods=['POST'])
def decrypt():
    data = request.json
    encrypted_message = data.get('encrypted_message')
    encoded_private_key = data.get('key')
    if not encrypted_message:
        return jsonify({'error': 'No encrypted message provided'}), 400
    
    try:
        encrypted_message_bytes = bytes.fromhex(encrypted_message)
        
        # Decode the private key from base64 and load it from PEM format
        private_key_pem = base64.b64decode(encoded_private_key).decode('utf-8')
        private_key = rsa.PrivateKey.load_pkcs1(private_key_pem.encode('utf-8'))
        
        decrypted_message = rsa.decrypt(encrypted_message_bytes, private_key).decode('utf-8')
        return jsonify({'decrypted_message': decrypted_message})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
