
(cl:in-package :asdf)

(defsystem "local_pkg-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :geometry_msgs-msg
)
  :components ((:file "_package")
    (:file "Control_Info" :depends-on ("_package_Control_Info"))
    (:file "_package_Control_Info" :depends-on ("_package"))
    (:file "Control_Info" :depends-on ("_package_Control_Info"))
    (:file "_package_Control_Info" :depends-on ("_package"))
    (:file "Local" :depends-on ("_package_Local"))
    (:file "_package_Local" :depends-on ("_package"))
    (:file "Local" :depends-on ("_package_Local"))
    (:file "_package_Local" :depends-on ("_package"))
    (:file "Master" :depends-on ("_package_Master"))
    (:file "_package_Master" :depends-on ("_package"))
    (:file "Master" :depends-on ("_package_Master"))
    (:file "_package_Master" :depends-on ("_package"))
    (:file "Serial_Info" :depends-on ("_package_Serial_Info"))
    (:file "_package_Serial_Info" :depends-on ("_package"))
    (:file "Serial_Info" :depends-on ("_package_Serial_Info"))
    (:file "_package_Serial_Info" :depends-on ("_package"))
  ))