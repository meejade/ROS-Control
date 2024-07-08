// Generated by gencpp from file firsttry/chat.msg
// DO NOT EDIT!


#ifndef FIRSTTRY_MESSAGE_CHAT_H
#define FIRSTTRY_MESSAGE_CHAT_H

#include <ros/service_traits.h>


#include <firsttry/chatRequest.h>
#include <firsttry/chatResponse.h>


namespace firsttry
{

struct chat
{

typedef chatRequest Request;
typedef chatResponse Response;
Request request;
Response response;

typedef Request RequestType;
typedef Response ResponseType;

}; // struct chat
} // namespace firsttry


namespace ros
{
namespace service_traits
{


template<>
struct MD5Sum< ::firsttry::chat > {
  static const char* value()
  {
    return "945e963769938e4ddc3288e80fdfddf4";
  }

  static const char* value(const ::firsttry::chat&) { return value(); }
};

template<>
struct DataType< ::firsttry::chat > {
  static const char* value()
  {
    return "firsttry/chat";
  }

  static const char* value(const ::firsttry::chat&) { return value(); }
};


// service_traits::MD5Sum< ::firsttry::chatRequest> should match
// service_traits::MD5Sum< ::firsttry::chat >
template<>
struct MD5Sum< ::firsttry::chatRequest>
{
  static const char* value()
  {
    return MD5Sum< ::firsttry::chat >::value();
  }
  static const char* value(const ::firsttry::chatRequest&)
  {
    return value();
  }
};

// service_traits::DataType< ::firsttry::chatRequest> should match
// service_traits::DataType< ::firsttry::chat >
template<>
struct DataType< ::firsttry::chatRequest>
{
  static const char* value()
  {
    return DataType< ::firsttry::chat >::value();
  }
  static const char* value(const ::firsttry::chatRequest&)
  {
    return value();
  }
};

// service_traits::MD5Sum< ::firsttry::chatResponse> should match
// service_traits::MD5Sum< ::firsttry::chat >
template<>
struct MD5Sum< ::firsttry::chatResponse>
{
  static const char* value()
  {
    return MD5Sum< ::firsttry::chat >::value();
  }
  static const char* value(const ::firsttry::chatResponse&)
  {
    return value();
  }
};

// service_traits::DataType< ::firsttry::chatResponse> should match
// service_traits::DataType< ::firsttry::chat >
template<>
struct DataType< ::firsttry::chatResponse>
{
  static const char* value()
  {
    return DataType< ::firsttry::chat >::value();
  }
  static const char* value(const ::firsttry::chatResponse&)
  {
    return value();
  }
};

} // namespace service_traits
} // namespace ros

#endif // FIRSTTRY_MESSAGE_CHAT_H