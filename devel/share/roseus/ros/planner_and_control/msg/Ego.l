;; Auto-generated. Do not edit!


(when (boundp 'planner_and_control::Ego)
  (if (not (find-package "PLANNER_AND_CONTROL"))
    (make-package "PLANNER_AND_CONTROL"))
  (shadow 'Ego (find-package "PLANNER_AND_CONTROL")))
(unless (find-package "PLANNER_AND_CONTROL::EGO")
  (make-package "PLANNER_AND_CONTROL::EGO"))

(in-package "ROS")
;;//! \htmlinclude Ego.msg.html


(defclass planner_and_control::Ego
  :super ros::object
  :slots (_x _y _heading _index _target_speed _target_brake _target_gear _speed _steer _brake _gear _auto_manual _map_folder _map_file ))

(defmethod planner_and_control::Ego
  (:init
   (&key
    ((:x __x) 0.0)
    ((:y __y) 0.0)
    ((:heading __heading) 0.0)
    ((:index __index) 0)
    ((:target_speed __target_speed) 0.0)
    ((:target_brake __target_brake) 0.0)
    ((:target_gear __target_gear) 0.0)
    ((:speed __speed) 0.0)
    ((:steer __steer) 0.0)
    ((:brake __brake) 0)
    ((:gear __gear) 0)
    ((:auto_manual __auto_manual) 0)
    ((:map_folder __map_folder) "")
    ((:map_file __map_file) "")
    )
   (send-super :init)
   (setq _x (float __x))
   (setq _y (float __y))
   (setq _heading (float __heading))
   (setq _index (round __index))
   (setq _target_speed (float __target_speed))
   (setq _target_brake (float __target_brake))
   (setq _target_gear (float __target_gear))
   (setq _speed (float __speed))
   (setq _steer (float __steer))
   (setq _brake (round __brake))
   (setq _gear (round __gear))
   (setq _auto_manual (round __auto_manual))
   (setq _map_folder (string __map_folder))
   (setq _map_file (string __map_file))
   self)
  (:x
   (&optional __x)
   (if __x (setq _x __x)) _x)
  (:y
   (&optional __y)
   (if __y (setq _y __y)) _y)
  (:heading
   (&optional __heading)
   (if __heading (setq _heading __heading)) _heading)
  (:index
   (&optional __index)
   (if __index (setq _index __index)) _index)
  (:target_speed
   (&optional __target_speed)
   (if __target_speed (setq _target_speed __target_speed)) _target_speed)
  (:target_brake
   (&optional __target_brake)
   (if __target_brake (setq _target_brake __target_brake)) _target_brake)
  (:target_gear
   (&optional __target_gear)
   (if __target_gear (setq _target_gear __target_gear)) _target_gear)
  (:speed
   (&optional __speed)
   (if __speed (setq _speed __speed)) _speed)
  (:steer
   (&optional __steer)
   (if __steer (setq _steer __steer)) _steer)
  (:brake
   (&optional __brake)
   (if __brake (setq _brake __brake)) _brake)
  (:gear
   (&optional __gear)
   (if __gear (setq _gear __gear)) _gear)
  (:auto_manual
   (&optional __auto_manual)
   (if __auto_manual (setq _auto_manual __auto_manual)) _auto_manual)
  (:map_folder
   (&optional __map_folder)
   (if __map_folder (setq _map_folder __map_folder)) _map_folder)
  (:map_file
   (&optional __map_file)
   (if __map_file (setq _map_file __map_file)) _map_file)
  (:serialization-length
   ()
   (+
    ;; float64 _x
    8
    ;; float64 _y
    8
    ;; float64 _heading
    8
    ;; int32 _index
    4
    ;; float32 _target_speed
    4
    ;; float32 _target_brake
    4
    ;; float32 _target_gear
    4
    ;; float32 _speed
    4
    ;; float32 _steer
    4
    ;; int32 _brake
    4
    ;; int16 _gear
    2
    ;; int16 _auto_manual
    2
    ;; string _map_folder
    4 (length _map_folder)
    ;; string _map_file
    4 (length _map_file)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64 _x
       (sys::poke _x (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _y
       (sys::poke _y (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _heading
       (sys::poke _heading (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; int32 _index
       (write-long _index s)
     ;; float32 _target_speed
       (sys::poke _target_speed (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _target_brake
       (sys::poke _target_brake (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _target_gear
       (sys::poke _target_gear (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _speed
       (sys::poke _speed (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _steer
       (sys::poke _steer (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; int32 _brake
       (write-long _brake s)
     ;; int16 _gear
       (write-word _gear s)
     ;; int16 _auto_manual
       (write-word _auto_manual s)
     ;; string _map_folder
       (write-long (length _map_folder) s) (princ _map_folder s)
     ;; string _map_file
       (write-long (length _map_file) s) (princ _map_file s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64 _x
     (setq _x (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _y
     (setq _y (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _heading
     (setq _heading (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; int32 _index
     (setq _index (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; float32 _target_speed
     (setq _target_speed (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _target_brake
     (setq _target_brake (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _target_gear
     (setq _target_gear (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _speed
     (setq _speed (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _steer
     (setq _steer (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; int32 _brake
     (setq _brake (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int16 _gear
     (setq _gear (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;; int16 _auto_manual
     (setq _auto_manual (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;; string _map_folder
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _map_folder (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; string _map_file
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _map_file (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(setf (get planner_and_control::Ego :md5sum-) "7b3b99500febf6cd8a603841e01e0e77")
(setf (get planner_and_control::Ego :datatype-) "planner_and_control/Ego")
(setf (get planner_and_control::Ego :definition-)
      "float64 x
float64 y
float64 heading
int32 index
float32 target_speed
float32 target_brake
float32 target_gear
float32 speed
float32 steer
int32 brake
int16 gear
int16 auto_manual
string map_folder
string map_file
")



(provide :planner_and_control/Ego "7b3b99500febf6cd8a603841e01e0e77")


