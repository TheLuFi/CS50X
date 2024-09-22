#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

    for (int a = 0; a < height; a++)
    {
        for (int b = 0; b < height + a + 3; b++)
        {
            if (b == height || b == height + 1 || a + b < height - 1)
            {
                printf(" ");
            }
            else
            {
                printf("#");
            }
        }
        printf("\n");
    }
}
