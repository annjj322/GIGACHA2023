;; Auto-generated. Do not edit!


(when (boundp 'local_pkg::Local)
  (if (not (find-package "LOCAL_PKG"))
    (make-package "LOCAL_PKG"))
  (shadow 'Local (find-package "LOCAL_PKG")))
(unless (find-package "LOCAL_PKG::LOCAL")
  (make-package "LOCAL_PKG::LOCAL"))

(in-package "ROS")
;;//! \htmlinclude Local.msg.html
(if (not (find-package "GEOMETRY_MSGS"))
  (ros::roseus-add-msgs "geometry_msgs"))


(defclass local_pkg::Local
  :super ros::object
  :slots (_x _y _heading _roll _pitch _dr_x _dr_y _hAcc _speeed _dis _orientation ))

(defmethod local_pkg::Local
  (:init
   (&key
    ((:x __x) 0.0)
    ((:y __y) 0.0)
    ((:heading __heading) 0.0)
    ((:roll __roll) 0.0)
    ((:pitch __pitch) 0.0)
    ((:dr_x __dr_x) 0.0)
    ((:dr_y __dr_y) 0.0)
    ((:hAcc __hAcc) 0)
    ((:speeed __speeed) 0.0)
    ((:dis __dis) 0.0)
    ((:orientation __orientation) (instance geometry_msgs::Quaternion :init))
    )
   (send-super :init)
   (setq _x (float __x))
   (setq _y (float __y))
   (setq _heading (float __heading))
   (setq _roll (float __roll))
   (setq _pitch (float __pitch))
   (setq _dr_x (float __dr_x))
   (setq _dr_y (float __dr_y))
   (setq _hAcc (round __hAcc))
   (setq _speeed (float __speeed))
   (setq _dis (float __dis))
   (setq _orientation __orientation)
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
  (:roll
   (&optional __roll)
   (if __roll (setq _roll __roll)) _roll)
  (:pitch
   (&optional __pitch)
   (if __pitch (setq _pitch __pitch)) _pitch)
  (:dr_x
   (&optional __dr_x)
   (if __dr_x (setq _dr_x __dr_x)) _dr_x)
  (:dr_y
   (&optional __dr_y)
   (if __dr_y (setq _dr_y __dr_y)) _dr_y)
  (:hAcc
   (&optional __hAcc)
   (if __hAcc (setq _hAcc __hAcc)) _hAcc)
  (:speeed
   (&optional __speeed)
   (if __speeed (setq _speeed __speeed)) _speeed)
  (:dis
   (&optional __dis)
   (if __dis (setq _dis __dis)) _dis)
  (:orientation
   (&rest __orientation)
   (if (keywordp (car __orientation))
       (send* _orientation __orientation)
     (progn
       (if __orientation (setq _orientation (car __orientation)))
       _orientation)))
  (:serialization-length
   ()
   (+
    ;; float64 _x
    8
    ;; float64 _y
    8
    ;; float64 _heading
    8
    ;; float64 _roll
    8
    ;; float64 _pitch
    8
    ;; float64 _dr_x
    8
    ;; float64 _dr_y
    8
    ;; int64 _hAcc
    8
    ;; float64 _speeed
    8
    ;; float64 _dis
    8
    ;; geometry_msgs/Quaternion _orientation
    (send _orientation :serialization-length)
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
     ;; float64 _roll
       (sys::poke _roll (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _pitch
       (sys::poke _pitch (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _dr_x
       (sys::poke _dr_x (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _dr_y
       (sys::poke _dr_y (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; int64 _hAcc
#+(or :alpha :irix6 :x86_64)
       (progn (sys::poke _hAcc (send s :buffer) (send s :count) :long) (incf (stream-count s) 8))
#-(or :alpha :irix6 :x86_64)
       (cond ((and (class _hAcc) (= (length (_hAcc . bv)) 2)) ;; bignum
              (write-long (ash (elt (_hAcc . bv) 0) 0) s)
              (write-long (ash (elt (_hAcc . bv) 1) -1) s))
             ((and (class _hAcc) (= (length (_hAcc . bv)) 1)) ;; big1
              (write-long (elt (_hAcc . bv) 0) s)
              (write-long (if (>= _hAcc 0) 0 #xffffffff) s))
             (t                                         ;; integer
              (write-long _hAcc s)(write-long (if (>= _hAcc 0) 0 #xffffffff) s)))
     ;; float64 _speeed
       (sys::poke _speeed (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _dis
       (sys::poke _dis (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; geometry_msgs/Quaternion _orientation
       (send _orientation :serialize s)
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
   ;; float64 _roll
     (setq _roll (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _pitch
     (setq _pitch (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _dr_x
     (setq _dr_x (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _dr_y
     (setq _dr_y (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; int64 _hAcc
#+(or :alpha :irix6 :x86_64)
      (setf _hAcc (prog1 (sys::peek buf ptr- :long) (incf ptr- 8)))
#-(or :alpha :irix6 :x86_64)
      (setf _hAcc (let ((b0 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4)))
                  (b1 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4))))
              (cond ((= b1 -1) b0)
                     ((and (= b1  0)
                           (<= lisp::most-negative-fixnum b0 lisp::most-positive-fixnum))
                      b0)
                    ((= b1  0) (make-instance bignum :size 1 :bv (integer-vector b0)))
                    (t (make-instance bignum :size 2 :bv (integer-vector b0 (ash b1 1)))))))
   ;; float64 _speeed
     (setq _speeed (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _dis
     (setq _dis (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; geometry_msgs/Quaternion _orientation
     (send _orientation :deserialize buf ptr-) (incf ptr- (send _orientation :serialization-length))
   ;;
   self)
  )

(setf (get local_pkg::Local :md5sum-) "02900f6dd7ae8d0a3ed2e4e2d3c5c924")
(setf (get local_pkg::Local :datatype-) "local_pkg/Local")
(setf (get local_pkg::Local :definition-)
      "float64 x
float64 y
float64 heading
float64 roll
float64 pitch
float64 dr_x
float64 dr_y
int64 hAcc
float64 speeed
float64 dis
geometry_msgs/Quaternion orientation

================================================================================
MSG: geometry_msgs/Quaternion
# This represents an orientation in free space in quaternion form.

float64 x
float64 y
float64 z
float64 w

")



(provide :local_pkg/Local "02900f6dd7ae8d0a3ed2e4e2d3c5c924")


