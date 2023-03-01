// Generated by gencpp from file semi_pkg/Perception.msg
// DO NOT EDIT!


#ifndef SEMI_PKG_MESSAGE_PERCEPTION_H
#define SEMI_PKG_MESSAGE_PERCEPTION_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace semi_pkg
{
template <class ContainerAllocator>
struct Perception_
{
  typedef Perception_<ContainerAllocator> Type;

  Perception_()
    : A_target(0)
    , A_objx(0.0)
    , A_objy(0.0)
    , bbox_size()
    , B_target_x()
    , B_target_y()
    , signname()  {
    }
  Perception_(const ContainerAllocator& _alloc)
    : A_target(0)
    , A_objx(0.0)
    , A_objy(0.0)
    , bbox_size(_alloc)
    , B_target_x(_alloc)
    , B_target_y(_alloc)
    , signname(_alloc)  {
  (void)_alloc;
    }



   typedef int64_t _A_target_type;
  _A_target_type A_target;

   typedef double _A_objx_type;
  _A_objx_type A_objx;

   typedef double _A_objy_type;
  _A_objy_type A_objy;

   typedef std::vector<int64_t, typename ContainerAllocator::template rebind<int64_t>::other >  _bbox_size_type;
  _bbox_size_type bbox_size;

   typedef std::vector<double, typename ContainerAllocator::template rebind<double>::other >  _B_target_x_type;
  _B_target_x_type B_target_x;

   typedef std::vector<double, typename ContainerAllocator::template rebind<double>::other >  _B_target_y_type;
  _B_target_y_type B_target_y;

   typedef std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other >  _signname_type;
  _signname_type signname;





  typedef boost::shared_ptr< ::semi_pkg::Perception_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::semi_pkg::Perception_<ContainerAllocator> const> ConstPtr;

}; // struct Perception_

typedef ::semi_pkg::Perception_<std::allocator<void> > Perception;

typedef boost::shared_ptr< ::semi_pkg::Perception > PerceptionPtr;
typedef boost::shared_ptr< ::semi_pkg::Perception const> PerceptionConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::semi_pkg::Perception_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::semi_pkg::Perception_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::semi_pkg::Perception_<ContainerAllocator1> & lhs, const ::semi_pkg::Perception_<ContainerAllocator2> & rhs)
{
  return lhs.A_target == rhs.A_target &&
    lhs.A_objx == rhs.A_objx &&
    lhs.A_objy == rhs.A_objy &&
    lhs.bbox_size == rhs.bbox_size &&
    lhs.B_target_x == rhs.B_target_x &&
    lhs.B_target_y == rhs.B_target_y &&
    lhs.signname == rhs.signname;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::semi_pkg::Perception_<ContainerAllocator1> & lhs, const ::semi_pkg::Perception_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace semi_pkg

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsFixedSize< ::semi_pkg::Perception_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::semi_pkg::Perception_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct IsMessage< ::semi_pkg::Perception_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::semi_pkg::Perception_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::semi_pkg::Perception_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::semi_pkg::Perception_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::semi_pkg::Perception_<ContainerAllocator> >
{
  static const char* value()
  {
    return "dbbed136df240d7f479ccfd9293ea715";
  }

  static const char* value(const ::semi_pkg::Perception_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0xdbbed136df240d7fULL;
  static const uint64_t static_value2 = 0x479ccfd9293ea715ULL;
};

template<class ContainerAllocator>
struct DataType< ::semi_pkg::Perception_<ContainerAllocator> >
{
  static const char* value()
  {
    return "semi_pkg/Perception";
  }

  static const char* value(const ::semi_pkg::Perception_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::semi_pkg::Perception_<ContainerAllocator> >
{
  static const char* value()
  {
    return "int64 A_target \n"
"float64 A_objx\n"
"float64 A_objy\n"
"\n"
"int64[] bbox_size\n"
"float64[] B_target_x\n"
"float64[] B_target_y\n"
"\n"
"string signname\n"
;
  }

  static const char* value(const ::semi_pkg::Perception_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::semi_pkg::Perception_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.A_target);
      stream.next(m.A_objx);
      stream.next(m.A_objy);
      stream.next(m.bbox_size);
      stream.next(m.B_target_x);
      stream.next(m.B_target_y);
      stream.next(m.signname);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct Perception_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::semi_pkg::Perception_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::semi_pkg::Perception_<ContainerAllocator>& v)
  {
    s << indent << "A_target: ";
    Printer<int64_t>::stream(s, indent + "  ", v.A_target);
    s << indent << "A_objx: ";
    Printer<double>::stream(s, indent + "  ", v.A_objx);
    s << indent << "A_objy: ";
    Printer<double>::stream(s, indent + "  ", v.A_objy);
    s << indent << "bbox_size[]" << std::endl;
    for (size_t i = 0; i < v.bbox_size.size(); ++i)
    {
      s << indent << "  bbox_size[" << i << "]: ";
      Printer<int64_t>::stream(s, indent + "  ", v.bbox_size[i]);
    }
    s << indent << "B_target_x[]" << std::endl;
    for (size_t i = 0; i < v.B_target_x.size(); ++i)
    {
      s << indent << "  B_target_x[" << i << "]: ";
      Printer<double>::stream(s, indent + "  ", v.B_target_x[i]);
    }
    s << indent << "B_target_y[]" << std::endl;
    for (size_t i = 0; i < v.B_target_y.size(); ++i)
    {
      s << indent << "  B_target_y[" << i << "]: ";
      Printer<double>::stream(s, indent + "  ", v.B_target_y[i]);
    }
    s << indent << "signname: ";
    Printer<std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other > >::stream(s, indent + "  ", v.signname);
  }
};

} // namespace message_operations
} // namespace ros

#endif // SEMI_PKG_MESSAGE_PERCEPTION_H
