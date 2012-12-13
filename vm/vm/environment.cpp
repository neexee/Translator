#include "environment.h"
#include <functional>
environment* environment::get_top()
{
  return top;
}
void environment::add_func(std::string name, std::list<std::function<void()>> code)
{
  functions[name] = code;
}
std::list<std::function<void()>> environment::get_code(std::string funcname)
{
 return functions[funcname];
}

void environment::add_local(std::string name, int value )
{
    lvariables[name] = value;
}
int& environment::get_local(std::string name)
{
  return lvariables[name];
}


