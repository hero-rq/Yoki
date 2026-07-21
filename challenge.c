#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

static void setup_io(void) {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
}

__attribute__((noinline))
static void print_banner(void) {
    puts("==================================");
    puts("      Archive Gate Validator      ");
    puts("==================================");
}

__attribute__((noinline))
static void maintenance_console(void) {
    char note[64];

    puts("[validator] Add an operator note:");
    read(STDIN_FILENO, note, 200);
    puts("[validator] Note recorded.");
}

__attribute__((noinline, used))
static void emergency_archive_unlock(void) {
    FILE *fp;
    char flag[128];

    puts("[+] Emergency archive unlock accepted.");

    fp = fopen("flag.txt", "r");
    if (fp == NULL) {
        puts("[-] flag.txt was not found.");
        puts("    Create it in the same directory as the binary.");
        exit(1);
    }

    if (fgets(flag, sizeof(flag), fp) == NULL) {
        puts("[-] Could not read flag.txt.");
        fclose(fp);
        exit(1);
    }

    fclose(fp);
    printf("[+] Archive secret: %s", flag);
}

int main(void) {
    setup_io();
    print_banner();
    maintenance_console();
    puts("[validator] Session closed.");
    return 0;
}
