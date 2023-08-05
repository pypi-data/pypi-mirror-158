// Generated by the gRPC C++ plugin.
// If you make any local change, they will be lost.
// source: graphscope/proto/engine_service.proto
// Original file comments:
// Copyright 2020 Alibaba Group Holding Limited. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
//
#ifndef GRPC_graphscope_2fproto_2fengine_5fservice_2eproto__INCLUDED
#define GRPC_graphscope_2fproto_2fengine_5fservice_2eproto__INCLUDED

#include "graphscope/proto/engine_service.pb.h"

#include <functional>
#include <grpc/impl/codegen/port_platform.h>
#include <grpcpp/impl/codegen/async_generic_service.h>
#include <grpcpp/impl/codegen/async_stream.h>
#include <grpcpp/impl/codegen/async_unary_call.h>
#include <grpcpp/impl/codegen/client_callback.h>
#include <grpcpp/impl/codegen/client_context.h>
#include <grpcpp/impl/codegen/completion_queue.h>
#include <grpcpp/impl/codegen/message_allocator.h>
#include <grpcpp/impl/codegen/method_handler.h>
#include <grpcpp/impl/codegen/proto_utils.h>
#include <grpcpp/impl/codegen/rpc_method.h>
#include <grpcpp/impl/codegen/server_callback.h>
#include <grpcpp/impl/codegen/server_callback_handlers.h>
#include <grpcpp/impl/codegen/server_context.h>
#include <grpcpp/impl/codegen/service_type.h>
#include <grpcpp/impl/codegen/status.h>
#include <grpcpp/impl/codegen/stub_options.h>
#include <grpcpp/impl/codegen/sync_stream.h>

namespace gs {
namespace rpc {

class EngineService final {
 public:
  static constexpr char const* service_full_name() {
    return "gs.rpc.EngineService";
  }
  class StubInterface {
   public:
    virtual ~StubInterface() {}
    // Drives the graph computation.
    std::unique_ptr< ::grpc::ClientReaderWriterInterface< ::gs::rpc::RunStepRequest, ::gs::rpc::RunStepResponse>> RunStep(::grpc::ClientContext* context) {
      return std::unique_ptr< ::grpc::ClientReaderWriterInterface< ::gs::rpc::RunStepRequest, ::gs::rpc::RunStepResponse>>(RunStepRaw(context));
    }
    std::unique_ptr< ::grpc::ClientAsyncReaderWriterInterface< ::gs::rpc::RunStepRequest, ::gs::rpc::RunStepResponse>> AsyncRunStep(::grpc::ClientContext* context, ::grpc::CompletionQueue* cq, void* tag) {
      return std::unique_ptr< ::grpc::ClientAsyncReaderWriterInterface< ::gs::rpc::RunStepRequest, ::gs::rpc::RunStepResponse>>(AsyncRunStepRaw(context, cq, tag));
    }
    std::unique_ptr< ::grpc::ClientAsyncReaderWriterInterface< ::gs::rpc::RunStepRequest, ::gs::rpc::RunStepResponse>> PrepareAsyncRunStep(::grpc::ClientContext* context, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncReaderWriterInterface< ::gs::rpc::RunStepRequest, ::gs::rpc::RunStepResponse>>(PrepareAsyncRunStepRaw(context, cq));
    }
    // Heart beat between coordinator and analytical engine
    virtual ::grpc::Status HeartBeat(::grpc::ClientContext* context, const ::gs::rpc::HeartBeatRequest& request, ::gs::rpc::HeartBeatResponse* response) = 0;
    std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::gs::rpc::HeartBeatResponse>> AsyncHeartBeat(::grpc::ClientContext* context, const ::gs::rpc::HeartBeatRequest& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::gs::rpc::HeartBeatResponse>>(AsyncHeartBeatRaw(context, request, cq));
    }
    std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::gs::rpc::HeartBeatResponse>> PrepareAsyncHeartBeat(::grpc::ClientContext* context, const ::gs::rpc::HeartBeatRequest& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::gs::rpc::HeartBeatResponse>>(PrepareAsyncHeartBeatRaw(context, request, cq));
    }
    class experimental_async_interface {
     public:
      virtual ~experimental_async_interface() {}
      // Drives the graph computation.
      #ifdef GRPC_CALLBACK_API_NONEXPERIMENTAL
      virtual void RunStep(::grpc::ClientContext* context, ::grpc::ClientBidiReactor< ::gs::rpc::RunStepRequest,::gs::rpc::RunStepResponse>* reactor) = 0;
      #else
      virtual void RunStep(::grpc::ClientContext* context, ::grpc::experimental::ClientBidiReactor< ::gs::rpc::RunStepRequest,::gs::rpc::RunStepResponse>* reactor) = 0;
      #endif
      // Heart beat between coordinator and analytical engine
      virtual void HeartBeat(::grpc::ClientContext* context, const ::gs::rpc::HeartBeatRequest* request, ::gs::rpc::HeartBeatResponse* response, std::function<void(::grpc::Status)>) = 0;
      #ifdef GRPC_CALLBACK_API_NONEXPERIMENTAL
      virtual void HeartBeat(::grpc::ClientContext* context, const ::gs::rpc::HeartBeatRequest* request, ::gs::rpc::HeartBeatResponse* response, ::grpc::ClientUnaryReactor* reactor) = 0;
      #else
      virtual void HeartBeat(::grpc::ClientContext* context, const ::gs::rpc::HeartBeatRequest* request, ::gs::rpc::HeartBeatResponse* response, ::grpc::experimental::ClientUnaryReactor* reactor) = 0;
      #endif
    };
    #ifdef GRPC_CALLBACK_API_NONEXPERIMENTAL
    typedef class experimental_async_interface async_interface;
    #endif
    #ifdef GRPC_CALLBACK_API_NONEXPERIMENTAL
    async_interface* async() { return experimental_async(); }
    #endif
    virtual class experimental_async_interface* experimental_async() { return nullptr; }
  private:
    virtual ::grpc::ClientReaderWriterInterface< ::gs::rpc::RunStepRequest, ::gs::rpc::RunStepResponse>* RunStepRaw(::grpc::ClientContext* context) = 0;
    virtual ::grpc::ClientAsyncReaderWriterInterface< ::gs::rpc::RunStepRequest, ::gs::rpc::RunStepResponse>* AsyncRunStepRaw(::grpc::ClientContext* context, ::grpc::CompletionQueue* cq, void* tag) = 0;
    virtual ::grpc::ClientAsyncReaderWriterInterface< ::gs::rpc::RunStepRequest, ::gs::rpc::RunStepResponse>* PrepareAsyncRunStepRaw(::grpc::ClientContext* context, ::grpc::CompletionQueue* cq) = 0;
    virtual ::grpc::ClientAsyncResponseReaderInterface< ::gs::rpc::HeartBeatResponse>* AsyncHeartBeatRaw(::grpc::ClientContext* context, const ::gs::rpc::HeartBeatRequest& request, ::grpc::CompletionQueue* cq) = 0;
    virtual ::grpc::ClientAsyncResponseReaderInterface< ::gs::rpc::HeartBeatResponse>* PrepareAsyncHeartBeatRaw(::grpc::ClientContext* context, const ::gs::rpc::HeartBeatRequest& request, ::grpc::CompletionQueue* cq) = 0;
  };
  class Stub final : public StubInterface {
   public:
    Stub(const std::shared_ptr< ::grpc::ChannelInterface>& channel);
    std::unique_ptr< ::grpc::ClientReaderWriter< ::gs::rpc::RunStepRequest, ::gs::rpc::RunStepResponse>> RunStep(::grpc::ClientContext* context) {
      return std::unique_ptr< ::grpc::ClientReaderWriter< ::gs::rpc::RunStepRequest, ::gs::rpc::RunStepResponse>>(RunStepRaw(context));
    }
    std::unique_ptr<  ::grpc::ClientAsyncReaderWriter< ::gs::rpc::RunStepRequest, ::gs::rpc::RunStepResponse>> AsyncRunStep(::grpc::ClientContext* context, ::grpc::CompletionQueue* cq, void* tag) {
      return std::unique_ptr< ::grpc::ClientAsyncReaderWriter< ::gs::rpc::RunStepRequest, ::gs::rpc::RunStepResponse>>(AsyncRunStepRaw(context, cq, tag));
    }
    std::unique_ptr<  ::grpc::ClientAsyncReaderWriter< ::gs::rpc::RunStepRequest, ::gs::rpc::RunStepResponse>> PrepareAsyncRunStep(::grpc::ClientContext* context, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncReaderWriter< ::gs::rpc::RunStepRequest, ::gs::rpc::RunStepResponse>>(PrepareAsyncRunStepRaw(context, cq));
    }
    ::grpc::Status HeartBeat(::grpc::ClientContext* context, const ::gs::rpc::HeartBeatRequest& request, ::gs::rpc::HeartBeatResponse* response) override;
    std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::gs::rpc::HeartBeatResponse>> AsyncHeartBeat(::grpc::ClientContext* context, const ::gs::rpc::HeartBeatRequest& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::gs::rpc::HeartBeatResponse>>(AsyncHeartBeatRaw(context, request, cq));
    }
    std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::gs::rpc::HeartBeatResponse>> PrepareAsyncHeartBeat(::grpc::ClientContext* context, const ::gs::rpc::HeartBeatRequest& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::gs::rpc::HeartBeatResponse>>(PrepareAsyncHeartBeatRaw(context, request, cq));
    }
    class experimental_async final :
      public StubInterface::experimental_async_interface {
     public:
      #ifdef GRPC_CALLBACK_API_NONEXPERIMENTAL
      void RunStep(::grpc::ClientContext* context, ::grpc::ClientBidiReactor< ::gs::rpc::RunStepRequest,::gs::rpc::RunStepResponse>* reactor) override;
      #else
      void RunStep(::grpc::ClientContext* context, ::grpc::experimental::ClientBidiReactor< ::gs::rpc::RunStepRequest,::gs::rpc::RunStepResponse>* reactor) override;
      #endif
      void HeartBeat(::grpc::ClientContext* context, const ::gs::rpc::HeartBeatRequest* request, ::gs::rpc::HeartBeatResponse* response, std::function<void(::grpc::Status)>) override;
      #ifdef GRPC_CALLBACK_API_NONEXPERIMENTAL
      void HeartBeat(::grpc::ClientContext* context, const ::gs::rpc::HeartBeatRequest* request, ::gs::rpc::HeartBeatResponse* response, ::grpc::ClientUnaryReactor* reactor) override;
      #else
      void HeartBeat(::grpc::ClientContext* context, const ::gs::rpc::HeartBeatRequest* request, ::gs::rpc::HeartBeatResponse* response, ::grpc::experimental::ClientUnaryReactor* reactor) override;
      #endif
     private:
      friend class Stub;
      explicit experimental_async(Stub* stub): stub_(stub) { }
      Stub* stub() { return stub_; }
      Stub* stub_;
    };
    class experimental_async_interface* experimental_async() override { return &async_stub_; }

   private:
    std::shared_ptr< ::grpc::ChannelInterface> channel_;
    class experimental_async async_stub_{this};
    ::grpc::ClientReaderWriter< ::gs::rpc::RunStepRequest, ::gs::rpc::RunStepResponse>* RunStepRaw(::grpc::ClientContext* context) override;
    ::grpc::ClientAsyncReaderWriter< ::gs::rpc::RunStepRequest, ::gs::rpc::RunStepResponse>* AsyncRunStepRaw(::grpc::ClientContext* context, ::grpc::CompletionQueue* cq, void* tag) override;
    ::grpc::ClientAsyncReaderWriter< ::gs::rpc::RunStepRequest, ::gs::rpc::RunStepResponse>* PrepareAsyncRunStepRaw(::grpc::ClientContext* context, ::grpc::CompletionQueue* cq) override;
    ::grpc::ClientAsyncResponseReader< ::gs::rpc::HeartBeatResponse>* AsyncHeartBeatRaw(::grpc::ClientContext* context, const ::gs::rpc::HeartBeatRequest& request, ::grpc::CompletionQueue* cq) override;
    ::grpc::ClientAsyncResponseReader< ::gs::rpc::HeartBeatResponse>* PrepareAsyncHeartBeatRaw(::grpc::ClientContext* context, const ::gs::rpc::HeartBeatRequest& request, ::grpc::CompletionQueue* cq) override;
    const ::grpc::internal::RpcMethod rpcmethod_RunStep_;
    const ::grpc::internal::RpcMethod rpcmethod_HeartBeat_;
  };
  static std::unique_ptr<Stub> NewStub(const std::shared_ptr< ::grpc::ChannelInterface>& channel, const ::grpc::StubOptions& options = ::grpc::StubOptions());

  class Service : public ::grpc::Service {
   public:
    Service();
    virtual ~Service();
    // Drives the graph computation.
    virtual ::grpc::Status RunStep(::grpc::ServerContext* context, ::grpc::ServerReaderWriter< ::gs::rpc::RunStepResponse, ::gs::rpc::RunStepRequest>* stream);
    // Heart beat between coordinator and analytical engine
    virtual ::grpc::Status HeartBeat(::grpc::ServerContext* context, const ::gs::rpc::HeartBeatRequest* request, ::gs::rpc::HeartBeatResponse* response);
  };
  template <class BaseClass>
  class WithAsyncMethod_RunStep : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithAsyncMethod_RunStep() {
      ::grpc::Service::MarkMethodAsync(0);
    }
    ~WithAsyncMethod_RunStep() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status RunStep(::grpc::ServerContext* /*context*/, ::grpc::ServerReaderWriter< ::gs::rpc::RunStepResponse, ::gs::rpc::RunStepRequest>* /*stream*/)  override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    void RequestRunStep(::grpc::ServerContext* context, ::grpc::ServerAsyncReaderWriter< ::gs::rpc::RunStepResponse, ::gs::rpc::RunStepRequest>* stream, ::grpc::CompletionQueue* new_call_cq, ::grpc::ServerCompletionQueue* notification_cq, void *tag) {
      ::grpc::Service::RequestAsyncBidiStreaming(0, context, stream, new_call_cq, notification_cq, tag);
    }
  };
  template <class BaseClass>
  class WithAsyncMethod_HeartBeat : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithAsyncMethod_HeartBeat() {
      ::grpc::Service::MarkMethodAsync(1);
    }
    ~WithAsyncMethod_HeartBeat() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status HeartBeat(::grpc::ServerContext* /*context*/, const ::gs::rpc::HeartBeatRequest* /*request*/, ::gs::rpc::HeartBeatResponse* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    void RequestHeartBeat(::grpc::ServerContext* context, ::gs::rpc::HeartBeatRequest* request, ::grpc::ServerAsyncResponseWriter< ::gs::rpc::HeartBeatResponse>* response, ::grpc::CompletionQueue* new_call_cq, ::grpc::ServerCompletionQueue* notification_cq, void *tag) {
      ::grpc::Service::RequestAsyncUnary(1, context, request, response, new_call_cq, notification_cq, tag);
    }
  };
  typedef WithAsyncMethod_RunStep<WithAsyncMethod_HeartBeat<Service > > AsyncService;
  template <class BaseClass>
  class ExperimentalWithCallbackMethod_RunStep : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    ExperimentalWithCallbackMethod_RunStep() {
    #ifdef GRPC_CALLBACK_API_NONEXPERIMENTAL
      ::grpc::Service::
    #else
      ::grpc::Service::experimental().
    #endif
        MarkMethodCallback(0,
          new ::grpc::internal::CallbackBidiHandler< ::gs::rpc::RunStepRequest, ::gs::rpc::RunStepResponse>(
            [this](
    #ifdef GRPC_CALLBACK_API_NONEXPERIMENTAL
                   ::grpc::CallbackServerContext*
    #else
                   ::grpc::experimental::CallbackServerContext*
    #endif
                     context) { return this->RunStep(context); }));
    }
    ~ExperimentalWithCallbackMethod_RunStep() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status RunStep(::grpc::ServerContext* /*context*/, ::grpc::ServerReaderWriter< ::gs::rpc::RunStepResponse, ::gs::rpc::RunStepRequest>* /*stream*/)  override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    #ifdef GRPC_CALLBACK_API_NONEXPERIMENTAL
    virtual ::grpc::ServerBidiReactor< ::gs::rpc::RunStepRequest, ::gs::rpc::RunStepResponse>* RunStep(
      ::grpc::CallbackServerContext* /*context*/)
    #else
    virtual ::grpc::experimental::ServerBidiReactor< ::gs::rpc::RunStepRequest, ::gs::rpc::RunStepResponse>* RunStep(
      ::grpc::experimental::CallbackServerContext* /*context*/)
    #endif
      { return nullptr; }
  };
  template <class BaseClass>
  class ExperimentalWithCallbackMethod_HeartBeat : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    ExperimentalWithCallbackMethod_HeartBeat() {
    #ifdef GRPC_CALLBACK_API_NONEXPERIMENTAL
      ::grpc::Service::
    #else
      ::grpc::Service::experimental().
    #endif
        MarkMethodCallback(1,
          new ::grpc::internal::CallbackUnaryHandler< ::gs::rpc::HeartBeatRequest, ::gs::rpc::HeartBeatResponse>(
            [this](
    #ifdef GRPC_CALLBACK_API_NONEXPERIMENTAL
                   ::grpc::CallbackServerContext*
    #else
                   ::grpc::experimental::CallbackServerContext*
    #endif
                     context, const ::gs::rpc::HeartBeatRequest* request, ::gs::rpc::HeartBeatResponse* response) { return this->HeartBeat(context, request, response); }));}
    void SetMessageAllocatorFor_HeartBeat(
        ::grpc::experimental::MessageAllocator< ::gs::rpc::HeartBeatRequest, ::gs::rpc::HeartBeatResponse>* allocator) {
    #ifdef GRPC_CALLBACK_API_NONEXPERIMENTAL
      ::grpc::internal::MethodHandler* const handler = ::grpc::Service::GetHandler(1);
    #else
      ::grpc::internal::MethodHandler* const handler = ::grpc::Service::experimental().GetHandler(1);
    #endif
      static_cast<::grpc::internal::CallbackUnaryHandler< ::gs::rpc::HeartBeatRequest, ::gs::rpc::HeartBeatResponse>*>(handler)
              ->SetMessageAllocator(allocator);
    }
    ~ExperimentalWithCallbackMethod_HeartBeat() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status HeartBeat(::grpc::ServerContext* /*context*/, const ::gs::rpc::HeartBeatRequest* /*request*/, ::gs::rpc::HeartBeatResponse* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    #ifdef GRPC_CALLBACK_API_NONEXPERIMENTAL
    virtual ::grpc::ServerUnaryReactor* HeartBeat(
      ::grpc::CallbackServerContext* /*context*/, const ::gs::rpc::HeartBeatRequest* /*request*/, ::gs::rpc::HeartBeatResponse* /*response*/)
    #else
    virtual ::grpc::experimental::ServerUnaryReactor* HeartBeat(
      ::grpc::experimental::CallbackServerContext* /*context*/, const ::gs::rpc::HeartBeatRequest* /*request*/, ::gs::rpc::HeartBeatResponse* /*response*/)
    #endif
      { return nullptr; }
  };
  #ifdef GRPC_CALLBACK_API_NONEXPERIMENTAL
  typedef ExperimentalWithCallbackMethod_RunStep<ExperimentalWithCallbackMethod_HeartBeat<Service > > CallbackService;
  #endif

  typedef ExperimentalWithCallbackMethod_RunStep<ExperimentalWithCallbackMethod_HeartBeat<Service > > ExperimentalCallbackService;
  template <class BaseClass>
  class WithGenericMethod_RunStep : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithGenericMethod_RunStep() {
      ::grpc::Service::MarkMethodGeneric(0);
    }
    ~WithGenericMethod_RunStep() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status RunStep(::grpc::ServerContext* /*context*/, ::grpc::ServerReaderWriter< ::gs::rpc::RunStepResponse, ::gs::rpc::RunStepRequest>* /*stream*/)  override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
  };
  template <class BaseClass>
  class WithGenericMethod_HeartBeat : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithGenericMethod_HeartBeat() {
      ::grpc::Service::MarkMethodGeneric(1);
    }
    ~WithGenericMethod_HeartBeat() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status HeartBeat(::grpc::ServerContext* /*context*/, const ::gs::rpc::HeartBeatRequest* /*request*/, ::gs::rpc::HeartBeatResponse* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
  };
  template <class BaseClass>
  class WithRawMethod_RunStep : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithRawMethod_RunStep() {
      ::grpc::Service::MarkMethodRaw(0);
    }
    ~WithRawMethod_RunStep() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status RunStep(::grpc::ServerContext* /*context*/, ::grpc::ServerReaderWriter< ::gs::rpc::RunStepResponse, ::gs::rpc::RunStepRequest>* /*stream*/)  override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    void RequestRunStep(::grpc::ServerContext* context, ::grpc::ServerAsyncReaderWriter< ::grpc::ByteBuffer, ::grpc::ByteBuffer>* stream, ::grpc::CompletionQueue* new_call_cq, ::grpc::ServerCompletionQueue* notification_cq, void *tag) {
      ::grpc::Service::RequestAsyncBidiStreaming(0, context, stream, new_call_cq, notification_cq, tag);
    }
  };
  template <class BaseClass>
  class WithRawMethod_HeartBeat : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithRawMethod_HeartBeat() {
      ::grpc::Service::MarkMethodRaw(1);
    }
    ~WithRawMethod_HeartBeat() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status HeartBeat(::grpc::ServerContext* /*context*/, const ::gs::rpc::HeartBeatRequest* /*request*/, ::gs::rpc::HeartBeatResponse* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    void RequestHeartBeat(::grpc::ServerContext* context, ::grpc::ByteBuffer* request, ::grpc::ServerAsyncResponseWriter< ::grpc::ByteBuffer>* response, ::grpc::CompletionQueue* new_call_cq, ::grpc::ServerCompletionQueue* notification_cq, void *tag) {
      ::grpc::Service::RequestAsyncUnary(1, context, request, response, new_call_cq, notification_cq, tag);
    }
  };
  template <class BaseClass>
  class ExperimentalWithRawCallbackMethod_RunStep : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    ExperimentalWithRawCallbackMethod_RunStep() {
    #ifdef GRPC_CALLBACK_API_NONEXPERIMENTAL
      ::grpc::Service::
    #else
      ::grpc::Service::experimental().
    #endif
        MarkMethodRawCallback(0,
          new ::grpc::internal::CallbackBidiHandler< ::grpc::ByteBuffer, ::grpc::ByteBuffer>(
            [this](
    #ifdef GRPC_CALLBACK_API_NONEXPERIMENTAL
                   ::grpc::CallbackServerContext*
    #else
                   ::grpc::experimental::CallbackServerContext*
    #endif
                     context) { return this->RunStep(context); }));
    }
    ~ExperimentalWithRawCallbackMethod_RunStep() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status RunStep(::grpc::ServerContext* /*context*/, ::grpc::ServerReaderWriter< ::gs::rpc::RunStepResponse, ::gs::rpc::RunStepRequest>* /*stream*/)  override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    #ifdef GRPC_CALLBACK_API_NONEXPERIMENTAL
    virtual ::grpc::ServerBidiReactor< ::grpc::ByteBuffer, ::grpc::ByteBuffer>* RunStep(
      ::grpc::CallbackServerContext* /*context*/)
    #else
    virtual ::grpc::experimental::ServerBidiReactor< ::grpc::ByteBuffer, ::grpc::ByteBuffer>* RunStep(
      ::grpc::experimental::CallbackServerContext* /*context*/)
    #endif
      { return nullptr; }
  };
  template <class BaseClass>
  class ExperimentalWithRawCallbackMethod_HeartBeat : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    ExperimentalWithRawCallbackMethod_HeartBeat() {
    #ifdef GRPC_CALLBACK_API_NONEXPERIMENTAL
      ::grpc::Service::
    #else
      ::grpc::Service::experimental().
    #endif
        MarkMethodRawCallback(1,
          new ::grpc::internal::CallbackUnaryHandler< ::grpc::ByteBuffer, ::grpc::ByteBuffer>(
            [this](
    #ifdef GRPC_CALLBACK_API_NONEXPERIMENTAL
                   ::grpc::CallbackServerContext*
    #else
                   ::grpc::experimental::CallbackServerContext*
    #endif
                     context, const ::grpc::ByteBuffer* request, ::grpc::ByteBuffer* response) { return this->HeartBeat(context, request, response); }));
    }
    ~ExperimentalWithRawCallbackMethod_HeartBeat() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status HeartBeat(::grpc::ServerContext* /*context*/, const ::gs::rpc::HeartBeatRequest* /*request*/, ::gs::rpc::HeartBeatResponse* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    #ifdef GRPC_CALLBACK_API_NONEXPERIMENTAL
    virtual ::grpc::ServerUnaryReactor* HeartBeat(
      ::grpc::CallbackServerContext* /*context*/, const ::grpc::ByteBuffer* /*request*/, ::grpc::ByteBuffer* /*response*/)
    #else
    virtual ::grpc::experimental::ServerUnaryReactor* HeartBeat(
      ::grpc::experimental::CallbackServerContext* /*context*/, const ::grpc::ByteBuffer* /*request*/, ::grpc::ByteBuffer* /*response*/)
    #endif
      { return nullptr; }
  };
  template <class BaseClass>
  class WithStreamedUnaryMethod_HeartBeat : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithStreamedUnaryMethod_HeartBeat() {
      ::grpc::Service::MarkMethodStreamed(1,
        new ::grpc::internal::StreamedUnaryHandler<
          ::gs::rpc::HeartBeatRequest, ::gs::rpc::HeartBeatResponse>(
            [this](::grpc::ServerContext* context,
                   ::grpc::ServerUnaryStreamer<
                     ::gs::rpc::HeartBeatRequest, ::gs::rpc::HeartBeatResponse>* streamer) {
                       return this->StreamedHeartBeat(context,
                         streamer);
                  }));
    }
    ~WithStreamedUnaryMethod_HeartBeat() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable regular version of this method
    ::grpc::Status HeartBeat(::grpc::ServerContext* /*context*/, const ::gs::rpc::HeartBeatRequest* /*request*/, ::gs::rpc::HeartBeatResponse* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    // replace default version of method with streamed unary
    virtual ::grpc::Status StreamedHeartBeat(::grpc::ServerContext* context, ::grpc::ServerUnaryStreamer< ::gs::rpc::HeartBeatRequest,::gs::rpc::HeartBeatResponse>* server_unary_streamer) = 0;
  };
  typedef WithStreamedUnaryMethod_HeartBeat<Service > StreamedUnaryService;
  typedef Service SplitStreamedService;
  typedef WithStreamedUnaryMethod_HeartBeat<Service > StreamedService;
};

}  // namespace rpc
}  // namespace gs


#endif  // GRPC_graphscope_2fproto_2fengine_5fservice_2eproto__INCLUDED
