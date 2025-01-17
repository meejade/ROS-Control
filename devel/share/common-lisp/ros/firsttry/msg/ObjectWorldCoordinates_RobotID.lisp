; Auto-generated. Do not edit!


(cl:in-package firsttry-msg)


;//! \htmlinclude ObjectWorldCoordinates_RobotID.msg.html

(cl:defclass <ObjectWorldCoordinates_RobotID> (roslisp-msg-protocol:ros-message)
  ((robot_id
    :reader robot_id
    :initarg :robot_id
    :type cl:string
    :initform "")
   (coordinates
    :reader coordinates
    :initarg :coordinates
    :type (cl:vector cl:float)
   :initform (cl:make-array 0 :element-type 'cl:float :initial-element 0.0)))
)

(cl:defclass ObjectWorldCoordinates_RobotID (<ObjectWorldCoordinates_RobotID>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <ObjectWorldCoordinates_RobotID>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'ObjectWorldCoordinates_RobotID)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name firsttry-msg:<ObjectWorldCoordinates_RobotID> is deprecated: use firsttry-msg:ObjectWorldCoordinates_RobotID instead.")))

(cl:ensure-generic-function 'robot_id-val :lambda-list '(m))
(cl:defmethod robot_id-val ((m <ObjectWorldCoordinates_RobotID>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader firsttry-msg:robot_id-val is deprecated.  Use firsttry-msg:robot_id instead.")
  (robot_id m))

(cl:ensure-generic-function 'coordinates-val :lambda-list '(m))
(cl:defmethod coordinates-val ((m <ObjectWorldCoordinates_RobotID>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader firsttry-msg:coordinates-val is deprecated.  Use firsttry-msg:coordinates instead.")
  (coordinates m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <ObjectWorldCoordinates_RobotID>) ostream)
  "Serializes a message object of type '<ObjectWorldCoordinates_RobotID>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'robot_id))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'robot_id))
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'coordinates))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let ((bits (roslisp-utils:encode-single-float-bits ele)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)))
   (cl:slot-value msg 'coordinates))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <ObjectWorldCoordinates_RobotID>) istream)
  "Deserializes a message object of type '<ObjectWorldCoordinates_RobotID>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'robot_id) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'robot_id) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'coordinates) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'coordinates)))
    (cl:dotimes (i __ros_arr_len)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:aref vals i) (roslisp-utils:decode-single-float-bits bits))))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<ObjectWorldCoordinates_RobotID>)))
  "Returns string type for a message object of type '<ObjectWorldCoordinates_RobotID>"
  "firsttry/ObjectWorldCoordinates_RobotID")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'ObjectWorldCoordinates_RobotID)))
  "Returns string type for a message object of type 'ObjectWorldCoordinates_RobotID"
  "firsttry/ObjectWorldCoordinates_RobotID")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<ObjectWorldCoordinates_RobotID>)))
  "Returns md5sum for a message object of type '<ObjectWorldCoordinates_RobotID>"
  "f3940801c7cc7e452ec2d947ccb47469")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'ObjectWorldCoordinates_RobotID)))
  "Returns md5sum for a message object of type 'ObjectWorldCoordinates_RobotID"
  "f3940801c7cc7e452ec2d947ccb47469")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<ObjectWorldCoordinates_RobotID>)))
  "Returns full string definition for message of type '<ObjectWorldCoordinates_RobotID>"
  (cl:format cl:nil "string robot_id~%float32[] coordinates~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'ObjectWorldCoordinates_RobotID)))
  "Returns full string definition for message of type 'ObjectWorldCoordinates_RobotID"
  (cl:format cl:nil "string robot_id~%float32[] coordinates~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <ObjectWorldCoordinates_RobotID>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'robot_id))
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'coordinates) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 4)))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <ObjectWorldCoordinates_RobotID>))
  "Converts a ROS message object to a list"
  (cl:list 'ObjectWorldCoordinates_RobotID
    (cl:cons ':robot_id (robot_id msg))
    (cl:cons ':coordinates (coordinates msg))
))
