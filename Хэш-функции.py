from math import sin
import struct

class MD5:
    
    # 1. выравнивание потока L’ mod 512 = 448 
    # 2. добавление длины сообщения
    # 3. инициализация буфера
    def _stap1to3(self, mes: str):
        m = mes.encode("utf-8")
        len_mes = (len(m) * 8) % 0x10000000000000000    #64битное представление 

        m += struct.pack("B", 0x80)                     #упаковка по формату
        while True:
            m += struct.pack("B", 0x0)
            if (len(m) * 8) % 512 == 448:
                break

        m += struct.pack("<Q", len_mes) #порядок от младшего байта к старшему

        #A = 67 45 23 01;
        #B = EF CD AB 89;
        #C = 98 BA DC FE;
        #D = 10 32 54 76
        buff = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476] 
        return m, buff
    
    def shift(self, a: int, n: int) -> int: #циклический сдвиг
        n = n % (len(str(a)) * 8)
        t1 = a << n
        t2 = a >> (len(str(a)) * 8 - n)
        return t1 | t2

    def _add(self, a, b): #сложение по модулю 2^32
        return (a + b) % pow(2, 32)

    def __init__(self):
        round = 16
        stage = 4
        self._iter = stage*round

        # 64 элементов T = 2^32 * sin n
        self._table = [int(0x100000000 * abs(sin(i))) for i in range(1, self._iter+1)]

        #обозначает величины сдвигов для каждой операции:
        #[0..15] 
        #[16..31]
        #[32..47]
        #[48..63] 
        self._values = [ 
            7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,
            5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,
            4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,
            6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21 ]

    def Function(self, mes: str):
        mes_bytes, parts = self._stap1to3(mes)
        mes_len = len(mes_bytes)
        step = 512 // 8

        #ДЕлим сообщение на блоки по 512-бит
        for i in range(0, mes_len, step):
            block = mes_bytes[i : i + step]

            #Делим прошлый кусок на 16 блоков по 32 бита
            x = struct.unpack("16L", block)

            #Инициализируем переменные для текущего куска
            a = parts[0]
            b = parts[1]
            c = parts[2]
            d = parts[3]

            #раундовая  функция
            for j in range(self._iter):
                
                if 0 <= j <= 15:
                    F = (b & c) | (~b & d)  # функция F
                    k = j
                
                elif 16 <= j <= 31:
                    F = (b & d) | (~d & c)  # функция G
                    k = (5 * j + 1) % 16
                
                elif 32 <= j <= 47:
                    F = b ^ c ^ d           # функция H
                    k = (3 * j + 5) % 16
                
                elif 48 <= i <= 63:
                    F = c ^ (~d | b)        # функция I
                    k = (7 * j) % 16

                F = self._add(F, x[k])              #x[k] — 32 битный блок
                F = self._add(F, self._table[j])
                F = self._add(F, a)
                F = self.shift(F, self._values[j])
                F = self._add(F, b)
                a = d
                d = c
                c = b
                b = F

            #Прибавляем результат текущего кускa к общему результату
            parts[0] += a
            parts[1] += b
            parts[2] += c
            parts[3] += d
            
        #для каждой переменной выполняется обратная перестановка байт.
        result = parts[0] + (parts[1] << 0x20) + (parts[2] << 0x40) + (parts[3] << 0x60)
        return f"{format(result, '08x')}"

from Merkle import MerkleHellman
from md5 import MD5
from work_file import *
from termcolor import colored, cprint

def main():
    dir = "message.json"
    hasher = MD5()
    cipher = MerkleHellman()
    prv_key = cipher.CreateKeys()

    while True:

        print("╔=====================================╗\n")
        x = int(input("\n[1] - Change document\n[2] - Check digital signature\n[3] - End\n"))
        print("╚=====================================╝\n")

        if x == 1:

            text = input("\nPrint the text: ")
            hash = hasher.Function(text)
            signature = cipher.Encrypt(hash, prv_key)
            print("\n")
            
            print("●•●•●•●•●•●•●•●•●•●•●•●•●•●•●•●•●•●•\n")
            print(colored('>>Substitution', 'red', attrs=['underline']))
            print("\n")
            print("Hash: ", hash, "Signature: ", signature)
            print("\n")
            write_json_file(dir, {"text": text, "signature": signature})
            print("●•●•●•●•●•●•●•●•●•●•●•●•●•●•●•●•●•●•")
            print("\n")

        elif x == 2:
            mes = read_json_file(dir)
            print("●•●•●•●•●•●•●•●•●•●•●•●•●•●•●•●•●•●•\n")
            print(colored('>>Сheck', 'red', attrs=['underline']))
            print("\n")
            signature = cipher.Decrypt(mes["signature"])
            hash_msg = hasher.Function(mes["text"])

            print("Hash: ", hash_msg, "Signature: ", signature)
            print("\n")

            print(
                "Success check\n"
                if hash_msg == signature
                else "The check failed. The mes changed\n"
            )
            print("●•●•●•●•●•●•●•●•●•●•●•●•●•●•●•●•●•●•\n")
        elif x == 3:
            print("Exit programm")
            break

if __name__ == "__main__":
        main()
