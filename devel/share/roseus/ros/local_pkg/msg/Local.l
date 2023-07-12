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
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass local_pkg::Local
  :super ros::object
  :slots (_header _x _y _heading _imu_heading _gps_heading _gps_heading_under_4_headAcc _roll _pitch _dr_x _dr_y _dead_m _encoder_left _encoder_right _dead_right _distance _encoder_x _encoder_y _hAcc _headAcc _gear _speeed _gspeed _dis _position_error_between_encoder_and_gps _orientation _distance_x _distance_y _distance_z ))

(defmethod local_pkg::Local
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:x __x) 0.0)
    ((:y __y) 0.0)
    ((:heading __heading) 0.0)
    ((:imu_heading __imu_heading) 0.0)
    ((:gps_heading __gps_heading) 0.0)
    ((:gps_heading_under_4_headAcc __gps_heading_under_4_headAcc) 0.0)
    ((:roll __roll) 0.0)
    ((:pitch __pitch) 0.0)
    ((:dr_x __dr_x) 0.0)
    ((:dr_y __dr_y) 0.0)
    ((:dead_m __dead_m) 0.0)
    ((:encoder_left __encoder_left) 0)
    ((:encoder_right __encoder_right) 0)
    ((:dead_right __dead_right) 0.0)
    ((:distance __distance) 0.0)
    ((:encoder_x __encoder_x) 0.0)
    ((:encoder_y __encoder_y) 0.0)
    ((:hAcc __hAcc) 0)
    ((:headAcc __headAcc) 0.0)
    ((:gear __gear) 0)
    ((:speeed __speeed) 0.0)
    ((:gspeed __gspeed) 0.0)
    ((:dis __dis) 0.0)
    ((:position_error_between_encoder_and_gps __position_error_between_encoder_and_gps) 0.0)
    ((:orientation __orientation) (instance geometry_msgs::Quaternion :init))
    ((:distance_x __distance_x) 0.0)
    ((:distance_y __distance_y) 0.0)
    ((:distance_z __distance_z) 0.0)
    )
   (send-super :init)
   (setq _header __header)
   (setq _x (float __x))
   (setq _y (float __y))
   (setq _heading (float __heading))
   (setq _imu_heading (float __imu_heading))
   (setq _gps_heading (float __gps_heading))
   (setq _gps_heading_under_4_headAcc (float __gps_heading_under_4_headAcc))
   (setq _roll (float __roll))
   (setq _pitch (float __pitch))
   (setq _dr_x (float __dr_x))
   (setq _dr_y (float __dr_y))
   (setq _dead_m (float __dead_m))
   (setq _encoder_left (round __encoder_left))
   (setq _encoder_right (round __encoder_right))
   (setq _dead_right (float __dead_right))
   (setq _distance (float __distance))
   (setq _encoder_x (float __encoder_x))
   (setq _encoder_y (float __encoder_y))
   (setq _hAcc (round __hAcc))
   (setq _headAcc (float __headAcc))
   (setq _gear (round __gear))
   (setq _speeed (float __speeed))
   (setq _gspeed (float __gspeed))
   (setq _dis (float __dis))
   (setq _position_error_between_encoder_and_gps (float __position_error_between_encoder_and_gps))
   (setq _orientation __orientation)
   (setq _distance_x (float __distance_x))
   (setq _distance_y (float __distance_y))
   (setq _distance_z (float __distance_z))
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:x
   (&optional __x)
   (if __x (setq _x __x)) _x)
  (:y
   (&optional __y)
   (if __y (setq _y __y)) _y)
  (:heading
   (&optional __heading)
   (if __heading (setq _heading __heading)) _heading)
  (:imu_heading
   (&optional __imu_heading)
   (if __imu_heading (setq _imu_heading __imu_heading)) _imu_heading)
  (:gps_heading
   (&optional __gps_heading)
   (if __gps_heading (setq _gps_heading __gps_heading)) _gps_heading)
  (:gps_heading_under_4_headAcc
   (&optional __gps_heading_under_4_headAcc)
   (if __gps_heading_under_4_headAcc (setq _gps_heading_under_4_headAcc __gps_heading_under_4_headAcc)) _gps_heading_under_4_headAcc)
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
  (:dead_m
   (&optional __dead_m)
   (if __dead_m (setq _dead_m __dead_m)) _dead_m)
  (:encoder_left
   (&optional __encoder_left)
   (if __encoder_left (setq _encoder_left __encoder_left)) _encoder_left)
  (:encoder_right
   (&optional __encoder_right)
   (if __encoder_right (setq _encoder_right __encoder_right)) _encoder_right)
  (:dead_right
   (&optional __dead_right)
   (if __dead_right (setq _dead_right __dead_right)) _dead_right)
  (:distance
   (&optional __distance)
   (if __distance (setq _distance __distance)) _distance)
  (:encoder_x
   (&optional __encoder_x)
   (if __encoder_x (setq _encoder_x __encoder_x)) _encoder_x)
  (:encoder_y
   (&optional __encoder_y)
   (if __encoder_y (setq _encoder_y __encoder_y)) _encoder_y)
  (:hAcc
   (&optional __hAcc)
   (if __hAcc (setq _hAcc __hAcc)) _hAcc)
  (:headAcc
   (&optional __headAcc)
   (if __headAcc (setq _headAcc __headAcc)) _headAcc)
  (:gear
   (&optional __gear)
   (if __gear (setq _gear __gear)) _gear)
  (:speeed
   (&optional __speeed)
   (if __speeed (setq _speeed __speeed)) _speeed)
  (:gspeed
   (&optional __gspeed)
   (if __gspeed (setq _gspeed __gspeed)) _gspeed)
  (:dis
   (&optional __dis)
   (if __dis (setq _dis __dis)) _dis)
  (:position_error_between_encoder_and_gps
   (&optional __position_error_between_encoder_and_gps)
   (if __position_error_between_encoder_and_gps (setq _position_error_between_encoder_and_gps __position_error_between_encoder_and_gps)) _position_error_between_encoder_and_gps)
  (:orientation
   (&rest __orientation)
   (if (keywordp (car __orientation))
       (send* _orientation __orientation)
     (progn
       (if __orientation (setq _orientation (car __orientation)))
       _orientation)))
  (:distance_x
   (&optional __distance_x)
   (if __distance_x (setq _distance_x __distance_x)) _distance_x)
  (:distance_y
   (&optional __distance_y)
   (if __distance_y (setq _distance_y __distance_y)) _distance_y)
  (:distance_z
   (&optional __distance_z)
   (if __distance_z (setq _distance_z __distance_z)) _distance_z)
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; float64 _x
    8
    ;; float64 _y
    8
    ;; float64 _heading
    8
    ;; float64 _imu_heading
    8
    ;; float64 _gps_heading
    8
    ;; float64 _gps_heading_under_4_headAcc
    8
    ;; float64 _roll
    8
    ;; float64 _pitch
    8
    ;; float64 _dr_x
    8
    ;; float64 _dr_y
    8
    ;; float64 _dead_m
    8
    ;; int64 _encoder_left
    8
    ;; int64 _encoder_right
    8
    ;; float64 _dead_right
    8
    ;; float64 _distance
    8
    ;; float64 _encoder_x
    8
    ;; float64 _encoder_y
    8
    ;; int64 _hAcc
    8
    ;; float64 _headAcc
    8
    ;; int64 _gear
    8
    ;; float64 _speeed
    8
    ;; float64 _gspeed
    8
    ;; float64 _dis
    8
    ;; float64 _position_error_between_encoder_and_gps
    8
    ;; geometry_msgs/Quaternion _orientation
    (send _orientation :serialization-length)
    ;; float64 _distance_x
    8
    ;; float64 _distance_y
    8
    ;; float64 _distance_z
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; float64 _x
       (sys::poke _x (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _y
       (sys::poke _y (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _heading
       (sys::poke _heading (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _imu_heading
       (sys::poke _imu_heading (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _gps_heading
       (sys::poke _gps_heading (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _gps_heading_under_4_headAcc
       (sys::poke _gps_heading_under_4_headAcc (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _roll
       (sys::poke _roll (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _pitch
       (sys::poke _pitch (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _dr_x
       (sys::poke _dr_x (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _dr_y
       (sys::poke _dr_y (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _dead_m
       (sys::poke _dead_m (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; int64 _encoder_left
#+(or :alpha :irix6 :x86_64)
       (progn (sys::poke _encoder_left (send s :buffer) (send s :count) :long) (incf (stream-count s) 8))
#-(or :alpha :irix6 :x86_64)
       (cond ((and (class _encoder_left) (= (length (_encoder_left . bv)) 2)) ;; bignum
              (write-long (ash (elt (_encoder_left . bv) 0) 0) s)
              (write-long (ash (elt (_encoder_left . bv) 1) -1) s))
             ((and (class _encoder_left) (= (length (_encoder_left . bv)) 1)) ;; big1
              (write-long (elt (_encoder_left . bv) 0) s)
              (write-long (if (>= _encoder_left 0) 0 #xffffffff) s))
             (t                                         ;; integer
              (write-long _encoder_left s)(write-long (if (>= _encoder_left 0) 0 #xffffffff) s)))
     ;; int64 _encoder_right
#+(or :alpha :irix6 :x86_64)
       (progn (sys::poke _encoder_right (send s :buffer) (send s :count) :long) (incf (stream-count s) 8))
#-(or :alpha :irix6 :x86_64)
       (cond ((and (class _encoder_right) (= (length (_encoder_right . bv)) 2)) ;; bignum
              (write-long (ash (elt (_encoder_right . bv) 0) 0) s)
              (write-long (ash (elt (_encoder_right . bv) 1) -1) s))
             ((and (class _encoder_right) (= (length (_encoder_right . bv)) 1)) ;; big1
              (write-long (elt (_encoder_right . bv) 0) s)
              (write-long (if (>= _encoder_right 0) 0 #xffffffff) s))
             (t                                         ;; integer
              (write-long _encoder_right s)(write-long (if (>= _encoder_right 0) 0 #xffffffff) s)))
     ;; float64 _dead_right
       (sys::poke _dead_right (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _distance
       (sys::poke _distance (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _encoder_x
       (sys::poke _encoder_x (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _encoder_y
       (sys::poke _encoder_y (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
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
     ;; float64 _headAcc
       (sys::poke _headAcc (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; int64 _gear
#+(or :alpha :irix6 :x86_64)
       (progn (sys::poke _gear (send s :buffer) (send s :count) :long) (incf (stream-count s) 8))
#-(or :alpha :irix6 :x86_64)
       (cond ((and (class _gear) (= (length (_gear . bv)) 2)) ;; bignum
              (write-long (ash (elt (_gear . bv) 0) 0) s)
              (write-long (ash (elt (_gear . bv) 1) -1) s))
             ((and (class _gear) (= (length (_gear . bv)) 1)) ;; big1
              (write-long (elt (_gear . bv) 0) s)
              (write-long (if (>= _gear 0) 0 #xffffffff) s))
             (t                                         ;; integer
              (write-long _gear s)(write-long (if (>= _gear 0) 0 #xffffffff) s)))
     ;; float64 _speeed
       (sys::poke _speeed (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _gspeed
       (sys::poke _gspeed (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _dis
       (sys::poke _dis (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _position_error_between_encoder_and_gps
       (sys::poke _position_error_between_encoder_and_gps (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; geometry_msgs/Quaternion _orientation
       (send _orientation :serialize s)
     ;; float64 _distance_x
       (sys::poke _distance_x (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _distance_y
       (sys::poke _distance_y (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _distance_z
       (sys::poke _distance_z (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; float64 _x
     (setq _x (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _y
     (setq _y (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _heading
     (setq _heading (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _imu_heading
     (setq _imu_heading (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _gps_heading
     (setq _gps_heading (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _gps_heading_under_4_headAcc
     (setq _gps_heading_under_4_headAcc (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _roll
     (setq _roll (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _pitch
     (setq _pitch (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _dr_x
     (setq _dr_x (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _dr_y
     (setq _dr_y (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _dead_m
     (setq _dead_m (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; int64 _encoder_left
#+(or :alpha :irix6 :x86_64)
      (setf _encoder_left (prog1 (sys::peek buf ptr- :long) (incf ptr- 8)))
#-(or :alpha :irix6 :x86_64)
      (setf _encoder_left (let ((b0 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4)))
                  (b1 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4))))
              (cond ((= b1 -1) b0)
                     ((and (= b1  0)
                           (<= lisp::most-negative-fixnum b0 lisp::most-positive-fixnum))
                      b0)
                    ((= b1  0) (make-instance bignum :size 1 :bv (integer-vector b0)))
                    (t (make-instance bignum :size 2 :bv (integer-vector b0 (ash b1 1)))))))
   ;; int64 _encoder_right
#+(or :alpha :irix6 :x86_64)
      (setf _encoder_right (prog1 (sys::peek buf ptr- :long) (incf ptr- 8)))
#-(or :alpha :irix6 :x86_64)
      (setf _encoder_right (let ((b0 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4)))
                  (b1 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4))))
              (cond ((= b1 -1) b0)
                     ((and (= b1  0)
                           (<= lisp::most-negative-fixnum b0 lisp::most-positive-fixnum))
                      b0)
                    ((= b1  0) (make-instance bignum :size 1 :bv (integer-vector b0)))
                    (t (make-instance bignum :size 2 :bv (integer-vector b0 (ash b1 1)))))))
   ;; float64 _dead_right
     (setq _dead_right (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _distance
     (setq _distance (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _encoder_x
     (setq _encoder_x (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _encoder_y
     (setq _encoder_y (sys::peek buf ptr- :double)) (incf ptr- 8)
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
   ;; float64 _headAcc
     (setq _headAcc (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; int64 _gear
#+(or :alpha :irix6 :x86_64)
      (setf _gear (prog1 (sys::peek buf ptr- :long) (incf ptr- 8)))
#-(or :alpha :irix6 :x86_64)
      (setf _gear (let ((b0 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4)))
                  (b1 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4))))
              (cond ((= b1 -1) b0)
                     ((and (= b1  0)
                           (<= lisp::most-negative-fixnum b0 lisp::most-positive-fixnum))
                      b0)
                    ((= b1  0) (make-instance bignum :size 1 :bv (integer-vector b0)))
                    (t (make-instance bignum :size 2 :bv (integer-vector b0 (ash b1 1)))))))
   ;; float64 _speeed
     (setq _speeed (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _gspeed
     (setq _gspeed (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _dis
     (setq _dis (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _position_error_between_encoder_and_gps
     (setq _position_error_between_encoder_and_gps (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; geometry_msgs/Quaternion _orientation
     (send _orientation :deserialize buf ptr-) (incf ptr- (send _orientation :serialization-length))
   ;; float64 _distance_x
     (setq _distance_x (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _distance_y
     (setq _distance_y (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _distance_z
     (setq _distance_z (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(setf (get local_pkg::Local :md5sum-) "c9625b1768e07229864bd2960c43b12d")
(setf (get local_pkg::Local :datatype-) "local_pkg/Local")
(setf (get local_pkg::Local :definition-)
      "std_msgs/Header header
float64 x
float64 y
float64 heading
float64 imu_heading
float64 gps_heading
float64 gps_heading_under_4_headAcc
float64 roll
float64 pitch
float64 dr_x
float64 dr_y
float64 dead_m
int64 encoder_left
int64 encoder_right
float64 dead_right
float64 distance
float64 encoder_x
float64 encoder_y
int64 hAcc
float64 headAcc
int64 gear
float64 speeed
float64 gspeed
float64 dis
float64 position_error_between_encoder_and_gps
geometry_msgs/Quaternion orientation
float64 distance_x
float64 distance_y
float64 distance_z

================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
string frame_id

================================================================================
MSG: geometry_msgs/Quaternion
# This represents an orientation in free space in quaternion form.

float64 x
float64 y
float64 z
float64 w

")



(provide :local_pkg/Local "c9625b1768e07229864bd2960c43b12d")


