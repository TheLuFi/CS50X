// Implements a dictionary's functionality
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 128;
int nodesize = 0;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    node *n = table[hash(word)];

    while (n != NULL)
    {

        if (strcasecmp(word, n->word) == 0)
        {
            // free(n);
            return true;
        }
        n = n->next;
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    int leng = strlen(word);
    int sum = 0;
    if (leng < 2)
    {
        for (int a = 0; a < leng; a++)
        {
            sum += toupper(word[a]);
        }
    }
    else
    {
        for (int a = 0; a < 3; a++)
        {
            sum += toupper(word[a]);
        }
    }

    sum = sum % 26;

    return sum;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    char *word = malloc((LENGTH + 1) * sizeof(char));
    if (word == NULL)
    {
        free(word);
        return false;
    }
    // Open the dictionary file
    FILE *source = fopen(dictionary, "r");
    if (source == NULL)
    {
        free(word);
        return false;
    }
    // Read each word in the file
    while (fscanf(source, "%s", word) != EOF)
    {

        // Add each word to the hash table
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            free(word);
            free(n);
            return false;
        }
        n->next = NULL;
        strcpy(n->word, word);
        int index = hash(word);
        node *list = table[index];
        n->next = list;
        table[index] = n;
        nodesize++;
    }
    // Close the dictionary file
    free(word);
    fclose(source);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return nodesize;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int a = 0; a < N; a++)
    {
        while (table[a] != NULL)
        {
            node *tmp = table[a];
            table[a] = table[a]->next;

            free(tmp);
        }
    }
    return true;
}
