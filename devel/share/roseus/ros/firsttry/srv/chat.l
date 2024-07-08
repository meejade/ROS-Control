;; Auto-generated. Do not edit!


(when (boundp 'firsttry::chat)
  (if (not (find-package "FIRSTTRY"))
    (make-package "FIRSTTRY"))
  (shadow 'chat (find-package "FIRSTTRY")))
(unless (find-package "FIRSTTRY::CHAT")
  (make-package "FIRSTTRY::CHAT"))
(unless (find-package "FIRSTTRY::CHATREQUEST")
  (make-package "FIRSTTRY::CHATREQUEST"))
(unless (find-package "FIRSTTRY::CHATRESPONSE")
  (make-package "FIRSTTRY::CHATRESPONSE"))

(in-package "ROS")





(defclass firsttry::chatRequest
  :super ros::object
  :slots (_a ))

(defmethod firsttry::chatRequest
  (:init
   (&key
    ((:a __a) "")
    )
   (send-super :init)
   (setq _a (string __a))
   self)
  (:a
   (&optional __a)
   (if __a (setq _a __a)) _a)
  (:serialization-length
   ()
   (+
    ;; string _a
    4 (length _a)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _a
       (write-long (length _a) s) (princ _a s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _a
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _a (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(defclass firsttry::chatResponse
  :super ros::object
  :slots (_b ))

(defmethod firsttry::chatResponse
  (:init
   (&key
    ((:b __b) "")
    )
   (send-super :init)
   (setq _b (string __b))
   self)
  (:b
   (&optional __b)
   (if __b (setq _b __b)) _b)
  (:serialization-length
   ()
   (+
    ;; string _b
    4 (length _b)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _b
       (write-long (length _b) s) (princ _b s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _b
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _b (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(defclass firsttry::chat
  :super ros::object
  :slots ())

(setf (get firsttry::chat :md5sum-) "945e963769938e4ddc3288e80fdfddf4")
(setf (get firsttry::chat :datatype-) "firsttry/chat")
(setf (get firsttry::chat :request) firsttry::chatRequest)
(setf (get firsttry::chat :response) firsttry::chatResponse)

(defmethod firsttry::chatRequest
  (:response () (instance firsttry::chatResponse :init)))

(setf (get firsttry::chatRequest :md5sum-) "945e963769938e4ddc3288e80fdfddf4")
(setf (get firsttry::chatRequest :datatype-) "firsttry/chatRequest")
(setf (get firsttry::chatRequest :definition-)
      "string a
---
string b

")

(setf (get firsttry::chatResponse :md5sum-) "945e963769938e4ddc3288e80fdfddf4")
(setf (get firsttry::chatResponse :datatype-) "firsttry/chatResponse")
(setf (get firsttry::chatResponse :definition-)
      "string a
---
string b

")



(provide :firsttry/chat "945e963769938e4ddc3288e80fdfddf4")


