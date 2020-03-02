#include <stdio.h>

int main(void)
{
    char answer[100];

    printf("What's Your Name?\n");
    scanf("%s", answer);
    printf("Hello %s!", answer);
    return 0;
}
