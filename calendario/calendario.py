import datetime
import time
import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
import threading

class CalendarioComAlertas:
    def __init__(self, arquivo_dados="calendario_data.json"):
        self.arquivo_dados = arquivo_dados
        self.eventos = self.carregar_eventos()
    
    def carregar_eventos(self):
        """Carrega eventos do arquivo JSON"""
        if os.path.exists(self.arquivo_dados):
            try:
                with open(self.arquivo_dados, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def salvar_eventos(self):
        """Salva eventos no arquivo JSON"""
        with open(self.arquivo_dados, 'w', encoding='utf-8') as f:
            json.dump(self.eventos, f, indent=4, ensure_ascii=False)
    
    def adicionar_evento(self, data, descricao, alerta_minutos=0):
        """Adiciona um novo evento ao calendário"""
        # Converter para string para usar como chave no dicionário
        data_str = data.strftime("%Y-%m-%d %H:%M")
        
        if data_str not in self.eventos:
            self.eventos[data_str] = []
        
        evento = {
            "descricao": descricao,
            "alerta_minutos": alerta_minutos,
            "notificado": False
        }
        
        self.eventos[data_str].append(evento)
        self.salvar_eventos()
        return f"Evento adicionado: {data_str} - {descricao}"
    
    def listar_eventos(self, data=None):
        """Lista todos os eventos ou eventos de uma data específica"""
        if data:
            data_str = data.strftime("%Y-%m-%d")
            eventos_do_dia = {}
            
            for data_evento, eventos in self.eventos.items():
                if data_evento.startswith(data_str):
                    eventos_do_dia[data_evento] = eventos
            
            return eventos_do_dia
        else:
            return self.eventos
    
    def verificar_alertas(self):
        """Verifica se há alertas para mostrar"""
        agora = datetime.datetime.now()
        alertas_encontrados = []
        
        for data_str, eventos in self.eventos.items():
            try:
                data_evento = datetime.datetime.strptime(data_str, "%Y-%m-%d %H:%M")
                
                for evento in eventos:
                    # Se ainda não foi notificado e está no tempo de alerta
                    if not evento["notificado"]:
                        tempo_restante = data_evento - agora
                        minutos_restantes = tempo_restante.total_seconds() / 60
                        
                        if 0 <= minutos_restantes <= evento["alerta_minutos"]:
                            mensagem = f"🔔 ALERTA: {evento['descricao']} às {data_str}"
                            alertas_encontrados.append(mensagem)
                            evento["notificado"] = True
            
            except ValueError:
                continue
        
        self.salvar_eventos()
        return alertas_encontrados
    
    def remover_evento(self, data, descricao):
        """Remove um evento específico"""
        data_str = data.strftime("%Y-%m-%d %H:%M")
        
        if data_str in self.eventos:
            # Filtra os eventos, mantendo apenas os que não correspondem à descrição
            eventos_originais = self.eventos[data_str]
            novos_eventos = [e for e in eventos_originais if e["descricao"] != descricao]
            
            if len(novos_eventos) == 0:
                # Se não há mais eventos nessa data, remove a data
                del self.eventos[data_str]
            else:
                self.eventos[data_str] = novos_eventos
            
            self.salvar_eventos()
            return True
        return False


class CalendarioGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Calendário com Alertas")
        self.root.geometry("700x500")
        
        # Centralizar a janela
        self.root.eval('tk::PlaceWindow . center')
        
        self.calendario = CalendarioComAlertas()
        
        self.criar_interface()
        self.iniciar_monitoramento()
    
    def criar_interface(self):
        # Configurar estilo
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10))
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        title_label = ttk.Label(main_frame, text="📅 Calendário com Alertas", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 15))
        
        # Formulário para adicionar eventos
        form_frame = ttk.LabelFrame(main_frame, text="Adicionar Novo Evento", padding="10")
        form_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Data e Hora
        ttk.Label(form_frame, text="Data e Hora:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.data_entry = ttk.Entry(form_frame, width=20, font=('Arial', 10))
        self.data_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        self.data_entry.insert(0, datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        
        # Descrição
        ttk.Label(form_frame, text="Descrição:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.desc_entry = ttk.Entry(form_frame, width=20, font=('Arial', 10))
        self.desc_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        
        # Alerta
        ttk.Label(form_frame, text="Alerta (minutos antes):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.alerta_entry = ttk.Entry(form_frame, width=20, font=('Arial', 10))
        self.alerta_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        self.alerta_entry.insert(0, "10")
        
        # Botão Adicionar
        add_button = ttk.Button(form_frame, text="Adicionar Evento", command=self.adicionar_evento)
        add_button.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Lista de eventos
        list_frame = ttk.LabelFrame(main_frame, text="Eventos Agendados", padding="10")
        list_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Treeview para mostrar eventos
        columns = ("Data", "Descrição", "Alerta (min)")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=10)
        
        # Configurar colunas
        col_widths = [180, 250, 100]
        for i, col in enumerate(columns):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=col_widths[i], minwidth=50)
        
        # Scrollbar para a treeview
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Layout da treeview e scrollbar
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Botão para remover evento
        remove_button = ttk.Button(main_frame, text="Remover Evento Selecionado", command=self.remover_evento)
        remove_button.grid(row=3, column=0, columnspan=2, pady=(0, 10))
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Pronto")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # Configurar expansão
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        form_frame.columnconfigure(1, weight=1)
        
        # Atualizar lista de eventos
        self.atualizar_lista_eventos()
    
    def adicionar_evento(self):
        data_str = self.data_entry.get()
        descricao = self.desc_entry.get()
        alerta_str = self.alerta_entry.get()
        
        if not descricao:
            messagebox.showerror("Erro", "Por favor, insira uma descrição para o evento.")
            return
        
        try:
            data = datetime.datetime.strptime(data_str, "%Y-%m-%d %H:%M")
            alerta = int(alerta_str) if alerta_str else 0
            
            resultado = self.calendario.adicionar_evento(data, descricao, alerta)
            self.atualizar_lista_eventos()
            
            # Limpar campo de descrição
            self.desc_entry.delete(0, tk.END)
            
            self.status_var.set(resultado)
            messagebox.showinfo("Sucesso", "Evento adicionado com sucesso!")
            
        except ValueError as e:
            messagebox.showerror("Erro", f"Formato de data/hora inválido!\nUse: AAAA-MM-DD HH:MM\nExemplo: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    def remover_evento(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Nenhum evento selecionado.")
            return
        
        item = self.tree.item(selecionado[0])
        valores = item['values']
        if not valores or len(valores) < 2:
            return
        
        data_str, descricao = valores[0], valores[1]
        
        try:
            data = datetime.datetime.strptime(data_str, "%Y-%m-%d %H:%M")
            if self.calendario.remover_evento(data, descricao):
                self.atualizar_lista_eventos()
                self.status_var.set(f"Evento removido: {data_str} - {descricao}")
                messagebox.showinfo("Sucesso", "Evento removido com sucesso!")
            else:
                messagebox.showerror("Erro", "Não foi possível remover o evento.")
        except ValueError:
            messagebox.showerror("Erro", "Erro ao processar data do evento.")
    
    def atualizar_lista_eventos(self):
        # Limpar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Adicionar eventos
        eventos = self.calendario.listar_eventos()
        for data_str, eventos_lista in eventos.items():
            for evento in eventos_lista:
                self.tree.insert("", tk.END, values=(
                    data_str, 
                    evento["descricao"], 
                    evento["alerta_minutos"]
                ))
    
    def verificar_alertas_gui(self):
        """Verifica alertas e mostra na interface"""
        alertas = self.calendario.verificar_alertas()
        for alerta in alertas:
            self.status_var.set(alerta)
            messagebox.showwarning("Alerta", alerta)
        
        # Agendar próxima verificação
        self.root.after(30000, self.verificar_alertas_gui)  # Verificar a cada 30 segundos
    
    def iniciar_monitoramento(self):
        """Inicia o monitoramento de alertas"""
        self.verificar_alertas_gui()


def main():
    """Função principal para executar a interface gráfica"""
    root = tk.Tk()
    app = CalendarioGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()