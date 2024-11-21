import tkinter as tk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Classe para o nó da árvore binária
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


# Classe para a árvore binária
class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        if self.root is None:
            self.root = Node(value)
        else:
            self._insert(self.root, value)

    def _insert(self, current, value):
        if value < current.value:
            if current.left is None:
                current.left = Node(value)
            else:
                self._insert(current.left, value)
        elif value > current.value:
            if current.right is None:
                current.right = Node(value)
            else:
                self._insert(current.right, value)
        else:
            messagebox.showinfo("Informação", "Valor já existe na árvore.")

    def remove(self, value):
        self.root = self._remove(self.root, value)

    def _remove(self, current, value):
        if current is None:
            messagebox.showinfo("Erro", "Valor não encontrado.")
            return None
        if value < current.value:
            current.left = self._remove(current.left, value)
        elif value > current.value:
            current.right = self._remove(current.right, value)
        else:
            if current.left is None:
                return current.right
            elif current.right is None:
                return current.left
            min_larger_node = self._find_min(current.right)
            current.value = min_larger_node.value
            current.right = self._remove(current.right, min_larger_node.value)
        return current

    def _find_min(self, current):
        while current.left is not None:
            current = current.left
        return current

    def get_nodes_edges(self):
        """
        Retorna os nós e arestas da árvore para visualização.
        """
        nodes = []
        edges = []
        self._collect_nodes_edges(self.root, None, nodes, edges)
        return nodes, edges

    def _collect_nodes_edges(self, current, parent, nodes, edges):
        if current:
            nodes.append((current.value, parent))  # Nó com seu pai
            if parent is not None:
                edges.append((parent, current.value))  # Conexão pai-filho
            self._collect_nodes_edges(current.left, current.value, nodes, edges)
            self._collect_nodes_edges(current.right, current.value, nodes, edges)


# Interface gráfica
class BinaryTreeApp:
    def __init__(self, root):
        self.tree = BinaryTree()

        self.root = root
        self.root.title("Árvore Binária")
        self.root.configure(bg="#2c3e50")

        # Estilo e layout
        self.header = tk.Label(root, text="Árvore Binária", font=("Arial", 24, "bold"), bg="#34495e", fg="white")
        self.header.pack(pady=10, fill=tk.X)

        self.label_insert = tk.Label(root, text="Insira um número:", font=("Arial", 14), bg="#2c3e50", fg="white")
        self.label_insert.pack(pady=5)

        self.entry_insert = tk.Entry(root, font=("Arial", 12), bg="#ecf0f1")
        self.entry_insert.pack(pady=5)

        self.button_insert = tk.Button(root, text="Inserir", command=self.insert_number, bg="#27ae60", fg="white", font=("Arial", 12), relief=tk.RAISED)
        self.button_insert.pack(pady=5)

        self.label_remove = tk.Label(root, text="Remova um número:", font=("Arial", 14), bg="#2c3e50", fg="white")
        self.label_remove.pack(pady=5)

        self.entry_remove = tk.Entry(root, font=("Arial", 12), bg="#ecf0f1")
        self.entry_remove.pack(pady=5)

        self.button_remove = tk.Button(root, text="Remover", command=self.remove_number, bg="#e74c3c", fg="white", font=("Arial", 12), relief=tk.RAISED)
        self.button_remove.pack(pady=5)

        self.button_display = tk.Button(root, text="Exibir Árvore", command=self.display_tree, bg="#2980b9", fg="white", font=("Arial", 12), relief=tk.RAISED)
        self.button_display.pack(pady=10)

        self.figure = Figure(figsize=(6, 4))
        self.ax = self.figure.add_subplot(111)
        self.ax.axis("off")

        self.canvas = FigureCanvasTkAgg(self.figure, root)
        self.canvas.get_tk_widget().pack(pady=10)

    def insert_number(self):
        try:
            value = int(self.entry_insert.get())
            self.tree.insert(value)
            self.entry_insert.delete(0, tk.END)
            messagebox.showinfo("Sucesso", f"Número {value} inserido na árvore.")
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um número válido.")

    def remove_number(self):
        try:
            value = int(self.entry_remove.get())
            self.tree.remove(value)
            self.entry_remove.delete(0, tk.END)
            messagebox.showinfo("Sucesso", f"Número {value} removido da árvore.")
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um número válido.")

    def display_tree(self):
        # Limpar o gráfico anterior
        self.ax.clear()
        self.ax.axis("off")

        # Obter nós e arestas da árvore
        nodes, edges = self.tree.get_nodes_edges()

        # Desenhar os nós e as conexões
        positions = self._compute_positions(self.tree.root, 0, 0, 1, {})
        for parent, child in edges:
            x1, y1 = positions[parent]
            x2, y2 = positions[child]
            self.ax.plot([x1, x2], [y1, y2], "k-")  # Linha de conexão

        for value, (x, y) in positions.items():
            self.ax.plot(x, y, "bo", ms=15)  # Nó
            self.ax.text(x, y, str(value), color="white", ha="center", va="center")  # Texto do nó

        self.canvas.draw()

    def _compute_positions(self, node, depth, x_min, x_max, positions):
        """
        Calcula as posições (x, y) dos nós para exibição em uma estrutura de árvore.
        """
        if node is None:
            return positions

        x = (x_min + x_max) / 2
        y = -depth
        positions[node.value] = (x, y)

        self._compute_positions(node.left, depth + 1, x_min, x, positions)
        self._compute_positions(node.right, depth + 1, x, x_max, positions)

        return positions


# Execução da aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = BinaryTreeApp(root)
    root.mainloop()
