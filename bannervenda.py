from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle

class BannerVenda(GridLayout):

    def __init__(self, **kwargs):
        self.rows=1
        super().__init__()
        # kwargs = {"continente": "Europa", "imagem_continente": "Europapin.png"}
        continente = kwargs['continente']
        imagem_continente = kwargs['imagem_continente']
        roteiro = kwargs['roteiro']
        foto_roteiro = kwargs['foto_roteiro']
        data = kwargs['data']
        preco = float(kwargs['preco'])
        duracao = kwargs['duracao']
        quantidade = float(kwargs['quantidade'])

        esquerda = FloatLayout()
        esquerda_imagem = Image(pos_hint={"right": 1 ,"top": 0.95}, size_hint= (1, 0.75), source=f"icones/fotos_clientes/{imagem_continente}")
        esquerda_label = Label(text=continente, size_hint=(1, 0.2), pos_hint={"right": 1 , "top": 0.2})
        esquerda.add_widget(esquerda_imagem)
        esquerda.add_widget(esquerda_label)
        meio = FloatLayout()
        if continente=='America':
            if duracao == "1_dia":
                endereco = 'icones/fotos_produtos/America/Um_dia'
            if duracao == "7_dias":
                endereco = 'icones/fotos_produtos/America/Sete_dias'
            if duracao == "10_dias":
                endereco = 'icones/fotos_produtos/America/Dez_dias'
            if duracao== "14_dias":
                endereco = 'icones/fotos_produtos/America/14_dias'
            if duracao == "21_dias":
                endereco = 'icones/fotos_produtos/America/21_dias'
        if continente=='Europa':
            if duracao == "1_dia":
                endereco = 'icones/fotos_produtos/Europa/Um_dia'
            if duracao == "7_dias":
                endereco = 'icones/fotos_produtos/Europa/Sete_dias'
            if duracao == "10_dias":
                endereco = 'icones/fotos_produtos/Europa/Dez_dias'
            if duracao== "14_dias":
                endereco = 'icones/fotos_produtos/Europa/14_dias'
            if duracao == "21_dias":
                endereco = 'icones/fotos_produtos/Europa/21_dias'
        if continente=='Asia':
            if duracao == "1_dia":
                endereco = 'icones/fotos_produtos/Asia/Um_dia'
            if duracao == "7_dias":
                endereco = 'icones/fotos_produtos/Asia/Sete_dias'
            if duracao == "10_dias":
                endereco = 'icones/fotos_produtos/Asia/Dez_dias'
            if duracao== "14_dias":
                endereco = 'icones/fotos_produtos/Asia/14_dias'
            if duracao == "21_dias":
                endereco = 'icones/fotos_produtos/Asia/21_dias'
        if continente=='Africa':
            if duracao == "1_dia":
                endereco = 'icones/fotos_produtos/Africa/Um_dia'
            if duracao == "7_dias":
                endereco = 'icones/fotos_produtos/Africa/Sete_dias'
            if duracao == "10_dias":
                endereco = 'icones/fotos_produtos/Africa/Dez_dias'
            if duracao== "14_dias":
                endereco = 'icones/fotos_produtos/Africa/14_dias'
            if duracao == "21_dias":
                endereco = 'icones/fotos_produtos/Africa/21_dias'
        meio_imagem = Image(pos_hint={"right": 1 ,"top": 0.95}, size_hint= (1, 0.75), source=f"{endereco}/{foto_roteiro}")
        meio_label = Label(text=roteiro, size_hint=(1, 0.2), pos_hint={"right": 1 , "top": 0.2})
        meio.add_widget(meio_imagem)
        meio.add_widget(meio_label)
        direita = FloatLayout()
        direita_label_data = Label(text=f"Data:{data}", size_hint=(1, 0.33), pos_hint={"right": 1 , "top": 0.9})
        direita_label_duracao = Label(text=f"Duração:{duracao}", size_hint=(1, 0.33), pos_hint={"right": 1 , "top": 0.65})
        direita_label_preco = Label(text=f"Preço R$:{preco:,.2f}", size_hint=(1, 0.33), pos_hint={"right": 1 , "top": 0.4})
        direita.add_widget(direita_label_data)
        direita.add_widget(direita_label_duracao)
        direita.add_widget(direita_label_preco)
        self.add_widget(esquerda)
        self.add_widget(meio)
        self.add_widget(direita)