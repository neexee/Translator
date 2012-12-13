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
    LOAD_CONST =5,
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
    running_code = env->get_code(name);
   // std::list<std::function<void()>>::iterator current_instruction; 
    for (current_instruction= running_code.begin(); current_instruction!= running_code.end(); current_instruction++)
    {
      (*current_instruction)();
    }
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
        std::cout<<"New function " << funcname <<" instructions:"<<instruction_number <<std::endl;
        env = new environment(env);
    }
    else
    {
        int value =0;
        s>>value; //read mark
        if(value == instruction_number)
        {
            env = env->get_top();
            env->add_func(current_func, current_code);
            current_code = std::list<std::function<void()>>();
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
                case LOAD_CONST:
                    s>>value;
                    ll = [value, this]
                    {
                        int v = value;
                        INFO(string("Loading const").c_str());
                        stack.push(v);  
                    };
                    break;
                case LOAD_FAST:
                    s>>name;
                    ll = [name, this]
                    {

                        stack.push(env->get_local(name));

                    };
                    break;
                case STORE_FAST:
                    s>>name;  
                    ll = [name, this]
                    {
                        int v = stack.top();
                        INFO ( string(string("Storing ")+ name).c_str());
                        env->get_local(name) = v;
                        stack.pop();
                    };
                    break;
                case BINARY_ADD:
                    ll =[this]
                    {
                        int v = stack.top();
                        stack.pop();
                        std::cout<<"Adding " << v <<std::endl;
                        stack.top() += v;
                    };
                    break;
                case BINARY_SUB:
                    ll = [this]
                    {
                        int v = stack.top();
                        stack.pop();
                        stack.top() -= v;
                    };
                    break;
                case BINARY_MUL:
                    ll =[this]
                    {
                        int v = stack.top();
                        stack.pop();
                        std::cout<<"Adding " << v <<std::endl;
                        stack.top() *= v;
                    };
                    break;
                case BINARY_DIV:
                    ll = [this]
                    {
                        int v = stack.top();
                        stack.pop();
                        std::cout<<"Adding " << v <<std::endl;
                        stack.top() /= v;
                    };
                    break;
                case RETURN_VALUE:
                   //clean stack
                    ll = [this]
                     {
                         std::cout<<"Pushing/returning " << stack.top() <<std::endl;
                     };
                     break;
                case PRINT:
                    s>>value;
                    ll =[value, this]
                    {
                        int v = value;
                        while(v)
                            {
                                std::cout<< "PROGRAM PRINT: "<<stack.top()<< std::endl;
                                stack.pop();
                                v--;
                            }
                        stack.push(v);
                    };
                    break;
                case CALL:
                    s>>name;
                    ll = [name,this]
                        {
                             run_func(name);
                        };
                        break;
		case COMPARE_OP:
		  s>>name;
		  ll = [name, this]
		  {
		    int a = stack.top();
		    stack.pop();
		    int b = stack.top();
		    int answer = compare(b, a, name);
		    stack.top() = answer;
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
		       return;
		    }
		     int index = 0;
		     for(std::list<std::function<void()>>::iterator it =running_code.begin(); it !=running_code.end(); it++ )
		     {
		       if(index == value -1)
		       {
			 current_instruction = it;
		         return;
			 
		      }
		       else
		       {
			 index++;
		       }
		     }
		  };
		  break;
		case JUMP:
		  s>> value; 
		  ll = [value, this]
		  {
		     int index = 0;
		     for(std::list<std::function<void()>>::iterator it =running_code.begin(); it !=running_code.end(); it++ )
		     {
		       if(index == value -1)
		       {
			 current_instruction = it;
			 return;
		       }
		       else
		       {
			 index++;
		       }
		     }
		  };
            }
        }
            current_code.push_back(ll);
      }
}
int executor::compare(int a, int b, std::string op)
{
  if(op == "<")
  {
    return a<b? 1: 0;
  }
  if(op == ">")
  {
    return a>b? 1: 0;
  }
  if(op == "=")
  {
    return a==b? 1: 0;
  }
  return false;
}
