#include "executor.h"
#include "environment.h"
#include <sstream>
#include <regex>
#include <map>
#include <iostream>
#include <list>
#include <functional>
#define DEBUG 0
#include "debug.h"
static enum Commands
{
    LOAD_CONST,
    LOAD_FAST,
    LOAD_GLOBAL,
    STORE_FAST,
    STORE_GLOBAL,
    BINARY_ADD,
    BINARY_SUB,
    BINARY_DIV,
    BINARY_MUL,
    RETURN_VALUE, 
    COMPARE_OP,
    JUMP_IF_FALSE,
    JUMP,
    CALL, 
    PRINT
} c;

static std::map<std::string, Commands> com_num;
executor::executor()
{
    env = new environment(nullptr);
   // current_code = new std::vector<std::function<void()>>();
    init();
}

executor::~executor()
{

    while(env)
    {
        auto oldenv = env;
        env = env->get_top();
        delete oldenv;
    }
    for(auto f : functions)
    {
        delete f.second;
    }
}
void executor::init()
{
    com_num["LOAD_CONST"] = LOAD_CONST;
    com_num["LOAD_FAST"]  = LOAD_FAST;
    com_num["LOAD_GLOBAL"] = LOAD_GLOBAL;
    com_num["STORE_FAST"] = STORE_FAST;
    com_num["STORE_GLOBAL"] = STORE_GLOBAL;

    com_num["BINARY_ADD"] = BINARY_ADD;
    com_num["BINARY_DIV"] = BINARY_DIV;
    com_num["BINARY_MUL"] = BINARY_MUL;
    com_num["BINARY_SUB"] = BINARY_SUB;

    com_num["RETURN_VALUE"] = RETURN_VALUE;
    com_num["PRINT"] = PRINT;
    com_num["CALL"] = CALL;

    com_num["JUMP_IF_FALSE"] = JUMP_IF_FALSE;
    com_num["COMPARE_OP"] = COMPARE_OP;
    com_num["JUMP"] = JUMP;
}
void executor::run_func(std::string name)
{
    env->running_code = *(get_code(name));
    env->current_instruction = 0;
    while (env->current_instruction < env->running_code.size())
    {
        auto instruction = env->running_code[env->current_instruction];
        env->current_instruction = instruction();
    }
    environment* oldenv = env;
    env = env->get_top();
    delete oldenv;
}
void executor::add_func(std::string name, std::vector<std::function<int()>>* code)
{
    functions[name] = code;
}
std::vector<std::function<int()>>* executor::get_code(std::string funcname)
{
    return functions[funcname];
}

void executor::exec(std::string instruction)
{
    using std::string;
    std::stringstream s(instruction);
    if(instruction.substr(0,4) == "func")
    {
        std::string funcname;
        s>>funcname;
        s>>funcname;
        s>>instruction_number;
        current_func = funcname;
	current_code = new std::vector<std::function<int()>>();
    }
    else
    {
        int value =0;
        s>>value; //read mark
        if(value == instruction_number)
        {
            ll = [this]
            {
			return env->running_code.size();
            };
            current_code->push_back(ll);;
            add_func(current_func, current_code);
        }
        else
        {
            std::stringstream s(instruction);      
            int mark;
            s>>mark;
            std::string comand;
            s>>comand;
            s>>comand;
            std::string name;
            int value = 0;
            int a =0;
            int b =0;
            switch(com_num[comand])
            {
	        case BINARY_MUL:
                    ll =[this]
                    {
                        int v = stack.top();
                        stack.pop();
//                        std::cout<<"MUL " << v << " TOP: "<< stack.top() <<std::endl;
                        stack.top() *= v;
			return env->current_instruction + 1;
                    };
                    break;
                case LOAD_CONST:
                    s>>value;
                    ll = [value, this]
                    {
                        int v = value;
                        INFO(string("Loading const").c_str());
                        stack.push(v);  
			return env->current_instruction +1;
                    };
                    break;
                case LOAD_FAST:
                    //Pushes a reference to the local varnames onto the stack.
                    s>>name;
                    ll = [name, this]
                    {
                        INFO(string("Loading fast").c_str());
                        stack.push(env->get_local(name));
			return env->current_instruction +1;
		    };
                    break;
                case STORE_FAST:	  
                    //Stores TOS into the local varnames
                    s>>name;  
                    ll = [name, this]
                    {
                        int v = stack.top();
                        INFO ( string(string("Storing ")+ name).c_str());
                        env->get_local(name) = v;
                        stack.pop();
			return env->current_instruction +1;
                    };
                    break;
                case BINARY_ADD:
                    ll =[this]
                    {
                        int v = stack.top();
                        stack.pop();
                        //            std::cout<<"Adding " << v<<", top = "<< stack.top() <<std::endl;
                        stack.top() += v;
			return env->current_instruction +1;
                    };
                    break;
                case BINARY_SUB:
                    ll = [this]
                    {
                        int v = stack.top();
//                        std::cout<< "Sub " << v<<std::endl;
                        stack.pop();
                        stack.top() -= v;
			return env->current_instruction +1;
                    };
                    break;
                case BINARY_DIV:
                    ll = [this]
                    {
                        int v = stack.top();
                        stack.pop();
//                        std::cout<<"Adding " << v <<std::endl;
                        stack.top() /= v;
			return env->current_instruction +1;
		      
		    };

                    break;
                case RETURN_VALUE:
                    //clean stack
                    ll = [this]
                    {
//                        std::cout<<"Pushing/returning somewhere " << stack.top() <<std::endl;
                        return env->running_code.size();
                    };
                    break;
                case PRINT:
                    s>>value;
                    ll =[value, this]
                    {
                        int v = value;
                        while(v)
                        {
                            std::cout<<stack.top()<< std::endl;
                            stack.pop();
                            v--;
                        }
                        stack.push(v);
			return env->current_instruction +1;
                    };
                    break;
                case CALL:
                    s>>name;
                    ll = [name,this]
                    {
                        INFO(string("Calling").c_str());
                        env = new environment(env);
                        run_func(name);
			return env->current_instruction +1;
                    };
                    break;
                case COMPARE_OP:
                    s>>name;
                    ll = [name, this]
                    {
                        int a = stack.top();
                        stack.pop();
                        int b = stack.top();  
                        int answer = compare(a, b, name);
                        stack.top() = answer;
			return env->current_instruction +1;
                    };
                    break;
                case JUMP_IF_FALSE:
                    s>>value;
                    ll =[value, this]
                    {
                        int flow = stack.top();
                        stack.pop();
                        if(flow)
                        {
                            return env->current_instruction +1;
                        }
                        //std::cout << "JUMP TO: " <<value<< std::endl;
                        return value;
                    };
                    break;
                case JUMP:
                    s>> value; 
                    ll = [value, this]
                    {
		      return value;
                    };
                    break;
            }
            current_code->push_back(ll);
        }

    }
}
int executor::compare(int a, int b, std::string op)
{
    if(op == "<")
    {
        return a<b? 0: 1;
    }
    if(op == ">")
    {
        return a>b? 0: 1;
    }
    if(op == "=")
    {
        return a==b? 1: 0;
    }
    return 0;
}
