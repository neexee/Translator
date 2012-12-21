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
    void add_func(std::string name, std::vector<std::function<int()>>* code);
    std::vector<std::function<int()>>* get_code(std::string funcname);
    
    environment* env;
    
    //std::map<std::string, int> variables;
    std::stack<int> stack;
    std::string current_func;
    int instruction_number;
    std::vector<std::function<int()>>* current_code;
    std::function<int()> ll;
    std::map<std::string, std::vector<std::function<int()>>*> functions;
    
};

#endif // EXECUTOR_H
