import sys
import threading
import grpc
import pubsub_pb2
import pubsub_pb2_grpc

def receive_messages(stub, sub_key, name):
    request = pubsub_pb2.SubscribeRequest(key=sub_key, client_name=name)
    try:

        for cell in stub.Subscribe(request):
            print(f"Value of cell: {cell.contents}") 
    except grpc.RpcError as e:
        print(f"Conexão encerrada com tópico {sub_key}.")

def main():

    if len(sys.argv) == 5:
        host, name, A, B = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    elif len(sys.argv) == 4:
        host, name, A, B = "localhost", sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    else:
        print("Usage: python client.py [[host]] name sub_key pub_key") 
        sys.exit(1)

    target = f"{host}:50051"
    channel = grpc.insecure_channel(target)
    stub = pubsub_pb2_grpc.PubSubServiceStub(channel)

    print(f"Subscribing to: {A}\nPublishing: {B}\n") 

    if A != 0:

        threading.Thread(target=receive_messages, args=(stub, A, name), daemon=True).start()

    if B != 0:

        cell = pubsub_pb2.Cell(contents=A) 
        request = pubsub_pb2.PublishRequest(key=B, cell=cell)
        stub.Publish(request) 

    if A != 0:
        # Impede que o script morra caso o cliente apenas se inscreva (A != 0)
        try:
            threading.Event().wait()
        except KeyboardInterrupt:
            pass

if __name__ == '__main__':
    main()
