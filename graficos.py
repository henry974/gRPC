import matplotlib.pyplot as plt
import pandas as pd


def gerar_grafico():
  
  df = pd.read_csv("benchmark.log")

  
  df_medio = df.groupby("tamanho_bytes")["rtt_ms"].mean().reset_index()

  print("\n--- RTT Médio por Tamanho de Mensagem ---")
  print(df_medio)

  
  plt.figure(figsize=(9, 6))
  bars=plt.bar(
    
      df_medio["tamanho_bytes"].astype(str),
      df_medio["rtt_ms"],
      color="royalblue",
      edgecolor="black",
  )
  plt.bar_label(bars, fmt='%.2f', padding=3)
  plt.xlabel("Tamanho da Mensagem (bytes)", fontsize=12)
  plt.ylabel("RTT Médio (ms)", fontsize=12)
  plt.title("Desempenho gRPC: RTT Médio vs Tamanho do Payload", fontsize=14)
  plt.grid(axis="y", linestyle="--", alpha=0.7)

  plt.savefig("grafico_rtt.png", dpi=300)
  print("\nGráfico salvo com sucesso como 'grafico_rtt.png'.")
  plt.show()


if __name__ == "__main__":
  gerar_grafico()
