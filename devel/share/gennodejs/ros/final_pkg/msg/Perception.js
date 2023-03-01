// Auto-generated. Do not edit!

// (in-package final_pkg.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class Perception {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.A_target = null;
      this.A_objx = null;
      this.A_objy = null;
      this.bbox_size = null;
      this.B_target_x = null;
      this.B_target_y = null;
      this.signname = null;
    }
    else {
      if (initObj.hasOwnProperty('A_target')) {
        this.A_target = initObj.A_target
      }
      else {
        this.A_target = 0;
      }
      if (initObj.hasOwnProperty('A_objx')) {
        this.A_objx = initObj.A_objx
      }
      else {
        this.A_objx = 0.0;
      }
      if (initObj.hasOwnProperty('A_objy')) {
        this.A_objy = initObj.A_objy
      }
      else {
        this.A_objy = 0.0;
      }
      if (initObj.hasOwnProperty('bbox_size')) {
        this.bbox_size = initObj.bbox_size
      }
      else {
        this.bbox_size = [];
      }
      if (initObj.hasOwnProperty('B_target_x')) {
        this.B_target_x = initObj.B_target_x
      }
      else {
        this.B_target_x = [];
      }
      if (initObj.hasOwnProperty('B_target_y')) {
        this.B_target_y = initObj.B_target_y
      }
      else {
        this.B_target_y = [];
      }
      if (initObj.hasOwnProperty('signname')) {
        this.signname = initObj.signname
      }
      else {
        this.signname = '';
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type Perception
    // Serialize message field [A_target]
    bufferOffset = _serializer.int64(obj.A_target, buffer, bufferOffset);
    // Serialize message field [A_objx]
    bufferOffset = _serializer.float64(obj.A_objx, buffer, bufferOffset);
    // Serialize message field [A_objy]
    bufferOffset = _serializer.float64(obj.A_objy, buffer, bufferOffset);
    // Serialize message field [bbox_size]
    bufferOffset = _arraySerializer.int64(obj.bbox_size, buffer, bufferOffset, null);
    // Serialize message field [B_target_x]
    bufferOffset = _arraySerializer.float64(obj.B_target_x, buffer, bufferOffset, null);
    // Serialize message field [B_target_y]
    bufferOffset = _arraySerializer.float64(obj.B_target_y, buffer, bufferOffset, null);
    // Serialize message field [signname]
    bufferOffset = _serializer.string(obj.signname, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type Perception
    let len;
    let data = new Perception(null);
    // Deserialize message field [A_target]
    data.A_target = _deserializer.int64(buffer, bufferOffset);
    // Deserialize message field [A_objx]
    data.A_objx = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [A_objy]
    data.A_objy = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [bbox_size]
    data.bbox_size = _arrayDeserializer.int64(buffer, bufferOffset, null)
    // Deserialize message field [B_target_x]
    data.B_target_x = _arrayDeserializer.float64(buffer, bufferOffset, null)
    // Deserialize message field [B_target_y]
    data.B_target_y = _arrayDeserializer.float64(buffer, bufferOffset, null)
    // Deserialize message field [signname]
    data.signname = _deserializer.string(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += 8 * object.bbox_size.length;
    length += 8 * object.B_target_x.length;
    length += 8 * object.B_target_y.length;
    length += object.signname.length;
    return length + 40;
  }

  static datatype() {
    // Returns string type for a message object
    return 'final_pkg/Perception';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'dbbed136df240d7f479ccfd9293ea715';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    int64 A_target
    float64 A_objx
    float64 A_objy
    
    int64[] bbox_size
    float64[] B_target_x
    float64[] B_target_y
    
    string signname
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new Perception(null);
    if (msg.A_target !== undefined) {
      resolved.A_target = msg.A_target;
    }
    else {
      resolved.A_target = 0
    }

    if (msg.A_objx !== undefined) {
      resolved.A_objx = msg.A_objx;
    }
    else {
      resolved.A_objx = 0.0
    }

    if (msg.A_objy !== undefined) {
      resolved.A_objy = msg.A_objy;
    }
    else {
      resolved.A_objy = 0.0
    }

    if (msg.bbox_size !== undefined) {
      resolved.bbox_size = msg.bbox_size;
    }
    else {
      resolved.bbox_size = []
    }

    if (msg.B_target_x !== undefined) {
      resolved.B_target_x = msg.B_target_x;
    }
    else {
      resolved.B_target_x = []
    }

    if (msg.B_target_y !== undefined) {
      resolved.B_target_y = msg.B_target_y;
    }
    else {
      resolved.B_target_y = []
    }

    if (msg.signname !== undefined) {
      resolved.signname = msg.signname;
    }
    else {
      resolved.signname = ''
    }

    return resolved;
    }
};

module.exports = Perception;
