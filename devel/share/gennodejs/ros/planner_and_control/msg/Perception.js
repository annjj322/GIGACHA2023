// Auto-generated. Do not edit!

// (in-package planner_and_control.msg)


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
      this.objx = null;
      this.objy = null;
      this.objr = null;
      this.signname = null;
      this.signx = null;
      this.signy = null;
      this.rightx = null;
      this.righty = null;
      this.tred = null;
      this.tyellow = null;
      this.tleft = null;
      this.tgreen = null;
      this.stop = null;
    }
    else {
      if (initObj.hasOwnProperty('objx')) {
        this.objx = initObj.objx
      }
      else {
        this.objx = [];
      }
      if (initObj.hasOwnProperty('objy')) {
        this.objy = initObj.objy
      }
      else {
        this.objy = [];
      }
      if (initObj.hasOwnProperty('objr')) {
        this.objr = initObj.objr
      }
      else {
        this.objr = [];
      }
      if (initObj.hasOwnProperty('signname')) {
        this.signname = initObj.signname
      }
      else {
        this.signname = '';
      }
      if (initObj.hasOwnProperty('signx')) {
        this.signx = initObj.signx
      }
      else {
        this.signx = [];
      }
      if (initObj.hasOwnProperty('signy')) {
        this.signy = initObj.signy
      }
      else {
        this.signy = [];
      }
      if (initObj.hasOwnProperty('rightx')) {
        this.rightx = initObj.rightx
      }
      else {
        this.rightx = [];
      }
      if (initObj.hasOwnProperty('righty')) {
        this.righty = initObj.righty
      }
      else {
        this.righty = [];
      }
      if (initObj.hasOwnProperty('tred')) {
        this.tred = initObj.tred
      }
      else {
        this.tred = false;
      }
      if (initObj.hasOwnProperty('tyellow')) {
        this.tyellow = initObj.tyellow
      }
      else {
        this.tyellow = false;
      }
      if (initObj.hasOwnProperty('tleft')) {
        this.tleft = initObj.tleft
      }
      else {
        this.tleft = false;
      }
      if (initObj.hasOwnProperty('tgreen')) {
        this.tgreen = initObj.tgreen
      }
      else {
        this.tgreen = false;
      }
      if (initObj.hasOwnProperty('stop')) {
        this.stop = initObj.stop
      }
      else {
        this.stop = false;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type Perception
    // Serialize message field [objx]
    bufferOffset = _arraySerializer.float64(obj.objx, buffer, bufferOffset, null);
    // Serialize message field [objy]
    bufferOffset = _arraySerializer.float64(obj.objy, buffer, bufferOffset, null);
    // Serialize message field [objr]
    bufferOffset = _arraySerializer.float64(obj.objr, buffer, bufferOffset, null);
    // Serialize message field [signname]
    bufferOffset = _serializer.string(obj.signname, buffer, bufferOffset);
    // Serialize message field [signx]
    bufferOffset = _arraySerializer.float64(obj.signx, buffer, bufferOffset, null);
    // Serialize message field [signy]
    bufferOffset = _arraySerializer.float64(obj.signy, buffer, bufferOffset, null);
    // Serialize message field [rightx]
    bufferOffset = _arraySerializer.float64(obj.rightx, buffer, bufferOffset, null);
    // Serialize message field [righty]
    bufferOffset = _arraySerializer.float64(obj.righty, buffer, bufferOffset, null);
    // Serialize message field [tred]
    bufferOffset = _serializer.bool(obj.tred, buffer, bufferOffset);
    // Serialize message field [tyellow]
    bufferOffset = _serializer.bool(obj.tyellow, buffer, bufferOffset);
    // Serialize message field [tleft]
    bufferOffset = _serializer.bool(obj.tleft, buffer, bufferOffset);
    // Serialize message field [tgreen]
    bufferOffset = _serializer.bool(obj.tgreen, buffer, bufferOffset);
    // Serialize message field [stop]
    bufferOffset = _serializer.bool(obj.stop, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type Perception
    let len;
    let data = new Perception(null);
    // Deserialize message field [objx]
    data.objx = _arrayDeserializer.float64(buffer, bufferOffset, null)
    // Deserialize message field [objy]
    data.objy = _arrayDeserializer.float64(buffer, bufferOffset, null)
    // Deserialize message field [objr]
    data.objr = _arrayDeserializer.float64(buffer, bufferOffset, null)
    // Deserialize message field [signname]
    data.signname = _deserializer.string(buffer, bufferOffset);
    // Deserialize message field [signx]
    data.signx = _arrayDeserializer.float64(buffer, bufferOffset, null)
    // Deserialize message field [signy]
    data.signy = _arrayDeserializer.float64(buffer, bufferOffset, null)
    // Deserialize message field [rightx]
    data.rightx = _arrayDeserializer.float64(buffer, bufferOffset, null)
    // Deserialize message field [righty]
    data.righty = _arrayDeserializer.float64(buffer, bufferOffset, null)
    // Deserialize message field [tred]
    data.tred = _deserializer.bool(buffer, bufferOffset);
    // Deserialize message field [tyellow]
    data.tyellow = _deserializer.bool(buffer, bufferOffset);
    // Deserialize message field [tleft]
    data.tleft = _deserializer.bool(buffer, bufferOffset);
    // Deserialize message field [tgreen]
    data.tgreen = _deserializer.bool(buffer, bufferOffset);
    // Deserialize message field [stop]
    data.stop = _deserializer.bool(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += 8 * object.objx.length;
    length += 8 * object.objy.length;
    length += 8 * object.objr.length;
    length += object.signname.length;
    length += 8 * object.signx.length;
    length += 8 * object.signy.length;
    length += 8 * object.rightx.length;
    length += 8 * object.righty.length;
    return length + 37;
  }

  static datatype() {
    // Returns string type for a message object
    return 'planner_and_control/Perception';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'ac796173eec7500d90ff0331b9cf57b9';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float64[] objx
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
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new Perception(null);
    if (msg.objx !== undefined) {
      resolved.objx = msg.objx;
    }
    else {
      resolved.objx = []
    }

    if (msg.objy !== undefined) {
      resolved.objy = msg.objy;
    }
    else {
      resolved.objy = []
    }

    if (msg.objr !== undefined) {
      resolved.objr = msg.objr;
    }
    else {
      resolved.objr = []
    }

    if (msg.signname !== undefined) {
      resolved.signname = msg.signname;
    }
    else {
      resolved.signname = ''
    }

    if (msg.signx !== undefined) {
      resolved.signx = msg.signx;
    }
    else {
      resolved.signx = []
    }

    if (msg.signy !== undefined) {
      resolved.signy = msg.signy;
    }
    else {
      resolved.signy = []
    }

    if (msg.rightx !== undefined) {
      resolved.rightx = msg.rightx;
    }
    else {
      resolved.rightx = []
    }

    if (msg.righty !== undefined) {
      resolved.righty = msg.righty;
    }
    else {
      resolved.righty = []
    }

    if (msg.tred !== undefined) {
      resolved.tred = msg.tred;
    }
    else {
      resolved.tred = false
    }

    if (msg.tyellow !== undefined) {
      resolved.tyellow = msg.tyellow;
    }
    else {
      resolved.tyellow = false
    }

    if (msg.tleft !== undefined) {
      resolved.tleft = msg.tleft;
    }
    else {
      resolved.tleft = false
    }

    if (msg.tgreen !== undefined) {
      resolved.tgreen = msg.tgreen;
    }
    else {
      resolved.tgreen = false
    }

    if (msg.stop !== undefined) {
      resolved.stop = msg.stop;
    }
    else {
      resolved.stop = false
    }

    return resolved;
    }
};

module.exports = Perception;
