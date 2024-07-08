# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "firsttry: 1 messages, 2 services")

set(MSG_I_FLAGS "-Ifirsttry:/home/turtle/Service_1/src/firsttry/msg;-Istd_msgs:/opt/ros/noetic/share/std_msgs/cmake/../msg;-Igeometry_msgs:/opt/ros/noetic/share/geometry_msgs/cmake/../msg;-Inav_msgs:/opt/ros/noetic/share/nav_msgs/cmake/../msg;-Iactionlib_msgs:/opt/ros/noetic/share/actionlib_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(firsttry_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/turtle/Service_1/src/firsttry/msg/ObjectWorldCoordinates_RobotID.msg" NAME_WE)
add_custom_target(_firsttry_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "firsttry" "/home/turtle/Service_1/src/firsttry/msg/ObjectWorldCoordinates_RobotID.msg" ""
)

get_filename_component(_filename "/home/turtle/Service_1/src/firsttry/srv/AddTwoInts.srv" NAME_WE)
add_custom_target(_firsttry_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "firsttry" "/home/turtle/Service_1/src/firsttry/srv/AddTwoInts.srv" ""
)

get_filename_component(_filename "/home/turtle/Service_1/src/firsttry/srv/chat.srv" NAME_WE)
add_custom_target(_firsttry_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "firsttry" "/home/turtle/Service_1/src/firsttry/srv/chat.srv" ""
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(firsttry
  "/home/turtle/Service_1/src/firsttry/msg/ObjectWorldCoordinates_RobotID.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/firsttry
)

### Generating Services
_generate_srv_cpp(firsttry
  "/home/turtle/Service_1/src/firsttry/srv/AddTwoInts.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/firsttry
)
_generate_srv_cpp(firsttry
  "/home/turtle/Service_1/src/firsttry/srv/chat.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/firsttry
)

### Generating Module File
_generate_module_cpp(firsttry
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/firsttry
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(firsttry_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(firsttry_generate_messages firsttry_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/turtle/Service_1/src/firsttry/msg/ObjectWorldCoordinates_RobotID.msg" NAME_WE)
add_dependencies(firsttry_generate_messages_cpp _firsttry_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/turtle/Service_1/src/firsttry/srv/AddTwoInts.srv" NAME_WE)
add_dependencies(firsttry_generate_messages_cpp _firsttry_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/turtle/Service_1/src/firsttry/srv/chat.srv" NAME_WE)
add_dependencies(firsttry_generate_messages_cpp _firsttry_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(firsttry_gencpp)
add_dependencies(firsttry_gencpp firsttry_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS firsttry_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(firsttry
  "/home/turtle/Service_1/src/firsttry/msg/ObjectWorldCoordinates_RobotID.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/firsttry
)

### Generating Services
_generate_srv_eus(firsttry
  "/home/turtle/Service_1/src/firsttry/srv/AddTwoInts.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/firsttry
)
_generate_srv_eus(firsttry
  "/home/turtle/Service_1/src/firsttry/srv/chat.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/firsttry
)

### Generating Module File
_generate_module_eus(firsttry
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/firsttry
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(firsttry_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(firsttry_generate_messages firsttry_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/turtle/Service_1/src/firsttry/msg/ObjectWorldCoordinates_RobotID.msg" NAME_WE)
add_dependencies(firsttry_generate_messages_eus _firsttry_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/turtle/Service_1/src/firsttry/srv/AddTwoInts.srv" NAME_WE)
add_dependencies(firsttry_generate_messages_eus _firsttry_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/turtle/Service_1/src/firsttry/srv/chat.srv" NAME_WE)
add_dependencies(firsttry_generate_messages_eus _firsttry_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(firsttry_geneus)
add_dependencies(firsttry_geneus firsttry_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS firsttry_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(firsttry
  "/home/turtle/Service_1/src/firsttry/msg/ObjectWorldCoordinates_RobotID.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/firsttry
)

### Generating Services
_generate_srv_lisp(firsttry
  "/home/turtle/Service_1/src/firsttry/srv/AddTwoInts.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/firsttry
)
_generate_srv_lisp(firsttry
  "/home/turtle/Service_1/src/firsttry/srv/chat.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/firsttry
)

### Generating Module File
_generate_module_lisp(firsttry
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/firsttry
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(firsttry_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(firsttry_generate_messages firsttry_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/turtle/Service_1/src/firsttry/msg/ObjectWorldCoordinates_RobotID.msg" NAME_WE)
add_dependencies(firsttry_generate_messages_lisp _firsttry_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/turtle/Service_1/src/firsttry/srv/AddTwoInts.srv" NAME_WE)
add_dependencies(firsttry_generate_messages_lisp _firsttry_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/turtle/Service_1/src/firsttry/srv/chat.srv" NAME_WE)
add_dependencies(firsttry_generate_messages_lisp _firsttry_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(firsttry_genlisp)
add_dependencies(firsttry_genlisp firsttry_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS firsttry_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(firsttry
  "/home/turtle/Service_1/src/firsttry/msg/ObjectWorldCoordinates_RobotID.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/firsttry
)

### Generating Services
_generate_srv_nodejs(firsttry
  "/home/turtle/Service_1/src/firsttry/srv/AddTwoInts.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/firsttry
)
_generate_srv_nodejs(firsttry
  "/home/turtle/Service_1/src/firsttry/srv/chat.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/firsttry
)

### Generating Module File
_generate_module_nodejs(firsttry
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/firsttry
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(firsttry_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(firsttry_generate_messages firsttry_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/turtle/Service_1/src/firsttry/msg/ObjectWorldCoordinates_RobotID.msg" NAME_WE)
add_dependencies(firsttry_generate_messages_nodejs _firsttry_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/turtle/Service_1/src/firsttry/srv/AddTwoInts.srv" NAME_WE)
add_dependencies(firsttry_generate_messages_nodejs _firsttry_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/turtle/Service_1/src/firsttry/srv/chat.srv" NAME_WE)
add_dependencies(firsttry_generate_messages_nodejs _firsttry_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(firsttry_gennodejs)
add_dependencies(firsttry_gennodejs firsttry_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS firsttry_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(firsttry
  "/home/turtle/Service_1/src/firsttry/msg/ObjectWorldCoordinates_RobotID.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/firsttry
)

### Generating Services
_generate_srv_py(firsttry
  "/home/turtle/Service_1/src/firsttry/srv/AddTwoInts.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/firsttry
)
_generate_srv_py(firsttry
  "/home/turtle/Service_1/src/firsttry/srv/chat.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/firsttry
)

### Generating Module File
_generate_module_py(firsttry
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/firsttry
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(firsttry_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(firsttry_generate_messages firsttry_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/turtle/Service_1/src/firsttry/msg/ObjectWorldCoordinates_RobotID.msg" NAME_WE)
add_dependencies(firsttry_generate_messages_py _firsttry_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/turtle/Service_1/src/firsttry/srv/AddTwoInts.srv" NAME_WE)
add_dependencies(firsttry_generate_messages_py _firsttry_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/turtle/Service_1/src/firsttry/srv/chat.srv" NAME_WE)
add_dependencies(firsttry_generate_messages_py _firsttry_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(firsttry_genpy)
add_dependencies(firsttry_genpy firsttry_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS firsttry_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/firsttry)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/firsttry
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(firsttry_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()
if(TARGET geometry_msgs_generate_messages_cpp)
  add_dependencies(firsttry_generate_messages_cpp geometry_msgs_generate_messages_cpp)
endif()
if(TARGET nav_msgs_generate_messages_cpp)
  add_dependencies(firsttry_generate_messages_cpp nav_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/firsttry)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/firsttry
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(firsttry_generate_messages_eus std_msgs_generate_messages_eus)
endif()
if(TARGET geometry_msgs_generate_messages_eus)
  add_dependencies(firsttry_generate_messages_eus geometry_msgs_generate_messages_eus)
endif()
if(TARGET nav_msgs_generate_messages_eus)
  add_dependencies(firsttry_generate_messages_eus nav_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/firsttry)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/firsttry
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(firsttry_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()
if(TARGET geometry_msgs_generate_messages_lisp)
  add_dependencies(firsttry_generate_messages_lisp geometry_msgs_generate_messages_lisp)
endif()
if(TARGET nav_msgs_generate_messages_lisp)
  add_dependencies(firsttry_generate_messages_lisp nav_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/firsttry)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/firsttry
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(firsttry_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()
if(TARGET geometry_msgs_generate_messages_nodejs)
  add_dependencies(firsttry_generate_messages_nodejs geometry_msgs_generate_messages_nodejs)
endif()
if(TARGET nav_msgs_generate_messages_nodejs)
  add_dependencies(firsttry_generate_messages_nodejs nav_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/firsttry)
  install(CODE "execute_process(COMMAND \"/usr/bin/python3\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/firsttry\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/firsttry
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(firsttry_generate_messages_py std_msgs_generate_messages_py)
endif()
if(TARGET geometry_msgs_generate_messages_py)
  add_dependencies(firsttry_generate_messages_py geometry_msgs_generate_messages_py)
endif()
if(TARGET nav_msgs_generate_messages_py)
  add_dependencies(firsttry_generate_messages_py nav_msgs_generate_messages_py)
endif()
