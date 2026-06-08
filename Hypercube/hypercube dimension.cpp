#include <fstream> 
#include <string>
#include <iostream>
#include <random>
#include <chrono>
#include <cmath>
using namespace std;

#define sim 100000

double random_walk();
long long combinatorio(int n, int x);
double teorico(int p);
int inicio_0(double p);

string vertice[100]; // We can define the array with a bigger size than N because we will only use the first N positions

int main()
{

random_walk();
return 0;

}

// Function used to calculate the hitting time computationally
double random_walk()
{
    int i, j, k, t, p, unos;
    double media, cuadrado, desv, contador[100];
    ofstream dimension("dimension.txt");
    bool final = false;

// We want the time until dimension 20 but we only take the pair values to have a general idea 
for(p=2; p<=20; p=p+2)
{
    // We also initialize the counter of 1's as 0
    for(i = 0; i <= p; i++) contador[i] = 0;

    media = 0.0;
    cuadrado = 0.0;

    //  We create a random generator to select a random vertex at each step of the walk
    unsigned seed1 = chrono::system_clock::now().time_since_epoch().count(); 
    mt19937_64 generator(seed1);   
    uniform_int_distribution<int> i_distribution(0, p - 1);
    // We perfom a number of simulations and calculate the time steps of each one until reaching the destination, and we calculate the average hitting time
    for(k = 0; k < sim; k++)
    {
        
        inicio_0(p); // We initialize the initial vertex as the string with all 0's
        // The variable "unos" counts the number of 1's of the current vertex so that we know whether we have reached the destination
        t = 0;
        unos = 0; // We initialize the counter of 1's as 0 if we start in the vertex with all 0's
        contador[unos]++;

        while(!final)
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

            if(unos == p) final = true; 

            t++;

        }

        // After a given simulation has ended, we reset the variables

        final = false;
        inicio_0(p);

        media += t;
        cuadrado += (double)t * t; // o definiendo t como long long

    }

    desv = sqrt(cuadrado/sim - (media/sim) * (media/sim));

    dimension << p << " " << media/sim << " " << desv/sqrt(sim) << " " << teorico(p) << " " << abs((media/sim-teorico(p)))/(media/sim)*100 << endl;
}


    dimension.close();

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

// We calculate the theorical mean hitting time using the analytical expression derived
double teorico(int p)
{

    int x, j;
    double suma, suma2;

    suma2 = 0.0;

    for(x = 0; x < p; x++)
    {
        suma = 0.0;
        for(j = 0; j <= x; j++)
        {
           suma += combinatorio(p, j);
        }

        suma = suma / combinatorio(p-1, x);

        suma2 += suma;
    }
    return suma2;
}


int inicio_0(double p)
{

int i;
for(i = 0; i < p; i++) vertice[i] = "0";

return 0;

}

