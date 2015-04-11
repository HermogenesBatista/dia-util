from dia_util.Bd.bd import ConnSqlite
import datetime
import os

class DiaUtil:

    connSqlite = ConnSqlite()
    feriados = 0
    results = []

    def __init__(self, data_inicio=datetime.date.today()):
        self.data_inicio = data_inicio
        print(os.path.join(self.connSqlite.BASE_DIRS, 'feriados.db'))

    
    def proximo_dia_util(self, date, dias_uteis, ans=False):
        ''' constroi uma data em dia útil, de acordo com os dias passados
        Ainda não foi implementado receber uma data em string'''

        if(not date):
            date = self.data_inicio
        else:
            self.data_inicio = date
        
        fim_de_semana = self.verifica_dia(date)

        if(fim_de_semana > 0):
            date = self.add_day(date, fim_de_semana)

        if(dias_uteis>=5):
            dias_extras = dias_uteis//5
            dias_corridos = dias_extras*7
            #adicionando os dias corridos
            date = self.add_day(date, dias_corridos)

            #removendo o excesso de dias uteis
            dias_uteis -=dias_extras*5

        #print(dias_uteis)
        for i in range(dias_uteis):
            #print(date)
            date = self.add_day(date, 1)
            adicional = self.verifica_dia(date)
            if(adicional>0):
                date = self.add_day(date, adicional)

        #print('aqui', date)
        if(ans):
            #print('aqui ans', date)
            temp = self.add_day(date, -1)

            if(int(temp.strftime('%w')) == 0):
                date = self.add_day(date, -3)
            else:
                date = self.add_day(date, -1)

        '''nesse ponto eu fazia uma verificação se caiu em algum feriado
           mas eu aplicava a consulta determinada pelo cadastro de feriados
           que temos na empresa, mas deixo a chamada do método pronto
           recuperaria a data inicial, e verificaria os feriados cadastrados
           passando como parametro a data inicial e a data nova
           o terceiro parametro seria uma identificação, no meu caso a filial da
           empresa'''

        date = self.verifica_feriado(date)

        return date

    def add_day(self, date, dias):
        add = datetime.timedelta(days=dias)
        date +=add
        return date
                

    def verifica_dia(self, date):
        '''metodo preparado para receber ou uma string como data ou um objeto
            datetime'''

        try:
            temp = int(date.strftime('%w'))
            
        except:
            #não encontrei um jeito de transformar diretamente para obj Date
            dt = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            temp = int(dt.strftime('%w'))
            
        if(temp == 6):
            return 2

        
        elif(temp == 0):
            return 1

        return 0

    def verifica_feriado(self, date):
        #print('entrou')
        self.feriados = self.connSqlite.select_sql(self.connSqlite.SQL_FERIADOS_BETWEEN, [self.data_inicio, date])

        self.results = len(self.feriados)
        temp = date
        #print(self.results)
        while(self.results > 0):
            #print(self.results)
            for n in self.feriados:
                date = self.add_day(date, 1)
                dia_semana = self.verifica_dia(date)

                if(dia_semana > 0):
                    date = self.add_day(date, dia_semana)

                self.feriados = self.connSqlite.select_sql(self.connSqlite.SQL_FERIADOS_BETWEEN, [temp, date])

                self.results = len(self.feriados)
                temp = date

        return date

    def conta_dia_util(self, data_inicio, data_fim, ans=False):
        print(data_inicio, data_fim)
        if(data_inicio == data_fim):
            if(ans):
                return 1
            else:
                return 0

        dia_semana_inicio = self.verifica_dia(data_inicio)

        print(dia_semana_inicio)
        if(dia_semana_inicio>0):
            data_inicio = self.add_day(data_inicio, dia_semana_inicio)

        dia_semana_fim = self.verifica_dia(data_fim)
        print(dia_semana_fim)
        if(dia_semana_fim > 0):
            data_fim = self.add_day(data_fim, -dia_semana_fim)

        dias_corridos = data_fim - data_inicio
        qtd_semanas = dias_corridos.days//7
        print(dias_corridos)
        dias_corridos_rest = dias_corridos.days - qtd_semanas*7
        print(dias_corridos_rest)
        temp_dia_inicio = int(data_inicio.strftime('%w'))

        if(dias_corridos_rest>=5 or (dias_corridos_rest>2
                                    and (temp_dia_inicio == 5
                                         or temp_dia_inicio == 4))):
            dias_corridos_rest -=2
        print(dias_corridos_rest, ' dia rest')
        dia_util = qtd_semanas*5
        print(dia_util)
        if(ans):    
            dia_util +=1

        print(dia_util,' - ')
        dados = [data_inicio, data_fim]
        dados.sort()
        self.feriados = self.connSqlite.select_sql(self.connSqlite.SQL_FERIADOS_BETWEEN, dados)

        self.results = len(self.feriados)

        print(self.results)
        print(dias_corridos_rest)
        #levando em consideração que o negativo significa "atraso" em dias uteis
        if(dia_util<0):
            dia_util -= dias_corridos_rest
        else:
            dia_util += dias_corridos_rest



        return dia_util
        
if __name__ == '__main__':
    data = DiaUtil()
    #print(data.data_inicio)
    data2 = datetime.date(year=2001, month=2, day=20)
    data_nova = data.proximo_dia_util(date=data2, dias_uteis=20, ans=True)
    print(data_nova)
    conta_dia_util = data.conta_dia_util(data_nova, data2, ans=True)
    print(conta_dia_util)
    #conta_dia_util = data.conta_dia_util(data2, date3, ans=False)
    #print(conta_dia_util)
    '''timeit.timeit("data.proximo_dia_util(date=data2, dias_uteis=100,
     ans=True)", setup="from __main__ import DiaUtil, data,
     data2, data_nova", number=800)'''
