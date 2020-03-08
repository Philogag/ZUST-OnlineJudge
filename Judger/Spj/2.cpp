#include <cstdio>
using namespace std;

#define AC 0
#define WA 1
#define ERROR -1

int spj(FILE *input, FILE *user_output);

void close_file(FILE *f)
{
    if (f != NULL)
    {
        fclose(f);
    }
}

int main(int argc, char *args[])
{
    FILE *input = NULL, *user_output = NULL;
    int result;
    if (argc != 3)
    {
        printf("Usage: spj x.in x.out\n");
        return ERROR;
    }
    input = fopen(args[1], "r");
    user_output = fopen(args[2], "r");
    if (input == NULL || user_output == NULL)
    {
        printf("Failed to open output file\n");
        close_file(input);
        close_file(user_output);
        return ERROR;
    }

    result = spj(input, user_output);
    printf("result: %d\n", result);

    close_file(input);
    close_file(user_output);
    return result;
}

int spj(FILE *input, FILE *user_output)
{
    int a, b, c;
    fscanf(input, "%d %d", &a, &b);
    fscanf(user_output, "%d", &c);
    if(a + b != c)
        return WA;
    else
        return AC;
}