import socket
from tkinter import *
import customtkinter as ctk
import threading

# Criar a janela principal da aplicação
app = ctk.CTk()
app.title('Principal')
largura = 600
altura = 600
app.geometry(f"{largura}x{altura}")
largura_tela = app.winfo_screenwidth()
altura_tela = app.winfo_screenheight()
pos_x = (largura_tela - largura) // 2
pos_y = (altura_tela - altura) // 2
app.geometry(f"+{pos_x}+{pos_y}")

# Função para lidar com a criação do servidor e interações
def criar_servidor():
    botao_servidor.destroy()
    botao_cliente.destroy()

    ip_maquina = socket.gethostbyname(socket.gethostname())
    ip_servidor_label = ctk.CTkLabel(app, text=f"IP do Servidor: {ip_maquina}")
    ip_servidor_label.pack()

    aguardando = ctk.CTkLabel(app, text='Aguardando Conexões...')
    aguardando.pack()

    def start_server():
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((ip_maquina, 5000))
        server.listen()

        client, cliente_ip = server.accept()

        aguardando.destroy()
        ip_servidor_label.destroy()

        ctk.CTkLabel(app, text=f"O cliente {cliente_ip} se conectou").pack()

        chat = ctk.CTkFrame(app, width=500)
        chat.pack()

        def enviar_mensagem_servidor(c):
            messagectk = ctk.CTkEntry(chat, placeholder_text='Digite sua mensagem', width=200)
            messagectk.pack(side=BOTTOM)

            def enviar_com_enter(event):
                if event.keysym == "Return":
                    ctk.CTkLabel(chat, text=f"Você: {messagectk.get()}").pack()
                    message = messagectk.get()
                    messagectk.delete(0, END)
                    c.send(message.encode())

            messagectk.bind("<Key>", enviar_com_enter)

        def receber_mensagem_servidor(c):
            while True:
                ctk.CTkLabel(chat, text=f"{cliente_ip[0]}: {c.recv(1024).decode()}").pack()

        threading.Thread(target=enviar_mensagem_servidor, args=(client,)).start()
        threading.Thread(target=receber_mensagem_servidor, args=(client,)).start()

    thread = threading.Thread(target=start_server)
    thread.daemon = True
    thread.start()

def criar_cliente():
    botao_servidor.destroy()
    botao_cliente.destroy()

    ip_label = ctk.CTkLabel(app, text="IP:")
    ip_label.pack()
    ip_entry = ctk.CTkEntry(app)
    ip_entry.pack()
    porta_label = ctk.CTkLabel(app, text="Porta:")
    porta_label.pack()
    porta_entry = ctk.CTkEntry(app)
    porta_entry.pack()

    def conectar_cliente():
        ip = ip_entry.get()
        porta = porta_entry.get()

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, int(porta)))

        ip_label.destroy()
        ip_entry.destroy()
        porta_label.destroy()
        porta_entry.destroy()
        botao_conectar.destroy()

        chat = ctk.CTkFrame(app, width=300, height=200, corner_radius=10)
        chat.pack(padx=20, pady=20)

        def enviar_mensagem_cliente(c):
            messagectk = ctk.CTkEntry(chat, placeholder_text='Digite sua mensagem', width=200)
            messagectk.pack(side=BOTTOM)

            def enviar_com_enter(event):
                if event.keysym == "Return":
                    ctk.CTkLabel(chat, text=f"Você: {messagectk.get()}").pack()
                    message = messagectk.get()
                    messagectk.delete(0, END)
                    c.send(message.encode())

            messagectk.bind("<Key>", enviar_com_enter)

        def receber_mensagem_cliente(c):
            while True:
                ctk.CTkLabel(chat, text=f"Servidor: {c.recv(1024).decode()}").pack()

        threading.Thread(target=enviar_mensagem_cliente, args=(client,)).start()
        threading.Thread(target=receber_mensagem_cliente, args=(client,)).start()

    botao_conectar = ctk.CTkButton(app, text="Conectar", command=conectar_cliente)
    botao_conectar.pack()

def criar_chat():
    chat_frame = Frame(app)
    chat_frame.pack(expand=True, fill=BOTH)

    chat_canvas = ctk.CTkCanvas(chat_frame)
    chat_canvas.pack(side=LEFT, expand=True, fill=BOTH)

    chat_scroll = ctk.CTkScrollbar(app, command=chat_canvas.yview)
    chat_scroll.pack(side=RIGHT, fill=Y)

    chat_canvas.configure(yscrollcommand=chat_scroll.set)

    chat_frame_window = chat_canvas.create_window((0, 0), window=chat_frame, anchor='nw', tags="frame")

    def on_configure(event):
        chat_canvas.configure(scrollregion=chat_canvas.bbox("all"))
        chat_canvas.yview_moveto(1.0)

    chat_canvas.bind("<Configure>", on_configure)

    def scroll(event):
        chat_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    app.bind_all("<MouseWheel>", scroll)

criar_chat()

botao_servidor = ctk.CTkButton(app, text="Servidor", command=criar_servidor)
botao_servidor.pack()

botao_cliente = ctk.CTkButton(app, text="Cliente", command=criar_cliente)
botao_cliente.pack()

app.mainloop()
