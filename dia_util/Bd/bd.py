# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import sqlite3
from datetime import datetime, date
__author__ = 'Administrador'

'''CRÉDITOS DOS FERIADOS NACIONAIS ENCONTRADOS ATÉ 2076
    http://www.anbima.com.br/feriados/feriados.asp'''

class ConnSqlite(sqlite3):
    SQL_INSERT = "INSERT INTO feriados(data_feriado, descricao, fixo_feriado, nacional)" \
                 "VALUES(?,?,?,?)"

    def __init__(self, bd='feriados.db'):
        self.conn = self.conn.connect(bd, detect_types=sqlite3.PARSE_DECLTYPES)
        self.cursor = self.conn

    def insere_dados(self, dados):
        self.cursor.execute(self.SQL_INSERT, dados)
        self.conn.commit()

    def create_table(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()
