;; Auto-generated. Do not edit!


(when (boundp 'firsttry::ObjectWorldCoordinates_RobotID)
  (if (not (find-package "FIRSTTRY"))
    (make-package "FIRSTTRY"))
  (shadow 'ObjectWorldCoordinates_RobotID (find-package "FIRSTTRY")))
(unless (find-package "FIRSTTRY::OBJECTWORLDCOORDINATES_ROBOTID")
  (make-package "FIRSTTRY::OBJECTWORLDCOORDINATES_ROBOTID"))

(in-package "ROS")
;;//! \htmlinclude ObjectWorldCoordinates_RobotID.msg.html


(defclass firsttry::ObjectWorldCoordinates_RobotID
  :super ros::object
  :slots (_robot_id _coordinates ))

(defmethod firsttry::ObjectWorldCoordinates_RobotID
  (:init
   (&key
    ((:robot_id __robot_id) "")
    ((:coordinates __coordinates) (make-array 0 :initial-element 0.0 :element-type :float))
    )
   (send-super :init)
   (setq _robot_id (string __robot_id))
   (setq _coordinates __coordinates)
   self)
  (:robot_id
   (&optional __robot_id)
   (if __robot_id (setq _robot_id __robot_id)) _robot_id)
  (:coordinates
   (&optional __coordinates)
   (if __coordinates (setq _coordinates __coordinates)) _coordinates)
  (:serialization-length
   ()
   (+
    ;; string _robot_id
    4 (length _robot_id)
    ;; float32[] _coordinates
    (* 4    (length _coordinates)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _robot_id
       (write-long (length _robot_id) s) (princ _robot_id s)
     ;; float32[] _coordinates
     (write-long (length _coordinates) s)
     (dotimes (i (length _coordinates))
       (sys::poke (elt _coordinates i) (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _robot_id
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _robot_id (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; float32[] _coordinates
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _coordinates (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _coordinates i) (sys::peek buf ptr- :float)) (incf ptr- 4)
     ))
   ;;
   self)
  )

(setf (get firsttry::ObjectWorldCoordinates_RobotID :md5sum-) "f3940801c7cc7e452ec2d947ccb47469")
(setf (get firsttry::ObjectWorldCoordinates_RobotID :datatype-) "firsttry/ObjectWorldCoordinates_RobotID")
(setf (get firsttry::ObjectWorldCoordinates_RobotID :definition-)
      "string robot_id
float32[] coordinates

")



(provide :firsttry/ObjectWorldCoordinates_RobotID "f3940801c7cc7e452ec2d947ccb47469")


