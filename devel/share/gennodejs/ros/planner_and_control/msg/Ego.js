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

class Ego {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.x = null;
      this.y = null;
      this.heading = null;
      this.index = null;
      this.target_speed = null;
      this.target_brake = null;
      this.target_gear = null;
      this.speed = null;
      this.steer = null;
      this.brake = null;
      this.gear = null;
      this.auto_manual = null;
      this.map_folder = null;
      this.map_file = null;
    }
    else {
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
      if (initObj.hasOwnProperty('index')) {
        this.index = initObj.index
      }
      else {
        this.index = 0;
      }
      if (initObj.hasOwnProperty('target_speed')) {
        this.target_speed = initObj.target_speed
      }
      else {
        this.target_speed = 0.0;
      }
      if (initObj.hasOwnProperty('target_brake')) {
        this.target_brake = initObj.target_brake
      }
      else {
        this.target_brake = 0.0;
      }
      if (initObj.hasOwnProperty('target_gear')) {
        this.target_gear = initObj.target_gear
      }
      else {
        this.target_gear = 0.0;
      }
      if (initObj.hasOwnProperty('speed')) {
        this.speed = initObj.speed
      }
      else {
        this.speed = 0.0;
      }
      if (initObj.hasOwnProperty('steer')) {
        this.steer = initObj.steer
      }
      else {
        this.steer = 0.0;
      }
      if (initObj.hasOwnProperty('brake')) {
        this.brake = initObj.brake
      }
      else {
        this.brake = 0;
      }
      if (initObj.hasOwnProperty('gear')) {
        this.gear = initObj.gear
      }
      else {
        this.gear = 0;
      }
      if (initObj.hasOwnProperty('auto_manual')) {
        this.auto_manual = initObj.auto_manual
      }
      else {
        this.auto_manual = 0;
      }
      if (initObj.hasOwnProperty('map_folder')) {
        this.map_folder = initObj.map_folder
      }
      else {
        this.map_folder = '';
      }
      if (initObj.hasOwnProperty('map_file')) {
        this.map_file = initObj.map_file
      }
      else {
        this.map_file = '';
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type Ego
    // Serialize message field [x]
    bufferOffset = _serializer.float64(obj.x, buffer, bufferOffset);
    // Serialize message field [y]
    bufferOffset = _serializer.float64(obj.y, buffer, bufferOffset);
    // Serialize message field [heading]
    bufferOffset = _serializer.float64(obj.heading, buffer, bufferOffset);
    // Serialize message field [index]
    bufferOffset = _serializer.int32(obj.index, buffer, bufferOffset);
    // Serialize message field [target_speed]
    bufferOffset = _serializer.float32(obj.target_speed, buffer, bufferOffset);
    // Serialize message field [target_brake]
    bufferOffset = _serializer.float32(obj.target_brake, buffer, bufferOffset);
    // Serialize message field [target_gear]
    bufferOffset = _serializer.float32(obj.target_gear, buffer, bufferOffset);
    // Serialize message field [speed]
    bufferOffset = _serializer.float32(obj.speed, buffer, bufferOffset);
    // Serialize message field [steer]
    bufferOffset = _serializer.float32(obj.steer, buffer, bufferOffset);
    // Serialize message field [brake]
    bufferOffset = _serializer.int32(obj.brake, buffer, bufferOffset);
    // Serialize message field [gear]
    bufferOffset = _serializer.int16(obj.gear, buffer, bufferOffset);
    // Serialize message field [auto_manual]
    bufferOffset = _serializer.int16(obj.auto_manual, buffer, bufferOffset);
    // Serialize message field [map_folder]
    bufferOffset = _serializer.string(obj.map_folder, buffer, bufferOffset);
    // Serialize message field [map_file]
    bufferOffset = _serializer.string(obj.map_file, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type Ego
    let len;
    let data = new Ego(null);
    // Deserialize message field [x]
    data.x = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [y]
    data.y = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [heading]
    data.heading = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [index]
    data.index = _deserializer.int32(buffer, bufferOffset);
    // Deserialize message field [target_speed]
    data.target_speed = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [target_brake]
    data.target_brake = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [target_gear]
    data.target_gear = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [speed]
    data.speed = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [steer]
    data.steer = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [brake]
    data.brake = _deserializer.int32(buffer, bufferOffset);
    // Deserialize message field [gear]
    data.gear = _deserializer.int16(buffer, bufferOffset);
    // Deserialize message field [auto_manual]
    data.auto_manual = _deserializer.int16(buffer, bufferOffset);
    // Deserialize message field [map_folder]
    data.map_folder = _deserializer.string(buffer, bufferOffset);
    // Deserialize message field [map_file]
    data.map_file = _deserializer.string(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += object.map_folder.length;
    length += object.map_file.length;
    return length + 64;
  }

  static datatype() {
    // Returns string type for a message object
    return 'planner_and_control/Ego';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '7b3b99500febf6cd8a603841e01e0e77';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float64 x
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
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new Ego(null);
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

    if (msg.index !== undefined) {
      resolved.index = msg.index;
    }
    else {
      resolved.index = 0
    }

    if (msg.target_speed !== undefined) {
      resolved.target_speed = msg.target_speed;
    }
    else {
      resolved.target_speed = 0.0
    }

    if (msg.target_brake !== undefined) {
      resolved.target_brake = msg.target_brake;
    }
    else {
      resolved.target_brake = 0.0
    }

    if (msg.target_gear !== undefined) {
      resolved.target_gear = msg.target_gear;
    }
    else {
      resolved.target_gear = 0.0
    }

    if (msg.speed !== undefined) {
      resolved.speed = msg.speed;
    }
    else {
      resolved.speed = 0.0
    }

    if (msg.steer !== undefined) {
      resolved.steer = msg.steer;
    }
    else {
      resolved.steer = 0.0
    }

    if (msg.brake !== undefined) {
      resolved.brake = msg.brake;
    }
    else {
      resolved.brake = 0
    }

    if (msg.gear !== undefined) {
      resolved.gear = msg.gear;
    }
    else {
      resolved.gear = 0
    }

    if (msg.auto_manual !== undefined) {
      resolved.auto_manual = msg.auto_manual;
    }
    else {
      resolved.auto_manual = 0
    }

    if (msg.map_folder !== undefined) {
      resolved.map_folder = msg.map_folder;
    }
    else {
      resolved.map_folder = ''
    }

    if (msg.map_file !== undefined) {
      resolved.map_file = msg.map_file;
    }
    else {
      resolved.map_file = ''
    }

    return resolved;
    }
};

module.exports = Ego;
