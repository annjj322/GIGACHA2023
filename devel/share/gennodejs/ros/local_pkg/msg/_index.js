
"use strict";

let SbgMagStatus = require('./SbgMagStatus.js');
let SbgMag = require('./SbgMag.js');
let SbgEkfQuat = require('./SbgEkfQuat.js');
let Master = require('./Master.js');
let Local = require('./Local.js');
let SbgAirDataStatus = require('./SbgAirDataStatus.js');
let SbgShipMotionStatus = require('./SbgShipMotionStatus.js');
let SbgImuData = require('./SbgImuData.js');
let SbgAirData = require('./SbgAirData.js');
let SbgGpsRaw = require('./SbgGpsRaw.js');
let SbgStatusCom = require('./SbgStatusCom.js');
let SbgGpsVel = require('./SbgGpsVel.js');
let SbgGpsPosStatus = require('./SbgGpsPosStatus.js');
let Perception = require('./Perception.js');
let SbgUtcTime = require('./SbgUtcTime.js');
let SbgGpsVelStatus = require('./SbgGpsVelStatus.js');
let SbgEkfNav = require('./SbgEkfNav.js');
let SbgGpsHdt = require('./SbgGpsHdt.js');
let SbgGpsPos = require('./SbgGpsPos.js');
let SbgEkfStatus = require('./SbgEkfStatus.js');
let SbgStatusGeneral = require('./SbgStatusGeneral.js');
let Path = require('./Path.js');
let SbgImuStatus = require('./SbgImuStatus.js');
let Serial_Info = require('./Serial_Info.js');
let SbgShipMotion = require('./SbgShipMotion.js');
let SbgImuShort = require('./SbgImuShort.js');
let Control_Info = require('./Control_Info.js');
let SbgStatus = require('./SbgStatus.js');
let SbgEvent = require('./SbgEvent.js');
let SbgStatusAiding = require('./SbgStatusAiding.js');
let SbgEkfEuler = require('./SbgEkfEuler.js');
let SbgOdoVel = require('./SbgOdoVel.js');
let SbgUtcTimeStatus = require('./SbgUtcTimeStatus.js');
let SbgMagCalib = require('./SbgMagCalib.js');
let SbgMagStatus = require('./SbgMagStatus.js');
let SbgMag = require('./SbgMag.js');
let SbgEkfQuat = require('./SbgEkfQuat.js');
let Master = require('./Master.js');
let Local = require('./Local.js');
let SbgAirDataStatus = require('./SbgAirDataStatus.js');
let SbgShipMotionStatus = require('./SbgShipMotionStatus.js');
let SbgImuData = require('./SbgImuData.js');
let SbgAirData = require('./SbgAirData.js');
let SbgGpsRaw = require('./SbgGpsRaw.js');
let SbgStatusCom = require('./SbgStatusCom.js');
let SbgGpsVel = require('./SbgGpsVel.js');
let SbgGpsPosStatus = require('./SbgGpsPosStatus.js');
let Perception = require('./Perception.js');
let SbgUtcTime = require('./SbgUtcTime.js');
let SbgGpsVelStatus = require('./SbgGpsVelStatus.js');
let SbgEkfNav = require('./SbgEkfNav.js');
let SbgGpsHdt = require('./SbgGpsHdt.js');
let SbgGpsPos = require('./SbgGpsPos.js');
let SbgEkfStatus = require('./SbgEkfStatus.js');
let SbgStatusGeneral = require('./SbgStatusGeneral.js');
let Path = require('./Path.js');
let SbgImuStatus = require('./SbgImuStatus.js');
let Serial_Info = require('./Serial_Info.js');
let SbgShipMotion = require('./SbgShipMotion.js');
let SbgImuShort = require('./SbgImuShort.js');
let Control_Info = require('./Control_Info.js');
let SbgStatus = require('./SbgStatus.js');
let SbgEvent = require('./SbgEvent.js');
let SbgStatusAiding = require('./SbgStatusAiding.js');
let SbgEkfEuler = require('./SbgEkfEuler.js');
let SbgOdoVel = require('./SbgOdoVel.js');
let SbgUtcTimeStatus = require('./SbgUtcTimeStatus.js');
let SbgMagCalib = require('./SbgMagCalib.js');

module.exports = {
  SbgMagStatus: SbgMagStatus,
  SbgMag: SbgMag,
  SbgEkfQuat: SbgEkfQuat,
  Master: Master,
  Local: Local,
  SbgAirDataStatus: SbgAirDataStatus,
  SbgShipMotionStatus: SbgShipMotionStatus,
  SbgImuData: SbgImuData,
  SbgAirData: SbgAirData,
  SbgGpsRaw: SbgGpsRaw,
  SbgStatusCom: SbgStatusCom,
  SbgGpsVel: SbgGpsVel,
  SbgGpsPosStatus: SbgGpsPosStatus,
  Perception: Perception,
  SbgUtcTime: SbgUtcTime,
  SbgGpsVelStatus: SbgGpsVelStatus,
  SbgEkfNav: SbgEkfNav,
  SbgGpsHdt: SbgGpsHdt,
  SbgGpsPos: SbgGpsPos,
  SbgEkfStatus: SbgEkfStatus,
  SbgStatusGeneral: SbgStatusGeneral,
  Path: Path,
  SbgImuStatus: SbgImuStatus,
  Serial_Info: Serial_Info,
  SbgShipMotion: SbgShipMotion,
  SbgImuShort: SbgImuShort,
  Control_Info: Control_Info,
  SbgStatus: SbgStatus,
  SbgEvent: SbgEvent,
  SbgStatusAiding: SbgStatusAiding,
  SbgEkfEuler: SbgEkfEuler,
  SbgOdoVel: SbgOdoVel,
  SbgUtcTimeStatus: SbgUtcTimeStatus,
  SbgMagCalib: SbgMagCalib,
  SbgMagStatus: SbgMagStatus,
  SbgMag: SbgMag,
  SbgEkfQuat: SbgEkfQuat,
  Master: Master,
  Local: Local,
  SbgAirDataStatus: SbgAirDataStatus,
  SbgShipMotionStatus: SbgShipMotionStatus,
  SbgImuData: SbgImuData,
  SbgAirData: SbgAirData,
  SbgGpsRaw: SbgGpsRaw,
  SbgStatusCom: SbgStatusCom,
  SbgGpsVel: SbgGpsVel,
  SbgGpsPosStatus: SbgGpsPosStatus,
  Perception: Perception,
  SbgUtcTime: SbgUtcTime,
  SbgGpsVelStatus: SbgGpsVelStatus,
  SbgEkfNav: SbgEkfNav,
  SbgGpsHdt: SbgGpsHdt,
  SbgGpsPos: SbgGpsPos,
  SbgEkfStatus: SbgEkfStatus,
  SbgStatusGeneral: SbgStatusGeneral,
  Path: Path,
  SbgImuStatus: SbgImuStatus,
  Serial_Info: Serial_Info,
  SbgShipMotion: SbgShipMotion,
  SbgImuShort: SbgImuShort,
  Control_Info: Control_Info,
  SbgStatus: SbgStatus,
  SbgEvent: SbgEvent,
  SbgStatusAiding: SbgStatusAiding,
  SbgEkfEuler: SbgEkfEuler,
  SbgOdoVel: SbgOdoVel,
  SbgUtcTimeStatus: SbgUtcTimeStatus,
  SbgMagCalib: SbgMagCalib,
};
