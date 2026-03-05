#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

int main() {
  srand(time(NULL));
  const char name[] = "Rybin Timofei Vacheslavovich";
  // char controlString = "";
  for (size_t i = 0; i < strlen(name); i++) {
    printf("%d", name[i]);
  }

  for(int i = 0; i < 5000; i++) {
    printf("%d", rand() % 10);
  }

  for (size_t i = 0; i < strlen(name); i++) {
    printf("%d", name[i]);
  }

  for(int i = 0; i < 5000; i++) {
    printf("%d", rand() % 10);
  }

  for (size_t i = 0; i < strlen(name); i++) {
    printf("%d", name[i]);
  }

  return 0;
}
