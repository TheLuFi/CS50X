#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    string phrase = get_string("Text: ");

    float L = (float) count_letters(phrase) / count_words(phrase) * 100;
    float S = (float) count_sentences(phrase) / count_words(phrase) * 100;

    int index = round(0.0588 * L - 0.296 * S - 15.8);
    int i = index;

    if (i >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (i < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", i);
    }
}

int count_letters(string text)
{
    int count = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (islower(text[i]) || isupper(text[i]))
        {
            count++;
        }
    }
    return count;
}

int count_words(string text)
{
    int count = 0;
    for (int i = 0, n = strlen(text); i <= n; i++)
    {
        if (isspace(text[i]) || text[i] == '\0')
        {
            count++;
        }
    }
    return count;
}

int count_sentences(string text)
{
    int count = 0;
    for (int i = 0, n = strlen(text); i <= n; i++)
    {
        if ((text[i]) == 33 || text[i] == 63 || text[i] == 46)
        {
            count++;
        }
    }
    return count;
}
