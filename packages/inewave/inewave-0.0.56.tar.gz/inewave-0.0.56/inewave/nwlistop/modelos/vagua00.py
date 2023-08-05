from inewave.config import MESES_DF, MAX_SERIES_SINTETICAS

from cfinterface.components.block import Block
from cfinterface.components.line import Line
from cfinterface.components.field import Field
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.floatfield import FloatField
from typing import List, IO
import numpy as np  # type: ignore
import pandas as pd  # type: ignore


class REE(Block):
    """
    Bloco com a informaçao do REE associado aos valores
    da água.
    """

    BEGIN_PATTERN = r"VALOR DAGUA \(\$\/MWh\)"
    END_PATTERN = ""

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line([LiteralField(12, 63)])

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, REE):
            return False
        bloco: REE = o
        if not all(
            [
                isinstance(self.data, str),
                isinstance(o.data, str),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    # Override
    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())[0]


class VAAnos(Block):
    """
    Bloco com as informações das tabelas de valor da água por
    REE por mês/ano de estudo.
    """

    BEGIN_PATTERN = "     ANO: "
    END_PATTERN = " MEDIA"

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha_ano = Line([IntegerField(4, 10)])
        campo_serie: List[Field] = [
            IntegerField(4, 2),
        ]
        campos_custos: List[Field] = [
            FloatField(8, 9 + 9 * i, 2) for i in range(len(MESES_DF) + 1)
        ]
        self.__linha = Line(campo_serie + campos_custos)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, VAAnos):
            return False
        bloco: VAAnos = o
        if not all(
            [
                isinstance(self.data, pd.DataFrame),
                isinstance(o.data, pd.DataFrame),
            ]
        ):
            return False
        else:
            return self.data.equals(bloco.data)

    # Override
    def read(self, file: IO):
        def converte_tabela_em_df():
            cols = ["Série"] + MESES_DF + ["Média"]
            df = pd.DataFrame(tabela, columns=cols)
            df["Ano"] = self.__ano
            df = df[["Ano"] + cols]
            df = df.astype({"Série": "int64", "Ano": "int64"})
            return df

        self.__ano = self.__linha_ano.read(file.readline())[0]
        file.readline()

        # Variáveis auxiliares
        tabela = np.zeros((MAX_SERIES_SINTETICAS, len(MESES_DF) + 2))
        i = 0
        while True:
            linha = file.readline()
            if self.ends(linha):
                tabela = tabela[:i, :]
                self.data = converte_tabela_em_df()
                break
            tabela[i, :] = self.__linha.read(linha)
            i += 1
