/****************************************************************
 * КАФЕДРА № 304 1 КУРС *
 *---------------------------------------------------------------*
 * Project Type : Win32 Console Application *
 * Project Name : First project *
 * File Name : First.cpp *
 * Language : C/C++ *
 * Programmer(s) : Рыбин.Т.В *
 * Modifyed By : *
 * Lit source : *
 * Created : 19/12/25 *
 * Last Revision : 19/12/25 *
 * Comment(s) : Сумма ряда. *
 ****************************************************************/
#include <iostream>     // ввод вывод 
#include <fstream>      // для работы с файлами (ifstream, ofstream)
using namespace std;    

// const char *FNAME = "tests/test1.txt";       // Цель теста 1: проверить работу программы при отстутствии инпут файла 
// const char *FNAME = "tests/test2.txt";       // Цель теста 2: проверить работу программы при пустом инпут файле 
// const char *FNAME = "tests/test3.txt";       // Цель теста 3: проверить работу программы при неккоректно параметре N 
// const char *FNAME = "tests/test4.txt";       // Цель теста 4: проверить работу программы при параметре N > 7
// const char *FNAME = "tests/test5.txt";       // Цель теста 5: проверить работу программы при параметре N < 0
// const char *FNAME = "tests/test6.txt";       // Цель теста 6: проверить работу программы при пустом параметре M
// const char *FNAME = "tests/test7.txt";       // Цель теста 7: проверить работу программы при неккоректно параметре M
// const char *FNAME = "tests/test8.txt";       // Цель теста 8: проверить работу программы при параметре M > 7
// const char *FNAME = "tests/test9.txt";       // Цель теста 9: проверить работу программы при параметре M < 0
// const char *FNAME = "tests/test10.txt";       // Цель теста 10: проверить работу теста при отстутствии i-той строки в VEC[0..6]
// const char *FNAME = "tests/test11.txt";       // Цель теста 11: проверить работу теста при неккоректной i-той строки в VEC[0..6]
// const char *FNAME = "tests/test12.txt";       // Цель теста 12: проверить работоспособность программы при корректном вводе чисел
// const char *FNAME = "tests/test13.txt";       // Цель теста 13: проверить работоспособность программы при корректном вводе чисел
// const char *FNAME = "tests/test14.txt";       // Цель теста 14: проверить работоспособность программы при корректном вводе чисел
const char *FNAME = "tests/test15.txt";       // Цель теста 15: проверить работоспособность программы при корректном вводе чисел


const char *FNAME_RES = "result.txt";  // имя выходного файла для результатов
const int VEC_SIZE = 7;                // размер исходного массива VEC (VEC[0]...VEC[6])
const int NEWVEC_SIZE = 7;             // размер нового массива (равен размеру VEC)

/*******************************************************************/
/*               О С Н О В Н А Я     П Р О Г Р А М М А             */
/*******************************************************************/

int main()
{
    // Объявление переменных
    // Обьявление переменных N, M, по заданию 
    int N;                   // параметр N из файла
    int M;                   // параметр M из файла
    // обьявление массивов для задания 
    float VEC[VEC_SIZE];     // исходный массив из 7 элементов
    float NEWVEC[NEWVEC_SIZE]; // новый массив
    // Открытие потоков 
    ifstream fin;            // поток для чтения из входного файла
    ofstream fout;           // поток для записи в выходной файл
    // Для циклов 
    int i;                   // переменная для циклов
    float sum_negative_first_N = 0;  // сумма отрицательных элементов VEC среди первых N
    float total_sum = 0;            // сумма всех элементов NEWVEC

    float sum_positive_first_N = 0;  // сумма положительных элементов NEWVEC среди первых N\

    float sum_negative_last_M = 0;   // сумма отрицательных элементов NEWVEC среди последних M

    float min_positive;              // наименьший положительный элемент
    int min_positive_index;     // индекс наименьшего положительного элемента
    
    // Открытие файлов
    fin.open(FNAME);     // открываем поток для чтения из входного файла
    fout.open(FNAME_RES); // открываем поток для записи в выходной файл
    
    // Проверка открытия входного файла 
    fin;
    if (fin.fail())
    {
        cout << "Ошибка: Файл " << FNAME << " не найден!\n";

        return 1; 
    }
    
    // Проверка, что файл не пустой
    if (fin.peek() == EOF)
    {
        cout << "Ошибка: файл " << FNAME << " пустой\n";
        fin.close();
        return 2;
    }
    
    // Чтение данных из файла с проверками
    // Чтение N
    fin >> N;
    if (fin.fail())
    {
        cout << "Ошибка чтения N из файла: неверный формат данных\n";
        fin.close();
        return 3;
    }
    
    // Проверка корректности N
    if (N < 0 || N > VEC_SIZE)
    {
        cout << "Ошибка: N должно быть в диапазоне от 0 до " << VEC_SIZE << "\n";
        fin.close();
        return 4;
    }
    
    // Чтение M
    fin >> M;
    if (fin.fail())
    {
        if (fin.eof())
        {
            cout << "Ошибка чтения M из файла: достигнут конец файла\n";
        }
        else
        {
            cout << "Ошибка чтения M из файла: неверный формат данных\n";
        }
        fin.close();
        return 5;
    }
    
    // Проверка корректности M
    if (M < 0 || M > VEC_SIZE)
    {
        cout << "Ошибка: M должно быть в диапазоне от 0 до " << VEC_SIZE << "\n";
        fin.close();
        return 6;
    }
    
    // Чтение массива VEC
    for (i = 0; i < VEC_SIZE; i++)
    {
        fin >> VEC[i];
        if (fin.fail())
        {
            cout << "Ошибка чтения элемента VEC[" << i << "] из файла\n";
            if (fin.eof())
            {
                cout << "недостаточно данных в файле (достигнут конец файла)\n";
            }
            else
            {
                cout << "Ошибка форматирования данных\n";
            }
            fin.close();
            return 7;
        }
    }
    
    fin.close(); // закрываем входной файл после чтения

    // ВЫВОД ВХОДНЫХ ДАННЫХ В КОНСОЛЬ
    cout << "=== ВХОДНЫЕ ДАННЫЕ ===" << endl;
    cout << "N = " << N << ", M = " << M << endl;
    cout << "Массив VEC: ";
    for (i = 0; i < VEC_SIZE; i++)
    {
        cout << VEC[i];
        cout << " ";
    }
    cout << endl << endl;
    
    // 2. Формирование нового массива NEWVEC
    
    for (i = 0; i < N; i++)
    {
        if (VEC[i] < 0)
        {
            sum_negative_first_N += VEC[i];
        }
    }
    
    for (i = 0; i < NEWVEC_SIZE; i++)
    {
        NEWVEC[i] = VEC[i] + sum_negative_first_N; 
    }
    
    // 3. Суммирование всех элементов сформированного массива
    for (i = 0; i < NEWVEC_SIZE; i++)
    {
        total_sum += NEWVEC[i];
    }
    
    // Суммирование положительных элементов NEWVEC среди первых N
    for (i = 0; i < N; i++)
    {
        if (NEWVEC[i] > 0)
        {
            sum_positive_first_N += NEWVEC[i];
        }
    }
    
    // Суммирование отрицательных элементов NEWVEC среди последних M
    for (i = VEC_SIZE - M; i < VEC_SIZE; i++)
    {
        if (NEWVEC[i] < 0)
        {
            sum_negative_last_M += NEWVEC[i];
        }
    }
    
    // 4. Печать сформированного массива и значений сумм
    cout << "=== РЕЗУЛЬТАТЫ ===" << endl;
    cout << "Сформированный массив NEWVEC: ";
    for (int i = 0; i < NEWVEC_SIZE; i++)
    {
        cout << NEWVEC[i];
        cout << " ";
    }
    cout << endl;
    cout << "Сумма всех элементов NEWVEC: " << total_sum << endl;
    cout << "Сумма положительных элементов NEWVEC среди первых N: " << sum_positive_first_N << endl;
    cout << "Сумма отрицательных элементов NEWVEC среди последних M: " << sum_negative_last_M << endl;
    
    // 5. Определение индекса наименьшего положительного элемента NEWVEC
    // Поиск в диапазоне от N до M (включительно)
    min_positive_index = -1;
    for (i = N; i <= M; i++)
    {
        if (NEWVEC[i] > 0 && (min_positive_index == -1 || NEWVEC[i] < min_positive))
        {
            min_positive = NEWVEC[i];
            min_positive_index = i;
        }
    }
    
    // Вывод результата поиска наименьшего положительного элемента
    if (min_positive_index != -1)
    {
        cout << "Наименьший положительный элемент NEWVEC (в диапазоне от N до M): NEWVEC[" << min_positive_index 
             << "] = " << min_positive << endl;
    }
    else
    {
        cout << "В массиве NEWVEC нет положительных элементов в диапазоне от N до M" << endl;
    }
    
    // Запись результатов в файл
    fout << "=== РЕЗУЛЬТАТЫ ===" << endl;
    fout << "Входные данные:" << endl;
    fout << "N = " << N << ", M = " << M << endl;
    fout << "Исходный массив VEC: ";
    for (i = 0; i < VEC_SIZE; i++)
    {
        fout << VEC[i];
        fout << " ";
    }
    fout << endl << endl;
    
    fout << "Сформированный массив NEWVEC: ";
    for (i = 0; i < NEWVEC_SIZE; i++)
    {
        fout << NEWVEC[i];
        fout << " ";
    }
    fout << endl;
    fout << "Сумма всех элементов NEWVEC: " << total_sum << endl;
    fout << "Сумма положительных элементов NEWVEC среди первых N: " << sum_positive_first_N << endl;
    fout << "Сумма отрицательных элементов NEWVEC среди последних M: " << sum_negative_last_M << endl;

    
    if (min_positive_index != -1)
    {
        fout << "Наименьший положительный элемент NEWVEC (в диапазоне от N до M): NEWVEC[" << min_positive_index 
             << "] = " << min_positive << endl;
    }
    else
    {
        fout << "В массиве NEWVEC нет положительных элементов в диапазоне от N до M" << endl;
    }
    
    fout.close();  // закрываем выходной файл
    
    cout << "\nРезультаты сохранены в " << FNAME_RES << endl;
    
    return 0;  // успешное завершение программы
}

