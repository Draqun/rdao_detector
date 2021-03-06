#include <stdio.h>
#include <pthread.h>

static volatile int r1 = 0;

void* deposit1(void *args) {
    for (int i=0; i<1000000; i++)
    {
        ++r1;
    }
    return NULL;
}

void* deposit2(void *args) {
    for (int i=0; i<1000000; i++)
    {
        ++r1;
    }
    return NULL;
}

int main() {
    pthread_t t1, t2;
    printf("App start work with r1 = %d\r\n", r1);

    pthread_create(&t1, NULL, deposit1, NULL);
    pthread_join(t1, NULL);

    pthread_create(&t2, NULL, deposit2, NULL);
    pthread_join(t2, NULL);
    printf("App finish work with r1 = %d\r\n", r1);
    return 0;
}
