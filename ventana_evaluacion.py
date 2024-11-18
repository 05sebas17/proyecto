from tkinter import Toplevel, StringVar, OptionMenu, Entry, Button, Label, messagebox


class VentanaEvaluacion:
    def __init__(self, trabajador, modelo):
        self.trabajador = trabajador
        self.modelo = modelo

        # Crear la ventana
        self.ventana = Toplevel()
        self.ventana.title("Evaluación de Salud")
        self.ventana.geometry("400x550")

        # Componentes de la interfaz
        self.crear_interfaz()

    def crear_interfaz(self):
        # Información del trabajador
        Label(self.ventana, text=f"Trabajador: {self.trabajador[1]}", font=("Arial", 14)).pack(pady=10)

        # Cómo se siente hoy
        Label(self.ventana, text="¿Cómo se siente hoy?").pack(pady=5)
        self.estado_animo = StringVar(value="Muy bien")
        opciones_animo = ["Muy bien", "Bien", "Normal", "No muy bien", "Muy mal"]
        OptionMenu(self.ventana, self.estado_animo, *opciones_animo).pack(pady=5)

        # Historial de COVID
        Label(self.ventana, text="¿Ha tenido COVID en los últimos 3 días?").pack(pady=5)
        self.covid_historial = StringVar(value="No")
        opciones_covid = ["Sí", "No"]
        OptionMenu(self.ventana, self.covid_historial, *opciones_covid).pack(pady=5)

        # Contacto con casos de COVID
        Label(self.ventana, text="¿Ha tenido contacto con alguien con COVID en los últimos 7 días?").pack(pady=5)
        self.contacto_covid = StringVar(value="No")
        opciones_contacto = ["Sí", "No"]
        OptionMenu(self.ventana, self.contacto_covid, *opciones_contacto).pack(pady=5)

        # Temperatura corporal
        Label(self.ventana, text="Ingrese su temperatura corporal (°C):").pack(pady=5)
        self.temperatura = Entry(self.ventana)
        self.temperatura.pack(pady=5)

        # Botón de evaluación
        Button(self.ventana, text="Evaluar", command=self.evaluar_trabajador).pack(pady=10)

    def evaluar_trabajador(self):
        try:
            # Validar temperatura
            temp = float(self.temperatura.get())
            if temp < 35 or temp > 39:
                raise ValueError("Temperatura fuera del rango permitido (35°C - 39°C).")

            # Evaluar condiciones del trabajador
            resultado = self.modelo.evaluar_condiciones(
                self.trabajador,
                self.estado_animo.get(),
                self.covid_historial.get(),
                self.contacto_covid.get(),
                temp,
            )

            # Generar reporte
            reporte = {
                "ID": self.trabajador[0],
                "Nombre": self.trabajador[1],
                "Estado de Ánimo": self.estado_animo.get(),
                "Historial COVID (3 días)": self.covid_historial.get(),
                "Contacto con Casos Positivos (7 días)": self.contacto_covid.get(),
                "Temperatura (°C)": temp,
                "IMC": self.trabajador[5],
                "Comorbilidades": self.trabajador[4],
                "Resultado": resultado,
            }
            self.modelo.generar_reporte(reporte)

            # Mostrar resultado
            messagebox.showinfo("Resultado", f"El trabajador {resultado}. Reporte generado.")
            self.ventana.destroy()

        except ValueError as e:
            messagebox.showerror("Error", str(e))
