from tkinter import Tk
from controlador import ControladorTrabajador

if __name__ == "__main__":
    root = Tk()
    root.title("Gestión de Trabajadores")
    root.geometry("1200x600")
    app = ControladorTrabajador(root)
    root.mainloop()
