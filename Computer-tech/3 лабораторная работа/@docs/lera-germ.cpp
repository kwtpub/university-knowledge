/****************************************************************
 * КАФЕДРА № 304 1 КУРС *
 *---------------------------------------------------------------*
 * Project Type : Win32 Console Application *
 * Project Name : First project *
 * File Name : First.cpp *
 * Language : C/C++ *
 * Programmer(s) : Малохлебов Г.М, Лисицина В.С *
 * Modifyed By : *
 * Lit source : *
 * Created : 19/12/25 *
 * Last Revision : 19/12/25 *
 * Comment(s) : Сумма ряда. *
 ****************************************************************/
#include <cmath>    // для abs()
#include <fstream>  // для работы с файлами (ifstream, ofstream)
#include <iostream> // ввод вывод

using namespace std;
const char* FNAME = "input.txt";      // имя входного файла с исходными данными
const char* FNAME_RES = "result.txt"; // имя выходного файла для результатов
// ОТЛИЧИЕ: В main.cpp: VEC_SIZE = 7, NEWVEC_SIZE = 7
const int VEC_SIZE = 8;               // размер исходного массива VEC
const int NEWVEC_SIZE = 10;           // размер нового массива (8 + GRN + сумма)
int main()
{

    // Объявление переменных
    // ОТЛИЧИЕ: В main.cpp читается N и M (вместо M и GRN)
    int M;                     // параметр M из файла
    float GRN;                 // значение GRN из файла
    float VEC[VEC_SIZE];       // исходный массив из 8 элементов
    float NEWVEC[NEWVEC_SIZE]; // новый массив
    // Открытие файлов
    ifstream fin(FNAME);      // создаем поток для чтения из входного файла
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
        10 "\n";
        cout << "Ошибка: M должно быть в диапазоне от 0 до " << VEC_SIZE << fin.close();
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
        if (i < VEC_SIZE - 1)
            cout << " ";
    }
    cout << endl << endl;
    // 2. Формирование нового массива NEWVEC
    // *** ГЛАВНОЕ ОТЛИЧИЕ ОТ main.cpp: ***
    // Здесь: NEWVEC[i] = сумма последних (i+1) элементов VEC, 
    //        + добавляется GRN и сумма abs(первых M элементов)
    // В main.cpp: NEWVEC[i] = VEC[i] + сумма отрицательных элементов VEC среди первых N
    
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
    {
        NEWVEC[VEC_SIZE + 1] = 0;
        for (int i = 0; i < M; i++)
            NEWVEC[VEC_SIZE + 1] += abs(VEC[i]);
    }
    // 3. Суммирование всех элементов сформированного массива
    float total_sum = 0;
    11 for (int i = 0; i < NEWVEC_SIZE; i++) { total_sum += NEWVEC[i]; }
    // 4. Печать сформированного массива и значения суммы
    cout << "=== РЕЗУЛЬТАТЫ ===" << endl;
    cout << "Сформированный массив NEWVEC: ";
    for (int i = 0; i < NEWVEC_SIZE; i++)
    {
        cout << NEWVEC[i];
        if (i < NEWVEC_SIZE - 1)
            cout << " ";
    }
    cout << endl;
    cout << "Сумма всех элементов NEWVEC: " << total_sum << endl;
    // 5. Поиск наименьшего положительного элемента
    float min_positive;
    int min_positive_index = -1;
    // Первый цикл: находим первый положительный элемент
    for (int i = 0; i < NEWVEC_SIZE; i++)
    {
        if (NEWVEC[i] > 0)
        {
            // Сразу присваиваем первый найденный положительный элемент
            min_positive = NEWVEC[i];
            min_positive_index = i;
            break; // выходим из цикла после нахождения первого положительного
        }
    }
    // Второй цикл: ищем минимальный среди остальных положительных элементов
    if (min_positive_index != -1)
    {
        for (int i = 0; i < NEWVEC_SIZE; i++)
        {
            if (NEWVEC[i] > 0 && NEWVEC[i] < min_positive)
            {
                // Найден меньший положительный элемент
                min_positive = NEWVEC[i];
            }
        }
    }
    // Вывод результата поиска всех элементов, равных min_positive
    // ОТЛИЧИЕ: В main.cpp выводится только один элемент (первый найденный в диапазоне)
    if (min_positive_index != -1)
    {
        cout << "Наименьшее положительное значение: " << min_positive << endl;
        cout << "Элементы, равные минимальному положительному:" << endl;
        for (int i = 0; i < NEWVEC_SIZE; i++)
        {
            if (NEWVEC[i] == min_positive)
            {
                cout << " NEWVEC[" << i << "] = " << min_positive << " (позиция: " << i + 1 << ")"
                     << endl;
            }
        }
    }
    else
    {
    }
    cout << "В массиве NEWVEC нет положительных элементов" << endl;
    12
        // Запись результатов в файл
        fout
        << "=== РЕЗУЛЬТАТЫ ===" << endl;
    fout << "Входные данные:" << endl;
    fout << "M = " << M << ", GRN = " << GRN << endl;
    fout << "Исходный массив VEC: ";
    for (int i = 0; i < VEC_SIZE; i++)
    {
        fout << VEC[i];
        if (i < VEC_SIZE - 1)
            fout << " ";
    }
    fout << endl << endl;
    fout << "Сформированный массив NEWVEC: ";
    for (int i = 0; i < NEWVEC_SIZE; i++)
    {
        fout << NEWVEC[i];
        if (i < NEWVEC_SIZE - 1)
            fout << " ";
    }
    fout << endl;
    fout << "Сумма всех элементов NEWVEC: " << total_sum << endl;
    if (min_positive_index != -1)
    {
        fout << "Наименьшее положительное значение: " << min_positive << endl;
        fout << "Элементы, равные минимальному положительному:" << endl;
        for (int i = 0; i < NEWVEC_SIZE; i++)
        {
            if (NEWVEC[i] == min_positive)
            {
                fout << " NEWVEC[" << i << "] = " << min_positive << " (позиция: " << i + 1 << ")"
                     << endl;
            }
        }
    }
    else
    {
    }
    fout << "В массиве NEWVEC нет положительных элементов" << endl;
    fout.close(); // закрываем выходной файл
    cout << "\nРезультаты сохранены в " << FNAME_RES << endl;
    return 0; // успешное завершение программы
}
