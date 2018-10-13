#include <sys/socket.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <netinet/in.h>
#include <limits.h>
#include <stdbool.h>


#define PORT 8080


//The most useful program ever written

int main()
{

    
    char array[10] = {"HELLO"};

    struct sockaddr_in myaddr = {0};
    int rc, listen_fd, client_fd = 0;

    listen_fd = socket( AF_INET, SOCK_STREAM, 0 );

    if(listen_fd < 0 )
        perror( "Socket" );

    myaddr.sin_port = htons( PORT );
    myaddr.sin_addr.s_addr = INADDR_ANY;
    myaddr.sin_family = AF_INET;

    rc = bind( listen_fd, (struct sockaddr*)&myaddr, sizeof(myaddr) );
    if( rc != 0)
        perror("bind");

    rc = listen( listen_fd, 3 );
    if( rc != 0 )
        perror( "listen" );

    client_fd = accept( listen_fd, NULL, NULL );
    if( client_fd < 0 )
        perror("Accept");


    printf( "Accepted connection\n" );
    fflush( stdout );

    //Let's burn down the house
    for( int i = 0; true; i++ )
        array[i] = 'f';

    printf("How the hell did I make it here?");

    return 0;
}
