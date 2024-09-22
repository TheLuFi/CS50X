#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // TODO: Prompt for start size
    int startsize;
    do
    {
        startsize = get_int("Start size: ");
    }
    while (startsize < 9);

    // TODO: Prompt for end size
    int endsize;
    do
    {
        endsize = get_int("End size: ");
    }
    while (startsize > endsize);

    // TODO: Calculate number of years until we reach threshold
    int total = 0;
    int n = 0;
    if (startsize != endsize)
    {
        for (n = 0; total < endsize; n++)
        {
            total = startsize + (startsize / 3) - (startsize / 4);
            startsize = total;
        }
    }

    // TODO: Print number of years
    printf("Years: %i\n", n);
}
