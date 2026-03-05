#include <iostream>     // ввод вывод 
#include <fstream>      // для работы с файлами (ifstream, ofstream)
#include <cmath>        // для abs()
using namespace std;    

const char *FNAME = "input.txt";       // имя входного файла с исходными данными
const char *FNAME_RES = "result.txt";  // имя выходного файла для результатовj
const int VEC_SIZE = 8;                // размер исходного массива VEC
const int NEWVEC_SIZE = 10;            // размер нового массива (8 + GRN + сумма)

/*******************************************************************/
/*               О С Н О В Н А Я     П Р О Г Р А М М А             */
/*******************************************************************/

int main()
{
    // Объявление переменных
    int M;                   // параметр M из файла
    float GRN;               // значение GRN из файла
    float VEC[VEC_SIZE];     // исходный массив из 8 элементов
    float NEWVEC[NEWVEC_SIZE]; // новый массив
    
    // Открытие файлов
    ifstream fin(FNAME);     // создаем поток для чтения из входного файла
    ofstream fout(FNAME_RES); // создаем поток для записи в выходной файл
    
    // Проверка открытия входного файла 
    if (!fin)
    {
        cout << "Файл " << FNAME << " не найден!\n";

        return 1;
    }
    
    // Чтение данных из файла с проверками
    // Чтение M
    if (!(fin >> M))
    {
        cout << "Ошибка чтения M из файла\n";
        fin.close();
        return 2;
    }
    
    // Проверка корректности M
    if (M < 0 || M > VEC_SIZE)
    {
        cout << "Ошибка: M должно быть в диапазоне от 0 до " << VEC_SIZE << "\n";
        fin.close();
        return 3;
    }
    
    // Чтение GRN
    if (!(fin >> GRN))
    {
        cout << "Ошибка чтения GRN из файла\n";
        fin.close();
        return 4;
    }
    
    // Чтение массива VEC
    for (int i = 0; i < VEC_SIZE; i++)
    {
        if (!(fin >> VEC[i]))

        {
            cout << "Ошибка чтения элемента VEC[" << i << "] из файла\n";
            cout << "Недостаточно данных в файле\n";
            fin.close();
            return 5;
        }
    }
    
    fin.close(); // закрываем входной файл после чтения

    // ВЫВОД ВХОДНЫХ ДАННЫХ В КОНСОЛЬ
    cout << "=== ВХОДНЫЕ ДАННЫЕ ===" << endl;
    cout << "M = " << M << ", GRN = " << GRN << endl;
    cout << "Массив VEC: ";
    for (int i = 0; i < VEC_SIZE; i++)
    {
        cout << VEC[i];
        if (i < VEC_SIZE - 1) cout << " ";
    }
    cout << endl << endl;
    
    // 2. Формирование нового массива NEWVEC
    // Первые 8 элементов - суммы последних элементов VEC
    for (int i = 0; i < VEC_SIZE; i++)
    {
        NEWVEC[i] = 0;
        // Сумма i+1 последних элементов VEC
        for (int j = VEC_SIZE - 1 - i; j < VEC_SIZE; j++)
        {
            NEWVEC[i] += VEC[j];
        }
    }
    
    // Добавляем GRN как предпоследний элемент
    NEWVEC[VEC_SIZE] = GRN;
    
    // Добавляем сумму абсолютных значений первых M элементов как последний элемент
    NEWVEC[VEC_SIZE + 1] = 0;
    for (int i = 0; i < M; i++)
    {
        NEWVEC[VEC_SIZE + 1] += abs(VEC[i]);
    }
    
    // 3. Суммирование всех элементов сформированного массива
    float total_sum = 0;
    for (int i = 0; i < NEWVEC_SIZE; i++)
    {
        total_sum += NEWVEC[i];
    }
    
    // 4. Печать сформированного массива и значения суммы
    cout << "=== РЕЗУЛЬТАТЫ ===" << endl;
    cout << "Сформированный массив NEWVEC: ";
    for (int i = 0; i < NEWVEC_SIZE; i++)
    {
        cout << NEWVEC[i];
        if (i < NEWVEC_SIZE - 1) cout << " ";
    }
    cout << endl;
    cout << "Сумма всех элементов NEWVEC: " << total_sum << endl;
    
    // 5. Поиск наименьшего положительного элемента (без флагов)
    float min_positive = 0;
    int min_positive_index = -1;
    
    for (int i = 0; i < NEWVEC_SIZE; i++)
    {
        if (NEWVEC[i] > 0)
        {
            if (min_positive_index == -1 || NEWVEC[i] < min_positive)
            {
                // Первый найденный положительный элемент или найден меньший
                min_positive = NEWVEC[i];
                min_positive_index = i;
            }
        }
    }
    
    // Вывод результата поиска наименьшего положительного элемента
    if (min_positive_index != -1)
    {
        cout << "Наименьший положительный элемент: NEWVEC[" << min_positive_index 
             << "] = " << min_positive << endl;
        cout << "Позиция (номер) элемента: " << min_positive_index + 1 << endl;
    }
    else
    {
        cout << "В массиве NEWVEC нет положительных элементов" << endl;
    }
    
    // Запись результатов в файл
    fout << "=== РЕЗУЛЬТАТЫ ===" << endl;
    fout << "Входные данные:" << endl;
    fout << "M = " << M << ", GRN = " << GRN << endl;
    fout << "Исходный массив VEC: ";
    for (int i = 0; i < VEC_SIZE; i++)
    {
        fout << VEC[i];
        if (i < VEC_SIZE - 1) fout << " ";
    }
    fout << endl << endl;
    
    fout << "Сформированный массив NEWVEC: ";
    for (int i = 0; i < NEWVEC_SIZE; i++)
    {
        fout << NEWVEC[i];
        if (i < NEWVEC_SIZE - 1) fout << " ";
    }
    fout << endl;
    fout << "Сумма всех элементов NEWVEC: " << total_sum << endl;

    
    if (min_positive_index != -1)
    {
        fout << "Наименьший положительный элемент: NEWVEC[" << min_positive_index 
             << "] = " << min_positive << endl;
        fout << "Позиция (номер) элемента: " << min_positive_index + 1 << endl;
    }
    else
    {
        fout << "В массиве NEWVEC нет положительных элементов" << endl;
    }
    
    fout.close();  // закрываем выходной файл
    
    cout << "\nРезультаты сохранены в " << FNAME_RES << endl;
    
    return 0;  // успешное завершение программы
}


