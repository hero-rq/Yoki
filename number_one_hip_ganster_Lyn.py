#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define FLAGSIZE_MAX 64
#define BUFFER_SIZE 8

char *buffer;
char *secret;

void init() {
    printf("Welcome to heap challenge!\n");
    buffer = (char *)malloc(BUFFER_SIZE);
    secret = (char *)malloc(BUFFER_SIZE);
    strncpy(buffer, "hello", BUFFER_SIZE);
    strncpy(secret, "world", BUFFER_SIZE);
}

void print_heap() {
    printf("Heap State:\n");
    printf("+-------------------+-------------+\n");
    printf("| Address           | Data        |\n");
    printf("+-------------------+-------------+\n");
    printf("| %p | %s       |\n", (void*)buffer, buffer);
    printf("| %p | %s       |\n", (void*)secret, secret);
    printf("+-------------------+-------------+\n");
    fflush(stdout);
}

void write_buffer() {
    printf("Enter data for buffer: ");
    fflush(stdout);
    scanf("%s", buffer); // Vulnerable to buffer overflow
}

void check_win() {
    if (strcmp(secret, "win") == 0) {
        printf("\nYOU WIN!\n");
        char flag[FLAGSIZE_MAX];
        FILE *f = fopen("flag.txt", "r");
        fgets(flag, FLAGSIZE_MAX, f);
        printf("Flag: %s\n", flag);
        fclose(f);
        fflush(stdout);
        exit(0);
    } else {
        printf("Try again!\n");
    }
}

int main() {
    init();
    int choice;

    while (1) {
        printf("\n1. Print Heap\n2. Write to Buffer\n3. Check Win\n4. Exit\n\nEnter your choice: ");
        scanf("%d", &choice);
        
        switch (choice) {
            case 1:
                print_heap();
                break;
            case 2:
                write_buffer();
                break;
            case 3:
                check_win();
                break;
            case 4:
                exit(0);
                break;
            default:
                printf("Invalid choice\n");
                break;
        }
    }

    return 0;
}

//gcc -o heap_challenge heap_challenge.c
// ./heap_challenge

//Vulnerability Explanation:
//The write_buffer function uses scanf("%s", buffer), which does not limit the input size, making it vulnerable to buffer overflow.
//By providing an input larger than 7 characters (plus null terminator), the secret variable can be overwritten.
//If secret is overwritten with "win", the check_win function will print the flag.

//modified code 
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define FLAGSIZE_MAX 64
#define BUFFER_SIZE 8

char *buffer;
char *secret;

void init() {
    printf("Welcome to heap challenge!\n");
    buffer = (char *)malloc(BUFFER_SIZE);
    secret = (char *)malloc(BUFFER_SIZE);
    strncpy(buffer, "hello", BUFFER_SIZE);
    strncpy(secret, "world", BUFFER_SIZE);
}

void print_heap() {
    printf("Heap State:\n");
    printf("+-------------------+-------------+\n");
    printf("| Address           | Data        |\n");
    printf("+-------------------+-------------+\n");
    printf("| %p | %s       |\n", (void*)buffer, buffer);
    printf("| %p | %s       |\n", (void*)secret, secret);
    printf("+-------------------+-------------+\n");
    fflush(stdout);
}

void write_buffer() {
    printf("Enter data for buffer: ");
    fflush(stdout);
    scanf("%8s", buffer); // Vulnerable to buffer overflow
}

void check_win() {
    if (strcmp(secret, "win") == 0) {
        printf("\nYOU WIN!\n");
        char flag[FLAGSIZE_MAX];
        FILE *f = fopen("flag.txt", "r");
        if (f) {
            fgets(flag, FLAGSIZE_MAX, f);
            printf("Flag: %s\n", flag);
            fclose(f);
        } else {
            printf("Flag file not found!\n");
        }
        fflush(stdout);
        exit(0);
    } else {
        printf("Try again!\n");
    }
}

int main() {
    init();
    int choice;

    while (1) {
        printf("\n1. Print Heap\n2. Write to Buffer\n3. Check Win\n4. Exit\n\nEnter your choice: ");
        scanf("%d", &choice);
        
        switch (choice) {
            case 1:
                print_heap();
                break;
            case 2:
                write_buffer();
                break;
            case 3:
                check_win();
                break;
            case 4:
                exit(0);
                break;
            default:
                printf("Invalid choice\n");
                break;
        }
    }

    return 0;
}

//do you think this is the right modified code? 
// why? or why not ? 
