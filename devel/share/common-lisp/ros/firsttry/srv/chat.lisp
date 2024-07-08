; Auto-generated. Do not edit!


(cl:in-package firsttry-srv)


;//! \htmlinclude chat-request.msg.html

(cl:defclass <chat-request> (roslisp-msg-protocol:ros-message)
  ((a
    :reader a
    :initarg :a
    :type cl:string
    :initform ""))
)

(cl:defclass chat-request (<chat-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <chat-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'chat-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name firsttry-srv:<chat-request> is deprecated: use firsttry-srv:chat-request instead.")))

(cl:ensure-generic-function 'a-val :lambda-list '(m))
(cl:defmethod a-val ((m <chat-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader firsttry-srv:a-val is deprecated.  Use firsttry-srv:a instead.")
  (a m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <chat-request>) ostream)
  "Serializes a message object of type '<chat-request>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'a))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'a))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <chat-request>) istream)
  "Deserializes a message object of type '<chat-request>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'a) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'a) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<chat-request>)))
  "Returns string type for a service object of type '<chat-request>"
  "firsttry/chatRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'chat-request)))
  "Returns string type for a service object of type 'chat-request"
  "firsttry/chatRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<chat-request>)))
  "Returns md5sum for a message object of type '<chat-request>"
  "945e963769938e4ddc3288e80fdfddf4")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'chat-request)))
  "Returns md5sum for a message object of type 'chat-request"
  "945e963769938e4ddc3288e80fdfddf4")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<chat-request>)))
  "Returns full string definition for message of type '<chat-request>"
  (cl:format cl:nil "string a~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'chat-request)))
  "Returns full string definition for message of type 'chat-request"
  (cl:format cl:nil "string a~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <chat-request>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'a))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <chat-request>))
  "Converts a ROS message object to a list"
  (cl:list 'chat-request
    (cl:cons ':a (a msg))
))
;//! \htmlinclude chat-response.msg.html

(cl:defclass <chat-response> (roslisp-msg-protocol:ros-message)
  ((b
    :reader b
    :initarg :b
    :type cl:string
    :initform ""))
)

(cl:defclass chat-response (<chat-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <chat-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'chat-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name firsttry-srv:<chat-response> is deprecated: use firsttry-srv:chat-response instead.")))

(cl:ensure-generic-function 'b-val :lambda-list '(m))
(cl:defmethod b-val ((m <chat-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader firsttry-srv:b-val is deprecated.  Use firsttry-srv:b instead.")
  (b m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <chat-response>) ostream)
  "Serializes a message object of type '<chat-response>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'b))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'b))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <chat-response>) istream)
  "Deserializes a message object of type '<chat-response>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'b) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'b) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<chat-response>)))
  "Returns string type for a service object of type '<chat-response>"
  "firsttry/chatResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'chat-response)))
  "Returns string type for a service object of type 'chat-response"
  "firsttry/chatResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<chat-response>)))
  "Returns md5sum for a message object of type '<chat-response>"
  "945e963769938e4ddc3288e80fdfddf4")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'chat-response)))
  "Returns md5sum for a message object of type 'chat-response"
  "945e963769938e4ddc3288e80fdfddf4")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<chat-response>)))
  "Returns full string definition for message of type '<chat-response>"
  (cl:format cl:nil "string b~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'chat-response)))
  "Returns full string definition for message of type 'chat-response"
  (cl:format cl:nil "string b~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <chat-response>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'b))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <chat-response>))
  "Converts a ROS message object to a list"
  (cl:list 'chat-response
    (cl:cons ':b (b msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'chat)))
  'chat-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'chat)))
  'chat-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'chat)))
  "Returns string type for a service object of type '<chat>"
  "firsttry/chat")