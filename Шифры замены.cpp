#include <stdio.h>
#include <iostream>
using namespace std;

const char POLYBIUS[5][5] = {           //массив букв для алгоритма
    { 'A', 'B', 'C' , 'D', 'E'},
    { 'F', 'G', 'H' , 'I', 'K'},
    { 'L', 'M', 'N' , 'O', 'P'},
    { 'Q', 'R', 'S' , 'T', 'U'},
    { 'V', 'W', 'X' , 'Y', 'Z'}
};

char encrypt(const char c) {            //функция шифрования

    for (int i = 0; i < 5; ++i)
        for (int j = 0; j < 5; ++j)
            if (POLYBIUS[i][j] == c)
                return POLYBIUS[(i + 1) % 5][j];
}

char decrypt(const char c) {            //функция дешифрования

    for (int i = 0; i < 5; ++i)
        for (int j = 0; j < 5; ++j)
            if (POLYBIUS[i][j] == c)
                return POLYBIUS[(i + 4) % 5][j];
}

int main() {

    setlocale(LC_ALL, "Russian");

    char c[] = "";          //переменная для слова
    int x;                  //переменная для выбора меню

    do {
        std::cout << std::endl;
        std::cout << std::endl;
        std::cout << " = \t      Меню            =" << endl;
        std::cout << " \t1) Ввести слово         " << endl;
        std::cout << " \t2) Зашифровать          " << endl;
        std::cout << " \t3) Дешифровка           " << endl;
        std::cout << " \t4) Завершить программу  " << endl;
        std::cout << "=                          =" << endl;
        std::cout << endl;

        std::cout << "\tВыбери задание" << endl;
        std::cin >> x;
        std::cout << endl;

        switch (x) {

        case 1:
            system("cls");
            cout << "---------------------------------------------------" << endl;
            std::cout << "Введите слово, которое хотите зашифровать" << std::endl;
            \std::cin >> c;
            std::cout << endl;
            break;
        case 2: 
            std::cout << "\tЗашифрованное слово:  ";
            for (int i = 0; c[i] != '\0'; ++i)
                std::cout << encrypt(c[i]);
            std::cout << std::endl;
            break;

        case 3:
            std::cout << "\tРасшифрованное слово:  ";
            for (int i = 0; c[i] != '\0'; ++i)
                std::cout << decrypt(encrypt(c[i]));
            std::cout << std::endl;
            break;
        case 4: 
            system("cls");
            exit(1);
            break;

        default: std::cout << "Произошла ошибка" << endl;
            std::cout << endl;
            std::cout << endl;
            break;
        }

    } while (x != 0);
    return 0;

}
