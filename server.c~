#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

#define BUF_SIZE 1024
void error_handling(char *message);

int main(int argc, char *argv[])
{   
    int serv_sock, clnt_sock;
    char message[BUF_SIZE];                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
    int str_len, i;
    
    struct sockaddr_in serv_adr, clnt_adr;
    socklen_t clnt_adr_sz;
    
    if(argc != 2){
        printf("Usage : %s <port>\n", argv[0]);
        exit(1);
    }
    
    serv_sock = socket(PF_INET, SOCK_STREAM, 0);
    if(serv_sock == -1)
        error_handling("socket() error");
     
    //网络地址初始化：利用字符串格式的IP地址和端口号初始化sockaddr_in结构体变量    
    memset(&serv_adr, 0, sizeof(serv_adr));       //结构体变量addr的所有成员初始化为0
    serv_adr.sin_family = AF_INET;                //指定地址族
    serv_adr.sin_addr.s_addr = htonl(INADDR_ANY); //自动获取IP地址
    serv_adr.sin_port = htons(atoi(argv[1]));     //基于字符串的端口号初始化
    
    if(bind(serv_sock, (struct sockaddr*)&serv_adr, sizeof(serv_adr)) == -1)
        error_handling("bind() error");
        
    if(listen(serv_sock, 5) == -1)
        error_handling("listen() error");
        
    clnt_adr_sz = sizeof(clnt_adr);
    
    for(i=0; i<5; i++)
    {   //循环实现回声效果
        clnt_sock = accept(serv_sock, (struct sockaddr*)&clnt_adr, &clnt_adr_sz);
        if(clnt_sock == -1)
            error_handling("accept() error");
        else
            printf("Connected client %d \n", i+1);
        
        while((str_len = read(clnt_sock, message, BUF_SIZE)) != 0)
            write(clnt_sock, message, str_len);
            //将客户端发送过来的message原封不动send回去
            
        close(clnt_sock);
    }
    close(serv_sock);
    return 0;
        
}

void error_handling(char *message)
{
    fputs(message, stderr);
    fputc('\n', stderr);
    exit(1);
}

