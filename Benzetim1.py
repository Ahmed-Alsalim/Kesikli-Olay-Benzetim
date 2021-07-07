'''
Ahmed Tawfiq
B181200553
'''

from beautifultable import BeautifulTable

############
Demo = True
############

if Demo:
    # Test etmek için bu değerler kullanılabilir. 
    musteriGelisZaman = [5, 11, 15, 20, 26]
    musteriServisSure = [10, 12, 15, 12, 14]
else:
    # kullanıcıdan veriler alınır.
    musteriGelisZaman = []
    musteriServisSure = []
    i = 1
    while True:
        arrival = input((f"Müşteri {i} geliş zamanı: "))
        service = input((f"Müşteri {i} servis süresi: "))
        if arrival == "" or service == "":
            break
        musteriGelisZaman.append(int(arrival))
        musteriServisSure.append(int(service))
        print("işlem bittiğinde boş bırakarak enter basınız.")
        i += 1

# Müşteri servis süreleriyle indexi koruyarak geliş zamanlara göre sıralanır.
temp = [
    musteriServisSure[musteriGelisZaman.index(m)]
    for m in sorted(musteriGelisZaman)
]

musteriServisSure = temp.copy()
musteriGelisZaman = sorted(musteriGelisZaman)

# Benzetim Zamanları bulmak için her müşterinin servis bitirme zamanları hesaplayıp
# geliş zamanlarla birleştirilir sonra tekrarlı değerleri kaldırarak sıralanır.
BenzetimZaman = []
bitirmeZamanlar = [musteriGelisZaman[0]]
for i in range(len(musteriGelisZaman)):
    BenzetimZaman.append(musteriGelisZaman[i])
    if musteriGelisZaman[i] >= bitirmeZamanlar[-1]:
        bitirmeZamanlar.append(musteriGelisZaman[i] + musteriServisSure[i])
    else:
        bitirmeZamanlar.append(musteriServisSure[i] + bitirmeZamanlar[-1])
BenzetimZaman.extend(bitirmeZamanlar)
bitirmeZamanlar.pop(0)
BenzetimZaman = sorted(list(dict.fromkeys(BenzetimZaman)))

# Her benzetim zamanında, o zamanda gelen müşteriyi eklenilir.
# Gelen yoksa boşluk eklenilir.
gelenMus = []
for b in BenzetimZaman:
    if b in musteriGelisZaman:
        gelenMus.append(musteriGelisZaman.index(b) + 1)
    else:
        gelenMus.append(None)

# Her benzetim zaman, bitirme zamanlar listesinde olup olmadığı kontrol edilir
# olsa, bu benzetim zamanında biten müşteri var demek ve numarası index ile bulunur.
bitenMus = []
for b in BenzetimZaman:
    if b in bitirmeZamanlar:
        bitenMus.append(bitirmeZamanlar.index(b) + 1)
    else:
        bitenMus.append(None)

devamEden = [1]
for b in bitenMus[1:-1]:
    # Biten müşteri yoksa:
    if b is None:
        if devamEden[-1] is None:
            # Önceki benzetim zamanında devam eden müşteri
            # yoksa, şimdi gelen müşteri servise girer.
            devamEden.append(gelenMus[len(devamEden)])
        else:
            # Önceki benzetim zamanında devam eden müşteri varsa aynısı devam eder.
            devamEden.append(devamEden[-1])
    # Biten müşteri varsa:
    elif gelenMus.index(b + 1) > (len(devamEden)):
        # Sonraki müşteri daha gelmediyse servis boş kalır.
        devamEden.append(None)
    else:
        # Sonraki müşteri geldiyse servise girer.
        devamEden.append(b + 1)
devamEden.append(None)

bitisZaman = []
for d in devamEden:
    if d is None:
        bitisZaman.append(None)
    else:
        bitisZaman.append(bitirmeZamanlar[d - 1])

# Gelen müşteri ile Servise giren (devam eden) müşterileri karşılaştırarak
# girmiş ancak servisi daha başlamayanları kuyruğa eklenilir.
Kuyruk = []
servis = []
kuyrukTemp = []
for i in range(len(BenzetimZaman)):
    Kuyruk.append(gelenMus[i])
    servis.append(devamEden[i])
    for k in Kuyruk:
        if k in servis:
            Kuyruk.remove(k)
    kuyrukTemp.append(Kuyruk.copy())
Kuyruk.clear()
for i in kuyrukTemp:
    temp = ""
    for ii in i:
        if ii != None:
            temp += str(ii) + ", "
    Kuyruk.append(temp[:-2])

# Servise giriş zaman ile geliş zamanın arasındaki fark
# hesaplayarak kuyrukta bekleme süreyi bulunur.
beklemeSure = []
for i, d in enumerate(devamEden):
    if d != None and i == devamEden.index(d):
        bekleme = BenzetimZaman[devamEden.index(d)] - BenzetimZaman[gelenMus.index(d)]
        beklemeSure.append(bekleme)
    else:
        beklemeSure.append("")
# Servisi devam eden müşteri yoksa, servisin boş kaldığı süreyi hesaplanır.
bosKalmaSure = [musteriGelisZaman[0]]
for d in devamEden[:-1]:
    if d is None:
        temp = BenzetimZaman[len(bosKalmaSure)] 
        - BenzetimZaman[len(bosKalmaSure) - 1]
        bosKalmaSure.append(temp)
    else:
        bosKalmaSure.append(None)
bosKalmaSure.append(None)

# Elde edilen değerleri güzelce bir tabloda yazdırılır.
print("Ahmed Tawfiq\nB181200553")
uyari="*Tablo düzgün görünmüyorsa ekranı büyütünüz."
finalTable = BeautifulTable()
finalTable.columns.append(BenzetimZaman, "Benzetim\nzamanı")
finalTable.columns.append(gelenMus, "Gelen\nmüşteri")
finalTable.columns.append(bitenMus, "Servisi\nbiten\nmüşteri")
finalTable.columns.append(Kuyruk, "Kuyrukta\nbekleyenler")
finalTable.columns.append(devamEden, "Servisi\ndevam eden")
finalTable.columns.append(bitisZaman, "Servis\nbitiş\nzamanı")
finalTable.columns.append(beklemeSure, "Kuyrukta\nbekleme\nsüresi")
finalTable.columns.append(bosKalmaSure, "Servisin\nboş kalma\nsüresi")
finalTable.set_style(BeautifulTable.STYLE_SEPARATED)
finalTable.columns.width = 13

Output = f'''Müşteri geliş zaman: {musteriGelisZaman}
Müşteri servis süre: {musteriServisSure}\n
{uyari}
{finalTable}'''
print(Output)

# İstenilirse elde edilen tabloyu bir text dosyada saklanılır.
save = input("Tablo, text dosyasında kaydedilsin mi? [E/H] ").upper()
if save == 'E':
    with open("Benzetim Tablosu.txt","w",encoding='UTF-8') as f:
        f.write(Output)
        print("Benzetim Tablosu.txt dosyasında kaydedildi.")
