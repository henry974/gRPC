import numpy as np
from PIL import Image

class Imagem:
    def __init__(self, dados: np.ndarray):
        arr = np.asarray(dados, dtype=np.float32)
        if arr.ndim == 2:
            self.dados = arr[:, :, np.newaxis] # Converte Cinza (H, W) para (H, W, 1)
        elif arr.ndim == 3:
            self.dados = arr
        else:
            raise ValueError(f"Matriz de imagem deve ser 2D ou 3D. Recebido: {arr.ndim}D")

    @property
    def altura(self) -> int:
        return self.dados.shape[0]

    @property
    def largura(self) -> int:
        return self.dados.shape[1]

    @property
    def canais(self) -> int:
        return self.dados.shape[2]

    @classmethod
    def from_arquivo(cls, caminho: str):
        Image.MAX_IMAGE_PIXELS = None
        
        with Image.open(caminho) as img:
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
                
            arr_bruto = np.array(img)
            
            if arr_bruto.dtype == np.uint16 or arr_bruto.dtype == np.int32 or img.mode.startswith('I'):
                fator_normalizacao = 65535.0
            else:
                fator_normalizacao = 255.0
                
            dados = arr_bruto.astype(np.float32) / fator_normalizacao
            
            return cls(dados)

    def salvar(self, caminho: str):
        dados_norm = np.clip(self.dados, 0.0, 1.0)
        
        dados_uint8 = (dados_norm * 255.0).astype(np.uint8)
        
        if self.canais == 1:
            img_pil = Image.fromarray(dados_uint8[:, :, 0], mode='L')
        else:
            img_pil = Image.fromarray(dados_uint8, mode='RGB')
            
        img_pil.save(caminho)
