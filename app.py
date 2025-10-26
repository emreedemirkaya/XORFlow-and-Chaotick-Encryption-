import hashlib
import base64
from flask import Flask, request, jsonify, render_template

# --- Çekirdek Şifreleme Mantığı ---

def _derive_chaotic_params_from_key(key: str) -> tuple[float, float]:
    """
    Verilen bir metin anahtarından deterministik olarak kaotik sistem
    parametreleri (r ve x0) türetir.
    """
    # Anahtarı SHA-256 ile hash'leyerek 32 byte'lık bir dizi elde et
    hasher = hashlib.sha256()
    hasher.update(key.encode('utf-8'))
    hashed_key = hasher.digest()

    # r (büyüme oranı) için ilk 8 byte'ı kullan
    # Kaos için r genellikle 3.57 ile 4.0 arasında olmalıdır.
    # 3.9 ile 3.9999 arasında bir değere haritalayalım.
    r_seed = int.from_bytes(hashed_key[:8], 'big')
    r = 3.9 + (r_seed / (2**64 - 1)) * 0.0999

    # x0 (başlangıç durumu) için sonraki 8 byte'ı kullan
    # x0, 0 ile 1 arasında olmalıdır (0 ve 1 hariç).
    x0_seed = int.from_bytes(hashed_key[8:16], 'big')
    x0 = (x0_seed / (2**64 - 1)) * 0.98 + 0.01  # 0.01 ile 0.99 arasında

    return r, x0

def _generate_chaotic_keystream(r: float, x0: float, length: int) -> bytes:
    """
    Lojistik Harita kullanarak belirtilen uzunlukta bir kaotik anahtar akışı üretir.
    """
    keystream = bytearray()
    x = x0
    for _ in range(length):
        # Lojistik Harita denklemi
        x = r * x * (1 - x)
        # 0-1 arasındaki ondalık sayıyı 0-255 arasındaki bir tam sayıya dönüştür
        keystream_byte = int(x * 255)
        keystream.append(keystream_byte)
    return bytes(keystream)

def _xor_bytes(data: bytes, keystream: bytes) -> bytes:
    """
    Verilen veri ile anahtar akışını XOR işlemine tabi tutar.
    """
    return bytes(a ^ b for a, b in zip(data, keystream))

# --- Uygulama Katmanı ---

def handle_encryption(text: str, key: str) -> dict:
    """Şifreleme işlemini yönetir."""
    r, x0 = _derive_chaotic_params_from_key(key)
    data_bytes = text.encode('utf-8')
    keystream = _generate_chaotic_keystream(r, x0, len(data_bytes))
    encrypted_bytes = _xor_bytes(data_bytes, keystream)
    
    # Sonucu Base64 formatında kodla
    result_base64 = base64.b64encode(encrypted_bytes).decode('utf-8')
    
    return {
        "result": result_base64,
        "keystream_sample": list(keystream[:16]) # İlk 16 byte'ı örnek olarak gönder
    }

def handle_decryption(base64_text: str, key: str) -> dict:
    """Şifre çözme işlemini yönetir."""
    try:
        encrypted_bytes = base64.b64decode(base64_text)
    except (base64.binascii.Error, ValueError):
        raise ValueError("Geçersiz Base64 formatı. Lütfen şifrelenmiş metni doğru girin.")

    r, x0 = _derive_chaotic_params_from_key(key)
    keystream = _generate_chaotic_keystream(r, x0, len(encrypted_bytes))
    decrypted_bytes = _xor_bytes(encrypted_bytes, keystream)
    
    try:
        result_text = decrypted_bytes.decode('utf-8')
    except UnicodeDecodeError:
        raise ValueError("Şifre çözme başarısız. Anahtar yanlış veya veri bozulmuş.")

    return {
        "result": result_text,
        "keystream_sample": list(keystream[:16]) # İlk 16 byte'ı örnek olarak gönder
    }

# --- Web Katmanı (Flask Rotaları) ---

app = Flask(__name__)

@app.route('/')
def index():
    """Ana sayfayı render eder."""
    return render_template('index.html')

@app.route('/cipher', methods=['POST'])
def cipher_route():
    """Şifreleme ve şifre çözme isteklerini işler."""
    try:
        data = request.get_json()
        text = data.get('text')
        key = data.get('key')
        mode = data.get('mode')

        if not text or not key:
            return jsonify({"error": "Metin ve anahtar alanları boş bırakılamaz."}), 400

        if mode == 'encrypt':
            response_data = handle_encryption(text, key)
        elif mode == 'decrypt':
            response_data = handle_decryption(text, key)
        else:
            return jsonify({"error": "Geçersiz işlem modu."}), 400
        
        return jsonify(response_data), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # Beklenmedik hatalar için genel bir hata mesajı
        return jsonify({"error": f"Beklenmedik bir sunucu hatası oluştu: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)

