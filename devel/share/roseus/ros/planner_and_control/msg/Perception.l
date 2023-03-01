;; Auto-generated. Do not edit!


(when (boundp 'planner_and_control::Perception)
  (if (not (find-package "PLANNER_AND_CONTROL"))
    (make-package "PLANNER_AND_CONTROL"))
  (shadow 'Perception (find-package "PLANNER_AND_CONTROL")))
(unless (find-package "PLANNER_AND_CONTROL::PERCEPTION")
  (make-package "PLANNER_AND_CONTROL::PERCEPTION"))

(in-package "ROS")
;;//! \htmlinclude Perception.msg.html


(defclass planner_and_control::Perception
  :super ros::object
  :slots (_objx _objy _objr _signname _signx _signy _rightx _righty _tred _tyellow _tleft _tgreen _stop ))

(defmethod planner_and_control::Perception
  (:init
   (&key
    ((:objx __objx) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:objy __objy) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:objr __objr) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:signname __signname) "")
    ((:signx __signx) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:signy __signy) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:rightx __rightx) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:righty __righty) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:tred __tred) nil)
    ((:tyellow __tyellow) nil)
    ((:tleft __tleft) nil)
    ((:tgreen __tgreen) nil)
    ((:stop __stop) nil)
    )
   (send-super :init)
   (setq _objx __objx)
   (setq _objy __objy)
   (setq _objr __objr)
   (setq _signname (string __signname))
   (setq _signx __signx)
   (setq _signy __signy)
   (setq _rightx __rightx)
   (setq _righty __righty)
   (setq _tred __tred)
   (setq _tyellow __tyellow)
   (setq _tleft __tleft)
   (setq _tgreen __tgreen)
   (setq _stop __stop)
   self)
  (:objx
   (&optional __objx)
   (if __objx (setq _objx __objx)) _objx)
  (:objy
   (&optional __objy)
   (if __objy (setq _objy __objy)) _objy)
  (:objr
   (&optional __objr)
   (if __objr (setq _objr __objr)) _objr)
  (:signname
   (&optional __signname)
   (if __signname (setq _signname __signname)) _signname)
  (:signx
   (&optional __signx)
   (if __signx (setq _signx __signx)) _signx)
  (:signy
   (&optional __signy)
   (if __signy (setq _signy __signy)) _signy)
  (:rightx
   (&optional __rightx)
   (if __rightx (setq _rightx __rightx)) _rightx)
  (:righty
   (&optional __righty)
   (if __righty (setq _righty __righty)) _righty)
  (:tred
   (&optional __tred)
   (if __tred (setq _tred __tred)) _tred)
  (:tyellow
   (&optional __tyellow)
   (if __tyellow (setq _tyellow __tyellow)) _tyellow)
  (:tleft
   (&optional __tleft)
   (if __tleft (setq _tleft __tleft)) _tleft)
  (:tgreen
   (&optional __tgreen)
   (if __tgreen (setq _tgreen __tgreen)) _tgreen)
  (:stop
   (&optional __stop)
   (if __stop (setq _stop __stop)) _stop)
  (:serialization-length
   ()
   (+
    ;; float64[] _objx
    (* 8    (length _objx)) 4
    ;; float64[] _objy
    (* 8    (length _objy)) 4
    ;; float64[] _objr
    (* 8    (length _objr)) 4
    ;; string _signname
    4 (length _signname)
    ;; float64[] _signx
    (* 8    (length _signx)) 4
    ;; float64[] _signy
    (* 8    (length _signy)) 4
    ;; float64[] _rightx
    (* 8    (length _rightx)) 4
    ;; float64[] _righty
    (* 8    (length _righty)) 4
    ;; bool _tred
    1
    ;; bool _tyellow
    1
    ;; bool _tleft
    1
    ;; bool _tgreen
    1
    ;; bool _stop
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64[] _objx
     (write-long (length _objx) s)
     (dotimes (i (length _objx))
       (sys::poke (elt _objx i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64[] _objy
     (write-long (length _objy) s)
     (dotimes (i (length _objy))
       (sys::poke (elt _objy i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64[] _objr
     (write-long (length _objr) s)
     (dotimes (i (length _objr))
       (sys::poke (elt _objr i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; string _signname
       (write-long (length _signname) s) (princ _signname s)
     ;; float64[] _signx
     (write-long (length _signx) s)
     (dotimes (i (length _signx))
       (sys::poke (elt _signx i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64[] _signy
     (write-long (length _signy) s)
     (dotimes (i (length _signy))
       (sys::poke (elt _signy i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64[] _rightx
     (write-long (length _rightx) s)
     (dotimes (i (length _rightx))
       (sys::poke (elt _rightx i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64[] _righty
     (write-long (length _righty) s)
     (dotimes (i (length _righty))
       (sys::poke (elt _righty i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; bool _tred
       (if _tred (write-byte -1 s) (write-byte 0 s))
     ;; bool _tyellow
       (if _tyellow (write-byte -1 s) (write-byte 0 s))
     ;; bool _tleft
       (if _tleft (write-byte -1 s) (write-byte 0 s))
     ;; bool _tgreen
       (if _tgreen (write-byte -1 s) (write-byte 0 s))
     ;; bool _stop
       (if _stop (write-byte -1 s) (write-byte 0 s))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64[] _objx
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _objx (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _objx i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; float64[] _objy
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _objy (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _objy i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; float64[] _objr
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _objr (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _objr i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; string _signname
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _signname (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; float64[] _signx
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _signx (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _signx i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; float64[] _signy
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _signy (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _signy i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; float64[] _rightx
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _rightx (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _rightx i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; float64[] _righty
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _righty (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _righty i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; bool _tred
     (setq _tred (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; bool _tyellow
     (setq _tyellow (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; bool _tleft
     (setq _tleft (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; bool _tgreen
     (setq _tgreen (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; bool _stop
     (setq _stop (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;;
   self)
  )

(setf (get planner_and_control::Perception :md5sum-) "ac796173eec7500d90ff0331b9cf57b9")
(setf (get planner_and_control::Perception :datatype-) "planner_and_control/Perception")
(setf (get planner_and_control::Perception :definition-)
      "float64[] objx
float64[] objy
float64[] objr

string signname
float64[] signx
float64[] signy

float64[] rightx
float64[] righty

bool tred
bool tyellow
bool tleft
bool tgreen

bool stop
")



(provide :planner_and_control/Perception "ac796173eec7500d90ff0331b9cf57b9")


