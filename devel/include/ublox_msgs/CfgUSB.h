// Generated by gencpp from file ublox_msgs/CfgUSB.msg
// DO NOT EDIT!


#ifndef UBLOX_MSGS_MESSAGE_CFGUSB_H
#define UBLOX_MSGS_MESSAGE_CFGUSB_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace ublox_msgs
{
template <class ContainerAllocator>
struct CfgUSB_
{
  typedef CfgUSB_<ContainerAllocator> Type;

  CfgUSB_()
    : vendorID(0)
    , productID(0)
    , reserved1()
    , reserved2()
    , powerConsumption(0)
    , flags(0)
    , vendorString()
    , productString()
    , serialNumber()  {
      reserved1.assign(0);

      reserved2.assign(0);

      vendorString.assign(0);

      productString.assign(0);

      serialNumber.assign(0);
  }
  CfgUSB_(const ContainerAllocator& _alloc)
    : vendorID(0)
    , productID(0)
    , reserved1()
    , reserved2()
    , powerConsumption(0)
    , flags(0)
    , vendorString()
    , productString()
    , serialNumber()  {
  (void)_alloc;
      reserved1.assign(0);

      reserved2.assign(0);

      vendorString.assign(0);

      productString.assign(0);

      serialNumber.assign(0);
  }



   typedef uint16_t _vendorID_type;
  _vendorID_type vendorID;

   typedef uint16_t _productID_type;
  _productID_type productID;

   typedef boost::array<uint8_t, 2>  _reserved1_type;
  _reserved1_type reserved1;

   typedef boost::array<uint8_t, 2>  _reserved2_type;
  _reserved2_type reserved2;

   typedef uint16_t _powerConsumption_type;
  _powerConsumption_type powerConsumption;

   typedef uint16_t _flags_type;
  _flags_type flags;

   typedef boost::array<int8_t, 32>  _vendorString_type;
  _vendorString_type vendorString;

   typedef boost::array<int8_t, 32>  _productString_type;
  _productString_type productString;

   typedef boost::array<int8_t, 32>  _serialNumber_type;
  _serialNumber_type serialNumber;



// reducing the odds to have name collisions with Windows.h 
#if defined(_WIN32) && defined(CLASS_ID)
  #undef CLASS_ID
#endif
#if defined(_WIN32) && defined(MESSAGE_ID)
  #undef MESSAGE_ID
#endif
#if defined(_WIN32) && defined(FLAGS_RE_ENUM)
  #undef FLAGS_RE_ENUM
#endif
#if defined(_WIN32) && defined(FLAGS_POWER_MODE)
  #undef FLAGS_POWER_MODE
#endif

  enum {
    CLASS_ID = 6u,
    MESSAGE_ID = 27u,
    FLAGS_RE_ENUM = 0u,
    FLAGS_POWER_MODE = 2u,
  };


  typedef boost::shared_ptr< ::ublox_msgs::CfgUSB_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::ublox_msgs::CfgUSB_<ContainerAllocator> const> ConstPtr;

}; // struct CfgUSB_

typedef ::ublox_msgs::CfgUSB_<std::allocator<void> > CfgUSB;

typedef boost::shared_ptr< ::ublox_msgs::CfgUSB > CfgUSBPtr;
typedef boost::shared_ptr< ::ublox_msgs::CfgUSB const> CfgUSBConstPtr;

// constants requiring out of line definition

   

   

   

   



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::ublox_msgs::CfgUSB_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::ublox_msgs::CfgUSB_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::ublox_msgs::CfgUSB_<ContainerAllocator1> & lhs, const ::ublox_msgs::CfgUSB_<ContainerAllocator2> & rhs)
{
  return lhs.vendorID == rhs.vendorID &&
    lhs.productID == rhs.productID &&
    lhs.reserved1 == rhs.reserved1 &&
    lhs.reserved2 == rhs.reserved2 &&
    lhs.powerConsumption == rhs.powerConsumption &&
    lhs.flags == rhs.flags &&
    lhs.vendorString == rhs.vendorString &&
    lhs.productString == rhs.productString &&
    lhs.serialNumber == rhs.serialNumber;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::ublox_msgs::CfgUSB_<ContainerAllocator1> & lhs, const ::ublox_msgs::CfgUSB_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace ublox_msgs

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsFixedSize< ::ublox_msgs::CfgUSB_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::ublox_msgs::CfgUSB_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::ublox_msgs::CfgUSB_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::ublox_msgs::CfgUSB_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::ublox_msgs::CfgUSB_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::ublox_msgs::CfgUSB_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::ublox_msgs::CfgUSB_<ContainerAllocator> >
{
  static const char* value()
  {
    return "d1797a4ed330d6193bc42a443c001b03";
  }

  static const char* value(const ::ublox_msgs::CfgUSB_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0xd1797a4ed330d619ULL;
  static const uint64_t static_value2 = 0x3bc42a443c001b03ULL;
};

template<class ContainerAllocator>
struct DataType< ::ublox_msgs::CfgUSB_<ContainerAllocator> >
{
  static const char* value()
  {
    return "ublox_msgs/CfgUSB";
  }

  static const char* value(const ::ublox_msgs::CfgUSB_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::ublox_msgs::CfgUSB_<ContainerAllocator> >
{
  static const char* value()
  {
    return "# UBX-CFG-USB (0x06 0x1B)\n"
"# USB Configuration\n"
"#\n"
"\n"
"uint8 CLASS_ID = 6\n"
"uint8 MESSAGE_ID = 27 \n"
"\n"
"uint16 vendorID             # Only set to registered Vendor IDs.                     \n"
"                            # Changing this field requires special Host drivers.\n"
"\n"
"uint16 productID            # Product ID. Changing this field requires special  \n"
"                            # Host drivers.\n"
"\n"
"uint8[2] reserved1          # Reserved\n"
"uint8[2] reserved2          # Reserved\n"
"\n"
"uint16 powerConsumption     # Power consumed by the device [mA]\n"
"\n"
"uint16 flags                # various configuration flags (see graphic below)\n"
"uint16 FLAGS_RE_ENUM = 0       # force re-enumeration\n"
"uint16 FLAGS_POWER_MODE = 2    # self-powered (1), bus-powered (0)\n"
"\n"
"int8[32] vendorString      # String containing the vendor name. \n"
"                           # 32 ASCII bytes including 0-termination.\n"
"int8[32] productString     # String containing the product name. \n"
"                           # 32 ASCII bytes including 0-termination.\n"
"int8[32] serialNumber      # String containing the serial number. \n"
"                           # 32 ASCII bytes including 0-termination. \n"
"                           # Changing the String fields requires special Host \n"
"                           # drivers.\n"
;
  }

  static const char* value(const ::ublox_msgs::CfgUSB_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::ublox_msgs::CfgUSB_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.vendorID);
      stream.next(m.productID);
      stream.next(m.reserved1);
      stream.next(m.reserved2);
      stream.next(m.powerConsumption);
      stream.next(m.flags);
      stream.next(m.vendorString);
      stream.next(m.productString);
      stream.next(m.serialNumber);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct CfgUSB_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::ublox_msgs::CfgUSB_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::ublox_msgs::CfgUSB_<ContainerAllocator>& v)
  {
    s << indent << "vendorID: ";
    Printer<uint16_t>::stream(s, indent + "  ", v.vendorID);
    s << indent << "productID: ";
    Printer<uint16_t>::stream(s, indent + "  ", v.productID);
    s << indent << "reserved1[]" << std::endl;
    for (size_t i = 0; i < v.reserved1.size(); ++i)
    {
      s << indent << "  reserved1[" << i << "]: ";
      Printer<uint8_t>::stream(s, indent + "  ", v.reserved1[i]);
    }
    s << indent << "reserved2[]" << std::endl;
    for (size_t i = 0; i < v.reserved2.size(); ++i)
    {
      s << indent << "  reserved2[" << i << "]: ";
      Printer<uint8_t>::stream(s, indent + "  ", v.reserved2[i]);
    }
    s << indent << "powerConsumption: ";
    Printer<uint16_t>::stream(s, indent + "  ", v.powerConsumption);
    s << indent << "flags: ";
    Printer<uint16_t>::stream(s, indent + "  ", v.flags);
    s << indent << "vendorString[]" << std::endl;
    for (size_t i = 0; i < v.vendorString.size(); ++i)
    {
      s << indent << "  vendorString[" << i << "]: ";
      Printer<int8_t>::stream(s, indent + "  ", v.vendorString[i]);
    }
    s << indent << "productString[]" << std::endl;
    for (size_t i = 0; i < v.productString.size(); ++i)
    {
      s << indent << "  productString[" << i << "]: ";
      Printer<int8_t>::stream(s, indent + "  ", v.productString[i]);
    }
    s << indent << "serialNumber[]" << std::endl;
    for (size_t i = 0; i < v.serialNumber.size(); ++i)
    {
      s << indent << "  serialNumber[" << i << "]: ";
      Printer<int8_t>::stream(s, indent + "  ", v.serialNumber[i]);
    }
  }
};

} // namespace message_operations
} // namespace ros

#endif // UBLOX_MSGS_MESSAGE_CFGUSB_H
