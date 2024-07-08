
(cl:in-package :asdf)

(defsystem "firsttry-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "ObjectWorldCoordinates_RobotID" :depends-on ("_package_ObjectWorldCoordinates_RobotID"))
    (:file "_package_ObjectWorldCoordinates_RobotID" :depends-on ("_package"))
  ))