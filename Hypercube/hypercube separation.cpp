// Program that calculates the mean hitting time as a function of node separation and gives a file: separacion.txt

#include <fstream> 
#include <string>
#include <iostream>
#include <random>
#include <chrono>
#include <cmath>
using namespace std;

#define N 14
#define sim 100000

double random_walk();
long long combinatorio(int n, int x);
int separacion(int s);
string vertice[N];

int main()
{

random_walk();



return 0;

}

// Function used to calculate the hitting time computationally
double random_walk()
{
    int i, j, k, t, s, unos;
    double media, cuadrado, desv, contador[N+1];
    ofstream separacion_file("separacion.txt");


    // We initialize the initial vertex as the string with all 0's

    // We also initialize the counter of 1's as 0
    for(i = 0; i <= N; i++) contador[i] = 0;


    //  We create a random generator to select a random vertex at each step of the walk
    unsigned seed1 = chrono::system_clock::now().time_since_epoch().count(); 
    mt19937_64 generator(seed1);   
    uniform_int_distribution<int> i_distribution(0, N - 1);


for(s=0; s<=N; s++)  
{
    media = 0.0;
    // We perfom a number of simulations and calculate the time steps of each one until reaching the destination, and we calculate the average hitting time
    for(k = 0; k < sim; k++)
    {
        // The variable "unos" counts the number of 1's of the current vertex so that we know whether we have reached the destination
        t = 0;
        unos = s; // We initialize the counter of 1's as 0 if we start in the vertex with all 0's
        contador[unos]++;
        separacion(s); // We initialize the initial vertex as the string with s 1's and N-s 0's

        while(unos != N) // We continue the walk until we reach the destination, which is the vertex with all 1's
        {
            j = i_distribution(generator);
            
            // We change the value of the j-th bit of the current vertex

            if(vertice[j] == "0") 
            {
                vertice[j] = "1";

                unos++;
            }

            else 
            {
                vertice[j] = "0";
                unos--;
            }

            contador[unos]++;

            t++;

        }

        // After a given simulation has ended, we reset the variables

        // We write the hitting time of the last simulation in the file and we add it to media, which calculates the average hitting time computationally
        media += t;
        cuadrado += (double)t * t; // o definiendo t como long long

    }

    separacion_file << s << " " << media / (double)sim << endl; // We write the separation distribution in the file
}




        return media/sim;
    
}


long long combinatorio(int n, int x) {
    if (x < 0 || x > n) return 0;
    if (x == 0 || x == n) return 1;
    
    // Propiedad de simetría: C(n, x) == C(n, n-x) ---> nos quedamos con el camino más corto 
    if (x > n - x) x = n - x; 

    // We write a compact expression of the combinatorial number to reduce the time cost of calculations
    long long comb = 1;
    for (int i = 1; i <= x; ++i) {
        comb = comb * (n - x + i) / i;
    }
    return comb;
}


int separacion(int s)
{
    int i;
    for(int i = 0; i < s; i++) vertice[i] = "1";
    for(int i = s; i< N; i++) vertice[i] = "0";

    return 0;

}