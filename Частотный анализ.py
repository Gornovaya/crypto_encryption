from collections import deque

alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
shift = int(input('введите сдвиг(целое число от 1 до 32):'))
key = input("Введите ключ (он состоит из неповторяющихся букв русского алфавита)")
print("Длина алфавита:", len(alphabet))


for i in key:                                   #удаление символов ключа из начального алфавита
    alphabet = alphabet.replace(i, '')

alphabet = key + alphabet                       #добавление ключа в алфавит

d = deque(alphabet)                             #сдвиг алфавита
d.rotate(shift)
alphabet = (''.join(list(d)))

print("Действующий алфавит:", alphabet)
print(len(alphabet))
print("\n")
print()

f = open('P&W.txt', 'rt', encoding='utf-8')
message = f.read().lower()
encMessage = ""
decMessage = ""

for sign in message:                            #шифрование введенного сообщения
    index = alphabet.find(sign)
    newIndex = index + shift
    if newIndex >= len(alphabet):
        newIndex -= len(alphabet)

    if sign in alphabet:
        encMessage = encMessage + alphabet[newIndex]
    else:
        encMessage = encMessage + sign

print("Зашиврованное сообщение:", encMessage)
print("\n")
print()

#сортировка по частоте
def sorting(dic):
    dic = {k: dic[k] for k in sorted(dic, key=dic.get, reverse=True)}
    return dic


origBig = {}

encBig = {}

#Создание списка частот открытого текста, отсортированных по частоте
for i in range(len(message)):

    if message[i] in alphabet and message[i+1] in alphabet:
        di = message[i] + message[i+1]
        if di in origBig.keys():
            origBig[di] += 1
        else:
            origBig.setdefault(di, 1)

origBig = sorting(origBig)
print(origBig)

#Создание списка частот зашифрованного текста, отсортированного по частоте
for i in range(len(encMessage)):

    if encMessage[i] in alphabet and encMessage[i+1] in alphabet:
        di = encMessage[i] + encMessage[i+1]
        if di in encBig.keys():
            encBig[di] += 1
        else:
            encBig.setdefault(di, 1)

encBig = sorting(encBig)
print(encBig)
print("\n")
print()

gom = []
hc = 0

for k in origBig.keys():
    gom.append(k)

for k in encBig.keys():
    encBig[k] = gom[hc]
    hc += 1

print(encBig)
print("\n")
print()

monoLang = {"а": 40487008, "б": 8051767, "в": 22930719, "г": 8564640, "д": 15052118,
            "е": 42691213, "ё": 184928, "ж": 4746916, "з": 8329904, "и": 37153142,
            "й": 6106262, "к": 17653469, "л": 22230174, "м": 16203060, "н": 33838881,
            "о": 55414481, "п": 14201572, "р": 23916825, "с": 27627040, "т": 31620970,
            "у": 13245712, "ф": 1335747, "х": 4904176, "ц": 2438807, "ч": 7300193,
            "ш": 3678738, "щ": 1822476, "ъ": 185452, "ы": 9595941,
            "ь": 8784613, "э": 1610107, "ю": 3220715, "я": 10139085}

monoLang = sorting(monoLang)
print("\n")

monograms = {"а": 0, "б": 0, "в": 0, "г": 0, "д": 0,
           "е": 0, "ё": 0, "ж": 0, "з": 0, "и": 0,
           "й": 0, "к": 0, "л": 0, "м": 0, "н": 0,
           "о": 0, "п": 0, "р": 0, "с": 0, "т": 0,
           "у": 0, "ф": 0, "х": 0, "ц": 0, "ч": 0,
           "ш": 0, "щ": 0, "ъ": 0, "ы": 0, "ь": 0,
           "э": 0, "ю": 0, "я": 0}


#создаем монограммы
for s in range(len(alphabet)):
    count = 0
    for l in range(len(encMessage)):
        if encMessage[l] == alphabet[s]:
            count += 1
    #print("Встречено букв", alphabet[s], ":", count)
    monograms[alphabet[s]] = count


monograms = sorting(monograms)

print("Частотность букв в зашифрованном сообщении:", '\n', monograms)


mog = []
ch = 0

for k in monoLang.keys():
    mog.append(k)

for k in monograms.keys():
    monograms[k] = mog[ch]
    ch += 1

print(monograms)
print("\n")

tEncDic = {}


#замена одних букв на другие
for k in encBig.keys():
    if not (k[0] in tEncDic.keys()) and not (k[1] in tEncDic.keys()):
        if not (encBig[k][0] in tEncDic.values()) and not (encBig[k][1] in tEncDic.values()):
            tEncDic.setdefault(k[0], encBig[k][0])
            tEncDic.setdefault(k[1], encBig[k][1])

for k in monograms.keys():
    if not(k in tEncDic.keys()):
        if not (monograms[k] in tEncDic.values()):
            tEncDic.setdefault(k, monograms[k])

print("------")            
print(tEncDic)

lostKeys = []
lostValues = []

for sign in alphabet:
    if not(sign in tEncDic.keys()):
        lostKeys.append(sign)

for sign in alphabet:
    if not(sign in tEncDic.values()):
        lostValues.append(sign)

print("-----\n")
print("Lost keys and Lost values\n")
print(lostKeys)
print(lostValues)
print("-----")

for i in range(len(lostKeys)):
    tEncDic.setdefault(lostKeys[i], lostValues[i])

print("------")  
print(tEncDic)
print("------")  

for sign in encMessage:

    if sign in alphabet:
        decMessage += tEncDic[sign]
    else:
        decMessage += sign

print("\n")
print(decMessage)
