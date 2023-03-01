;; Auto-generated. Do not edit!


(when (boundp 'final_pkg::Perception)
  (if (not (find-package "FINAL_PKG"))
    (make-package "FINAL_PKG"))
  (shadow 'Perception (find-package "FINAL_PKG")))
(unless (find-package "FINAL_PKG::PERCEPTION")
  (make-package "FINAL_PKG::PERCEPTION"))

(in-package "ROS")
;;//! \htmlinclude Perception.msg.html


(defclass final_pkg::Perception
  :super ros::object
  :slots (_A_target _A_objx _A_objy _bbox_size _B_target_x _B_target_y _signname ))

(defmethod final_pkg::Perception
  (:init
   (&key
    ((:A_target __A_target) 0)
    ((:A_objx __A_objx) 0.0)
    ((:A_objy __A_objy) 0.0)
    ((:bbox_size __bbox_size) (make-array 0 :initial-element 0 :element-type :integer))
    ((:B_target_x __B_target_x) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:B_target_y __B_target_y) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:signname __signname) "")
    )
   (send-super :init)
   (setq _A_target (round __A_target))
   (setq _A_objx (float __A_objx))
   (setq _A_objy (float __A_objy))
   (setq _bbox_size __bbox_size)
   (setq _B_target_x __B_target_x)
   (setq _B_target_y __B_target_y)
   (setq _signname (string __signname))
   self)
  (:A_target
   (&optional __A_target)
   (if __A_target (setq _A_target __A_target)) _A_target)
  (:A_objx
   (&optional __A_objx)
   (if __A_objx (setq _A_objx __A_objx)) _A_objx)
  (:A_objy
   (&optional __A_objy)
   (if __A_objy (setq _A_objy __A_objy)) _A_objy)
  (:bbox_size
   (&optional __bbox_size)
   (if __bbox_size (setq _bbox_size __bbox_size)) _bbox_size)
  (:B_target_x
   (&optional __B_target_x)
   (if __B_target_x (setq _B_target_x __B_target_x)) _B_target_x)
  (:B_target_y
   (&optional __B_target_y)
   (if __B_target_y (setq _B_target_y __B_target_y)) _B_target_y)
  (:signname
   (&optional __signname)
   (if __signname (setq _signname __signname)) _signname)
  (:serialization-length
   ()
   (+
    ;; int64 _A_target
    8
    ;; float64 _A_objx
    8
    ;; float64 _A_objy
    8
    ;; int64[] _bbox_size
    (* 8    (length _bbox_size)) 4
    ;; float64[] _B_target_x
    (* 8    (length _B_target_x)) 4
    ;; float64[] _B_target_y
    (* 8    (length _B_target_y)) 4
    ;; string _signname
    4 (length _signname)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int64 _A_target
#+(or :alpha :irix6 :x86_64)
       (progn (sys::poke _A_target (send s :buffer) (send s :count) :long) (incf (stream-count s) 8))
#-(or :alpha :irix6 :x86_64)
       (cond ((and (class _A_target) (= (length (_A_target . bv)) 2)) ;; bignum
              (write-long (ash (elt (_A_target . bv) 0) 0) s)
              (write-long (ash (elt (_A_target . bv) 1) -1) s))
             ((and (class _A_target) (= (length (_A_target . bv)) 1)) ;; big1
              (write-long (elt (_A_target . bv) 0) s)
              (write-long (if (>= _A_target 0) 0 #xffffffff) s))
             (t                                         ;; integer
              (write-long _A_target s)(write-long (if (>= _A_target 0) 0 #xffffffff) s)))
     ;; float64 _A_objx
       (sys::poke _A_objx (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _A_objy
       (sys::poke _A_objy (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; int64[] _bbox_size
     (write-long (length _bbox_size) s)
     (dotimes (i (length _bbox_size))
#+(or :alpha :irix6 :x86_64)
       (progn (sys::poke (elt _bbox_size i) (send s :buffer) (send s :count) :long) (incf (stream-count s) 8))
#-(or :alpha :irix6 :x86_64)
       (cond ((and (class (elt _bbox_size i)) (= (length ((elt _bbox_size i) . bv)) 2)) ;; bignum
              (write-long (ash (elt ((elt _bbox_size i) . bv) 0) 0) s)
              (write-long (ash (elt ((elt _bbox_size i) . bv) 1) -1) s))
             ((and (class (elt _bbox_size i)) (= (length ((elt _bbox_size i) . bv)) 1)) ;; big1
              (write-long (elt ((elt _bbox_size i) . bv) 0) s)
              (write-long (if (>= (elt _bbox_size i) 0) 0 #xffffffff) s))
             (t                                         ;; integer
              (write-long (elt _bbox_size i) s)(write-long (if (>= (elt _bbox_size i) 0) 0 #xffffffff) s)))
       )
     ;; float64[] _B_target_x
     (write-long (length _B_target_x) s)
     (dotimes (i (length _B_target_x))
       (sys::poke (elt _B_target_x i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64[] _B_target_y
     (write-long (length _B_target_y) s)
     (dotimes (i (length _B_target_y))
       (sys::poke (elt _B_target_y i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; string _signname
       (write-long (length _signname) s) (princ _signname s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int64 _A_target
#+(or :alpha :irix6 :x86_64)
      (setf _A_target (prog1 (sys::peek buf ptr- :long) (incf ptr- 8)))
#-(or :alpha :irix6 :x86_64)
      (setf _A_target (let ((b0 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4)))
                  (b1 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4))))
              (cond ((= b1 -1) b0)
                     ((and (= b1  0)
                           (<= lisp::most-negative-fixnum b0 lisp::most-positive-fixnum))
                      b0)
                    ((= b1  0) (make-instance bignum :size 1 :bv (integer-vector b0)))
                    (t (make-instance bignum :size 2 :bv (integer-vector b0 (ash b1 1)))))))
   ;; float64 _A_objx
     (setq _A_objx (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _A_objy
     (setq _A_objy (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; int64[] _bbox_size
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _bbox_size (instantiate integer-vector n))
     (dotimes (i n)
#+(or :alpha :irix6 :x86_64)
      (setf (elt _bbox_size i) (prog1 (sys::peek buf ptr- :long) (incf ptr- 8)))
#-(or :alpha :irix6 :x86_64)
      (setf (elt _bbox_size i) (let ((b0 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4)))
                  (b1 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4))))
              (cond ((= b1 -1) b0)
                     ((and (= b1  0)
                           (<= lisp::most-negative-fixnum b0 lisp::most-positive-fixnum))
                      b0)
                    ((= b1  0) (make-instance bignum :size 1 :bv (integer-vector b0)))
                    (t (make-instance bignum :size 2 :bv (integer-vector b0 (ash b1 1)))))))
     ))
   ;; float64[] _B_target_x
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _B_target_x (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _B_target_x i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; float64[] _B_target_y
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _B_target_y (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _B_target_y i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; string _signname
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _signname (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(setf (get final_pkg::Perception :md5sum-) "dbbed136df240d7f479ccfd9293ea715")
(setf (get final_pkg::Perception :datatype-) "final_pkg/Perception")
(setf (get final_pkg::Perception :definition-)
      "int64 A_target
float64 A_objx
float64 A_objy

int64[] bbox_size
float64[] B_target_x
float64[] B_target_y

string signname
")



(provide :final_pkg/Perception "dbbed136df240d7f479ccfd9293ea715")


