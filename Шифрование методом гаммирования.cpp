#include <stdio.h>
#include <iostream>
#include <math.h>
#include <stdio.h>
#include <conio.h>
#include <string>
#include <conio.h>
#include <cmath>
#define POW(A,B) 

using namespace std;

void decimalToBinary(int op1, int aOp[]) {          //представление числа в битах
    int result, i = 0;
    do {
        result = op1 % 2;
        op1 /= 2;
        aOp[i] = result;
        i++;
    } while (op1 > 0);
}


int binaryToDecimal(int array[]) {                  //представление в десятичной форме
    int sum = 0, i;
    for (i = 0; i < 8; i++) {
        if (array[i]) sum += pow(2, i);
    }
    return sum;
}


void showBinary(int array[], int n) {               //показать число в двоичной форме
    int i;
    for (i = n - 1; i >= 0; i--) {
        printf("%d ", array[i]);

    }
    printf("\n");
}

int addBinary(int a1[], int a2[], int result[]) {   //исключающее или
    int i, c = 0;
    for (i = 0; i < 8; i++) {
        result[i] = (a1[i] ^ a2[i]); //a xor b 
        c = ((a1[i] | a2[i]) & !(a1[i] & a2[i]));
    }
    result[i] = c;
    return c;
}


int ipow(int a, int b)                              //функция возведения в степень
{
    if (b > 0)
        return a * ipow(a, b - 1);
    else
        return 1;
}


int main() {

    setlocale(LC_ALL, "Russian");

    int op1, op2, op3, sum, sum2;
    int  aOp1[8] = { 0,0,0,0,0,0,0,0 };             //число для шифрования
    int  aOp2[8] = { 0,0,0,0,0,0,0,0 };             //ключ
    int  aOp3[8] = { 0,0,0,0,0,0,0,0 };             //вспомогательная переменная
    int  aSum[8] = { 0,0,0,0,0,0,0,0 };             // зашифрованное значение
    int  aSum2[8] = { 0,0,0,0,0,0,0,0 };            // дешифрованное значение
    char s[255];                                    //для строки в обычном виде
    char k[255];                                    //ключ в обычном виде
    int binary[2048];                               //для строки в двоичном виде
    int binary2[2048];                              //для ключа в двоичном виде
    int res[2048];                                  //переменные для дешифрованиея
    int res2[2048];
    int ns,nk = 0;                                  //длина строки и ключа

    

    int ch;                                         //переменная для выбора меню

    do {
        std::cout << std::endl;
        std::cout << std::endl;
        std::cout << " = \t           Меню                =" << endl;
        std::cout << " \t1) Ввести число и ключ           " << endl;
        std::cout << " \t2) Шифрование/дешифрование числа " << endl;
        std::cout << " \t3) Шифрование/дешифрование слова " << endl;
        std::cout << " \t4) Завершить                     " << endl;
        std::cout << "=                                  =" << endl;
        std::cout << endl;

        std::cout << "\tВыбери задание" << endl;
        std::cin >> ch;
        std::cout << endl;

        switch (ch) {

        case 1:
            system("cls");
            cout << "---------------------------------------------------" << endl;
            std::cout << "Введите число и ключ (0 до 255)" << std::endl;
            if (scanf_s("%d %d", &op1, &op2) != 1) 
            {
                system("pause");
                printf("Упс, ошибочка вышла. Пожалуйста, попробуйте еще раз.\n");
                std:cout << std::endl;
                scanf_s("%*[^\n]");
            }
            while (op1 < 0 || op1 > 255 || op2 < 0 || op2 > 255) {
                printf("Введите число и ключ (0 до 255): ");
                scanf_s("%d %d", &op1, &op2);
            }

            decimalToBinary(op1, aOp1);
            decimalToBinary(op2, aOp2);
            std::cout << endl;
            printf("Бинарное представление числа: ", op1);
            showBinary(aOp1, 8);
            printf("Бинарное представление ключа:  ", op2);
            showBinary(aOp2, 8);
            std::cout << endl;

            break;

        case 2:
            std::cout << "\tЗашифрованное значение:  ";
            if (!addBinary(aOp1, aOp2, aSum)) {
                showBinary(aSum, 8);
                sum = binaryToDecimal(aSum);
                printf("\tЗашифрованное значение в десятичном виде : %d", sum);
                std::cout << std::endl;
                op3 = sum;
                decimalToBinary(op3, aOp3);
            }
            else {
                printf("Overflow");
            }
            std::cout << std::endl;

            std::cout << "\tДешифрованное значение:  ";
            if (!addBinary(aOp3, aOp2, aSum2)) {
                showBinary(aSum2, 8);
                op3 = binaryToDecimal(aSum2);
                printf("\tДешифрованное значение в десятичном виде : %d", op3);
            }
            else {
                printf("Ошибка");
            }
            std::cout << std::endl;

            break;

        case 3:
        {
            system("cls");
            cout << "---------------------------------------------------" << endl;
            std::cout << "Введите строку" << std::endl;
            std::cin >> s;
            std::cout << "Введите ключ" << std::endl;
            std::cin >> k;
            ns = strlen(s);
            nk = strlen(k);

            cout << endl;
            printf("'%s' Строка в бинарном виде: ", s);
            int c, power, a = 0;
            for (int i = 0; i < ns; i++)
            {
                c = s[i];
                for (power = 7; power + 1; power--, a++)
                    if (c >= (1 << power))
                    {
                        c -= (1 << power);
                        binary[a] = 1;
                    }
                    else {
                        binary[a] = 0;
                    }
            }

            for (int i = 0; i < a; i++)             //печать строки в двоичном виде
            {
                cout << binary[i];
            }
                
            cout << endl;

            printf("'%s' Ключ в бинарном виде: ", s);
            int c2, power2, a2 = 0;
            for (int i = 0; i < nk; i++)
            {
                c2 = k[i];
                for (power2 = 7; power2 + 1; power2--, a2++)
                    if (c2 >= (1 << power2))
                    {
                        c2 -= (1 << power2);
                        binary2[a2] = 1;
                    }
                    else {
                        binary2[a2] = 0;
                    }
            }

            int i = 0;
            for (int i = 0; i < a2; i++)             //печать ключа в двоичном виде
                cout << binary2[i];
            cout << endl;
            cout << endl;
           
            cout << "Шифрование:  " << endl;
            for (int i = 0; i < a && i < a2; i++)
            {
                res[i] = (binary[i] ^ binary2[i]); //a xor b 
                cout << res[i];
            }

            cout << endl;
            
            for (int i = 0; i < a2; i++)
            {
                res2[i] = (binary2[i] ^ res[i]); //a xor b 
                cout << res2[i];
            }

            cout << endl;

            char dec;
            char dec2;
            
            cout << "Обратно в символы: ";
            /*Дальше преобразовываем каждые 8 бит
            массива binary по отдельности в символ
            начиная со старшего бита
            например 2^7*binary[0] + 2^6*binary[1] + ... +2^0*binary[7]
            таким образом получаем первый символ и.т.д*/
            while (1)
            {
                dec = 0;
                for (int j = 7; j >= 0; j--)//перебираем очередные 8 "бит"
                {
                    dec += ipow(2, (j)) * res2[i];
                    i++;
                }
                cout << dec;
                if (i >= a)//не забываем, что в a у нас остался размер двоичного массива
                    break;
            }
            cout << endl;
            _getch();
            break;
        }
        case 4:
            system("cls");
            exit(1);
            break;

        default: std::cout << "Произошла ошибка" << endl;
            std::cout << endl;
            std::cout << endl;
            break;
        }

    } while (ch != 0);
    return 0;

}
