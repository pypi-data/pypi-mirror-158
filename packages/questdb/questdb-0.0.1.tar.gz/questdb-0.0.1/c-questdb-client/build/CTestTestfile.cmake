# CMake generated Testfile for 
# Source directory: /Users/adam/questdb/repos/py-questdb-client/c-questdb-client
# Build directory: /Users/adam/questdb/repos/py-questdb-client/c-questdb-client/build
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(rust_tests "cargo" "test" "--features" "insecure_skip_verify" "--" "--nocapture")
set_tests_properties(rust_tests PROPERTIES  WORKING_DIRECTORY "/Users/adam/questdb/repos/py-questdb-client/c-questdb-client" _BACKTRACE_TRIPLES "/Users/adam/questdb/repos/py-questdb-client/c-questdb-client/CMakeLists.txt;101;add_test;/Users/adam/questdb/repos/py-questdb-client/c-questdb-client/CMakeLists.txt;0;")
add_test(test_line_sender "/Users/adam/questdb/repos/py-questdb-client/c-questdb-client/build/test_line_sender")
set_tests_properties(test_line_sender PROPERTIES  _BACKTRACE_TRIPLES "/Users/adam/questdb/repos/py-questdb-client/c-questdb-client/CMakeLists.txt;119;add_test;/Users/adam/questdb/repos/py-questdb-client/c-questdb-client/CMakeLists.txt;124;compile_test;/Users/adam/questdb/repos/py-questdb-client/c-questdb-client/CMakeLists.txt;0;")
subdirs("corrosion")
