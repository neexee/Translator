#include <iostream>
#include <fstream>
#include <string>
#include "executor.h"
void print_help(char* progname)
{
  std::cout<< "Use: " + std::string(progname) + " file"<<std::endl;
}
int main(int argc, char **argv)
{
    using std::fstream;
    if(argc< 2)
    {
      print_help(argv[0]);
      return 0;
    }
    fstream source(argv[1], fstream::in);
    if(source.fail())
    {
       std::cout<<argv[1]<< " not found!"<< std::endl;
       print_help(argv[0]);
    }
    executor ex;
    while(source.good())
    {
      std::string instruction; 
      getline(source, instruction);
      ex.exec(instruction);
    }
    
    ex.run_func("main");
    source.close();
    return 0;
}
