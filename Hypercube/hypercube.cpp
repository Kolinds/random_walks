// Program that calculates the mean hitting time of a random walk in the N-dimensional hypercube starting in the vertex with all 0's and finishing at the vertex with all 1's
// The program gives the files tiempos_N.txt and estadistica_N.txt (to plot the histogram) and tiempo_acumulado_N.txt (to plot the time as a function of depth)

#include <fstream> 
#include <string>
#include <iostream>
#include <random>
#include <chrono>
#include <cmath>
using namespace std;

#define N 10
#define sim 1000000

double random_walk();
long long combinatorio(int n, int x);
double teorico();
int inicio_0();
int inicio_mitad();
string vertice[N];

int main()
{

cout << "The average number of steps for " << N << " dimensions is: " << random_walk() << endl;
cout << "The theoretical average number of steps for " << N << " dimensions is: " << teorico() << endl;



return 0;

}

// Function used to calculate the hitting time computationally
double random_walk()
{
    int i, j, k, t, unos;
    double media, cuadrado, desv, contador[N+1];
    ofstream tiempos("tiempos_N=" + to_string(N) + ".txt");
    ofstream estadistica("estadistica_N=" + to_string(N) + ".txt");
    ofstream tiempo_acumulado("tiempo_acumulado_N=" + to_string(N) + ".txt");
    bool final = false;


    // We initialize the initial vertex as the string with all 0's

    inicio_0();



    // We also initialize the counter of 1's as 0
    for(i = 0; i <= N; i++) contador[i] = 0;


    //  We create a random generator to select a random vertex at each step of the walk
    unsigned seed1 = chrono::system_clock::now().time_since_epoch().count(); 
    mt19937_64 generator(seed1);   
    uniform_int_distribution<int> i_distribution(0, N - 1);

    media = 0.0;
    cuadrado = 0.0;

  
    // We perfom a number of simulations and calculate the time steps of each one until reaching the destination, and we calculate the average hitting time
    for(k = 0; k < sim; k++)
    {
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

            if(unos == N) final = true; 

            t++;

        }

        // After a given simulation has ended, we reset the variables

        final = false;
        inicio_0();

        // We write the hitting time of the last simulation in the file and we add it to media, which calculates the average hitting time computationally
        tiempos << t << endl;
        media += t;
        cuadrado += (double)t * t;

    }

    desv = sqrt(cuadrado/sim - (media/sim) * (media/sim));

    estadistica << media/sim << " " << desv << endl;

    for(i=0; i<=N; i++) tiempo_acumulado << contador[i] << endl;

    tiempos.close();
    estadistica.close();
    tiempo_acumulado.close();

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
double teorico()
{

    int x, j;
    double suma, suma2;

    suma2 = 0.0;

    for(x = 0; x < N; x++)
    {
        suma = 0.0;
        for(j = 0; j <= x; j++)
        {
           suma += combinatorio(N, j);
        }

        suma = suma / combinatorio(N-1, x);

        suma2 += suma;
    }
    return suma2;
}


int inicio_0()
{

int i;
for(i = 0; i < N; i++) vertice[i] = "0";

return 0;

}
