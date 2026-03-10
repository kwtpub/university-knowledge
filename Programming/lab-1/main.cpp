/****************************************************************
*
* Project Type  : Win32 Console Application
* Project Name  : Lab 1, Task 3
* File Name     : main.cpp
* Language      : C/C++
* Programmer    : Рыбин Т.В. Калинин.К.Е
* Created       : 06/03/26
* Comment       : Символьные данные. Вариант 4.
*
****************************************************************/

#include <fstream>  // для работы с файлами (ifstream)
#include <iostream> // ввод/вывод

using namespace std;

/*******************************************************************/
/*                 О С Н О В Н А Я   П Р О Г Р А М М А            */
/*******************************************************************/

int main()
{
    // Выберите нужный набор входных данных:
    const int MAX_LINE_LEN = 256; // максимальная длина строки
    // const char* inputPath = "tests/input1.txt";  // Тест 1: общие слова есть, символ чаще в 1-й строке.
    // const char* inputPath = "tests/input2.txt";  // Тест 2: общих слов нет, символ чаще во 2-й строке.
    const char* inputPath = "tests/input3.txt";     // Тест 3: общих слов нет, частоты символа равны.
    // const char* inputPath = "tests/input4.txt";  // Тест 4: дубли слов в первой строке.
    // const char* inputPath = "tests/input5.txt";  // Тест 5: лишние пробелы в строках.
    // const char* inputPath = "tests/input6.txt";  // Тест 6 (ошибка): файл пустой.
    // const char* inputPath = "tests/input7.txt";  // Тест 7 (ошибка): есть символ, но нет строк.
    // const char* inputPath = "tests/input8.txt";  // Тест 8 (ошибка): есть символ и одна строка, вторая отсутствует.
    // const char* inputPath = "tests/input9.txt";  // Тест 9 (ошибка): файл не существует.
    // const char* inputPath = "tests/input10.txt"; // Тест 10 (ошибка): первый символ — пробел/таб/перенос строки.

    // Файл и входные данные
    ifstream fin;                   // поток для чтения входного файла
    char symbol;                    // заданный символ
    char firstLine[MAX_LINE_LEN];   // первая строка слов
    char secondLine[MAX_LINE_LEN];  // вторая строка слов

    // Задание 1: общие слова
    bool hasCommonWords;            // флаг наличия общих слов
    bool seenBefore;                // флаг: слово уже встречалось раньше в первой строке
    bool foundInSecond;             // флаг: слово найдено во второй строке
    bool wordsEqual;                // флаг: два слова совпадают

    // Задание 2: частота символа
    int firstCount;                 // количество вхождений символа в первой строке
    int secondCount;                // количество вхождений символа во второй строке

    // Вспомогательные индексы
    int i;                          // позиция в первой строке (перебор слов)
    int j;                          // позиция для поиска дублей / во второй строке
    int bw1, ew1;                   // границы текущего слова в первой строке
    int bw2, ew2;                   // границы слова при сравнении
    int k;                          // индекс при посимвольном сравнении

    // Открытие входного файла
    fin.open(inputPath);

    // Проверка открытия входного файла
    if (fin.fail()) {
        cout << "Ошибка: Файл " << inputPath << " не найден!\n";
        return 1;
    }

    // Проверка, что файл не пустой
    if (fin.peek() == EOF) {
        cout << "Ошибка: файл " << inputPath << " пустой\n";
        fin.close();
        return 2;
    }

    // Чтение символа
    // get() - читает ровно один байт, включая пробелы и переносы строк
    fin.get(symbol);
    if (fin.fail() || symbol == ' ' || symbol == '\t' || symbol == '\n') {
        cout << "Ошибка чтения символа из файла: неверный формат данных\n";
        fin.close();
        return 3;
    }

    // Переход на следующую строку перед getline
    // a >> symbol
    // \n >> tmp
    char tmp;
    fin.get(tmp);
    // пропускаем '\n' после символа

    // Чтение первой строки
    fin.getline(firstLine, MAX_LINE_LEN);

    if (fin.fail()) {
        cout << "Ошибка чтения первой строки из файла\n";
        cout << "недостаточно данных в файле (достигнут конец файла)\n";
        fin.close();
        return 4;
    }

    // Чтение второй строки
    fin.getline(secondLine, MAX_LINE_LEN);
    if (fin.fail()) {
        cout << "Ошибка чтения второй строки из файла\n";
        if (fin.eof()) {
            cout << "недостаточно данных в файле (достигнут конец файла)\n";
        }
        else {
            cout << "Ошибка форматирования данных\n";
        }
        fin.close();
        return 5;
    }

    fin.close(); // закрываем входной файл после чтения

    // Вывод входных данных
    cout << "Символ: " << symbol << '\n';
    cout << "Первая строка: " << firstLine << '\n';
    cout << "Вторая строка: " << secondLine << '\n';

    /*******************************************************************/
    /* 1. Слова, встречающиеся в обеих строках                         */
    /*******************************************************************/

    cout << "\nСлова, встречающиеся в обеих строках:" << '\n';

    i = 0;
    hasCommonWords = false;

    // Перебираем слова первой строки
    while (firstLine[i] != '\0') {
        // Пропускаем пробелы, находим начало слова
        while (firstLine[i] <= ' ' && firstLine[i] != '\0') {
            i++;
        }
        if (firstLine[i] == '\0') {
            break;
        }

        // Границы текущего слова в firstLine
        bw1 = i;
        while (firstLine[i] != ' ' && firstLine[i] != '\0') {
            i++;
        }
        ew1 = i - 1;

        // Проверяем, встречалось ли это слово раньше в firstLine (до bw1)
        seenBefore = false;
        j = 0;
        while (j < bw1 && !seenBefore) {
            while (firstLine[j] <= ' ' && j < bw1) {
                j++;
            }
            if (j >= bw1) {
                break;
            }
            bw2 = j;
            while (firstLine[j] != ' ' && firstLine[j] != '\0' && j < bw1) {
                j++;
            }
            ew2 = j - 1;

            // Сравниваем слова по границам
            if (ew1 - bw1 == ew2 - bw2) {
                wordsEqual = true;
                for (k = 0; k <= ew1 - bw1; k++) {
                    if (firstLine[bw1 + k] != firstLine[bw2 + k]) {
                        wordsEqual = false;
                        break;
                    }
                }
                if (wordsEqual) {
                    seenBefore = true;
                }
            }
        }
        if (seenBefore) {
            continue;
        }

        // Ищем слово из firstLine[bw1..ew1] во второй строке
        foundInSecond = false;
        j = 0;
        while (secondLine[j] != '\0' && !foundInSecond) {
            while (secondLine[j] <= ' ' && secondLine[j] != '\0') {
                j++;
            }
            if (secondLine[j] == '\0') {
                break;
            }
            bw2 = j;
            while (secondLine[j] != ' ' && secondLine[j] != '\0') {
                j++;
            }
            ew2 = j - 1;

            // Сравниваем слова по границам
            if (ew1 - bw1 == ew2 - bw2) {
                wordsEqual = true;
                for (k = 0; k <= ew1 - bw1; k++) {
                    if (firstLine[bw1 + k] != secondLine[bw2 + k]) {
                        wordsEqual = false;
                        break;
                    }
                }
                if (wordsEqual) {
                    foundInSecond = true;
                }
            }
        }

        if (foundInSecond) {
            // Выводим слово по границам
            for (k = bw1; k <= ew1; k++) {
                cout << firstLine[k];
            }
            cout << '\n';
            hasCommonWords = true;
        }
    }

    if (!hasCommonWords) {
        cout << "(общих слов нет)" << '\n';
    }

    /*******************************************************************/
    /* 2. Строка, в которой символ встречается чаще                    */
    /*******************************************************************/

    cout << "\nСравнение частоты символа:" << '\n';

    firstCount = 0;
    secondCount = 0;

    i = 0;
    while (firstLine[i] != '\0') {
        if (firstLine[i] == symbol) {
            firstCount++;
        }
        i++;
    }

    i = 0;
    while (secondLine[i] != '\0') {
        if (secondLine[i] == symbol) {
            secondCount++;
        }
        i++;
    }

    if (firstCount > secondCount) {
        cout << "Символ '" << symbol << "' чаще встречается в первой строке: "
             << firstCount << " против " << secondCount << "." << '\n';
    }
    else if (secondCount > firstCount) {
        cout << "Символ '" << symbol << "' чаще встречается во второй строке: "
             << secondCount << " против " << firstCount << "." << '\n';
    }
    else {
        cout << "Символ '" << symbol << "' встречается одинаково в обеих строках: "
             << firstCount << "." << '\n';
    }

    return 0;
}
