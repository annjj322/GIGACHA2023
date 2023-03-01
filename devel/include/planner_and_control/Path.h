// Generated by gencpp from file planner_and_control/Path.msg
// DO NOT EDIT!


#ifndef PLANNER_AND_CONTROL_MESSAGE_PATH_H
#define PLANNER_AND_CONTROL_MESSAGE_PATH_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace planner_and_control
{
template <class ContainerAllocator>
struct Path_
{
  typedef Path_<ContainerAllocator> Type;

  Path_()
    : x()
    , y()
    , heading()
    , k()
    , select_lane(0)  {
    }
  Path_(const ContainerAllocator& _alloc)
    : x(_alloc)
    , y(_alloc)
    , heading(_alloc)
    , k(_alloc)
    , select_lane(0)  {
  (void)_alloc;
    }



   typedef std::vector<double, typename ContainerAllocator::template rebind<double>::other >  _x_type;
  _x_type x;

   typedef std::vector<double, typename ContainerAllocator::template rebind<double>::other >  _y_type;
  _y_type y;

   typedef std::vector<double, typename ContainerAllocator::template rebind<double>::other >  _heading_type;
  _heading_type heading;

   typedef std::vector<double, typename ContainerAllocator::template rebind<double>::other >  _k_type;
  _k_type k;

   typedef int16_t _select_lane_type;
  _select_lane_type select_lane;





  typedef boost::shared_ptr< ::planner_and_control::Path_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::planner_and_control::Path_<ContainerAllocator> const> ConstPtr;

}; // struct Path_

typedef ::planner_and_control::Path_<std::allocator<void> > Path;

typedef boost::shared_ptr< ::planner_and_control::Path > PathPtr;
typedef boost::shared_ptr< ::planner_and_control::Path const> PathConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::planner_and_control::Path_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::planner_and_control::Path_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::planner_and_control::Path_<ContainerAllocator1> & lhs, const ::planner_and_control::Path_<ContainerAllocator2> & rhs)
{
  return lhs.x == rhs.x &&
    lhs.y == rhs.y &&
    lhs.heading == rhs.heading &&
    lhs.k == rhs.k &&
    lhs.select_lane == rhs.select_lane;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::planner_and_control::Path_<ContainerAllocator1> & lhs, const ::planner_and_control::Path_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace planner_and_control

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsFixedSize< ::planner_and_control::Path_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::planner_and_control::Path_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct IsMessage< ::planner_and_control::Path_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::planner_and_control::Path_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::planner_and_control::Path_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::planner_and_control::Path_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::planner_and_control::Path_<ContainerAllocator> >
{
  static const char* value()
  {
    return "0e23544cfda31e4456235bd2624aadc2";
  }

  static const char* value(const ::planner_and_control::Path_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x0e23544cfda31e44ULL;
  static const uint64_t static_value2 = 0x56235bd2624aadc2ULL;
};

template<class ContainerAllocator>
struct DataType< ::planner_and_control::Path_<ContainerAllocator> >
{
  static const char* value()
  {
    return "planner_and_control/Path";
  }

  static const char* value(const ::planner_and_control::Path_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::planner_and_control::Path_<ContainerAllocator> >
{
  static const char* value()
  {
    return "float64[] x\n"
"float64[] y\n"
"float64[] heading\n"
"float64[] k\n"
"int16 select_lane\n"
;
  }

  static const char* value(const ::planner_and_control::Path_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::planner_and_control::Path_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.x);
      stream.next(m.y);
      stream.next(m.heading);
      stream.next(m.k);
      stream.next(m.select_lane);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct Path_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::planner_and_control::Path_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::planner_and_control::Path_<ContainerAllocator>& v)
  {
    s << indent << "x[]" << std::endl;
    for (size_t i = 0; i < v.x.size(); ++i)
    {
      s << indent << "  x[" << i << "]: ";
      Printer<double>::stream(s, indent + "  ", v.x[i]);
    }
    s << indent << "y[]" << std::endl;
    for (size_t i = 0; i < v.y.size(); ++i)
    {
      s << indent << "  y[" << i << "]: ";
      Printer<double>::stream(s, indent + "  ", v.y[i]);
    }
    s << indent << "heading[]" << std::endl;
    for (size_t i = 0; i < v.heading.size(); ++i)
    {
      s << indent << "  heading[" << i << "]: ";
      Printer<double>::stream(s, indent + "  ", v.heading[i]);
    }
    s << indent << "k[]" << std::endl;
    for (size_t i = 0; i < v.k.size(); ++i)
    {
      s << indent << "  k[" << i << "]: ";
      Printer<double>::stream(s, indent + "  ", v.k[i]);
    }
    s << indent << "select_lane: ";
    Printer<int16_t>::stream(s, indent + "  ", v.select_lane);
  }
};

} // namespace message_operations
} // namespace ros

#endif // PLANNER_AND_CONTROL_MESSAGE_PATH_H
