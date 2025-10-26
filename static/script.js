document.addEventListener('DOMContentLoaded', () => {
    // Gerekli HTML elementlerini seç
    const textInput = document.getElementById('text-input');
    const keyInput = document.getElementById('key-input');
    const encryptBtn = document.getElementById('encrypt-btn');
    const decryptBtn = document.getElementById('decrypt-btn');
    const resultOutput = document.getElementById('result-output');
    const copyBtn = document.getElementById('copy-btn');
    const errorMessage = document.getElementById('error-message');
    
    // Keystream için özel elementler
    const keystreamContainer = document.getElementById('keystream-container');
    const keystreamOutput = document.getElementById('keystream-output');

    // Sunucuya şifreleme/çözme isteği gönderen ana fonksiyon
    const handleCipherRequest = async (mode) => {
        const text = textInput.value.trim();
        const key = keyInput.value.trim();

        // Her yeni istekte arayüzü temizle
        errorMessage.style.display = 'none';
        keystreamContainer.style.display = 'none';
        resultOutput.innerHTML = '<span class="placeholder">İşleniyor...</span>';
        copyBtn.disabled = true;

        // Girdi kontrolü
        if (!text || !key) {
            errorMessage.textContent = 'Metin ve anahtar alanları boş bırakılamaz.';
            errorMessage.style.display = 'block';
            resultOutput.innerHTML = '<span class="placeholder">Sonucunuz burada görünecektir.</span>';
            return;
        }

        try {
            // Sunucuya POST isteği gönder
            const response = await fetch('/cipher', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text, key, mode }),
            });

            // Sunucudan gelen yanıtı JSON olarak al
            const data = await response.json();

            // Yanıt başarılı ise (HTTP 200 OK)
            if (response.ok) {
                resultOutput.textContent = data.result;
                copyBtn.disabled = false;

                // --- KAOTİK ANAHTAR AKIŞINI GÖSTERME BÖLÜMÜ ---
                // Sunucudan 'keystream_sample' verisi geldiyse ve boş değilse
                if (data.keystream_sample && data.keystream_sample.length > 0) {
                    // Gelen byte dizisini (ör: [12, 255, 34]) okunabilir Hex formatına çevir (ör: "0C FF 22")
                    const hexString = data.keystream_sample
                        .map(byte => byte.toString(16).padStart(2, '0').toUpperCase())
                        .join(' ');
                    
                    keystreamOutput.textContent = hexString;
                    keystreamContainer.style.display = 'block'; // Konteyneri görünür yap
                }

            } else { // Yanıt hatalı ise (HTTP 400, 500 vb.)
                errorMessage.textContent = data.error || 'Bilinmeyen bir hata oluştu.';
                errorMessage.style.display = 'block';
                resultOutput.innerHTML = '<span class="placeholder">Sonucunuz burada görünecektir.</span>';
            }
        } catch (error) { // Sunucuya ulaşılamazsa (ağ hatası vb.)
            errorMessage.textContent = 'Sunucuyla iletişim kurulamadı. Lütfen sunucunun çalıştığından emin olun.';
            errorMessage.style.display = 'block';
            resultOutput.innerHTML = '<span class="placeholder">Sonucunuz burada görünecektir.</span>';
        }
    };

    // Butonlara tıklama olaylarını ekle
    encryptBtn.addEventListener('click', () => handleCipherRequest('encrypt'));
    decryptBtn.addEventListener('click', () => handleCipherRequest('decrypt'));

    // Kopyala butonu işlevi
    copyBtn.addEventListener('click', () => {
        const textToCopy = resultOutput.textContent;
        // Sadece gerçek bir sonuç varken kopyala
        if (textToCopy && !resultOutput.querySelector('.placeholder')) {
            navigator.clipboard.writeText(textToCopy).then(() => {
                copyBtn.textContent = 'Kopyalandı!';
                setTimeout(() => {
                    copyBtn.textContent = 'Kopyala';
                }, 2000);
            });
        }
    });
});

