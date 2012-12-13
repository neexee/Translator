#ifndef EXECUTOR_H
#define EXECUTOR_H
#include <list>
#include <stack>
#include <map>
#include <string>
#include <vector>
#include "environment.h"
class executor
{
    public:
    executor();
    virtual ~executor();
    void exec(std::string str);
    void run_func(std::string name);
    
private:
    // just int 
    void init();
    int compare(int a, int b, std::string op);
    environment* env;
    
    //std::map<std::string, int> variables;
    std::stack<int> stack;
    std::string current_func;
    int instruction_number;
    std::list<std::function<void()>> current_code;
    std::function<void()> ll;
    std::list<std::function<void()>>::iterator current_instruction;
    std::list<std::function<void()>> running_code;
    
};

#endif // EXECUTOR_H
