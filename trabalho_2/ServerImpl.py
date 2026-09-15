from concurrent import futures
import queue
import grpc
import pubsub_pb2
import pubsub_pb2_grpc
from collections import defaultdict

class PubSubServicer(pubsub_pb2_grpc.PubSubServiceServicer):
    def __init__(self):
        self.objs = {} 
        self.clientes = defaultdict(list) 

    def Subscribe(self, request, context):
        key = request.key
        client_queue = queue.Queue()
        self.clientes[key].append(client_queue)

        print(f"[{request.client_name}] Inscrito na chave: {key}")

        
        if key in self.objs:
            client_queue.put(self.objs[key])

        try:
        
            while context.is_active():
                try:
                    cell = client_queue.get(timeout=1.0)
                    yield cell
                except queue.Empty:
                    continue
        finally:
            self.clientes[key].remove(client_queue)

    def Publish(self, request, context):
        key = request.key
        cell = request.cell
        
        
        self.objs[key] = cell
        
        
        for client_queue in self.clientes[key]:
            client_queue.put(cell)
            
        return pubsub_pb2.PublishResponse(success=True)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pubsub_pb2_grpc.add_PubSubServiceServicer_to_server(PubSubServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server ready.") 
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
