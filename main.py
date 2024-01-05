# BankApp
import sqlite3

csv_path = r'C:\Users\ykyas\OneDrive\Masaüstü\SQLiteDB\project\mockData.csv'
dbPath = r'C:\Users\ykyas\OneDrive\Masaüstü\SQLiteDB\project\bankCustomer.db'
db = sqlite3.connect(dbPath, timeout=4)
cursor = db.cursor()
create_table_query = """
    CREATE TABLE IF NOT EXISTS customer(
        tc INTEGER PRIMARY KEY,
        isim TEXT,
        sifre INTEGER,
        maas INTEGER,
        kira INTEGER,
        fatura INTEGER,
        aidat INTEGER,
        ev BOOLEAN,
        araba BOOLEAN
)
"""
cursor.execute(create_table_query)
cursor.close()


class Musteri():
    def __init__(self, tc, isim, sifre):
        self.tc = tc
        self.isim = isim
        self.sifre = sifre
        self.bakiye = 0


class Banka():
    def __init__(self):
        self.müsteriler = list()
        self.müsteriler.append(Musteri("123", "Battal", "123"))
        self.müsteriler.append(Musteri("321", "Ahmet", "321"))

    def müsteri_ol(self, tc, isim, sifre):
        self.müsteriler.append(Musteri(tc, isim, sifre))
        print("Bankamıza kayıt olduğunuz için teşekkür ederiz:)")


def dbConnect(tc, isim, sifre, maas, kira, fatura, aidat, ev, araba):
    with sqlite3.connect(dbPath) as db:
        cursor = db.cursor()
        try:
            insert_query = """
            INSERT INTO customer(tc,isim,sifre,maas,kira,fatura,aidat,ev,araba)
            VALUES(?,?,?,?,?,?,?,?,?)
            """
            cursor.execute(insert_query, (tc, isim, sifre, maas, kira, fatura, aidat, ev, araba))
            db.commit()
            print("Customer added successfully.")
        except sqlite3.Error as e:
            print(f"Error adding customer: {e}")
        finally:
            cursor.close()


def check_tc_in_db(tc):
    with sqlite3.connect(dbPath) as db:
        cursor = db.cursor()
        try:
            query = "SELECT * FROM customer WHERE tc=?"
            cursor.execute(query, (tc,))
            result = cursor.fetchone()

            if result:
                print("TC bulundu.")
                return True
            else:
                print("TC bulunamadı.")
                return False

        except sqlite3.Error as e:
            print(f"Error checking TC in database: {e}")
            return False
        finally:
            cursor.close()

def check_name_and_password_in_db(tc, isim, sifre):
    with sqlite3.connect(dbPath) as db:
        cursor = db.cursor()
        try:
            query = "SELECT * FROM customer WHERE tc=? AND isim=? AND sifre=?"
            cursor.execute(query, (tc, isim, sifre))
            result = cursor.fetchone()

            if result:
                print("TC, isim ve şifre eşleşiyor.")
                return True
            else:
                print("TC, isim veya şifre eşleşmiyor.")
                return False

        except sqlite3.Error as e:
            print(f"Error checking name and password in database: {e}")
            return False
        finally:
            cursor.close()


banka = Banka()
menü = """
    \tKÜÇÜKLER Bankasına Hoş Geldiniz

    1) Müşteriyim
    2) Müşteri Olmak İstiyorum
    Q) Çıkış

"""
m_menü = """
    \tHoş Geldiniz Sayın {}

    1) Bakiye Sorgula
    2) Para Yatır
    3) Para Transfer Et
    4) Para Çek
    5) Kredi Çek
    Q) Çıkış

"""
y_menü = "Ana menüye dönmek için enter'a basınız."

while True:
    print(menü)
    secim = input("Seçiminiz:")
    if secim == "1":
        girilen_tc = input("TC no giriniz:")

        tc_no = [a.tc for a in banka.müsteriler]
        if check_tc_in_db(girilen_tc):
            for müsteri in banka.müsteriler:
                if girilen_tc == müsteri.tc:
                    girilen_sifre = input("Şifre giriniz:")
                    if girilen_sifre == müsteri.sifre:
                        while True:
                            print(m_menü.format(müsteri.isim))
                            secim2 = input("Seçiminiz:")
                            if secim2 == "1":
                                print("Bakiyeniz:", müsteri.bakiye)
                                input(y_menü)
                            elif secim2 == "2":
                                yatırılan_tutar = int(input("Miktar:"))
                                onay = input("Kendi hesabınıza {} TL para yatırmayı onaylıyor musunuz?(E/H):".format(
                                    yatırılan_tutar))
                                onay = onay.lower()
                                if onay == "e":
                                    müsteri.bakiye += yatırılan_tutar
                                    print("Paranız yatırıldı.")
                                    input(y_menü)
                                elif onay == "h":
                                    print("İşleminiz iptal edildi.")
                                    input(y_menü)
                                else:
                                    print("Hatalı seçim yaptınız.")
                                    input(y_menü)
                            elif secim2 == "3":
                                hedef_tc = input("Yatırılacak hesabın TC no:")
                                if hedef_tc in tc_no:
                                    for müsteri2 in banka.müsteriler:
                                        if hedef_tc == müsteri2.tc:
                                            transfer_tutar = int(input("Miktar:"))
                                            if transfer_tutar <= müsteri.bakiye:
                                                onay = input(
                                                    "{} adlı müşterimize, {} TL tutarında parayı göndermeyi onaylıyor musunuz?(E/H):".format(
                                                        müsteri2.isim, transfer_tutar))
                                                onay = onay.lower()
                                                if onay == "e":
                                                    müsteri2.bakiye += transfer_tutar
                                                    müsteri2.bakiye += transfer_tutar
                                                    müsteri.bakiye -= transfer_tutar
                                                    print("Paranız yatırıldı.")
                                                    input(y_menü)
                                                elif onay == "h":
                                                    print("İşlem iptal edildi.")
                                                    input(y_menü)
                                                else:
                                                    print("Hatalı seçim yaptınız.")
                                                    input(y_menü)
                                            else:
                                                print("Bakiyeniz yetersiz!")
                                                input(y_menü)
                                        else:
                                            print("Yanlış tc girildi.")
                                            input(y_menü)
                            elif secim2 == "4":
                                cekilecek_tutar = int(input("Miktar:"))
                                if cekilecek_tutar <= müsteri.bakiye:
                                    müsteri.bakiye -= cekilecek_tutar
                                    print("İşlem tamamlandı.")
                                    input(y_menü)
                                else:
                                    print("Bakiyeniz yetersiz!")
                                    input(y_menü)
                            elif secim2 == "q" or secim2 == "Q":
                                print("Çıkış yapılıyor.")
                                input(y_menü)
                                break
                            else:
                                input(y_menü)
                    else:
                        print("\nYanlış şifre girdiniz!!Ana menüye dönüyorsunuz...")
        else:
            print("Bu bilgiye sahip bir müşterimiz bulunmamaktadır.")
    elif secim == "2":
        tc = int(input("TC giriniz:"))
        name = input("İsim giriniz:")
        key = input("Şifre giriniz:")
        # İnformations for credit point
        salary = int(input("Maaşınızı giriniz:"))
        rent = int(input("Aylık ödenen kira tutarı,eviniz varsa \"0\" giriniz:"))
        bill = int(input("Aylık toplam fatura tutarı:"))
        dues = int(input("Aidat ödüyorsan tutar,ödemiyorsanız 0 giriniz:"))
        if rent <= 400:
            house = True
        else:
            house = False
            car = bool(input("Araban var mı:").lower())

        dbConnect(tc, name, key, salary, rent, bill, dues, house, car)

        banka.müsteri_ol(tc, name, key)
        input(y_menü)
    elif secim == "q" or secim == "Q":
        break
    else:
        input(y_menü)
