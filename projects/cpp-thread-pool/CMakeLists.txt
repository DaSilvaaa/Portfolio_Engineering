cmake_minimum_required(VERSION 3.16)
project(cpp_thread_pool CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
find_package(Threads REQUIRED)

add_library(tp INTERFACE)
target_include_directories(tp INTERFACE include)
target_link_libraries(tp INTERFACE Threads::Threads)

enable_testing()
add_executable(tests tests/test_main.cpp)
target_link_libraries(tests PRIVATE tp)

if(MSVC)
    target_compile_options(tests PRIVATE /W4)
else()
    target_compile_options(tests PRIVATE -Wall -Wextra -Wpedantic)
endif()

set(SANITIZE "" CACHE STRING "address,undefined ou thread")
if(SANITIZE AND NOT MSVC)
    target_compile_options(tests PRIVATE -fsanitize=${SANITIZE} -fno-omit-frame-pointer -g)
    target_link_options(tests PRIVATE -fsanitize=${SANITIZE})
endif()

add_test(NAME tests COMMAND tests)