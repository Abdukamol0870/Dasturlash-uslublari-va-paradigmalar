
class Taom:
    def __init__(self, nomi, narxi):
        if not nomi or narxi <= 0:
            raise ValueError("Taom nomi va narxi to'g'ri bo'lishi kerak!")
        self.nomi = nomi
        self.narxi = narxi
        self.__sotilgan = 0

    @property
    def sotilgan(self):
        return self.__sotilgan

    def sotuvni_qayd_etish(self, miqdor):
        self.__sotilgan += miqdor

    def __str__(self):
        return f"{self.nomi} - {self.narxi:,} so'm"

class Stol:
    def __init__(self, raqam):
        self.raqam = raqam
        self.__joriy_buyurtma = None

    @property
    def band(self):
        return self.__joriy_buyurtma is not None

    def buyurtma_ochish(self):
        if self.band:
            raise ValueError("Stol band!")
        self.__joriy_buyurtma = Buyurtma(self)

    def taom_qoshish(self, taom, miqdor=1):
        if not self.band:
            raise ValueError("Avval buyurtma oching!")
        self.__joriy_buyurtma.taom_qoshish(taom, miqdor)

    def hisobni_yopish(self):
        if not self.band:
            raise ValueError("Stolda faol buyurtma yo'q!")
        buyurtma = self.__joriy_buyurtma
        jami = buyurtma.hisobni_yopish()
        self.__joriy_buyurtma = None
        return jami

    def __str__(self):
        holat = "Band" if self.band else "Bo'sh"
        return f"Stol {self.raqam}: {holat}"


class Buyurtma:
    jami_buyurtmalar = 0

    def __init__(self, stol):
        self.stol = stol
        self.__taomlar = {}
        self.__yopilgan = False
        Buyurtma.jami_buyurtmalar += 1

    @property
    def jami_summa(self):
        return sum(taom.narxi * miqdor
                   for taom, miqdor in self.__taomlar.items())

    @property
    def tarkib(self):
        return tuple(self.__taomlar.items())

    @staticmethod
    def xizmat_haqi(summa):
        return summa * 0.10

    def taom_qoshish(self, taom, miqdor):
        if self.__yopilgan:
            raise ValueError("Yopilgan buyurtmaga taom qo'shib bo'lmaydi!")
        if not isinstance(miqdor, int) or isinstance(miqdor, bool) or miqdor <= 0:
            raise ValueError("Miqdor musbat butun son bo'lishi kerak!")
        self.__taomlar[taom] = self.__taomlar.get(taom, 0) + miqdor

    def hisobni_yopish(self):
        if self.__yopilgan:
            raise ValueError("Buyurtma allaqachon yopilgan!")

        summa = self.jami_summa
        xizmat = self.xizmat_haqi(summa)
        self.__yopilgan = True

        print(f"\nStol: {self.stol.raqam}")
        print(f"Taomlar summasi: {summa:,.0f} so'm")
        print(f"Xizmat haqi (10%): {xizmat:,.0f} so'm")
        print(f"Jami to'lov: {summa + xizmat:,.0f} so'm")

        return summa + xizmat

    def __len__(self):
        return sum(self.__taomlar.values())

    def __str__(self):
        return f"Buyurtma: {len(self)} ta taom, {self.jami_summa:,} so'm"


class Restoran:
    def __init__(self, nomi):
        self.nomi = nomi
        self.taomlar = []
        self.stollar = []

    @property
    def jami_tushum(self):
        return self.__tushum

    def __str__(self):
        return f"Restoran: {self.nomi}"

    def taom_qoshish(self, taom):
        self.taomlar.append(taom)

    def stol_qoshish(self, stol):
        self.stollar.append(stol)

    def hisobni_yakunlash(self, stol):
        buyurtma = stol._Stol__joriy_buyurtma
        if buyurtma is None:
            raise ValueError("Stolda faol buyurtma yo'q!")

        jami = stol.hisobni_yopish()
        self.__tushum += jami

        for taom, miqdor in buyurtma.tarkib:
            taom.sotuvni_qayd_etish(miqdor)

        return jami

    def tushumni_boshlash(self):
        self.__tushum = 0

    def eng_kop_sotilgan(self):
        if not self.taomlar:
            return "Taomlar mavjud emas"
        return max(self.taomlar, key=lambda taom: taom.sotilgan)


def main():
    restoran = Restoran("Mazali Taom")
    restoran.tushumni_boshlash()

    osh = Taom("Osh", 35000)
    shorva = Taom("Sho'rva", 25000)
    somsa = Taom("Somsa", 12000)

    restoran.taom_qoshish(osh)
    restoran.taom_qoshish(shorva)
    restoran.taom_qoshish(somsa)

    stol1 = Stol(1)
    stol2 = Stol(2)
    restoran.stol_qoshish(stol1)
    restoran.stol_qoshish(stol2)

    stol1.buyurtma_ochish()
    stol1.taom_qoshish(osh, 2)
    stol1.taom_qoshish(shorva, 1)

    restoran.hisobni_yakunlash(stol1)

    stol2.buyurtma_ochish()
    stol2.taom_qoshish(somsa, 3)
    restoran.hisobni_yakunlash(stol2)

    print("\n RESTORAN HISOBOTI ")
    print(restoran)
    print(f"Jami tushum: {restoran.jami_tushum:,.0f} so'm")
    print(f"Eng ko'p sotilgan taom: {restoran.eng_kop_sotilgan()}")
    print("\nTaomlar:")
    for taom in restoran.taomlar:
        print(f"{taom} | Sotilgan: {taom.sotilgan} ta")

    print("\nStollar:")
    for stol in restoran.stollar:
        print(stol)

if __name__ == "__main__":
    main()