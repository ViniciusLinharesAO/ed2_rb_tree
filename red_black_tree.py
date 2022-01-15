from enum import Enum
from typing import Union

EMPTY_MSG = "The tree's currently empty"

class Color(Enum):
    '''
    Color é um enum que contem as possibilidades de cores para os nós na árvore rubro-negra:
    - RED = 'RED';
    - BLACK = 'BLACK';
    '''
    RED = 'RED'
    BLACK = 'BLACK'

class RedBlackTree:
    '''
    Red black tree (árvore rubro negra) é a definição da própria árvore:
    - tamanho (size) é a quantidade de nós na árvore;
    - NIL seria a definição de que existem folhas, ou nós (Node), e que estes tem como valor vazio (None) e cor preta (black);
    - root
    - ordered
    '''
    def __init__(self):
        self.size = 0
        self.NIL = self.Node(value=None, color=Color.BLACK)
        self.root = self.NIL
        self.ordered = []
        pass

    class Node():
        '''
        Um nó (Node) na árvore rubro-negra:
        - valor (value), sendo este do tipo int;
        - cor (color), que pode ser "vermelho" ou "preto";
        - nó pai (parent);
        - nó derivado na direita (right), que pode não existir (None);
        - nó derivado na esquerda (left), que pode não existir (None);
        '''
        def __init__(self, value=None, color=Color.RED):
            self.value: int = value
            self.color: Color = color
            self.parent: __class__ = None
            self.right: __class__ = None
            self.left: __class__ = None

        def __repr__(self):
            return f'<Node value:{self.value} color:{self.color.value}>'

    def left_rotate(self, base_node: Node):
        right_node = base_node.right
        base_node.right = right_node.left

        if right_node.left != self.NIL:
            right_node.left.parent = base_node

        right_node.parent = base_node.parent

        if base_node.parent == self.NIL:
            self.root = right_node
        elif base_node == base_node.parent.left:
            base_node.parent.left = right_node
        else:
            base_node.parent.right = right_node

        right_node.left = base_node
        base_node.parent = right_node

    def right_rotate(self, base_node: Node):
        left_node = base_node.left
        base_node.left = left_node.right

        if left_node.right != self.NIL:
            left_node.right.parent = base_node

        left_node.parent = base_node.parent

        if base_node.parent == self.NIL:
            self.root = left_node
        elif base_node == base_node.parent.right:
            base_node.parent.right = left_node
        else:
            base_node.parent.left = left_node

        left_node.right = base_node
        base_node.parent = left_node

    def insert(self, new_value: int):
        new_node = self.Node(value = new_value)
        self._insert(new_node)
        self.size += 1
        print(f'adicionado o valor: {new_value}\n')

    def _insert(self, new_node: Node):
        nil = self.NIL
        root = self.root

        while root != self.NIL:
            nil = root

            if new_node.value < root.value :
                root = root.left
            else:
                root = root.right

        new_node.parent = nil

        if nil == self.NIL:
            self.root = new_node
        elif new_node.value < nil.value:
            nil.left = new_node
        else:
            nil.right = new_node

        new_node.left = self.NIL
        new_node.right = self.NIL
        new_node.color = Color.RED
        self.adapt_colors_insert(new_node)

    def adapt_colors_insert(self, new_node: Node):
        """
        fix das cores quando insere um novo nó
        """
        i = 0
        while new_node.parent.color == Color.RED:
            if new_node.parent == new_node.parent.parent.left:
                y = new_node.parent.parent.right

                if y.color == Color.RED:
                    new_node.parent.color = Color.BLACK
                    y.color = Color.BLACK
                    new_node.parent.parent.color = Color.RED
                    new_node = new_node.parent.parent
                else:
                    if new_node == new_node.parent.right:
                        new_node = new_node.parent
                        self.left_rotate(new_node)

                    new_node.parent.color = Color.BLACK
                    new_node.parent.parent.color = Color.RED
                    self.right_rotate(new_node.parent.parent)
            else:
                y = new_node.parent.parent.left

                if y.color == Color.RED:
                    new_node.parent.color = Color.BLACK
                    y.color = Color.BLACK
                    new_node.parent.parent.color = Color.RED
                    new_node = new_node.parent.parent
                else:
                    if new_node == new_node.parent.left:
                        new_node = new_node.parent
                        self.right_rotate(new_node)

                    new_node.parent.color = Color.BLACK
                    new_node.parent.parent.color = Color.RED
                    self.left_rotate(new_node.parent.parent)
            i += 1
        self.root.color = Color.BLACK

    def transplant(self, base_node: Node, moved_node: Node):
        """
        alterar posição durante deleção
        """
        if base_node.parent == self.NIL:
            self.root = moved_node
        elif base_node == base_node.parent.left:
            base_node.parent.left = moved_node
        else:
            base_node.parent.right = moved_node

        moved_node.parent = base_node.parent

    def remove(self, target: int) -> Union[None, Node]:
        if self.size == 0:
            print(EMPTY_MSG)
            return None

        target_node = self.search(target)
        if target_node != None:
            self._remove(target_node)
        else:
            return None
        self.size -= 1
        print(f'removido o valor: {target}\n')
        return target_node

    def _remove(self, target_node: Node):
        original_node = target_node
        original_color = original_node.color
        if target_node.left == self.NIL:
            adjacent_node = target_node.right
            self.transplant(target_node, target_node.right)
        elif target_node.right == self.NIL:
            adjacent_node = target_node.left
            self.transplant(target_node, target_node.left)
        else:
            original_node = self._min_node(target_node.right)
            original_color = original_node.color
            adjacent_node = original_node.right
            if original_node.parent == target_node:
                adjacent_node.parent = original_node
            else:
                self.transplant(original_node, original_node.right)
                original_node.right = target_node.right
                original_node.right.parent = original_node
            self.transplant(target_node,original_node)
            original_node.left = target_node.left
            original_node.left.parent = original_node
            original_node.color = target_node.color
        if original_color == Color.BLACK:
            self.adapt_colors_remove(adjacent_node)

    def adapt_colors_remove(self, node: Node):
        """
        fix das cores quando remove um novo nó
        """
        while node != self.root and node.color == Color.BLACK:
            if node == node.parent.left:
                w = node.parent.right

                if w.color == Color.RED:
                    w.color = Color.BLACK
                    node.parent.color = Color.RED
                    self.left_rotate(node.parent)
                    w = node.parent.right
                if w.left.color == Color.BLACK and w.right.color == Color.BLACK:
                    w.color = Color.RED
                    node = node.parent
                else:
                    if w.right.color == Color.BLACK:
                        w.left.color = Color.BLACK
                        w.color = Color.RED
                        self.right_rotate(w)
                        w = node.parent.right

                    w.color = node.parent.color
                    node.parent.color = Color.BLACK
                    w.right.color = Color.BLACK
                    self.left_rotate(node.parent)
                    node = self.root
            else:
                w = node.parent.left

                if w.color == Color.RED:
                    w.color = Color.BLACK
                    node.parent.color = Color.RED
                    self.right_rotate(node.parent)
                    w = node.parent.left

                if w.right.color == Color.BLACK and w.left.color == Color.BLACK:
                    w.color = Color.RED
                    node = node.parent
                else:
                    if w.left.color == Color.BLACK:
                        w.right.color = Color.BLACK
                        w.color = Color.RED
                        self.left_rotate(w)
                        w = node.parent.left

                    w.color = node.parent.color
                    node.parent.color = Color.BLACK
                    w.left.color = Color.BLACK
                    self.right_rotate(node.parent)
                    node = self.root

        node.color = Color.BLACK

    def search(self, target: int) -> Union[None, Node]:
        if self.size == 0:
            return None
        return self._search(self.root, target)

    def _search(self, current_node: Node, target: int) -> Union[None, Node]:
        if current_node == self.NIL:
            return None
        elif target == current_node.value:
            return current_node
        elif target < current_node.value:
            return self._search(current_node.left, target)
        else:
            return self._search(current_node.right, target)

    def _min_node(self, current: Node) -> Node:
        if current.left != self.NIL:
            current = current.left

        return current

    def inprint(self):
        """
        inprint imprime os valores (value), de forma ordenada, contidos na àrvore;
        """
        if self.size == 0:
            print(EMPTY_MSG)
            return

        self._inprint(self.root)
        print(self.ordered)

        self.ordered = []

    def _inprint(self, target: Node):
        """
        _inprint ordenada os valores (value);
        - Utiliza de 'ordered' da propria àrvore para manter o resultado, enquanto a varre de forma "crescente";
        """
        if target != self.NIL and target.value != None:
            self._inprint(target.left)
            self.ordered.append(target)
            self._inprint(target.right)

rb2 = RedBlackTree()

list_to_insert = [1,2,3,4,5,6,7,8,9]
for value in list_to_insert:
    rb2.insert(value)

list_to_delete = [2]
for value in list_to_delete:
    rb2.remove(value)

rb2.inprint()

print()
print(rb2.search(9))

