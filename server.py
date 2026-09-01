from concurrent import futures
from datetime import datetime, timezone
import grpc
import experimento_pb2
import experimento_pb2_grpc

class ServicoDesempenhoServicer(experimento_pb2_grpc.ServicoDesempenhoServicer):
    def Enviar(self, request, context):
        tamanho = len(request.payload)
        timestamp_utc = (
                datetime.now(timezone.utc)
                .isoformat(timespec="microseconds")
                .replace("+00:00", "Z")
            )
        print(f"[servidor] Recebido payload de {tamanho} bytes em {timestamp_utc}")

        return experimento_pb2.MensagemConfirmacao(
                tamanho_recebido = tamanho, timestamp=timestamp_utc)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    experimento_pb2_grpc.add_ServicoDesempenhoServicer_to_server( ServicoDesempenhoServicer(), server)
    server.add_insecure_port("[::]:50051")
    print("Servidor gRPC iniciado")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()










