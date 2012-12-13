project(vm)
SET (DEBUG "1")
SET (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS}  -std=c++11")
add_executable(vm environment.cpp executor.cpp main.cpp debug.cpp)

install(TARGETS vm RUNTIME DESTINATION bin)
