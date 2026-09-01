import time
import datetime
import csv
import grpc
import experimento_pb2
import experimento_pb2_grpc

def run(num_chamadas: int, ip: str, S: list, file: str):
    print("Iniciando benchmark...")

    with grpc.insecure_channel(ip) as channel:
        stub = experimento_pb2_grpc.ServicoDesempenhoStub(channel)

        with open(file, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "tamanho_bytes", "indice_chamada", "rtt_ms"])
            
            for t in S:
                payload = b'0' * t
                for i in range(1, num_chamadas + 1):
                    msg = experimento_pb2.MensagemRequisicao(payload = payload)

                    begin = time.perf_counter()
                    ans = stub.Enviar(msg)
                    end = time.perf_counter()

                    rtt_ms = (end - begin) * 1000
                    timestamp = datetime.datetime.now().isoformat()

                    writer.writerow([timestamp, t, i, rtt_ms])
    print(f"Benchmark finalizado. Informações gravadas no arquivo {file}.")

if __name__ == "__main__":
    run(num_chamadas = 20, 
        ip = "localhost:50051", 
        S = [10000, 1, 100000, 1000000], 
        file = "benchmark.log")
