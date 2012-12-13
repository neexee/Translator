#ifndef ENVIRONMENT_H
#define ENVIRONMENT_H
#include <vector>
#include <map>
#include <string>
#include <list>
#include <functional>
class environment
{

  public:
    environment(environment* _top) : top(_top){};
    virtual ~environment(){};
    environment* get_top();
    void add_local(std::string name, int value=0);
    int& get_local(std::string name);
    void add_func(std::string name, std::list<std::function<void()>> code);
    std::list<std::function<void()>> get_code(std::string funcname);
  private:
    environment* top;
    std::map<std::string, int> lvariables;
    std::map<std::string, std::list<std::function<void()>>> functions;
};

#endif // ENVIRONMENT_H
