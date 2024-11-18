import pandas as pd

class ModeloTrabajador:
    def __init__(self, file_path="base_datos_trabajadores_100_personas_colombia.xlsx"):
        self.file_path = file_path
        self.datos = pd.read_excel(file_path)
        self.reportes = [] 

    def obtener_trabajadores(self):
        return self.datos

    def evaluar_condiciones(self, trabajador, estado_animo, covid_historial, contacto_covid, temperatura):
        try:
            temperatura = float(temperatura)
        except ValueError:
            raise ValueError("La temperatura ingresada no es válida. Por favor, ingrese un número.")

        try:
            imc = float(trabajador[5])  # Supongamos que el IMC está en la columna 5
        except ValueError:
            raise ValueError(f"El valor del IMC '{trabajador[5]}' no es válido. Por favor, revisa los datos.")
        
        comorbilidades = trabajador[4]  # Supongamos que las comorbilidades están en la columna 4

        # temperatura
        if temperatura > 37.5:
            return "NO puede trabajar (Fiebre detectada)."
        elif temperatura > 37.2:
            temperatura_elevada = True  # Temperatura elevada pero no fiebre
        else:
            temperatura_elevada = False  # Temperatura normal

        # Si tuvo COVID en los últimos 3 días, no puede trabajar // si siempre entonces no trabaja 
        if covid_historial == "Sí":
            return "NO puede trabajar (COVID en los últimos 3 días)."

        # Evaluación de contacto con casos positivos 
        riesgo = 0
        if contacto_covid == "Sí":
            # Evaluación del estado de ánimo
            if estado_animo in ["No muy bien", "Muy mal"]:
                riesgo += 1

            # Evaluación de comorbilidades
            if comorbilidades != "Ninguna":
                if comorbilidades in ["Hipertensión"]:
                    riesgo += 2  # Comorbilidades moderadas aumentan el riesgo
                elif comorbilidades in ["diabetes", "asma"]:
                    riesgo += 3  # Comorbilidades graves tienen mayor impacto

            # imc
            if imc > 30 and imc <= 35:
                riesgo += 1  # Riesgo incrementado por obesidad leve
            elif imc > 35:
                riesgo += 2  # Riesgo incrementado por obesidad severa

            # Si hay temperatura elevada
            if temperatura_elevada:
                riesgo += 1

            # decisión basada en balance
            if riesgo >= 3:
                return "NO puede trabajar (alto riesgo tras contacto positivo)."
            return "Puede trabajar hoy (balance positivo tras contacto positivo)."

        if temperatura_elevada:
            return "puede trabajar hoy (temperatura elevada, sin fiebre ni contacto positivo)."

        return "puede trabajar hoy."

    def clasificar_trabajadores(self, criterio):
        if criterio in self.datos.columns:
            self.datos = self.datos.sort_values(by=criterio)
        return self.datos

    def calcular_riesgo(self):
        def riesgo_fila(row):
            riesgo = 0
            if row["Edad"] > 60:
                riesgo += 2
            elif row["Edad"] > 40:
                riesgo += 1

            if row["Comorbilidades"] != "Ninguna":
                riesgo += 2

            if row["Contacto con casos positivos"] == "Sí":
                riesgo += 1

            if riesgo >= 4:
                return "Alto Riesgo"
            elif 2 <= riesgo < 4:
                return "Riesgo Moderado"
            else:
                return "Bajo Riesgo"

        self.datos["Nivel de Riesgo"] = self.datos.apply(riesgo_fila, axis=1)
        return self.datos

    def exportar_reporte(self, file_path):
        self.datos.to_excel(file_path, index=False)

    def agregar_paciente(self, nuevo_paciente):
        nuevo_paciente["ID"] = len(self.datos) + 1
        nuevo_paciente_df = pd.DataFrame([nuevo_paciente])
        self.datos = pd.concat([self.datos, nuevo_paciente_df], ignore_index=True)
        self.datos.to_excel(self.file_path, index=False)

    def generar_reporte(self, reporte):
        # aca generamos el reporte y se exporta  como Excel
        self.reportes.append(reporte)
        df = pd.DataFrame(self.reportes)
        df.to_excel("reporte_evaluaciones.xlsx", index=False)
