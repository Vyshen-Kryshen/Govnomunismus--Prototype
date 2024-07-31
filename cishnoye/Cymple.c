#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>


// Структура с двумя вещественными компонентами.
typedef struct Vec2
{
    float f, s;
} Vec2;


// Структура круга, как шаблон для объектов коллизий.
typedef struct ColliderCircle
{
    float centerX;
    float centerY;
    float directionOnX;
    float directionOnY;
    float radius;
    int mass;
    bool isCollide;
} ColliderCircle;


// Инициализатор для создания объектов по шаблону структуры круга, а так же выделение памяти на него.
ColliderCircle init(float centerX, float centerY, float directionOnX, float directionOnY, float radius, int mass)
{
    ColliderCircle *ptr = NULL;
    ptr = malloc(sizeof(float) * 7 + sizeof(int) * 2);
    if (ptr)
    {
        ptr->centerX = centerX;
        ptr->centerY = centerY;
        ptr->directionOnX = directionOnX;
        ptr->directionOnY = directionOnY;
        ptr->radius = radius;
        ptr->mass = mass;
        ptr->isCollide = false;
        return *ptr;
    };
};


// Функция проверки столконвения.
bool checkCollision(ColliderCircle *fccPtr, ColliderCircle *sccPtr)
{
    if ((fccPtr->centerX - sccPtr->centerX <= 0) && (fccPtr->centerY - sccPtr->centerY <= 0))
    {
        fccPtr->isCollide = true;
        sccPtr->isCollide = true;

        return true;
    }
    else
    {
        return false;
    };
};


// Функция произведения двух векторов.
float scalarProduct(Vec2 fvec, Vec2 svec)
{
    float result = (fvec.f * svec.f) + (fvec.s * svec.s);
    return result;
};


// Функция для отражения направления.
Vec2 vecrefl(Vec2 vec, Vec2 surfvec)
{
    Vec2 result;

    result.f = (2 * surfvec.f * scalarProduct(vec, surfvec) / scalarProduct(surfvec, surfvec) - vec.f);
    result.s = (2 * surfvec.s * scalarProduct(vec, surfvec) / scalarProduct(surfvec, surfvec) - vec.s);

    return result;
}


// Функция-обработчик столкновения.
void handleOfCollide(ColliderCircle *fccPtr, ColliderCircle *sccPtr)
{
    Vec2 fdirection = {fccPtr->directionOnX, fccPtr->directionOnY};
    Vec2 fnormall = {fccPtr->directionOnY, fccPtr->directionOnX};

    Vec2 sdirection = {sccPtr->directionOnX, sccPtr->directionOnY};
    Vec2 snormall = {sccPtr->directionOnY, sccPtr->directionOnX};

    float fresult[2] = {vecrefl(fdirection, fnormall).f, vecrefl(fdirection, fnormall).s};
    float sresult[2] = {vecrefl(sdirection, snormall).f, vecrefl(sdirection, snormall).s};

    fccPtr->directionOnX = fresult[0];
    fccPtr->directionOnY = fresult[1];
    
    sccPtr->directionOnX = sresult[0];
    sccPtr->directionOnY = sresult[1];
};
