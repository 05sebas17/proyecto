from tkinter import Frame, Label, Button, Scrollbar, StringVar, OptionMenu, Entry, Toplevel, filedialog, messagebox
from tkinter.ttk import Treeview


class VistaTrabajador(Frame):
    def __init__(self, master, controlador):
        super().__init__(master)
        self.controlador = controlador
        self.crear_interfaz()

    def crear_interfaz(self):
        Label(self, text="Gestión de Trabajadores", font=("Arial", 16)).pack(pady=10)

        self.tree = Treeview(self, columns=self.controlador.obtener_columnas(), show="headings")
        for col in self.controlador.obtener_columnas():
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)

        self.tree.bind("<Double-1>", self.abrir_ventana_evaluacion)  # Evento de doble clic
        self.tree.pack(fill="both", expand=True)

        scrollbar = Scrollbar(self, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        Button(self, text="Cargar Datos", command=self.mostrar_datos).pack(pady=5)
        Button(self, text="Calcular Riesgo", command=self.controlador.calcular_riesgo).pack(pady=5)
        Button(self, text="Agregar trabajador", command=self.abrir_formulario_agregar).pack(pady=5)
        Button(self, text="Exportar Reporte", command=self.exportar_reporte).pack(pady=5)

    def mostrar_datos(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in self.controlador.obtener_datos().itertuples(index=False):
            self.tree.insert("", "end", values=row)

    def abrir_formulario_agregar(self):
        ventana = Toplevel(self)
        ventana.title("Agregar trabajador")
        ventana.geometry("400x600")

        campos = {
            "Identificación": {"tipo": "numero"},
            "Nombre": {"tipo": "texto"},
            "Dirección": {"tipo": "texto-numero"},
            "Ciudad": {"tipo": "desplegable", "opciones": ["Bogotá", "Medellín", "Cali", "Cartagena", "Barranquilla"]},
            "Estado de Salud": {"tipo": "desplegable", "opciones": ["Bueno", "Regular", "Malo"]},
            "Comorbilidades": {"tipo": "desplegable", "opciones": ["Diabetes", "Hipertensión", "Asma", "Ninguna"]},
            "Edad": {"tipo": "numero"},
            "Peso (kg)": {"tipo": "numero"},
            "Estatura (m)": {"tipo": "decimal"},
            "Contacto con casos positivos": {"tipo": "desplegable", "opciones": ["Sí", "No"]},
        }

        entradas = {}
        for idx, (campo, config) in enumerate(campos.items()):
            Label(ventana, text=campo).grid(row=idx, column=0, pady=5, sticky="w")
            if config["tipo"] in {"texto", "numero", "decimal", "texto-numero"}:
                entrada = Entry(ventana)
                entrada.grid(row=idx, column=1, pady=5)
                entradas[campo] = entrada
            elif config["tipo"] == "desplegable":
                valor = StringVar(value=config["opciones"][0])
                menu = OptionMenu(ventana, valor, *config["opciones"])
                menu.grid(row=idx, column=1, pady=5)
                entradas[campo] = valor

        def guardar_paciente():
            try:
                nuevo_paciente = {}
                for campo, config in campos.items():
                    if config["tipo"] == "numero":
                        nuevo_paciente[campo] = int(entradas[campo].get())
                    elif config["tipo"] == "decimal":
                        nuevo_paciente[campo] = float(entradas[campo].get())
                    else:
                        nuevo_paciente[campo] = entradas[campo].get()
                self.controlador.agregar_paciente(nuevo_paciente)
                self.mostrar_datos()
                ventana.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        Button(ventana, text="Guardar", command=guardar_paciente).grid(row=len(campos), column=0, columnspan=2, pady=10)

    def abrir_ventana_evaluacion(self, event):
        item = self.tree.selection()
        if not item:
            messagebox.showerror("Error", "Seleccione un trabajador.")
            return

        trabajador = self.tree.item(item[0], "values")
        self.controlador.mostrar_ventana_evaluacion(trabajador)

    def exportar_reporte(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            self.controlador.exportar_reporte(file_path)
