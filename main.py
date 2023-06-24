from kivy.app import App
from kivy.lang import Builder
from telas import *
from botoes import *
import requests
from bannervenda import BannerVenda
from bannervendedor import BannerVendedor
import os
from functools import partial
from myfirebase import MyFirebase
from datetime import datetime

GUI = Builder.load_file("main.kv")
class MainApp(App):
    continente = None
    roteiro = None
    duracao = None
    foto_produto = None
    id_label = None
    endereco = None

    def build(self):
        self.firebase = MyFirebase()
        return GUI

    def on_start(self):
        # carregas as fotos de perfil
        foto_cliente = None
        self.foto_cliente = foto_cliente
        arquivos = os.listdir('icones/fotos_perfil')
        pagina_fotoperfil = self.root.ids['fotoperfilpage']
        lista_fotos = pagina_fotoperfil.ids['lista_fotos_perfil']
        for foto in arquivos:
           imagem = ImageButton(source=f"icones/fotos_perfil/{foto}", on_release=partial(self.mudar_foto_perfil, foto))
           lista_fotos.add_widget(imagem)
        # carregar os continentes
        arquivos = os.listdir('icones/fotos_clientes')
        pagina_adicionarvendas = self.root.ids["adicionarroteiropage"]
        lista_clientes = pagina_adicionarvendas.ids['lista_clientes']
        for foto_cliente in arquivos:
            imagem = ImageButton(source=f"icones/fotos_clientes/{foto_cliente}", on_release=partial(self.selecionar_cliente, foto_cliente))
            label = LabelButton(text=foto_cliente.replace("pin.png","").capitalize(), on_release=partial(self.selecionar_cliente, foto_cliente))
            lista_clientes.add_widget(imagem)
            lista_clientes.add_widget(label)
        # carregar os roteiros
        #arquivos = os.listdir('icones/fotos_produtos')
        #pagina_adicionarvendas = self.root.ids["adicionarroteiropage"]
        #lista_produtos = pagina_adicionarvendas.ids['lista_produtos']
        #for foto_produto in arquivos:
        #    imagem = ImageButton(source=f"icones/fotos_produtos/{foto_produto}", on_release=partial(self.selecionar_produto, foto_produto))
        #    label = LabelButton(text=foto_produto.replace("pin.png",""), on_release=partial(self.selecionar_produto, foto_produto))
        #    lista_produtos.add_widget(imagem)
        #    lista_produtos.add_widget(label)


        # carrega as infos do usuario
        self.carregar_infos_usuario()

    def carregar_infos_usuario(self):
        try:
            #with open("refreshtoken.txt", "r") as arquivo:
            #    refresh_token = arquivo.read()
            #local_id, id_token = self.firebase.trocar_token()
            #self.local_id = local_id
            #self.id_token = id_token

            #pegar informacoes do usuario
            requisicao = requests.get(f"https://aplicativovendascarte-default-rtdb.firebaseio.com/{self.local_id}.json?auth={self.id_token}")
            requisicao_dic = requisicao.json()

            #preenche o id unico
            id_vendedor = requisicao_dic["id_vendedor"]
            self.id_vendedor = id_vendedor
            pagina_ajustes = self.root.ids["ajustespage"]
            pagina_ajustes.ids["id_vendedor"].text = f"Seu ID unico :{id_vendedor}"

            # preencher total de vendas
            total_roteiros = requisicao_dic["total_roteiros"]
            self.total_roteiros = total_roteiros
            homepage = self.root.ids["homepage"]
            homepage.ids["label_total_vendas"].text = f"[color=#000000]Valor Total dos Roteiros:[/color] [b]R${total_roteiros}[/b]"

            #preencher equipe
            self.equipe = requisicao_dic["equipe"]

            # preencher foto de perfil
            avatar = requisicao_dic['avatar']
            self.avatar = avatar
            foto_perfil = self.root.ids['foto_perfil']
            foto_perfil.source = f"icones/fotos_perfil/{avatar}"

            # preencher lista de vendas
            print(requisicao_dic)
            try:
                vendas = requisicao_dic['roteiros']
                self.roteiros = vendas
                pagina_homepage = self.root.ids['homepage']
                lista_vendas = pagina_homepage.ids['lista_vendas']
                for id_venda in vendas:
                    venda = vendas[id_venda]
                    banner = BannerVenda(continente=venda['continente'], imagem_continente=venda['imagem_continente'],
                                        roteiro=venda['roteiro'], foto_roteiro=venda['foto_roteiro'],
                                        data=venda['data'], preco=venda['preco'], duracao=venda['duracao'],
                                        quantidade=venda['quantidade'])
                    lista_vendas.add_widget(banner)
            except Exception as execao:
                print(execao)
            #preenche equipe de clientes
            equipe = requisicao_dic["equipe"]
            lista_equipe = equipe.split(",")
            pagina_listavendedores = self.root.ids["listaclientespage"]
            lista_vendedores = pagina_listavendedores.ids["lista_vendedores"]
            for id_vendedor_equipe in lista_equipe:
                if id_vendedor_equipe != "":
                    banner_vendedor = BannerVendedor(id_vendedor=id_vendedor_equipe)
                    lista_vendedores.add_widget(banner_vendedor)
            self.mudar_tela("homepage")
        except:
            pass


    def mudar_tela(self, id_tela):
        gerenciador_telas = self.root.ids['screen_manager']
        gerenciador_telas.current = id_tela

    def mudar_foto_perfil(self, foto, *args):
        foto_perfil = self.root.ids['foto_perfil']
        foto_perfil.source = f"icones/fotos_perfil/{foto}"
        info = f'{{"avatar": "{foto}"}}'
        requisicao = requests.patch(f"https://aplicativovendascarte-default-rtdb.firebaseio.com/{self.local_id}.json?auth={self.id_token}",
                                      data=info)
        self.avatar = foto
        self.mudar_tela('ajustespage')

    def adicionar_vendedor(self, id_vendedor_adicionado):
        link = f'https://aplicativovendascarte-default-rtdb.firebaseio.com/.json?orderBy="id_vendedor"&equalTo="{id_vendedor_adicionado}"'
        requisicao = requests.get(link)
        requisicao_dic = requisicao.json()
        pagina_adicionarvendedor = self.root.ids["adicionarclientepage"]
        mensagem_texto = pagina_adicionarvendedor.ids["mensagem_outrovendedor"]
        if requisicao_dic == {}:
            mensagem_texto.text = "Usuário não encontrado"
        else:
            equipe = self.equipe.split(",")
            if id_vendedor_adicionado in equipe:
                mensagem_texto.text = "Cliente já faz parte do grupo de viajantes"
            else:
                self.equipe = self.equipe + f",{id_vendedor_adicionado}"
                info = f'{{"equipe":"{self.equipe}"}}'
                requests.patch(f"https://aplicativovendascarte-default-rtdb.firebaseio.com/{self.local_id}.json?auth={self.id_token}",
                               data=info)
                mensagem_texto.text = "Cliente adicionado ao grupo de viajantes"
                pagina_listavendedores = self.root.ids["listaclientespage"]
                lista_vendedores = pagina_listavendedores.ids["lista_vendedores"]
                banner_vendedor = BannerVendedor(id_vendedor=id_vendedor_adicionado)
                lista_vendedores.add_widget(banner_vendedor)

    def selecionar_cliente(self, foto_cliente, *args):
        #pintar de branco todas as outras letras
        pagina_adicionarvendas = self.root.ids["adicionarroteiropage"]
        lista_clientes = pagina_adicionarvendas.ids['lista_clientes']
        for item in list(lista_clientes.children):
            item.color = (1, 1, 1, 1)
            #pintar de laranja o item selecionado atraves do parametro foto
            try:
                texto = item.text
                #texto = item.lower()
                texto = texto + "pin.png"
                if foto_cliente == texto:
                    item.color = (237/255, 122/255, 43/255, 1)
                    self.foto_cliente = foto_cliente
            except:
                pass

    def selecionar_produto(self, foto_produto, *args):
        # pintar de branco todas as outras letras
        pagina_adicionarvendas = self.root.ids["adicionarroteiropage"]
        lista_produtos = pagina_adicionarvendas.ids['lista_produtos']
        for item in list(lista_produtos.children):
            item.color = (1, 1, 1, 1)
            # pintar de laranja o item selecionado atraves do parametro foto
            try:
                texto = item.text
                # texto = item.lower()
                texto = texto + "pin.png"
                if foto_produto == texto:
                    item.color = (237 / 255, 122 / 255, 43 / 255, 1)
                    self.foto_produto = foto_produto
            except:
                pass

    def selecionar_unidade(self, id_label, *args):
        pagina_adicionarvendas = self.root.ids["adicionarroteiropage"]
        pagina_adicionarvendas.ids["1_dia"].color = (1, 1, 1, 1)
        pagina_adicionarvendas.ids["7_dias"].color = (1, 1, 1, 1)
        pagina_adicionarvendas.ids["10_dias"].color = (1, 1, 1, 1)
        pagina_adicionarvendas.ids["14_dias"].color = (1, 1, 1, 1)
        pagina_adicionarvendas.ids["21_dias"].color = (1, 1, 1, 1)
        #selecionar de laranja
        pagina_adicionarvendas.ids[id_label].color = (237 / 255, 122 / 255, 43 / 255, 1)
        self.id_label = id_label
        if self.foto_cliente == "":
            pagina_adicionarvendas.ids["label_selecione_cliente"].color = (1, 0, 0, 1)
        else:
            try:
                if self.foto_cliente =="Americapin.png":
                    if self.id_label =="1_dia":
                        endereco = 'icones/fotos_produtos/America/Um_dia'
                        print(endereco)
                    if self.id_label =="7_dias":
                        endereco = 'icones/fotos_produtos/America/Sete_dias'
                    if self.id_label =="10_dias":
                        endereco = 'icones/fotos_produtos/America/Dez_dias'
                    if self.id_label =="14_dias":
                        endereco = 'icones/fotos_produtos/America/14_dias'
                    if self.id_label == "21_dias":
                        endereco = 'icones/fotos_produtos/America/21_dias'
                if self.foto_cliente == "Europapin.png":
                    if self.id_label == "1_dia":
                        endereco = 'icones/fotos_produtos/Europa/Um_dia'
                    if self.id_label == "7_dias":
                        endereco = 'icones/fotos_produtos/Europa/Sete_dias'
                    if self.id_label == "10_dias":
                        endereco = 'icones/fotos_produtos/Europa/Dez_dias'
                    if self.id_label == "14_dias":
                        endereco = 'icones/fotos_produtos/Europa/14_dias'
                    if self.id_label == "21_dias":
                        endereco = 'icones/fotos_produtos/Europa/21_dias'
                if self.foto_cliente == "Asiapin.png":
                    if self.id_label == "1_dia":
                        endereco = 'icones/fotos_produtos/Asia/Um_dia'
                    if self.id_label == "7_dias":
                        endereco = 'icones/fotos_produtos/Asia/Sete_dias'
                    if self.id_label == "10_dias":
                        endereco = 'icones/fotos_produtos/Asia/Dez_dias'
                    if self.id_label == "14_dias":
                        endereco = 'icones/fotos_produtos/Asia/14_dias'
                    if self.id_label == "21_dias":
                        endereco = 'icones/fotos_produtos/Asia/21_dias'
                if self.foto_cliente == "Africapin.png":
                    if self.id_label == "1_dia":
                        endereco = 'icones/fotos_produtos/Africa/Um_dia'
                    if self.id_label == "7_dias":
                        endereco = 'icones/fotos_produtos/Africa/Sete_dias'
                    if self.id_label == "10_dias":
                        endereco = 'icones/fotos_produtos/Africa/Dez_dias'
                    if self.id_label == "14_dias":
                        endereco = 'icones/fotos_produtos/Africa/14_dias'
                    if self.id_label == "21_dias":
                        endereco = 'icones/fotos_produtos/Africa/21_dias'
                # carregar os roteiros
                self.endereco = endereco
                arquivos = os.listdir(endereco)
                pagina_adicionarvendas = self.root.ids["adicionarroteiropage"]
                lista_produtos = pagina_adicionarvendas.ids['lista_produtos']
                for item in list(lista_produtos.children):
                    lista_produtos.remove_widget(item)
                for foto_produto in arquivos:
                    imagem = ImageButton(source=f"{endereco}/{foto_produto}",
                                         on_release=partial(self.selecionar_produto, foto_produto))
                    label = LabelButton(text=foto_produto.replace("pin.png", ""),
                                        on_release=partial(self.selecionar_produto, foto_produto))
                    lista_produtos.add_widget(imagem)
                    lista_produtos.add_widget(label)
            except:
                pagina_adicionarvendas.ids["label_selecione_cliente"].color = (1, 0, 0, 1)

    def adicionar_venda(self):
        if self.foto_cliente:
           imagem_continente = self.foto_cliente
           continente = self.foto_cliente.replace("pin.png","")
        if self.foto_produto:
           foto_roteiro = self.foto_produto
           roteiro = self.foto_produto.replace("pin.png","")
        if self.id_label:
           duracao = self.id_label
        pagina_adicionarvendas = self.root.ids["adicionarroteiropage"]
        data = pagina_adicionarvendas.ids["data_viagem"].text
        preco = pagina_adicionarvendas.ids["preco_total"].text
        quantidade = pagina_adicionarvendas.ids["quantidade"].text
        if not self.foto_cliente:
           pagina_adicionarvendas.ids["label_selecione_cliente"].color = (1, 0, 0, 1)
        if not self.foto_produto:
           pagina_adicionarvendas.ids["label_selecione_produto"].color = (1, 0, 0, 1)
        if not self.id_label:
            pagina_adicionarvendas.ids["1_dia"].color = (1, 0, 0, 1)
            pagina_adicionarvendas.ids["7_dias"].color = (1, 0, 0, 1)
            pagina_adicionarvendas.ids["10_dias"].color = (1, 0, 0, 1)
            pagina_adicionarvendas.ids["14_dias"].color = (1, 0, 0, 1)
            pagina_adicionarvendas.ids["21_dias"].color = (1, 0, 0, 1)

        # consistencia dos campos de input
        if data=="" or len(data)<10:
            pagina_adicionarvendas.ids["label_data"].color = (1, 0, 0, 1)
        else:
           if preco!="" and quantidade!="" :
               try:
                  preco = float(preco)
                  quantidade = float(quantidade)
                  if self.foto_cliente and self.foto_produto and self.id_label and data and preco and quantidade and (type(preco)==float) and (type(quantidade)==float):
                      info = f'{{"continente": "{continente}", "roteiro": "{roteiro}", "imagem_continente": "{imagem_continente}","foto_roteiro": "{foto_roteiro}","data": "{data}", "preco": "{preco}", "quantidade": "{quantidade}","duracao": "{duracao}"}}'
                      requests.post(f"https://aplicativovendascarte-default-rtdb.firebaseio.com/{self.local_id}/roteiros.json?auth={self.id_token}",data= info)
                  #foto_roteiro = f"{self.endereco}/{foto_roteiro}"
                  #print(foto_roteiro)
                  banner = BannerVenda(continente=continente, roteiro=roteiro, imagem_continente=imagem_continente, foto_roteiro=foto_roteiro, data=data, preco=preco, duracao=duracao, quantidade=quantidade)
                  pagina_homepage = self.root.ids['homepage']
                  lista_vendas = pagina_homepage.ids['lista_vendas']
                  lista_vendas.add_widget(banner)
                  requisicao = requests.get(f"https://aplicativovendascarte-default-rtdb.firebaseio.com/{self.local_id}/total_roteiros.json?auth={self.id_token}")
                  total_roteiros = float(requisicao.json())
                  total_roteiros += preco
                  info = f'{{"total_roteiros": "{total_roteiros}"}}'
                  requests.patch(f"https://aplicativovendascarte-default-rtdb.firebaseio.com/{self.local_id}.json?auth={self.id_token}", data=info)
                  homepage = self.root.ids["homepage"]
                  homepage.ids["label_total_vendas"].text = f"[color=#000000]Valor Total dos Roteiros:[/color] [b]R${total_roteiros}[/b]"
                  self.mudar_tela("homepage")
                  #self.foto_cliente = None
                  #self.foto_produto = None
                  #self.id_label = None
               except:
                   pagina_adicionarvendas.ids["label_preco"].color = (1, 0, 0, 1)
                   pagina_adicionarvendas.ids["label_quantidade"].color = (1, 0, 0, 1)

    def carregar_todas_vendas(self):
        pagina_todasvendas = self.root.ids["listavendaspage"]
        lista_vendas = pagina_todasvendas.ids["lista_vendas"]
        for item in list(lista_vendas.children):
            lista_vendas.remove_widget(item)
        # pegar informacoes da empresa
        requisicao = requests.get(f'https://aplicativovendascarte-default-rtdb.firebaseio.com/.json?orderBy="id_vendedor"')
        requisicao_dic = requisicao.json()

        # preencher foto de perfil
        foto_perfil = self.root.ids['foto_perfil']
        foto_perfil.source = "icones/fotos_perfil/icon.png"

        total_roteiros = 0
        for local_id_usuario in requisicao_dic:
            try:
               vendas = requisicao_dic[local_id_usuario]["roteiros"]
               for id_venda in vendas:
                   venda = vendas[id_venda]
                   total_roteiros += float(venda['preco'])
                   banner = BannerVenda(continente=venda['continente'], imagem_continente=venda['imagem_continente'],
                                        roteiro=venda['roteiro'], foto_roteiro=venda['foto_roteiro'],
                                        data=venda['data'], preco=venda['preco'], duracao=venda['duracao'],
                                        quantidade=venda['quantidade'])
                   lista_vendas.add_widget(banner)
            except:
                pass

        # preencher total de vendas
        pagina_todasvendas.ids["label_total_vendas"].text = f"[color=#000000]Valor Total dos Roteiros:[/color] [b]R${total_roteiros}[/b]"
        self.mudar_tela("listavendaspage")

    def sair_todas_vendas(self, id_tela, *args):
        foto_perfil = self.root.ids['foto_perfil']
        foto_perfil.source = f"icones/fotos_perfil/{self.avatar}"
        self.mudar_tela(id_tela)

    def carregar_vendas_vendedor(self, dic_info_vendedor, *args):
        try:
            vendas = dic_info_vendedor["roteiros"]
            pagina_vendasoutrovendedor = self.root.ids["vendasoutroclientepage"]
            lista_vendas = pagina_vendasoutrovendedor.ids["lista_vendas"]
            for item in list(lista_vendas.children):
                lista_vendas.remove_widget(item)
            for id_venda in vendas:
                venda = vendas[id_venda]
                banner = BannerVenda(continente=venda['continente'], imagem_continente=venda['imagem_continente'],
                                     roteiro=venda['roteiro'], foto_roteiro=venda['foto_roteiro'],
                                     data=venda['data'], preco=venda['preco'], duracao=venda['duracao'],
                                     quantidade=venda['quantidade'])
                lista_vendas.add_widget(banner)
        except:
            pass
        total_roteiros = dic_info_vendedor["total_roteiros"]
        pagina_vendasoutrovendedor.ids["label_total_vendas"].text = f"[color=#000000]Valor Total dos Roteiros:[/color] [b]R${total_roteiros}[/b]"
        # preencher foto de perfil
        foto_perfil = self.root.ids['foto_perfil']
        avatar = dic_info_vendedor["avatar"]
        foto_perfil.source = f"icones/fotos_perfil/{avatar}"
        self.mudar_tela("vendasoutroclientepage")


MainApp().run()
