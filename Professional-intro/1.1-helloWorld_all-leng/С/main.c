#include <stdio.h>
#include <wchar.h>
#include <locale.h>

const int CHAR_SIZE = 304;   // 0–303
const int INT_SIZE = 25;
const int FLOAT_SIZE = 25;

int main() {
    setlocale(LC_ALL, "");

    // === 1–2. Объявление массивов ===
    char charArray[CHAR_SIZE]; // массив не инициализируется, остаются буферные значения
    int intArray[INT_SIZE];
    float floatArray[FLOAT_SIZE];

    // Заполнение числовых массивов
    for (int i = 0; i < INT_SIZE; i++)
        intArray[i] = i + 1;

    for (int i = 0; i < FLOAT_SIZE; i++)
        floatArray[i] = (float)(i + 1) / 2;

    // === Вывод числовых массивов ===
    printf("=== Целочисленный массив ===\n");
    for (int i = 0; i < INT_SIZE; i++)
        printf("%2d - %d\n", i, intArray[i]);
  // %2d означает, что будет выведено целое число с минимальной шириной поля 2 
  // Второй %d означает обычный вывод целого числа без ограничения ширины.

    printf("\n=== Вещественный массив ===\n");
    for (int i = 0; i < FLOAT_SIZE; i++)
        printf("%2d - %.2f\n", i, floatArray[i]);
/*
 * %2d — вывод целого числа с минимальной шириной поля 2 символа, при
 * необходимости дополняется пробелами слева.
 * " - " — просто текст, который выводится как есть. 
 * %.2f — вывод числа с плавающей точкой (float или double) с точностью до 2 знаков после десятичной точки. 
*/
    // === Символьный массив (ASCII номер - символ) ===
    printf("\n=== Символьный массив (ASCII номер - символ) ===\n");
    for (int i = 0; i < CHAR_SIZE; i++) {
        unsigned char c = charArray[i];
        if (c >= 32 && c <= 126)
            printf("%3u - %c\t", c, c);
        else
            printf("%3u - .\t", c);
        if ((i + 1) % 5 == 0) printf("\n");
    }

    // === 3. Работа с фамилией Рыбин ===
    wchar_t surname_cyr1[] = L"Рыбин";                        // 3.1 // wchar потому что символы занимают больше одного байьа
    wchar_t surname_cyr2[] = {L'Р', L'ы', L'б', L'и', L'н', L'\0'}; // 3.2
    char surname_lat1[] = "Rybin";                            // 3.3
    char surname_lat2[] = {'R','y','b','i','n','\0'};         // 3.4
    // char surname_lat3[] = {'Р', 'ы','\0'};         // 3.4

    // 3.5 Размеры строк
    printf("\nРазмеры строк:\n");
    wprintf(L"surname_cyr1: %lu байт\n", sizeof(surname_cyr1));
    wprintf(L"surname_cyr2: %lu байт\n", sizeof(surname_cyr2));
    printf("surname_lat1: %lu байт\n", sizeof(surname_lat1));
    printf("surname_lat2: %lu байт\n", sizeof(surname_lat2));

    // 3.6 Вывод строк
    printf("\nВывод латиницей с %%s:\n");
    printf("%s\n%s\n", surname_lat1, surname_lat2);

    wprintf(L"\nВывод кириллицей с %%ls:\n");
    wprintf(L"%ls\n%ls\n", surname_cyr1, surname_cyr2);

    printf("\nВывод с %%c (латиница):\n");
    for (int i = 0; surname_lat1[i] != '\0'; i++)
        printf("%c ", surname_lat1[i]);
    printf("\n");

    wprintf(L"\nВывод с %%lc (кириллица):\n");
    for (int i = 0; surname_cyr1[i] != L'\0'; i++)
        wprintf(L"%lc ", surname_cyr1[i]);
    wprintf(L"\n");

    // 3.7 Дважды латиницей с \0
    printf("\n3.7 Дважды латиницей с \\0:\n");
    printf("%s\0%s\n", surname_lat1, surname_lat1);

    // 3.8 Кириллица + латиница с \r
    printf("\n3.8 Кириллица + латиница с \\r \n");
    printf("%s\r%s\n", surname_cyr1, surname_lat1);

    // 3.9 В кавычках
    printf("\n3.9 В кавычках:\n");
    printf("\"%s\"\n", surname_lat1);

    // 3.10 Первые три буквы N раз
    int N = 20;
    printf("\n3.10 Первые три буквы %d раз:\n", N);
    for (int i = 0; i < N; i++)
        printf("%.3s ", surname_lat1);
    printf("\n");

    return 0;
}
