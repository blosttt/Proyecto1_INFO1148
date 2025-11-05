# gramatica.py
class GramaticaAritmetica:
    def __init__(self):
        # Gramática original con recursión izquierda
        self.gramatica_original = {
            'E': [['E', '+', 'T'], ['E', '-', 'T'], ['T']],
            'T': [['T', '*', 'F'], ['T', '/', 'F'], ['T', '%', 'F'], ['F']],
            'F': [['(', 'E', ')'], ['id'], ['num']]
        }
        
        # Gramática sin recursión izquierda
        self.gramatica_sin_recursion = {
            'E': [['T', "E'"]],
            "E'": [['+', 'T', "E'"], ['-', 'T', "E'"], ['ε']],
            'T': [['F', "T'"]],
            "T'": [['*', 'F', "T'"], ['/', 'F', "T'"], ['%', 'F', "T'"], ['ε']],
            'F': [['(', 'E', ')'], ['id'], ['num']]
        }
    
    def calcular_first(self):
        first = {
            'E': set(), "E'": set(), 
            'T': set(), "T'": set(), 
            'F': set()
        }
        
        # Símbolos terminales
        terminales = {'+', '-', '*', '/', '%', '(', ')', 'id', 'num', 'ε'}
        
        # Calcular First iterativamente
        cambio = True
        while cambio:
            cambio = False
            for no_terminal, producciones in self.gramatica_sin_recursion.items():
                for produccion in producciones:
                    primer_simbolo = produccion[0]
                    
                    if primer_simbolo in terminales:
                        if primer_simbolo not in first[no_terminal]:
                            first[no_terminal].add(primer_simbolo)
                            cambio = True
                    else:
                        # Es un no terminal, agregar su First
                        for simbolo in first[primer_simbolo]:
                            if simbolo != 'ε' and simbolo not in first[no_terminal]:
                                first[no_terminal].add(simbolo)
                                cambio = True
        
        return first
    
    def calcular_follow(self, first):
        follow = {
            'E': set(), "E'": set(),
            'T': set(), "T'": set(), 
            'F': set()
        }
        
        # FOLLOW(E) contiene $
        follow['E'].add('$')
        
        cambio = True
        while cambio:
            cambio = False
            for no_terminal, producciones in self.gramatica_sin_recursion.items():
                for produccion in producciones:
                    for i, simbolo in enumerate(produccion):
                        if simbolo in self.gramatica_sin_recursion.keys():  # Es no terminal
                            # Regla 1: A → αBβ
                            if i + 1 < len(produccion):
                                next_simbolo = produccion[i + 1]
                                if next_simbolo in first:  # Es no terminal
                                    # Agregar FIRST(β) - ε a FOLLOW(B)
                                    for first_sim in first[next_simbolo]:
                                        if first_sim != 'ε' and first_sim not in follow[simbolo]:
                                            follow[simbolo].add(first_sim)
                                            cambio = True
                                else:  # Es terminal
                                    if next_simbolo not in follow[simbolo]:
                                        follow[simbolo].add(next_simbolo)
                                        cambio = True
                            
                            # Regla 2: A → αB o A → αBβ donde ε ∈ FIRST(β)
                            if i + 1 >= len(produccion) or 'ε' in first.get(produccion[i + 1], set()):
                                # Agregar FOLLOW(A) a FOLLOW(B)
                                for follow_sim in follow[no_terminal]:
                                    if follow_sim not in follow[simbolo]:
                                        follow[simbolo].add(follow_sim)
                                        cambio = True
        
        return follow
    
    def generar_tabla_sintactica(self, first, follow):
        tabla = {}
        terminales = ['+', '-', '*', '/', '%', '(', ')', 'id', 'num', '$']
        no_terminales = ['E', "E'", 'T', "T'", 'F']
        
        # Inicializar tabla
        for nt in no_terminales:
            tabla[nt] = {}
            for t in terminales:
                tabla[nt][t] = None
        
        # Llenar tabla
        for no_terminal, producciones in self.gramatica_sin_recursion.items():
            for produccion in producciones:
                first_produccion = self.calcular_first_produccion(produccion, first)
                
                for terminal in first_produccion:
                    if terminal != 'ε':
                        if tabla[no_terminal][terminal] is None:
                            tabla[no_terminal][terminal] = produccion
                        else:
                            print(f"Conflicto en tabla[{no_terminal}][{terminal}]")
                
                if 'ε' in first_produccion:
                    for terminal in follow[no_terminal]:
                        if tabla[no_terminal][terminal] is None:
                            tabla[no_terminal][terminal] = produccion
                        else:
                            print(f"Conflicto en tabla[{no_terminal}][{terminal}]")
        
        return tabla
    
    def calcular_first_produccion(self, produccion, first):
        result = set()
        
        for simbolo in produccion:
            if simbolo in first:  # Es no terminal
                result.update(first[simbolo] - {'ε'})
                if 'ε' not in first[simbolo]:
                    break
            else:  # Es terminal
                result.add(simbolo)
                break
        else:
            # Todos los símbolos pueden ser ε
            result.add('ε')
        
        return result