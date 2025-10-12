/**
 * @file simple_program.c
 * @brief Simple C program for testing obfuscation
 * 
 * This is a basic C program that can be used to test
 * the obfuscation passes.
 */

#include <stdio.h>
#include <string.h>

/**
 * @brief Simple function that performs basic operations
 * @param x Input value
 * @return Computed result
 */
int compute(int x) {
    int result = 0;
    
    // Simple computation
    for (int i = 0; i < x; i++) {
        result += i * 2;
    }
    
    return result;
}

/**
 * @brief Function with string operations
 * @param message Input message
 */
void print_message(const char* message) {
    printf("Message: %s\n", message);
}

/**
 * @brief Main function
 * @return Exit status
 */
int main() {
    const char* secret = "This is a secret message";
    int value = 10;
    
    printf("Starting computation...\n");
    
    int result = compute(value);
    printf("Result: %d\n", result);
    
    print_message(secret);
    
    return 0;
}
