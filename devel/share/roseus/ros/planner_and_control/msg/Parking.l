;; Auto-generated. Do not edit!


(when (boundp 'planner_and_control::Parking)
  (if (not (find-package "PLANNER_AND_CONTROL"))
    (make-package "PLANNER_AND_CONTROL"))
  (shadow 'Parking (find-package "PLANNER_AND_CONTROL")))
(unless (find-package "PLANNER_AND_CONTROL::PARKING")
  (make-package "PLANNER_AND_CONTROL::PARKING"))

(in-package "ROS")
;;//! \htmlinclude Parking.msg.html


(defclass planner_and_control::Parking
  :super ros::object
  :slots (_index _on ))

(defmethod planner_and_control::Parking
  (:init
   (&key
    ((:index __index) 0)
    ((:on __on) nil)
    )
   (send-super :init)
   (setq _index (round __index))
   (setq _on __on)
   self)
  (:index
   (&optional __index)
   (if __index (setq _index __index)) _index)
  (:on
   (&optional __on)
   (if __on (setq _on __on)) _on)
  (:serialization-length
   ()
   (+
    ;; int32 _index
    4
    ;; bool _on
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int32 _index
       (write-long _index s)
     ;; bool _on
       (if _on (write-byte -1 s) (write-byte 0 s))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int32 _index
     (setq _index (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; bool _on
     (setq _on (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;;
   self)
  )

(setf (get planner_and_control::Parking :md5sum-) "08ee4255d6c0b7ed5813480b1d774735")
(setf (get planner_and_control::Parking :datatype-) "planner_and_control/Parking")
(setf (get planner_and_control::Parking :definition-)
      "int32 index
bool on # for controller target_index (look_ahead)
")



(provide :planner_and_control/Parking "08ee4255d6c0b7ed5813480b1d774735")


