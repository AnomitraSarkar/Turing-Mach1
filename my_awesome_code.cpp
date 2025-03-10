#include <iostream>

using namespace std;

// Custom Pseudo-Random Number Generator using Linear Congruential Generator (LCG)
class MyPRNG {
private:
    unsigned int seed;

public:
    MyPRNG(unsigned int s = 12345) : seed(s) {}

    // Generates a pseudo-random number between 0 and max
    unsigned int next(unsigned int max) {
        // LCG parameters
        const unsigned int a = 1664525;      // Multiplier
        const unsigned int c = 1013904223;   // Increment
        const unsigned int m = 4294967296;   // Modulus (2^32)

        seed = (a * seed + c) % m;           // Update seed
        return seed % max;                   // Return result between 0 and max-1
    }
};

int main() {
    const int numFlips = 25000;
    int heads = 0, tails = 0;

    // Create an instance of the custom PRNG with a seed
    MyPRNG prng(42);  // You can change the seed value for different results

    // Simulate coin flips
    for (int i = 0; i < numFlips; ++i) {
        if (prng.next(2) == 0)
            ++heads;
        else
            ++tails;
    }

    // Output results
    std::cout << "Total Flips: " << numFlips << "\n";
    std::cout << "Heads: " << heads << "\n";
    std::cout << "Tails: " << tails << "\n";

    return 0;
}

~ contributed by anomitra sarkar