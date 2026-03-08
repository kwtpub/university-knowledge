/****************************************************************
*
* Project Type  : Win32 Console Application
* Project Name  : Lab 1, Task 3
* File Name     : main.cpp
* Language      : C/C++
* Programmer    : student
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
    const int MAX_WORD_LEN = 64;  // максимальная длина одного слова
    const int MAX_WORDS = 128;    // максимум слов для массива уже выведенных
    // const char* inputPath = "tests/input1.txt"; // Тест 1: общие слова есть, символ чаще в 1-й строке.
    // const char* inputPath = "tests/input2.txt"; // Тест 2: общих слов нет, символ чаще во 2-й строке.
    // const char* inputPath = "tests/input3.txt"; // Тест 3: общих слов нет, частоты символа равны.
    // const char* inputPath = "tests/input4.txt"; // Тест 4: дубли слов в первой строке.
    // const char* inputPath = "tests/input5.txt"; // Тест 5: лишние пробелы в строках.
    // const char* inputPath = "tests/input6.txt"; // Тест 6 (ошибка): файл пустой.
    // const char* inputPath = "tests/input7.txt"; // Тест 7 (ошибка): есть символ, но нет строк.
    // const char* inputPath = "tests/input8.txt"; // Тест 8 (ошибка): есть символ и одна строка, вторая отсутствует.
    // const char* inputPath = "tests/input9.txt"; // Тест 9 (ошибка): файл не существует.

    // Файл и входные данные
    ifstream fin;                               // поток для чтения входного файла
    char symbol;                                // заданный символ
    char firstLine[MAX_LINE_LEN];               // первая строка слов
    char secondLine[MAX_LINE_LEN];              // вторая строка слов

    // Задание 1: общие слова
    char word[MAX_WORD_LEN];                    // текущее слово из первой строки
    char word2[MAX_WORD_LEN];                   // текущее слово из второй строки
    char printedWords[MAX_WORDS][MAX_WORD_LEN]; // уже выведенные слова (для устранения дублей)
    int printedCount;                           // количество уже выведенных слов
    bool hasCommonWords;                        // флаг наличия общих слов
    bool alreadyPrinted;                        // флаг: слово уже выводилось
    bool foundInSecond;                         // флаг: слово найдено во второй строке

    // Задание 2: частота символа
    int firstCount;                             // количество вхождений символа в первой строке
    int secondCount;                            // количество вхождений символа во второй строке

    // Вспомогательные индексы
    int pos1;                                   // позиция в первой строке
    int pos2;                                   // позиция во второй строке
    int wi;                                     // индекс при записи символов в слово
    int i;                                      // счётчик цикла
    int ci;                                     // индекс при посимвольном сравнении

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
    fin >> symbol;
    if (fin.fail()) {
        cout << "Ошибка чтения символа из файла: неверный формат данных\n";
        fin.close();
        return 3;
    }

    // Переход на следующую строку перед getline
    fin.ignore('\n');

    // Чтение первой строки
    if (!fin.getline(firstLine, MAX_LINE_LEN)) {
        cout << "Ошибка чтения первой строки из файла\n";
        if (fin.eof()) {
            cout << "недостаточно данных в файле (достигнут конец файла)\n";
        }
        else {
            cout << "Ошибка форматирования данных\n";
        }
        fin.close();
        return 4;
    }

    // Чтение второй строки
    if (!fin.getline(secondLine, MAX_LINE_LEN)) {
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

    pos1 = 0;
    printedCount = 0;
    hasCommonWords = false;

    // Перебираем слова первой строки
    while (true) {
        // Пропускаем пробелы
        while (firstLine[pos1] != '\0' && firstLine[pos1] == ' ') {
            ++pos1;
        }
        if (firstLine[pos1] == '\0') {
            break;
        }

        // Читаем слово из первой строки
        wi = 0;
        while (firstLine[pos1] != '\0' && firstLine[pos1] != ' ') {
            if (wi < MAX_WORD_LEN - 1) {
                word[wi] = firstLine[pos1];
                ++wi;
            }
            ++pos1;
        }
        word[wi] = '\0';

        // Проверяем, не выводили ли это слово уже
        alreadyPrinted = false;
        for (i = 0; i < printedCount; ++i) {
            ci = 0;
            while (word[ci] != '\0' && printedWords[i][ci] != '\0') {
                if (word[ci] != printedWords[i][ci]) {
                    break;
                }
                ++ci;
            }
            if (word[ci] == printedWords[i][ci]) {
                alreadyPrinted = true;
                break;
            }
        }
        if (alreadyPrinted) {
            continue;
        }

        // Ищем слово во второй строке
        foundInSecond = false;
        pos2 = 0;

        while (true) {
            while (secondLine[pos2] != '\0' && secondLine[pos2] == ' ') {
                ++pos2;
            }
            if (secondLine[pos2] == '\0') {
                break;
            }

            wi = 0;
            while (secondLine[pos2] != '\0' && secondLine[pos2] != ' ') {
                if (wi < MAX_WORD_LEN - 1) {
                    word2[wi] = secondLine[pos2];
                    ++wi;
                }
                ++pos2;
            }
            word2[wi] = '\0';

            // Сравниваем word и word2
            ci = 0;
            while (word[ci] != '\0' && word2[ci] != '\0') {
                if (word[ci] != word2[ci]) {
                    break;
                }
                ++ci;
            }
            if (word[ci] == word2[ci]) {
                foundInSecond = true;
                break;
            }
        }

        if (foundInSecond) {
            cout << word << '\n';
            hasCommonWords = true;

            // Запоминаем слово чтобы не выводить дубли
            if (printedCount < MAX_WORDS) {
                ci = 0;
                while (word[ci] != '\0' && ci < MAX_WORD_LEN - 1) {
                    printedWords[printedCount][ci] = word[ci];
                    ++ci;
                }
                printedWords[printedCount][ci] = '\0';
                ++printedCount;
            }
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
            ++firstCount;
        }
        ++i;
    }

    i = 0;
    while (secondLine[i] != '\0') {
        if (secondLine[i] == symbol) {
            ++secondCount;
        }
        ++i;
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
