// Auto-generated. Do not edit!

// (in-package local_pkg.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let geometry_msgs = _finder('geometry_msgs');
let std_msgs = _finder('std_msgs');

//-----------------------------------------------------------

class Local {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.header = null;
      this.x = null;
      this.y = null;
      this.heading = null;
      this.imu_heading = null;
      this.gps_heading = null;
      this.gps_heading_under_4_headAcc = null;
      this.roll = null;
      this.pitch = null;
      this.dr_x = null;
      this.dr_y = null;
      this.dead_m = null;
      this.encoder_left = null;
      this.encoder_right = null;
      this.dead_right = null;
      this.distance = null;
      this.encoder_x = null;
      this.encoder_y = null;
      this.hAcc = null;
      this.headAcc = null;
      this.gear = null;
      this.speeed = null;
      this.gspeed = null;
      this.dis = null;
      this.position_error_between_encoder_and_gps = null;
      this.orientation = null;
      this.distance_x = null;
      this.distance_y = null;
      this.distance_z = null;
    }
    else {
      if (initObj.hasOwnProperty('header')) {
        this.header = initObj.header
      }
      else {
        this.header = new std_msgs.msg.Header();
      }
      if (initObj.hasOwnProperty('x')) {
        this.x = initObj.x
      }
      else {
        this.x = 0.0;
      }
      if (initObj.hasOwnProperty('y')) {
        this.y = initObj.y
      }
      else {
        this.y = 0.0;
      }
      if (initObj.hasOwnProperty('heading')) {
        this.heading = initObj.heading
      }
      else {
        this.heading = 0.0;
      }
      if (initObj.hasOwnProperty('imu_heading')) {
        this.imu_heading = initObj.imu_heading
      }
      else {
        this.imu_heading = 0.0;
      }
      if (initObj.hasOwnProperty('gps_heading')) {
        this.gps_heading = initObj.gps_heading
      }
      else {
        this.gps_heading = 0.0;
      }
      if (initObj.hasOwnProperty('gps_heading_under_4_headAcc')) {
        this.gps_heading_under_4_headAcc = initObj.gps_heading_under_4_headAcc
      }
      else {
        this.gps_heading_under_4_headAcc = 0.0;
      }
      if (initObj.hasOwnProperty('roll')) {
        this.roll = initObj.roll
      }
      else {
        this.roll = 0.0;
      }
      if (initObj.hasOwnProperty('pitch')) {
        this.pitch = initObj.pitch
      }
      else {
        this.pitch = 0.0;
      }
      if (initObj.hasOwnProperty('dr_x')) {
        this.dr_x = initObj.dr_x
      }
      else {
        this.dr_x = 0.0;
      }
      if (initObj.hasOwnProperty('dr_y')) {
        this.dr_y = initObj.dr_y
      }
      else {
        this.dr_y = 0.0;
      }
      if (initObj.hasOwnProperty('dead_m')) {
        this.dead_m = initObj.dead_m
      }
      else {
        this.dead_m = 0.0;
      }
      if (initObj.hasOwnProperty('encoder_left')) {
        this.encoder_left = initObj.encoder_left
      }
      else {
        this.encoder_left = 0;
      }
      if (initObj.hasOwnProperty('encoder_right')) {
        this.encoder_right = initObj.encoder_right
      }
      else {
        this.encoder_right = 0;
      }
      if (initObj.hasOwnProperty('dead_right')) {
        this.dead_right = initObj.dead_right
      }
      else {
        this.dead_right = 0.0;
      }
      if (initObj.hasOwnProperty('distance')) {
        this.distance = initObj.distance
      }
      else {
        this.distance = 0.0;
      }
      if (initObj.hasOwnProperty('encoder_x')) {
        this.encoder_x = initObj.encoder_x
      }
      else {
        this.encoder_x = 0.0;
      }
      if (initObj.hasOwnProperty('encoder_y')) {
        this.encoder_y = initObj.encoder_y
      }
      else {
        this.encoder_y = 0.0;
      }
      if (initObj.hasOwnProperty('hAcc')) {
        this.hAcc = initObj.hAcc
      }
      else {
        this.hAcc = 0;
      }
      if (initObj.hasOwnProperty('headAcc')) {
        this.headAcc = initObj.headAcc
      }
      else {
        this.headAcc = 0.0;
      }
      if (initObj.hasOwnProperty('gear')) {
        this.gear = initObj.gear
      }
      else {
        this.gear = 0;
      }
      if (initObj.hasOwnProperty('speeed')) {
        this.speeed = initObj.speeed
      }
      else {
        this.speeed = 0.0;
      }
      if (initObj.hasOwnProperty('gspeed')) {
        this.gspeed = initObj.gspeed
      }
      else {
        this.gspeed = 0.0;
      }
      if (initObj.hasOwnProperty('dis')) {
        this.dis = initObj.dis
      }
      else {
        this.dis = 0.0;
      }
      if (initObj.hasOwnProperty('position_error_between_encoder_and_gps')) {
        this.position_error_between_encoder_and_gps = initObj.position_error_between_encoder_and_gps
      }
      else {
        this.position_error_between_encoder_and_gps = 0.0;
      }
      if (initObj.hasOwnProperty('orientation')) {
        this.orientation = initObj.orientation
      }
      else {
        this.orientation = new geometry_msgs.msg.Quaternion();
      }
      if (initObj.hasOwnProperty('distance_x')) {
        this.distance_x = initObj.distance_x
      }
      else {
        this.distance_x = 0.0;
      }
      if (initObj.hasOwnProperty('distance_y')) {
        this.distance_y = initObj.distance_y
      }
      else {
        this.distance_y = 0.0;
      }
      if (initObj.hasOwnProperty('distance_z')) {
        this.distance_z = initObj.distance_z
      }
      else {
        this.distance_z = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type Local
    // Serialize message field [header]
    bufferOffset = std_msgs.msg.Header.serialize(obj.header, buffer, bufferOffset);
    // Serialize message field [x]
    bufferOffset = _serializer.float64(obj.x, buffer, bufferOffset);
    // Serialize message field [y]
    bufferOffset = _serializer.float64(obj.y, buffer, bufferOffset);
    // Serialize message field [heading]
    bufferOffset = _serializer.float64(obj.heading, buffer, bufferOffset);
    // Serialize message field [imu_heading]
    bufferOffset = _serializer.float64(obj.imu_heading, buffer, bufferOffset);
    // Serialize message field [gps_heading]
    bufferOffset = _serializer.float64(obj.gps_heading, buffer, bufferOffset);
    // Serialize message field [gps_heading_under_4_headAcc]
    bufferOffset = _serializer.float64(obj.gps_heading_under_4_headAcc, buffer, bufferOffset);
    // Serialize message field [roll]
    bufferOffset = _serializer.float64(obj.roll, buffer, bufferOffset);
    // Serialize message field [pitch]
    bufferOffset = _serializer.float64(obj.pitch, buffer, bufferOffset);
    // Serialize message field [dr_x]
    bufferOffset = _serializer.float64(obj.dr_x, buffer, bufferOffset);
    // Serialize message field [dr_y]
    bufferOffset = _serializer.float64(obj.dr_y, buffer, bufferOffset);
    // Serialize message field [dead_m]
    bufferOffset = _serializer.float64(obj.dead_m, buffer, bufferOffset);
    // Serialize message field [encoder_left]
    bufferOffset = _serializer.int64(obj.encoder_left, buffer, bufferOffset);
    // Serialize message field [encoder_right]
    bufferOffset = _serializer.int64(obj.encoder_right, buffer, bufferOffset);
    // Serialize message field [dead_right]
    bufferOffset = _serializer.float64(obj.dead_right, buffer, bufferOffset);
    // Serialize message field [distance]
    bufferOffset = _serializer.float64(obj.distance, buffer, bufferOffset);
    // Serialize message field [encoder_x]
    bufferOffset = _serializer.float64(obj.encoder_x, buffer, bufferOffset);
    // Serialize message field [encoder_y]
    bufferOffset = _serializer.float64(obj.encoder_y, buffer, bufferOffset);
    // Serialize message field [hAcc]
    bufferOffset = _serializer.int64(obj.hAcc, buffer, bufferOffset);
    // Serialize message field [headAcc]
    bufferOffset = _serializer.float64(obj.headAcc, buffer, bufferOffset);
    // Serialize message field [gear]
    bufferOffset = _serializer.int64(obj.gear, buffer, bufferOffset);
    // Serialize message field [speeed]
    bufferOffset = _serializer.float64(obj.speeed, buffer, bufferOffset);
    // Serialize message field [gspeed]
    bufferOffset = _serializer.float64(obj.gspeed, buffer, bufferOffset);
    // Serialize message field [dis]
    bufferOffset = _serializer.float64(obj.dis, buffer, bufferOffset);
    // Serialize message field [position_error_between_encoder_and_gps]
    bufferOffset = _serializer.float64(obj.position_error_between_encoder_and_gps, buffer, bufferOffset);
    // Serialize message field [orientation]
    bufferOffset = geometry_msgs.msg.Quaternion.serialize(obj.orientation, buffer, bufferOffset);
    // Serialize message field [distance_x]
    bufferOffset = _serializer.float64(obj.distance_x, buffer, bufferOffset);
    // Serialize message field [distance_y]
    bufferOffset = _serializer.float64(obj.distance_y, buffer, bufferOffset);
    // Serialize message field [distance_z]
    bufferOffset = _serializer.float64(obj.distance_z, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type Local
    let len;
    let data = new Local(null);
    // Deserialize message field [header]
    data.header = std_msgs.msg.Header.deserialize(buffer, bufferOffset);
    // Deserialize message field [x]
    data.x = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [y]
    data.y = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [heading]
    data.heading = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [imu_heading]
    data.imu_heading = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [gps_heading]
    data.gps_heading = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [gps_heading_under_4_headAcc]
    data.gps_heading_under_4_headAcc = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [roll]
    data.roll = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [pitch]
    data.pitch = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [dr_x]
    data.dr_x = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [dr_y]
    data.dr_y = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [dead_m]
    data.dead_m = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [encoder_left]
    data.encoder_left = _deserializer.int64(buffer, bufferOffset);
    // Deserialize message field [encoder_right]
    data.encoder_right = _deserializer.int64(buffer, bufferOffset);
    // Deserialize message field [dead_right]
    data.dead_right = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [distance]
    data.distance = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [encoder_x]
    data.encoder_x = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [encoder_y]
    data.encoder_y = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [hAcc]
    data.hAcc = _deserializer.int64(buffer, bufferOffset);
    // Deserialize message field [headAcc]
    data.headAcc = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [gear]
    data.gear = _deserializer.int64(buffer, bufferOffset);
    // Deserialize message field [speeed]
    data.speeed = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [gspeed]
    data.gspeed = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [dis]
    data.dis = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [position_error_between_encoder_and_gps]
    data.position_error_between_encoder_and_gps = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [orientation]
    data.orientation = geometry_msgs.msg.Quaternion.deserialize(buffer, bufferOffset);
    // Deserialize message field [distance_x]
    data.distance_x = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [distance_y]
    data.distance_y = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [distance_z]
    data.distance_z = _deserializer.float64(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += std_msgs.msg.Header.getMessageSize(object.header);
    return length + 248;
  }

  static datatype() {
    // Returns string type for a message object
    return 'local_pkg/Local';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'c9625b1768e07229864bd2960c43b12d';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    std_msgs/Header header
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
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new Local(null);
    if (msg.header !== undefined) {
      resolved.header = std_msgs.msg.Header.Resolve(msg.header)
    }
    else {
      resolved.header = new std_msgs.msg.Header()
    }

    if (msg.x !== undefined) {
      resolved.x = msg.x;
    }
    else {
      resolved.x = 0.0
    }

    if (msg.y !== undefined) {
      resolved.y = msg.y;
    }
    else {
      resolved.y = 0.0
    }

    if (msg.heading !== undefined) {
      resolved.heading = msg.heading;
    }
    else {
      resolved.heading = 0.0
    }

    if (msg.imu_heading !== undefined) {
      resolved.imu_heading = msg.imu_heading;
    }
    else {
      resolved.imu_heading = 0.0
    }

    if (msg.gps_heading !== undefined) {
      resolved.gps_heading = msg.gps_heading;
    }
    else {
      resolved.gps_heading = 0.0
    }

    if (msg.gps_heading_under_4_headAcc !== undefined) {
      resolved.gps_heading_under_4_headAcc = msg.gps_heading_under_4_headAcc;
    }
    else {
      resolved.gps_heading_under_4_headAcc = 0.0
    }

    if (msg.roll !== undefined) {
      resolved.roll = msg.roll;
    }
    else {
      resolved.roll = 0.0
    }

    if (msg.pitch !== undefined) {
      resolved.pitch = msg.pitch;
    }
    else {
      resolved.pitch = 0.0
    }

    if (msg.dr_x !== undefined) {
      resolved.dr_x = msg.dr_x;
    }
    else {
      resolved.dr_x = 0.0
    }

    if (msg.dr_y !== undefined) {
      resolved.dr_y = msg.dr_y;
    }
    else {
      resolved.dr_y = 0.0
    }

    if (msg.dead_m !== undefined) {
      resolved.dead_m = msg.dead_m;
    }
    else {
      resolved.dead_m = 0.0
    }

    if (msg.encoder_left !== undefined) {
      resolved.encoder_left = msg.encoder_left;
    }
    else {
      resolved.encoder_left = 0
    }

    if (msg.encoder_right !== undefined) {
      resolved.encoder_right = msg.encoder_right;
    }
    else {
      resolved.encoder_right = 0
    }

    if (msg.dead_right !== undefined) {
      resolved.dead_right = msg.dead_right;
    }
    else {
      resolved.dead_right = 0.0
    }

    if (msg.distance !== undefined) {
      resolved.distance = msg.distance;
    }
    else {
      resolved.distance = 0.0
    }

    if (msg.encoder_x !== undefined) {
      resolved.encoder_x = msg.encoder_x;
    }
    else {
      resolved.encoder_x = 0.0
    }

    if (msg.encoder_y !== undefined) {
      resolved.encoder_y = msg.encoder_y;
    }
    else {
      resolved.encoder_y = 0.0
    }

    if (msg.hAcc !== undefined) {
      resolved.hAcc = msg.hAcc;
    }
    else {
      resolved.hAcc = 0
    }

    if (msg.headAcc !== undefined) {
      resolved.headAcc = msg.headAcc;
    }
    else {
      resolved.headAcc = 0.0
    }

    if (msg.gear !== undefined) {
      resolved.gear = msg.gear;
    }
    else {
      resolved.gear = 0
    }

    if (msg.speeed !== undefined) {
      resolved.speeed = msg.speeed;
    }
    else {
      resolved.speeed = 0.0
    }

    if (msg.gspeed !== undefined) {
      resolved.gspeed = msg.gspeed;
    }
    else {
      resolved.gspeed = 0.0
    }

    if (msg.dis !== undefined) {
      resolved.dis = msg.dis;
    }
    else {
      resolved.dis = 0.0
    }

    if (msg.position_error_between_encoder_and_gps !== undefined) {
      resolved.position_error_between_encoder_and_gps = msg.position_error_between_encoder_and_gps;
    }
    else {
      resolved.position_error_between_encoder_and_gps = 0.0
    }

    if (msg.orientation !== undefined) {
      resolved.orientation = geometry_msgs.msg.Quaternion.Resolve(msg.orientation)
    }
    else {
      resolved.orientation = new geometry_msgs.msg.Quaternion()
    }

    if (msg.distance_x !== undefined) {
      resolved.distance_x = msg.distance_x;
    }
    else {
      resolved.distance_x = 0.0
    }

    if (msg.distance_y !== undefined) {
      resolved.distance_y = msg.distance_y;
    }
    else {
      resolved.distance_y = 0.0
    }

    if (msg.distance_z !== undefined) {
      resolved.distance_z = msg.distance_z;
    }
    else {
      resolved.distance_z = 0.0
    }

    return resolved;
    }
};

module.exports = Local;
