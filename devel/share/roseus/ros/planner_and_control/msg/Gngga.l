;; Auto-generated. Do not edit!


(when (boundp 'planner_and_control::Gngga)
  (if (not (find-package "PLANNER_AND_CONTROL"))
    (make-package "PLANNER_AND_CONTROL"))
  (shadow 'Gngga (find-package "PLANNER_AND_CONTROL")))
(unless (find-package "PLANNER_AND_CONTROL::GNGGA")
  (make-package "PLANNER_AND_CONTROL::GNGGA"))

(in-package "ROS")
;;//! \htmlinclude Gngga.msg.html


(defclass planner_and_control::Gngga
  :super ros::object
  :slots (_latitude _longitude _quality_indicator ))

(defmethod planner_and_control::Gngga
  (:init
   (&key
    ((:latitude __latitude) 0.0)
    ((:longitude __longitude) 0.0)
    ((:quality_indicator __quality_indicator) "")
    )
   (send-super :init)
   (setq _latitude (float __latitude))
   (setq _longitude (float __longitude))
   (setq _quality_indicator (string __quality_indicator))
   self)
  (:latitude
   (&optional __latitude)
   (if __latitude (setq _latitude __latitude)) _latitude)
  (:longitude
   (&optional __longitude)
   (if __longitude (setq _longitude __longitude)) _longitude)
  (:quality_indicator
   (&optional __quality_indicator)
   (if __quality_indicator (setq _quality_indicator __quality_indicator)) _quality_indicator)
  (:serialization-length
   ()
   (+
    ;; float64 _latitude
    8
    ;; float64 _longitude
    8
    ;; string _quality_indicator
    4 (length _quality_indicator)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64 _latitude
       (sys::poke _latitude (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _longitude
       (sys::poke _longitude (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; string _quality_indicator
       (write-long (length _quality_indicator) s) (princ _quality_indicator s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64 _latitude
     (setq _latitude (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _longitude
     (setq _longitude (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; string _quality_indicator
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _quality_indicator (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(setf (get planner_and_control::Gngga :md5sum-) "887c2979d6bd1163174852792c69db98")
(setf (get planner_and_control::Gngga :datatype-) "planner_and_control/Gngga")
(setf (get planner_and_control::Gngga :definition-)
      "float64 latitude
float64 longitude
string quality_indicator # 0 - fix not available, 1 - GPS fix, 2 - Differential GPS fix


")



(provide :planner_and_control/Gngga "887c2979d6bd1163174852792c69db98")


