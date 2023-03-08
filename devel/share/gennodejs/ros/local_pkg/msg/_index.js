
"use strict";

let Serial_Info = require('./Serial_Info.js');
let SbgStatusAiding = require('./SbgStatusAiding.js');
let SbgGpsPosStatus = require('./SbgGpsPosStatus.js');
let SbgEkfStatus = require('./SbgEkfStatus.js');
let SbgImuData = require('./SbgImuData.js');
let SbgImuStatus = require('./SbgImuStatus.js');
let SbgMagStatus = require('./SbgMagStatus.js');
let SbgEvent = require('./SbgEvent.js');
let SbgUtcTimeStatus = require('./SbgUtcTimeStatus.js');
let SbgShipMotion = require('./SbgShipMotion.js');
let SbgImuShort = require('./SbgImuShort.js');
let SbgMag = require('./SbgMag.js');
let SbgGpsVelStatus = require('./SbgGpsVelStatus.js');
let Control_Info = require('./Control_Info.js');
let SbgShipMotionStatus = require('./SbgShipMotionStatus.js');
let SbgStatusCom = require('./SbgStatusCom.js');
let SbgEkfQuat = require('./SbgEkfQuat.js');
let SbgEkfNav = require('./SbgEkfNav.js');
let Master = require('./Master.js');
let SbgAirDataStatus = require('./SbgAirDataStatus.js');
let Local = require('./Local.js');
let SbgStatusGeneral = require('./SbgStatusGeneral.js');
let SbgUtcTime = require('./SbgUtcTime.js');
let SbgStatus = require('./SbgStatus.js');
let SbgMagCalib = require('./SbgMagCalib.js');
let SbgOdoVel = require('./SbgOdoVel.js');
let SbgGpsPos = require('./SbgGpsPos.js');
let SbgGpsVel = require('./SbgGpsVel.js');
let SbgGpsRaw = require('./SbgGpsRaw.js');
let SbgEkfEuler = require('./SbgEkfEuler.js');
let SbgGpsHdt = require('./SbgGpsHdt.js');
let SbgAirData = require('./SbgAirData.js');
let Serial_Info = require('./Serial_Info.js');
let SbgStatusAiding = require('./SbgStatusAiding.js');
let SbgGpsPosStatus = require('./SbgGpsPosStatus.js');
let SbgEkfStatus = require('./SbgEkfStatus.js');
let SbgImuData = require('./SbgImuData.js');
let SbgImuStatus = require('./SbgImuStatus.js');
let SbgMagStatus = require('./SbgMagStatus.js');
let SbgEvent = require('./SbgEvent.js');
let SbgUtcTimeStatus = require('./SbgUtcTimeStatus.js');
let SbgShipMotion = require('./SbgShipMotion.js');
let SbgImuShort = require('./SbgImuShort.js');
let SbgMag = require('./SbgMag.js');
let SbgGpsVelStatus = require('./SbgGpsVelStatus.js');
let Control_Info = require('./Control_Info.js');
let SbgShipMotionStatus = require('./SbgShipMotionStatus.js');
let SbgStatusCom = require('./SbgStatusCom.js');
let SbgEkfQuat = require('./SbgEkfQuat.js');
let SbgEkfNav = require('./SbgEkfNav.js');
let Master = require('./Master.js');
let SbgAirDataStatus = require('./SbgAirDataStatus.js');
let Local = require('./Local.js');
let SbgStatusGeneral = require('./SbgStatusGeneral.js');
let SbgUtcTime = require('./SbgUtcTime.js');
let SbgStatus = require('./SbgStatus.js');
let SbgMagCalib = require('./SbgMagCalib.js');
let SbgOdoVel = require('./SbgOdoVel.js');
let SbgGpsPos = require('./SbgGpsPos.js');
let SbgGpsVel = require('./SbgGpsVel.js');
let SbgGpsRaw = require('./SbgGpsRaw.js');
let SbgEkfEuler = require('./SbgEkfEuler.js');
let SbgGpsHdt = require('./SbgGpsHdt.js');
let SbgAirData = require('./SbgAirData.js');

module.exports = {
  Serial_Info: Serial_Info,
  SbgStatusAiding: SbgStatusAiding,
  SbgGpsPosStatus: SbgGpsPosStatus,
  SbgEkfStatus: SbgEkfStatus,
  SbgImuData: SbgImuData,
  SbgImuStatus: SbgImuStatus,
  SbgMagStatus: SbgMagStatus,
  SbgEvent: SbgEvent,
  SbgUtcTimeStatus: SbgUtcTimeStatus,
  SbgShipMotion: SbgShipMotion,
  SbgImuShort: SbgImuShort,
  SbgMag: SbgMag,
  SbgGpsVelStatus: SbgGpsVelStatus,
  Control_Info: Control_Info,
  SbgShipMotionStatus: SbgShipMotionStatus,
  SbgStatusCom: SbgStatusCom,
  SbgEkfQuat: SbgEkfQuat,
  SbgEkfNav: SbgEkfNav,
  Master: Master,
  SbgAirDataStatus: SbgAirDataStatus,
  Local: Local,
  SbgStatusGeneral: SbgStatusGeneral,
  SbgUtcTime: SbgUtcTime,
  SbgStatus: SbgStatus,
  SbgMagCalib: SbgMagCalib,
  SbgOdoVel: SbgOdoVel,
  SbgGpsPos: SbgGpsPos,
  SbgGpsVel: SbgGpsVel,
  SbgGpsRaw: SbgGpsRaw,
  SbgEkfEuler: SbgEkfEuler,
  SbgGpsHdt: SbgGpsHdt,
  SbgAirData: SbgAirData,
  Serial_Info: Serial_Info,
  SbgStatusAiding: SbgStatusAiding,
  SbgGpsPosStatus: SbgGpsPosStatus,
  SbgEkfStatus: SbgEkfStatus,
  SbgImuData: SbgImuData,
  SbgImuStatus: SbgImuStatus,
  SbgMagStatus: SbgMagStatus,
  SbgEvent: SbgEvent,
  SbgUtcTimeStatus: SbgUtcTimeStatus,
  SbgShipMotion: SbgShipMotion,
  SbgImuShort: SbgImuShort,
  SbgMag: SbgMag,
  SbgGpsVelStatus: SbgGpsVelStatus,
  Control_Info: Control_Info,
  SbgShipMotionStatus: SbgShipMotionStatus,
  SbgStatusCom: SbgStatusCom,
  SbgEkfQuat: SbgEkfQuat,
  SbgEkfNav: SbgEkfNav,
  Master: Master,
  SbgAirDataStatus: SbgAirDataStatus,
  Local: Local,
  SbgStatusGeneral: SbgStatusGeneral,
  SbgUtcTime: SbgUtcTime,
  SbgStatus: SbgStatus,
  SbgMagCalib: SbgMagCalib,
  SbgOdoVel: SbgOdoVel,
  SbgGpsPos: SbgGpsPos,
  SbgGpsVel: SbgGpsVel,
  SbgGpsRaw: SbgGpsRaw,
  SbgEkfEuler: SbgEkfEuler,
  SbgGpsHdt: SbgGpsHdt,
  SbgAirData: SbgAirData,
};
