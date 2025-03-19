from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDButton, MDButtonText
from kivy.core.window import Window
from kivymd.uix.card import MDCard
from kivymd.uix.textfield import MDTextField
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.button import MDIconButton
from kivy.lang import Builder
from kivymd.uix.dialog import (MDDialog, MDDialogHeadlineText, MDDialogSupportingText, MDDialogButtonContainer)
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image
from kivy.storage.jsonstore import JsonStore
from kivy.clock import Clock
import random


class MenuPrincipal(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_menu()
    def on_modo_solitario(self, *args):
        solitario_screen = self.manager.get_screen('solitario')
        solitario_screen.iniciar_juego()
        self.manager.current = 'solitario'
    def create_menu(self):
        layout = MDRelativeLayout()
        
        # Main Title
        title = MDLabel(
            text="AHORCADO",
            halign="center",
            pos_hint={"center_x": 0.5, "center_y": 0.8},
            font_style="Display",
            bold=True,
            font_size="48sp"
        )
        
        # Subtitle
        subtitle = MDLabel(
            text="¡Juega y mejora tu vocabulario!",
            halign="center",
            pos_hint={"center_x": 0.5, "center_y": 0.7},
            font_style="Body",
            font_size="18sp"
        )
        
        # Solo Mode Button
        btn_solitario = MDCard(
            size_hint=(0.8, 0.15),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            elevation=2,
            ripple_behavior=True,
            on_release=self.on_modo_solitario,
            md_bg_color=self.theme_cls.primaryColor
        )
        btn_solitario.add_widget(
            MDLabel(
                text="JUGAR MODO SOLITARIO",
                halign="center",
                theme_text_color="Custom",
                text_color="black",
                bold=True
            )
        )
        
        # Statistics Button
        btn_stats = MDCard(
            size_hint=(0.8, 0.15),
            pos_hint={"center_x": 0.5, "center_y": 0.3},
            elevation=2,
            ripple_behavior=True,
            on_release=self.show_stats
        )
        btn_stats.add_widget(
            MDLabel(
                text="ESTADÍSTICAS",
                halign="center",
                bold=True
            )
        )
        
       
        
        # Add all widgets to layout
        layout.add_widget(title)
        layout.add_widget(subtitle)
        layout.add_widget(btn_solitario)
        layout.add_widget(btn_stats)
        
        self.add_widget(layout)
    
    def show_stats(self, *args):
        dialog = MDDialog(
            MDDialogHeadlineText(text="Estadísticas de Juego"),
            MDDialogSupportingText(
                text=f"Nivel Actual: {self.manager.get_screen('solitario').current_level}\n"
                     f"Palabras Completadas: {self.manager.get_screen('solitario').palabras_completadas}\n"
                     f"Palabras por Nivel: {self.manager.get_screen('solitario').palabras_por_nivel}"
            ),
            MDDialogButtonContainer(
                MDButton(
                    MDButtonText(text="Cerrar"),
                    style="text",
                    on_release=lambda x: dialog.dismiss()
                )
            )
        )
        dialog.open()
    
    
    def reset_progress(self, *args):
        solitario_screen = self.manager.get_screen('solitario')
        solitario_screen.current_level = 1
        solitario_screen.palabras_completadas = 0
        solitario_screen.palabras_usadas = {str(i): [] for i in range(1, 11)}
        solitario_screen.palabras_acertadas = {str(i): [] for i in range(1, 11)}
        solitario_screen.guardar_estado_juego()   
class ModoSolitario(MDScreen):
    current_level = NumericProperty(1)
    letras_usadas = StringProperty('')
    palabra_oculta = StringProperty('')
    intentos = NumericProperty(6)
    estado_ahorcado = StringProperty('')
    palabras_completadas = NumericProperty(0)
    palabras_por_nivel = NumericProperty(20)
    palabras_usadas = {}  # Dictionary to track used words per level
    palabras_acertadas = {} 
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.palabra_actual = ''
        self.cargar_estado_juego()
        Clock.schedule_once(self.iniciar_juego)
    def actualizar_estado_ahorcado(self):
        estados_ahorcado = [
            '''
      +---+
      |   |
      O   |
     /|\  |
     / \  |
          |
    =========''',
            '''
      +---+
      |   |
      O   |
     /|\  |
     /    |
          |
    =========''',
            '''
      +---+
      |   |
      O   |
     /|\  |
          |
          |
    =========''',
            '''
      +---+
      |   |
      O   |
     /|   |
          |
          |
    =========''',
            '''
      +---+
      |   |
      O   |
      |   |
          |
          |
    =========''',
            '''
      +---+
      |   |
      O   |
          |
          |
          |
    =========''',
            '''
      +---+
      |   |
          |
          |
          |
          |
    ========='''
        ]
        self.estado_ahorcado = estados_ahorcado[self.intentos]
        return self.estado_ahorcado
    def cargar_estado_juego(self):
        try:
            store = JsonStore('game_state.json')
            data = store.get('estado')
            self.current_level = data['nivel']
            self.palabras_completadas = data['palabras_completadas']
            self.palabras_usadas = data['palabras_usadas']
            self.palabras_acertadas = data['palabras_acertadas']
        except:
            self.current_level = 1
            self.palabras_completadas = 0
            self.palabras_usadas = {str(i): [] for i in range(1, 11)}
            self.palabras_acertadas = {str(i): [] for i in range(1, 11)}
    def guardar_estado_juego(self):
        store = JsonStore('game_state.json')
        store.put('estado', 
                 nivel=self.current_level,
                 palabras_completadas=self.palabras_completadas,
                 palabras_usadas=self.palabras_usadas,
                 palabras_acertadas=self.palabras_acertadas)
    def seleccionar_nueva_palabra(self):
        app = MDApp.get_running_app()
        nivel = str(self.current_level)
        palabras_disponibles = [word for word in app.palabras[self.current_level] 
                              if word not in self.palabras_usadas[nivel]]
        if not palabras_disponibles:
            self.palabras_usadas[nivel] = []
            palabras_disponibles = app.palabras[self.current_level]
        
        palabra = random.choice(palabras_disponibles)
        self.palabras_usadas[nivel].append(palabra)
        return palabra
    def procesar_letra(self, letra):
        if not letra.isalpha():
            return
            
        letra = letra.upper()
        if letra in self.letras_usadas:
            return

        self.letras_usadas += letra
        
        if letra in self.palabra_actual:
            nueva_palabra = ''
            palabra_actual_list = list(self.palabra_oculta.replace(" ", ""))
            
            for i in range(len(self.palabra_actual)):
                if self.palabra_actual[i] == letra:
                    palabra_actual_list[i] = letra
                    
            nueva_palabra = ' '.join(palabra_actual_list)
            self.palabra_oculta = nueva_palabra
            
            if '_' not in self.palabra_oculta.replace(" ", ""):
                nivel = str(self.current_level)
                self.palabras_acertadas[nivel].append(self.palabra_actual)
                self.palabras_completadas += 1
                
                mensaje = f"¡{self.palabras_completadas}/{self.palabras_por_nivel} palabras completadas!"
                
                if self.palabras_completadas >= self.palabras_por_nivel:
                    self.current_level += 1
                    self.palabras_completadas = 0
                    mensaje = "¡Felicitaciones! ¡Avanzas al siguiente nivel!"
                
                self.guardar_estado_juego()
                self.mostrar_dialogo("¡Palabra Correcta!", mensaje)
                self.iniciar_juego()
                
        else:
            self.intentos -= 1
            self.actualizar_estado_ahorcado()
            
            if self.intentos == 0:
                if self.palabras_completadas > 0:
                    self.palabras_completadas -= 1
                else:
                    if self.current_level > 1:
                        self.current_level -= 1
                        self.palabras_completadas = self.palabras_por_nivel - 1
                
                self.guardar_estado_juego()
                self.mostrar_dialogo("¡Perdiste!", f"La palabra era: {self.palabra_actual}")
                self.iniciar_juego()

    def iniciar_juego(self, *args):
        self.palabra_actual = self.seleccionar_nueva_palabra()
        self.palabra_oculta =  ' '.join(['_' * len(self.palabra_actual)])
        self.letras_usadas = ''
        self.intentos = 6
        self.actualizar_estado_ahorcado()
    def reiniciar_juego(self, *args):
        self.iniciar_juego()


    def mostrar_dialogo(self, titulo, texto):
        if titulo == "¡Perdiste!":
            button_text = "Palabra Anterior"
        elif self.palabras_completadas >= self.palabras_por_nivel:
            button_text = "Siguiente Nivel"
        else:
            button_text = "Siguiente Palabra"
            
        dialog = MDDialog(
            MDDialogHeadlineText(text=titulo),
            MDDialogSupportingText(text=texto),
            MDDialogButtonContainer(
                RelativeLayout(),
                MDButton(
                    MDButtonText(text=button_text),
                    style="text",
                    on_release=lambda x: (
                        self.siguiente_nivel() if button_text == "Siguiente Nivel" else self.reiniciar_juego(),
                        dialog.dismiss()
                    ),
                ),
                spacing="8dp",
            ),
        )
        dialog.open()

    def siguiente_nivel(self):
        if self.current_level < 10:
            self.current_level += 1
        self.reiniciar_juego()
class LoadingScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDRelativeLayout()
        
        # Add logo image
        logo = Image(
            source='logoDVLLSOFT.jpeg',
            size_hint=(0.8, 0.8),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        layout.add_widget(logo)
        self.add_widget(layout)
class AhorcadoApp(MDApp):
    def __init__(self):
        super().__init__()
        self.current_level = 1
        self.palabras = {
            # Level 1 - 50 words (4 letters)
            1: ['CASA', 'MESA', 'GATO', 'PATO', 'LUNA', 'SOL', 'PEZ', 'FLOR', 'TAZA', 'VASO',
                'BOTE', 'PERA', 'MANO', 'PIES', 'PELO', 'CARA', 'BOCA', 'DEDO', 'ROJO', 'AZUL',
                'GRIS', 'ROSA', 'CAMA', 'SOPA', 'PAPA', 'MAMA', 'TORO', 'LOBO', 'RANA', 'SAPO',
                'PINO', 'ROSA', 'NUBE', 'LAGO', 'MAR', 'RIO', 'TREN', 'BICI', 'MOTO', 'AUTO',
                'PALA', 'BOLA', 'DADO', 'COPA', 'VELA', 'PATO', 'MONO', 'OSOS', 'LEON', 'BUHO'],

            # Level 2 - 50 words (5-6 letters)
            2: ['PERRO', 'GATOS', 'RATON', 'TIGRE', 'LECHE', 'QUESO', 'DULCE', 'PAPEL', 'LIBRO', 'LAPIZ',
                'PLUMA', 'RELOJ', 'CARRO', 'BARCO', 'AVION', 'PLATO', 'VASO', 'SILLA', 'MESA', 'CAMA',
                'ARBOL', 'PLAYA', 'MONTE', 'CIELO', 'NUBES', 'LLUVIA', 'NIEVE', 'FUEGO', 'AGUA', 'TIERRA',
                'VERDE', 'AZUL', 'ROJO', 'NEGRO', 'BLANCO', 'ROSA', 'FELIZ', 'TRISTE', 'RAPIDO', 'LENTO',
                'ARRIBA', 'ABAJO', 'CERCA', 'LEJOS', 'DENTRO', 'FUERA', 'SOBRE', 'BAJO', 'ANTES', 'AHORA'],

            # Level 3 - 50 words (7-8 letters)
            3: ['VENTANA', 'ESCUELA', 'GUITARRA', 'DELFIN', 'MANZANA', 'NARANJA', 'ESTRELLA', 'TELEFONO', 'LAMPARA', 'PESCADO',
                'PLATANO', 'CEBOLLA', 'GALLINA', 'CABALLO', 'TORTUGA', 'CONEJO', 'PALOMA', 'BALLENA', 'TIBURON', 'PULPO',
                'CAMARON', 'LANGOSTA', 'CANGREJO', 'LAGARTO', 'IGUANA', 'TORTUGA', 'GALLETA', 'HELADO', 'YOGURT', 'FRIJOL',
                'ARROZ', 'ENSALADA', 'PESCADO', 'AMARILLO', 'MORADO', 'NARANJA', 'DORADO', 'PLATEADO', 'ARMARIO', 'COCINA',
                'JARDIN', 'GARAGE', 'BALCON', 'BOTELLA', 'TENEDOR', 'CUCHARA', 'CUCHILLO', 'SABANA', 'ALMOHADA', 'CORTINA'],

            # Level 4 - 50 words (9 letters)
            4: ['ZAPATILLA', 'PARAGUAS', 'ELEFANTE', 'COCODRILO', 'MARIPOSA', 'SERPIENTE', 'ORDENADOR', 'BIBLIOTECA', 'CHOCOLATE', 'MANDARINA',
                'BERENJENA', 'AGUACATE', 'MELOCOTON', 'CALABAZA', 'GIRASOLES', 'MARGARITA', 'ORQUIDEA', 'GLADIOLO', 'CARRETERA', 'AUTOPISTA',
                'SEMAFORO', 'ESCALERA', 'ASCENSOR', 'TELEFONO', 'TELEVISION', 'COMPUTADOR', 'IMPRESORA', 'CUADERNO', 'LAPICERO', 'BORRADOR',
                'SACAPUNTA', 'MOCHILA', 'PANTALON', 'CAMISETA', 'CALCETINES', 'ZAPATILLA', 'CHAQUETA', 'BUFANDA', 'PARAGUAS', 'SOMBRILLA',
                'DELANTAL', 'SERVILLETA', 'TENEDOR', 'CUCHARA', 'CUCHILLO', 'CAFETERA', 'LICUADORA', 'BATIDORA', 'TOSTADOR', 'MICROONDA'],

            # Level 5 - 50 words (10 letters)
            5: ['DINOSAURIO', 'HIPOPOTAMO', 'RINOCERONTE', 'ESCARABAJO', 'SALTAMONTES', 'COMPUTADORA', 'DICCIONARIO', 'CALENDARIO', 'ESTUDIANTE',
                'PROFESORES', 'CARPINTERO', 'ARQUITECTO', 'INGENIERO', 'PERIODISTA', 'FOTOGRAFO', 'ASTRONAUTA', 'BOMBERO', 'POLICIA', 'CONDUCTOR',
                'CARTERO', 'PANADERO', 'COCINERO', 'FUTBOLISTA', 'BASQUETBOL', 'VOLEIBOL', 'GIMNASIO', 'NATACION', 'ATLETISMO', 'CICLISMO',
                'PATINAJE', 'ESCALADA', 'MONTAÑISMO', 'ACUATICO', 'SUBMARINO', 'HELICOPTERO', 'MOTOCICLETA', 'CAMIONETA', 'AMBULANCIA',
                'FERROCARRIL', 'CRUCERO', 'VELERO', 'PESQUERO', 'PETROLERO', 'MERCANTE', 'PASAJEROS', 'COMERCIAL', 'INDUSTRIAL', 'RESIDENCIAL',
                'COMERCIAL', 'EDUCATIVO'],

            # Level 6 - 50 words (11-12 letters)
            6: ['AGRICULTURA', 'ARQUITECTURA', 'ASTRONOMIA', 'ARQUEOLOGIA', 'ANTROPOLOGIA', 'BIOQUIMICA', 'CARDIOLOGIA', 'CLIMATOLOGIA',
                'CRIMINOLOGIA', 'DERMATOLOGIA', 'ENDOCRINOLOGIA', 'EPIDEMIOLOGIA', 'FARMACOLOGIA', 'FISIOTERAPIA', 'GASTRONOMIA',
                'HEMATOLOGIA', 'HIDROELECTRICA', 'INMUNOLOGIA', 'KINESIOLOGIA', 'LABORATORIO', 'MATEMATICAS', 'METEOROLOGIA',
                'MICROBIOLOGIA', 'NEUROCIENCIA', 'ODONTOLOGIA', 'OFTALMOLOGIA', 'PALEONTOLOGIA', 'PARASITOLOGIA', 'PSICOLOGIA',
                'PSIQUIATRIA', 'RADIOLOGIA', 'REUMATOLOGIA', 'SISMOLOGIA', 'SOCIOLOGIA', 'TECNOLOGIA', 'TOXICOLOGIA', 'TRAUMATOLOGIA',
                'VETERINARIA', 'VULCANOLOGIA', 'ZOOLOGIA', 'AERONAUTICA', 'AGRICULTURA', 'APICULTURA', 'AVICULTURA', 'PISCICULTURA',
                'SILVICULTURA', 'HORTICULTURA', 'FLORICULTURA', 'ACUICULTURA', 'AGRICULTURA'],

            # Level 7 - 50 words (13-14 letters)
            7: ['INTERNACIONAL', 'EXTRAORDINARIO', 'REVOLUCIONARIO', 'BIODIVERSIDAD', 'BIOTECNOLOGIA', 'COMUNICACION',
                'CONSERVACION', 'CONSTRUCCION', 'CONTAMINACION', 'DEFORESTACION', 'DEMOCRATICO', 'DEPARTAMENTO',
                'DESARROLLADOR', 'DETERMINACION', 'DISCRIMINACION', 'DOCUMENTACION', 'ELECTRICIDAD', 'ENCICLOPEDIA',
                'ENTRETENIMIENTO', 'ESPECIALISTA', 'ESTABLECIMIENTO', 'EXPERIMENTAL', 'FINANCIAMIENTO', 'FOTOGRAFIA',
                'GASTRONOMICO', 'GENERACION', 'GUBERNAMENTAL', 'HABITACIONAL', 'IDENTIFICACION', 'IMAGINACION',
                'IMPLEMENTACION', 'IMPORTACION', 'INDEPENDIENTE', 'INFRAESTRUCTURA', 'INSTITUCIONAL', 'INSTRUMENTAL',
                'INTELIGENCIA', 'INTERCAMBIO', 'INTERFERENCIA', 'INTERNACIONAL', 'INTERPRETACION', 'INVESTIGACION',
                'LABORATORIO', 'MANUFACTURERO', 'MATEMATICAS', 'MEDICAMENTO', 'METABOLISMO', 'METODOLOGIA',
                'MICROORGANISMO', 'MODERNIZACION'],

            # Level 8 - 50 words (15-16 letters)
            8: ['ADMINISTRATIVO', 'ANTIBACTERIANO', 'ANTIINFLAMATORIO', 'BIODEGRADABLE', 'CARDIOVASCULAR', 'CINEMATOGRAFICO',
                'CIRCUNFERENCIA', 'CLASIFICACION', 'COLABORACION', 'COMERCIALIZACION', 'COMPETITIVIDAD', 'COMPUTACIONAL',
                'CONFIDENCIAL', 'CONFIGURACION', 'CONOCIMIENTO', 'CONSIDERABLE', 'CONSTITUCIONAL', 'CONTEMPORANEO',
                'CONTRADICCION', 'CORRESPONDENCIA', 'DESCENTRALIZADO', 'DIFERENCIACION', 'DISCRIMINACION', 'DISPONIBILIDAD',
                'DIVERSIFICACION', 'DOCUMENTACION', 'ELECTRODOMESTICO', 'ELECTROMAGNETICO', 'EMPRENDIMIENTO', 'ENTRETENIMIENTO',
                'ESPECIALIZADO', 'ESPECIFICACION', 'ESTABLECIMIENTO', 'ESTANDARIZACION', 'ESTRATEGICO', 'ESTRUCTURACION',
                'EXPERIMENTAL', 'EXTRAORDINARIO', 'FARMACEUTICO', 'FUNCIONAMIENTO', 'FUNDAMENTAL', 'GENERALIZADO',
                'HIDROELECTRICO', 'IDENTIFICACION', 'IMPLEMENTACION', 'INDEPENDIENTE', 'INFRAESTRUCTURA', 'INSTITUCIONAL',
                'INTERNACIONAL', 'INTERPRETACION'],

            # Level 9 - 50 words (17-18 letters)
            9: ['ANTICONSTITUCIONAL', 'BIODEGRADABILIDAD', 'COMERCIALIZADORA', 'CONCEPTUALIZACION', 'CONFIDENCIALIDAD',
                'CONTEXTUALIZADO', 'CONTRAPRODUCENTE', 'CORRESPONDIENTE', 'DEMOCRATIZACION', 'DESCENTRALIZACION',
                'DESENVOLVIMIENTO', 'DESPROPORCIONAL', 'DETERMINACION', 'DIFERENCIADOR', 'DISCRIMINATORIO',
                'EJEMPLIFICACION', 'ELECTROCARDIOGRAMA', 'ELECTROMAGNETISMO', 'EMPRENDEDURISMO', 'ESPECIALIZACION',
                'ESTANDARIZACION', 'ESTRUCTURAMIENTO', 'EXPERIMENTACION', 'EXTRAORDINARIAMENTE', 'FINANCIAMIENTO',
                'FUNCIONAMIENTO', 'GUBERNAMENTAL', 'HETEROGENEIDAD', 'HIDROELECTRICA', 'HISTORIOGRAFIA',
                'HOMOGENEIZACION', 'HORIZONTALIDAD', 'IDENTIFICADOR', 'IMPLEMENTACION', 'IMPROVISACION',
                'INDEPENDENCIA', 'INDUSTRIALIZACION', 'INFRAESTRUCTURAL', 'INSTITUCIONALIDAD', 'INSTRUMENTACION',
                'INTELECTUALIDAD', 'INTERCULTURALIDAD', 'INTERDISCIPLINAR', 'INTERNACIONALIZACION', 'INTERPRETATIVO',
                'INVESTIGADOR', 'JURISDICCIONAL', 'MANUFACTURACION', 'MERCADOTECNIA', 'METEOROLOGICO'],

            # Level 10 - 50 words (19+ letters)
            10: ['ANTICONSTITUCIONALIDAD', 'ELECTROENCEFALOGRAMA', 'OTORRINOLARINGOLOGO', 'INTERDISCIPLINARIO',
                'INTERNACIONALIZACION', 'ELECTROENCEFALOGRAFICO', 'INSTITUCIONALIZACIÓN', 'CONTRAREVOLUCIONARIO',
                'DESPROPORCIONADAMENTE', 'ELECTROCARDIOGRAFICO', 'ESPECTROFOTOMETRICO', 'FOTOLUMINISCENCIA',
                'GASTROINTESTINAL', 'HIDROELECTRICIDAD', 'INCONSTITUCIONALIDAD', 'INDUSTRIALIZACION',
                'INSTRUMENTALIZACION', 'INTERCONTINENTAL', 'INTERNACIONALMENTE', 'INTERPROFESIONAL',
                'INTRADEPARTAMENTAL', 'MAGNETOELECTRICO', 'MICROORGANISMOS', 'MULTIDISCIPLINARIO',
                'NEUROFISIOLOGICO', 'ORGANIZACIONAL', 'PALEONTOLOGICO', 'PARALINGUISTICO', 'PSICOLINGUISTICA',
                'PSICOTERAPEUTICO', 'RADIOELECTRICO', 'RADIOTELEFONICO', 'REPRESENTATIVIDAD', 'RESPONSABILIDAD',
                'REVOLUCIONARIO', 'SIGNIFICATIVIDAD', 'SOCIOECONOMICO', 'SOCIOPOLITICO', 'SUBDESARROLLADO',
                'SUPERINTENDENCIA', 'SUSTENTABILIDAD', 'TELECOMUNICACION', 'TERMODINAMICO', 'TERRITORIALIDAD',
                'TRIDIMENSIONAL', 'TRIGONOMETRICO', 'ULTRAVIOLETA', 'UNIDIMENSIONAL', 'UNIVERSITARIO',
                'VIDEOCONFERENCIA']
        }
    def build(self):
        # Load KV file
        Builder.load_file('ahorcado.kv')
        
        # Set theme colors and style
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        
        # Create screen manager
        sm = ScreenManager()
        
        # Add screens
        sm.add_widget(LoadingScreen(name='loading'))
        sm.add_widget(MenuPrincipal(name='menu'))
        sm.add_widget(ModoSolitario(name='solitario'))
      
        
        # Set current screen
        sm.current = 'loading'
        Clock.schedule_once(lambda dt: self.switch_to_menu(sm), 4)
        # Bind keyboard
        Window.bind(on_key_down=self.on_keyboard)
        
        return sm


    def switch_to_menu(self, screen_manager):
        screen_manager.current = 'menu'
    def on_keyboard(self, window, key, *args):
        if 97 <= key <= 122:  # Letters a-z
            letra = chr(key).upper()
            if self.root.current == 'solitario':
                self.root.get_screen('solitario').procesar_letra(letra)


if __name__ == '__main__':
    AhorcadoApp().run()


















