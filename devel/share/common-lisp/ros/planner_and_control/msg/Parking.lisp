; Auto-generated. Do not edit!


(cl:in-package planner_and_control-msg)


;//! \htmlinclude Parking.msg.html

(cl:defclass <Parking> (roslisp-msg-protocol:ros-message)
  ((index
    :reader index
    :initarg :index
    :type cl:integer
    :initform 0)
   (on
    :reader on
    :initarg :on
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass Parking (<Parking>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Parking>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Parking)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name planner_and_control-msg:<Parking> is deprecated: use planner_and_control-msg:Parking instead.")))

(cl:ensure-generic-function 'index-val :lambda-list '(m))
(cl:defmethod index-val ((m <Parking>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader planner_and_control-msg:index-val is deprecated.  Use planner_and_control-msg:index instead.")
  (index m))

(cl:ensure-generic-function 'on-val :lambda-list '(m))
(cl:defmethod on-val ((m <Parking>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader planner_and_control-msg:on-val is deprecated.  Use planner_and_control-msg:on instead.")
  (on m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Parking>) ostream)
  "Serializes a message object of type '<Parking>"
  (cl:let* ((signed (cl:slot-value msg 'index)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'on) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Parking>) istream)
  "Deserializes a message object of type '<Parking>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'index) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
    (cl:setf (cl:slot-value msg 'on) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Parking>)))
  "Returns string type for a message object of type '<Parking>"
  "planner_and_control/Parking")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Parking)))
  "Returns string type for a message object of type 'Parking"
  "planner_and_control/Parking")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Parking>)))
  "Returns md5sum for a message object of type '<Parking>"
  "08ee4255d6c0b7ed5813480b1d774735")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Parking)))
  "Returns md5sum for a message object of type 'Parking"
  "08ee4255d6c0b7ed5813480b1d774735")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Parking>)))
  "Returns full string definition for message of type '<Parking>"
  (cl:format cl:nil "int32 index~%bool on # for controller target_index (look_ahead)~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Parking)))
  "Returns full string definition for message of type 'Parking"
  (cl:format cl:nil "int32 index~%bool on # for controller target_index (look_ahead)~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Parking>))
  (cl:+ 0
     4
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Parking>))
  "Converts a ROS message object to a list"
  (cl:list 'Parking
    (cl:cons ':index (index msg))
    (cl:cons ':on (on msg))
))
