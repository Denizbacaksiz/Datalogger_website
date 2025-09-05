# **Django Datalogger Projesi** 

Datalogger projesi cihaz verilerini SQL veritabanında tutarak ve websitesinde gösteren bir projedir. Genel cihaz bilgileri ana sayfada görülebilir. İstenen cihazın üstüne tıklanması durumunda cihazın detaylı sayfasına gidilir. Detaylı cihaz sayfasında cihaz ismi , son cihaz verileri , verilerin tarihleri saatleri ve istenen verileri düzenleme veya silme özelliği bulunmaktadır. Ana sayfada ek olarak karşılaştırma özelliği yer almaktadır. Tıklanma durumunda karşılaştırma sayfasına gidilir ve kullanıcının karşılaştırmak istediği cihazları seçmesi istenir. Eğer cihazlar aynı kanallara sahipse son verileri karşılaştırılır değilse ortak kanallar olmadığı için bir hata mesajı gösterilir. Bu proje barındırdığı API'ler sayesinde entegre edilen cihazlardan veri çekmek amacıyla tasarlanmıştır.


## Özellikler 

* Genel cihaz bilgilerini sergileyen basit ana sayfa tasarımı
* Karşılaştırma özelliğiyle cihazlar arası veri karşılaştırma
* Detaylı cihaz görünümüyle veri manipülasyonu ve veri silme
* Cihaz üzerinde veya lokal ağda paylaşımlı kullanım
* Filtreleme ile istenilen tarih ve saat aralığındaki verileri sıralama
* Filtrelemeyle entegre her bir kanal için ayrı veri grafiği
* AJAX ile ana sayfada 30 saniyede bir yenileme ile gelen veri kontrolü




# **Kurulum Adımları ve Gereksinimler** 
## Gereksinimler 

- Python 3.13
- MySQL Server 8.0.43
- Visual studio code veya herhangi bir python editörü
- Git


## Ortam Ayarlarının Yapılması 
NOT: Python , python pip ve mysql dosyaları kurulduktan sonra sistem path'ine eklenmemiş olabiliyor eğer kayıtlı değilse kayıt için aşağıdaki adımları takip ediniz kayıtlı ise kurulum adımından devam ediniz.(Pip'in Path'e eklenme sebebi bazen ana path üzerinden pip görünmeyebiliyor olduğundan dolayıdır.)

1-Arama kutusuna "Sistem ortam değişkenlerini düzenleyin" yazın ve çıkan uygulamaya tıklayın.

2-Gelişmiş Menüsünde "Ortam Değişkenleri..." kutusuna tıklayın

3-Sistem değişkenleri bölümünde "Path" adındaki sistem değişkenine çift tıklayarak ya da üstüne tıklayıp düzenle seçeneğine tıklayın.

4-Yeni seçeneğine tıklanarak python'un kurulu olduğu dosyaya gidilir ve dosya adresi yeni path olarak eklenir.(Genelde "C:\Users\User\AppData\Local\Programs\Python" adresinde bulunur) 

5-Yeni seçeneğine tıklanarak python'un kurulu olduğu dosyada Scripts dosya adresi yeni path olarak eklenir.(Genelde "C:\Users\User\AppData\Local\Programs\Python\Python313\Scripts" adresinde bulunur)

6-Yeni seçeneğine tıklanarak mysql'in kurulu olduğu dosyaya gidilir ve dosya adresi yeni path olarak eklenir.(Genelde "C:\Program Files\MySQL" adresinde bulunur)

## Kurulum 
1) proje dosyasını indir
    - git clone https://github.com/Denizbacaksiz/Datalogger_website

2) CMD üzerinden mysql'e bağlan (MySQL kurulumunda belirlenen şifreyi isteyecektir)
    - mysql -u root -p

3) Terminalde mysql açıkken database oluştur
    - CREATE DATABASE device_datas;

4) Terminalde mysql açıkken database kontrolü yap
    - SHOW DATABASES;

5) Kod editöründe dosyayı aç ve terminale bağlan

6) Pip ile pipenv , djangorestframework ve mysqlclient indir
    - pip install pipenv
    - pip install djangorestframework
    - pip install mysqlclient

7) Sanal çevre aktivasyonunu yap. Terminalde
    - pipenv shell

8) Database migrasyonunu tamamla(Bu adım database içindeki tabloları Django modellerine göre oluşturacaktır).Terminalde
    - python manage.py migrate

9) Tüm kurulum adımları tamamlandı. Serveri başlatmak için terminalde 
    - python manage.py runserver (Cihaz üzerinden Kullanım için)
    - python manage.py runserver <Bilgisayar_IP>:8000 (Lokal ağda 8000 Portundan Paylaşım İçin)


---
# **Örnek Python Requestleri** 

# CİHAZ EKLEME 
```python
import requests
import json

url = 'http://127.0.0.1:8000/api/device/add_device/'

data = {
    "name": "Thermostat",
    "device_id": "thermo_001"
}

headers = {'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(data), headers=headers)
print("Durum Kodu:", response.status_code)
print("Yanıt:", response.text)
```



# CİHAZ VERİSİ EKLEME 
```python
import requests
import json

url = 'http://127.0.0.1:8000/api/device/termo_001/add_data/'  

data = {
    "temperature": 25.5,
    "humidity": 60,
    "pressure": 1013.2
}

headers = {'Content-Type': 'application/json'}

try:
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print("Durum Kodu:", response.status_code)
    print("Yanıt:", response.text)
except requests.exceptions.RequestException as e:
    print(f"Hata oluştu: {e}")

print("="*50)
```



# CİHAZ VERİSİ GÜNCELLEME 
```python
import requests
import json

url = 'http://127.0.0.1:8000/api/device/termo_001/update_data/'  

data = {
    "temperature": 26.0,
    "humidity": 65
}

headers = {'Content-Type': 'application/json'}

try:
    response = requests.patch(url, data=json.dumps(data), headers=headers)
    print("Durum Kodu:", response.status_code)
    print("Yanıt:", response.text)
except requests.exceptions.RequestException as e:
    print(f"Hata oluştu: {e}")

print("="*50)
```


# CİHAZ VERİSİ SİLME 
```python
import requests
import json

url = 'http://127.0.0.1:8000/api/device/termo_001/delete_data/'

try:
    response = requests.delete(url)
    print("Durum Kodu:", response.status_code)
    print("Yanıt:", response.text)
except requests.exceptions.RequestException as e:
    print(f"Hata oluştu: {e}")

print("="*50)
```


# CİHAZ SİLME 
```python
import requests
import json

url = 'http://127.0.0.1:8000/api/device/termo_001/delete_device/'

try:
    response = requests.delete(url)
    print("Durum Kodu:", response.status_code)
    print("Yanıt:", response.text)
except requests.exceptions.RequestException as e:
    print(f"Hata oluştu: {e}")
```
---
