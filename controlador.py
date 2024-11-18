from modelo import ModeloTrabajador
from vista import VistaTrabajador
from ventana_evaluacion import VentanaEvaluacion


class ControladorTrabajador:
    def __init__(self, root):
        self.modelo = ModeloTrabajador()
        self.vista = VistaTrabajador(root, self)
        self.vista.pack(fill="both", expand=True)

    def obtener_columnas(self):
        return self.modelo.obtener_trabajadores().columns.tolist()

    def obtener_datos(self):
        return self.modelo.obtener_trabajadores()

    def clasificar_por(self, criterio):
        self.modelo.clasificar_trabajadores(criterio)

    def calcular_riesgo(self):
        self.modelo.calcular_riesgo()

    def exportar_reporte(self, file_path):
        self.modelo.exportar_reporte(file_path)

    def agregar_paciente(self, nuevo_paciente):
        self.modelo.agregar_paciente(nuevo_paciente)

    def mostrar_ventana_evaluacion(self, trabajador):
        VentanaEvaluacion(trabajador, self.modelo)
