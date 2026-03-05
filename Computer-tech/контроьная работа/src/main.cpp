#include <iostream>
#include <windows.h>
using namespace std;

int main()
{
    // Подключение русского языка в консоли
    SetConsoleOutputCP(65001);  
    SetConsoleCP(65001);
    
    // Подсчёт уникальных чисел (встречающихся ровно один раз) --------------------
    {
        const int N = 10;  // размер массива
        int Arr[N] = {1, 3, 6, 4, 10, 1, 7, 6, 15, 9};  // исходный массив (пример с повторами)
        
        int uniqueCount = 0;  // счётчик уникальных чисел

        // Печать исходного массива
        cout << "=== Подсчёт уникальных чисел в массиве ===" << endl;
        cout << "Массив из " << N << " элементов:" << endl;
        for (int i = 0; i < N; i++) {
            cout << Arr[i] << " ";
        }
        cout << endl;

        // Выводим заголовок для списка уникальных чисел
        cout << "\nУникальные числа (встречающиеся ровно один раз): ";
        
        // Проверяем каждый элемент
        for (int i = 0; i < N; i++) {
            int count = 0;
            // Считаем, сколько раз Arr[i] встречается в массиве
            for (int j = 0; j < N; j++) {
                if (Arr[i] == Arr[j]) {
                    count++;
                }
            }
            // Если элемент встречается ровно один раз — он уникален
            if (count == 1) {
                cout << Arr[i] << " ";
                uniqueCount++;
            }
        }

        // Если ни одного уникального числа не найдено
        if (uniqueCount == 0) {
            cout << "Нет уникальных чисел.";
        }
        cout << endl;

        // Вывод общего количества
        cout << "\nКоличество уникальных чисел: " << uniqueCount << endl;

        // Дополнительно: вывод индексов уникальных чисел
        cout << "\nИндексы уникальных чисел: ";
        bool found = false;
        for (int i = 0; i < N; i++) {
            int count = 0;
            for (int j = 0; j < N; j++) {
                if (Arr[i] == Arr[j]) {
                    count++;
                }
            }
            if (count == 1) {
                cout << i << " ";
                found = true;
            }
        }
        if (!found) {
            cout << "—";
        }
        cout << endl;
    }

    return 0;
}