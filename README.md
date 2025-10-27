<img width="1470" height="956" alt="Ekran Resmi 2025-10-26 17 43 59" src="https://github.com/user-attachments/assets/8f24b8d6-5db0-4211-88d6-0788976d8ec2" />
<img width="1470" height="956" alt="Ekran Resmi 2025-10-26 17 44 16" src="https://github.com/user-attachments/assets/ed03900f-757c-496e-bf4f-a8e11e48023f" />
<img width="1470" height="956" alt="Ekran Resmi 2025-10-26 17 44 24" src="https://github.com/user-attachments/assets/383328bb-172f-4cd4-acfe-acecc5b0f0e7" />



Kaotik Akış Şifreleme Web Uygulaması 

Bu proje, metinleri Lojistik Harita (Logistic Map) tabanlı kaotik bir anahtar akışı kullanarak şifreleyen ve çözen basit bir web uygulamasıdır. Kullanıcı tarafından sağlanan bir anahtar, kaotik sistem için başlangıç parametrelerini (r ve x0) türetmek için kullanılır ve bu sistem, metni XORlamak için kullanılan tahmin edilemez bir anahtar akışı (keystream) üretir.

Bu uygulama, standart XOR şifrelemesine kıyasla daha yüksek bir güvenlik seviyesi sunmayı amaçlamaktadır, çünkü anahtar akışı basit bir tekrarlanan anahtara değil, kaotik bir denkleme dayanmaktadır.

✨ Temel Özellikler

Kaotik Şifreleme: Geleneksel XOR yerine Lojistik Harita denklemi ile anahtar akışı üretir.

Anahtar Türetme: Girdiğiniz metin anahtarını SHA-256 ile hash'leyerek kaotik sistem için r ve x0 parametrelerini deterministik olarak türetir.

Base64 Çıktı: Şifrelenmiş veriyi, metin olarak kolayca kopyalanıp yapıştırılabilmesi için Base64 formatında sunar.

Anahtar Akışı Önizlemesi: Güvenlik sürecini görselleştirmek için şifreleme/çözme işleminde kullanılan kaotik anahtar akışının ilk 16 baytını Hex formatında gösterir.


🛠️ Kullanılan Teknolojiler

Backend: Python 3, Flask

Frontend: HTML5, CSS3, JavaScript (ES6+)

Kriptografi: hashlib (SHA-256), Lojistik Harita, XOR

📖 Nasıl Kullanılır

Şifreleme:

"Metin..." alanına şifrelemek istediğiniz metni girin (örn: Emre Demirkaya).

"Anahtar..." alanına bir anahtar girin (örn: beşiktaş).

Şifrele butonuna tıklayın.

"Sonuç" kutusunda Base64 formatında şifrelenmiş metni göreceksiniz (örn: mgCFeUS1Vs6OILYTg3I=).

Ayrıca, "Üretilen Anahtar Akışı" kutusunda bu şifreleme için üretilen gizli anahtarın ilk 16 baytını göreceksiniz.(örn: DF 6D F7 1C 64 F1 33 A3 E7 52 DD 72 FA 13)

Şifre Çözme:

"Sonuç" kutusundaki Base64 formatlı metni kopyalayın.

Kopyaladığınız bu metni "Metin..." alanına yapıştırın.

"Anahtar..." alanına şifreleme yaparken kullandığınız aynı anahtarı girin.

Şifre Çöz butonuna tıklayın.

"Sonuç" kutusunda orijinal metniniz olan Merhaba Dünya'yı göreceksiniz.
