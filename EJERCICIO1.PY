import tkinter as tk
from tkinter import ttk, messagebox
import random

class Personaje:
    def __init__(self, nombre, vida, ataque, defensa):
        self.__nombre = nombre
        self.__vida = 0
        self.set_vida(vida)
        self.__ataque = ataque
        self.__defensa = defensa

    def get_nombre(self):
        return self.__nombre

    def get_vida(self):
        return self.__vida

    def get_ataque(self):
        return self.__ataque

    def get_defensa(self):
        return self.__defensa

    def set_vida(self, nueva_vida):
        self.__vida = max(0, min(100, nueva_vida))

    def esta_vivo(self):
        return self.__vida > 0

    def atacar(self, objetivo):
        raise NotImplementedError("Este método debe implementarse en la subclase.")


class Guerrero(Personaje):
    def atacar(self, objetivo):
        dano = int(self.get_ataque() * 1.2 - objetivo.get_defensa())
        dano = max(1, dano)
        objetivo.set_vida(objetivo.get_vida() - dano)
        return f"💥 {self.get_nombre()} ataca con fuerza bruta!\nDaño: {dano}"


class Mago(Personaje):
    def atacar(self, objetivo):
        dano = self.get_ataque()  # Ignora defensa
        objetivo.set_vida(objetivo.get_vida() - dano)
        return f"✨ {self.get_nombre()} lanza un hechizo!\nDaño (ignora defensa): {dano}"


class Arquero(Personaje):
    def atacar(self, objetivo):
        if self.get_ataque() > objetivo.get_defensa():
            dano = (self.get_ataque() - objetivo.get_defensa()) * 2
        else:
            dano = self.get_ataque() - objetivo.get_defensa()
        dano = max(1, dano)
        objetivo.set_vida(objetivo.get_vida() - dano)
        return f"🏹 {self.get_nombre()} dispara una flecha!\nDaño: {dano}"


class JuegoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Guardians of the Ancient Kingdom")
        self.root.geometry("800x600")
        
        # Variables del juego
        self.jugador1 = None
        self.jugador2 = None
        self.turno = 1
        
        # Configurar estilo
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#333')
        self.style.configure('TButton', font=('Arial', 12), padding=10)
        
        self.crear_menu_principal()
    
    def crear_menu_principal(self):
        self.limpiar_pantalla()
        
        frame = ttk.Frame(self.root)
        frame.pack(expand=True, fill='both', padx=50, pady=50)
        
        tk.Label(frame, text="👑 Guardians of the Ancient Kingdom 👑", 
                font=('Arial', 20, 'bold'), bg='#333', fg='gold').pack(pady=20)
        
        ttk.Button(frame, text="Nueva Partida", command=self.crear_personajes).pack(pady=10, fill='x')
        ttk.Button(frame, text="Instrucciones", command=self.mostrar_instrucciones).pack(pady=10, fill='x')
        ttk.Button(frame, text="Salir", command=self.root.quit).pack(pady=10, fill='x')
    
    def crear_personajes(self):
        self.limpiar_pantalla()
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Pestañas para cada jugador
        self.frame_jugador1 = ttk.Frame(self.notebook)
        self.frame_jugador2 = ttk.Frame(self.notebook)
        
        self.notebook.add(self.frame_jugador1, text="Jugador 1")
        self.notebook.add(self.frame_jugador2, text="Jugador 2")
        
        # Controles para crear personaje
        self.crear_controles_personaje(self.frame_jugador1, 1)
        self.crear_controles_personaje(self.frame_jugador2, 2)
        
        # Botón para comenzar batalla
        ttk.Button(self.root, text="Comenzar Batalla", command=self.iniciar_combate).pack(pady=20)
    
    def crear_controles_personaje(self, frame, num_jugador):
        # Variables
        self.clase_var = tk.StringVar(value="guerrero")
        self.nombre_var = tk.StringVar(value=f"Jugador {num_jugador}")
        
        # Frame principal
        main_frame = ttk.Frame(frame)
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Selección de clase
        ttk.Label(main_frame, text="Selecciona tu clase:").grid(row=0, column=0, sticky='w', pady=5)
        
        clases_frame = ttk.Frame(main_frame)
        clases_frame.grid(row=1, column=0, sticky='w', pady=5)
        
        tk.Radiobutton(clases_frame, text="Guerrero 🛡️", variable=self.clase_var,
                      value="guerrero", bg='#333', fg='white', selectcolor='#444').pack(anchor='w')
        tk.Radiobutton(clases_frame, text="Mago 🔮", variable=self.clase_var,
                      value="mago", bg='#333', fg='white', selectcolor='#444').pack(anchor='w')
        tk.Radiobutton(clases_frame, text="Arquero 🏹", variable=self.clase_var,
                      value="arquero", bg='#333', fg='white', selectcolor='#444').pack(anchor='w')
        
        # Nombre del personaje
        ttk.Label(main_frame, text="Nombre del personaje:").grid(row=2, column=0, sticky='w', pady=5)
        ttk.Entry(main_frame, textvariable=self.nombre_var).grid(row=3, column=0, sticky='ew', pady=5)
        
        # Atributos
        ttk.Label(main_frame, text="Distribuye tus puntos (10 disponibles):").grid(row=4, column=0, sticky='w', pady=10)
        
        atributos_frame = ttk.Frame(main_frame)
        atributos_frame.grid(row=5, column=0, sticky='ew')
        
        # Vida
        ttk.Label(atributos_frame, text="Vida:").grid(row=0, column=0, padx=5)
        self.vida_slider = tk.Scale(atributos_frame, from_=1, to=10, orient='horizontal', bg='#333', fg='white')
        self.vida_slider.grid(row=0, column=1, padx=5)
        
        # Ataque
        ttk.Label(atributos_frame, text="Ataque:").grid(row=1, column=0, padx=5)
        self.ataque_slider = tk.Scale(atributos_frame, from_=1, to=10, orient='horizontal', bg='#333', fg='white')
        self.ataque_slider.grid(row=1, column=1, padx=5)
        
        # Defensa
        ttk.Label(atributos_frame, text="Defensa:").grid(row=2, column=0, padx=5)
        self.defensa_slider = tk.Scale(atributos_frame, from_=0, to=10, orient='horizontal', bg='#333', fg='white')
        self.defensa_slider.grid(row=2, column=1, padx=5)
        
        # Valores iniciales
        self.vida_slider.set(4)
        self.ataque_slider.set(3)
        self.defensa_slider.set(3)
    
    def iniciar_combate(self):
        # Crear personajes
        try:
            self.jugador1 = self.crear_personaje_actual(1)
            self.jugador2 = self.crear_personaje_actual(2)
            
            self.limpiar_pantalla()
            self.turno = 1
            
            # Frame principal
            main_frame = ttk.Frame(self.root)
            main_frame.pack(expand=True, fill='both', padx=10, pady=10)
            
            # Panel de información
            info_frame = ttk.Frame(main_frame)
            info_frame.pack(fill='x', pady=10)
            
            # Jugador 1
            self.jugador1_frame = ttk.Frame(info_frame)
            self.jugador1_frame.pack(side='left', expand=True, fill='both', padx=5)
            self.actualizar_info_jugador(self.jugador1, self.jugador1_frame)
            
            # VS
            ttk.Label(info_frame, text="VS", font=('Arial', 24)).pack(side='left', padx=20)
            
            # Jugador 2
            self.jugador2_frame = ttk.Frame(info_frame)
            self.jugador2_frame.pack(side='left', expand=True, fill='both', padx=5)
            self.actualizar_info_jugador(self.jugador2, self.jugador2_frame)
            
            # Log del combate
            self.log_frame = ttk.Frame(main_frame)
            self.log_frame.pack(expand=True, fill='both', pady=10)
            
            self.log_text = tk.Text(self.log_frame, height=10, wrap='word', bg='#333', fg='white')
            self.log_text.pack(expand=True, fill='both')
            
            # Panel de acciones
            acciones_frame = ttk.Frame(main_frame)
            acciones_frame.pack(fill='x', pady=10)
            
            ttk.Label(acciones_frame, text=f"Turno {self.turno} - {self.jugador1.get_nombre()}", 
                     font=('Arial', 12, 'bold')).pack()
            
            ttk.Button(acciones_frame, text="Atacar", command=self.ejecutar_turno).pack(pady=5, fill='x')
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron crear los personajes: {str(e)}")
    
    def crear_personaje_actual(self, num_jugador):
        # Obtener valores de los controles
        clase = self.clase_var.get()
        nombre = self.nombre_var.get()
        vida = self.vida_slider.get() * 10
        ataque = self.ataque_slider.get() * 10
        defensa = self.defensa_slider.get() * 10
        
        # Validar distribución de puntos
        total = self.vida_slider.get() + self.ataque_slider.get() + self.defensa_slider.get()
        if total > 10:
            raise ValueError("La suma de los puntos no debe exceder 10")
        
        # Crear personaje según la clase seleccionada
        if clase == "guerrero":
            return Guerrero(nombre, vida, ataque, defensa)
        elif clase == "mago":
            return Mago(nombre, vida, ataque, defensa)
        elif clase == "arquero":
            return Arquero(nombre, vida, ataque, defensa)
    
    def actualizar_info_jugador(self, jugador, frame):
        for widget in frame.winfo_children():
            widget.destroy()
        
        ttk.Label(frame, text=jugador.get_nombre(), font=('Arial', 14, 'bold')).pack()
        
        clase = "Guerrero 🛡️" if isinstance(jugador, Guerrero) else \
               "Mago 🔮" if isinstance(jugador, Mago) else "Arquero 🏹"
        ttk.Label(frame, text=clase).pack()
        
        ttk.Label(frame, text=f"Vida: {jugador.get_vida()}").pack()
        ttk.Label(frame, text=f"Ataque: {jugador.get_ataque()}").pack()
        ttk.Label(frame, text=f"Defensa: {jugador.get_defensa()}").pack()
    
    def ejecutar_turno(self):
        jugador_actual = self.jugador1 if self.turno % 2 == 1 else self.jugador2
        oponente = self.jugador2 if self.turno % 2 == 1 else self.jugador1
        
        resultado = jugador_actual.atacar(oponente)
        self.log_text.insert('end', f"Turno {self.turno}: {resultado}\n")
        self.log_text.insert('end', f"Vida de {oponente.get_nombre()}: {oponente.get_vida()}\n\n")
        self.log_text.see('end')
        
        # Actualizar información
        self.actualizar_info_jugador(self.jugador1, self.jugador1_frame)
        self.actualizar_info_jugador(self.jugador2, self.jugador2_frame)
        
        # Verificar si el combate ha terminado
        if not oponente.esta_vivo():
            self.finalizar_combate(jugador_actual)
            return
        
        self.turno += 1
    
    def finalizar_combate(self, ganador):
        self.log_text.insert('end', f"🏁 ¡Combate terminado! 🎉 {ganador.get_nombre()} gana la batalla!\n\n")
        
        # Botones post-combate
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Frame):
                widget.destroy()
        
        frame = ttk.Frame(self.root)
        frame.pack(expand=True, fill='both', padx=50, pady=50)
        
        ttk.Button(frame, text="Nueva Partida", command=self.crear_personajes).pack(pady=10, fill='x')
        ttk.Button(frame, text="Salir", command=self.root.quit).pack(pady=10, fill='x')
    
    def mostrar_instrucciones(self):
        instrucciones = """
        🏰 Guardians of the Ancient Kingdom 🏰

        Instrucciones del juego:

        1. Crea tus personajes:
           - Elige una clase (Guerrero, Mago o Arquero)
           - Distribuye tus puntos entre Vida, Ataque y Defensa
           - Dale un nombre a tu personaje

        2. Combate por turnos:
           - Cada turno el personaje atacará automáticamente
           - El juego muestra los resultados de cada ataque

        3. Gana el combate reduciendo la vida del oponente a 0
        """
        messagebox.showinfo("Instrucciones", instrucciones)
    
    def limpiar_pantalla(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    juego = JuegoGUI(root)
    root.mainloop()