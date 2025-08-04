#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

const int numBytes = 512;

int main(int argc, char *argv[])
{
    // Accept a single command-line argument
    if (argc != 2)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }

    // Open the memory card
    FILE *card = fopen(argv[1], "r");
    if (card == NULL)
    {
        return 1;
    }
    // While there's still data left to read from the memory card
    uint8_t buffer[numBytes];
    int count = 0;
    char *filename = malloc(numBytes);

    FILE *img = NULL;
    while (fread(buffer, 1, numBytes, card) == numBytes)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && ((buffer[3] & 0xf0) == 0xe0))
        {
            if (count != 0 && img != NULL)
            {
                fclose(img);
            }
            if (filename != NULL || img != NULL)
            {
                sprintf(filename, "%03i.jpg", count);
                img = fopen(filename, "w");
                count++;
            }
        }
        if (img != NULL)
        {
            fwrite(buffer, 1, numBytes, img);
        }
    }
    fclose(img);
    free(filename);
    fclose(card);
}
