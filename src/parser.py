# parser.py
from gramatica import GramaticaAritmetica

class AnalizadorSintactico:
    def __init__(self):
        self.gramatica = GramaticaAritmetica()
        self.first = self.gramatica.calcular_first()
        self.follow = self.gramatica.calcular_follow(self.first)
        self.tabla = self.gramatica.generar_tabla_sintactica(self.first, self.follow)
        self.pila = []
        self.entrada = []
        self.errores_sintacticos = []
    
    def analizar(self, tokens):
        self.errores_sintacticos = []
        
        # Convertir tokens a formato de entrada
        self.entrada = []
        for token in tokens:
            if token['tipo'] == 'NUM':
                self.entrada.append('num')
            elif token['tipo'] == 'ID':
                self.entrada.append('id')
            elif token['tipo'] in ['OP', 'PAREN']:
                self.entrada.append(token['valor'])
            elif token['tipo'] == 'EOF':
                self.entrada.append('$')
        
        # Inicializar pila
        self.pila = ['$', 'E']
        
        print("\n=== ANÁLISIS SINTÁCTICO ===")
        print(f"Pila: {self.pila}")
        print(f"Entrada: {self.entrada}")
        
        paso = 1
        while len(self.pila) > 0 and len(self.entrada) > 0:
            print(f"\n--- Paso {paso} ---")
            print(f"Pila: {self.pila}")
            print(f"Entrada: {self.entrada}")
            
            tope_pila = self.pila[-1]
            actual_entrada = self.entrada[0]
            
            if tope_pila == actual_entrada:
                # Coincidencia
                print(f"Coincidencia: '{tope_pila}'")
                self.pila.pop()
                self.entrada.pop(0)
            elif tope_pila in self.tabla:
                # Es un no terminal
                produccion = self.tabla[tope_pila].get(actual_entrada)
                
                if produccion is not None:
                    print(f"Aplicando: {tope_pila} -> {' '.join(produccion)}")
                    self.pila.pop()
                    
                    # Agregar producción en orden inverso (excepto ε)
                    if produccion != ['ε']:
                        for simbolo in reversed(produccion):
                            if simbolo != 'ε':
                                self.pila.append(simbolo)
                else:
                    error_msg = f"Error sintáctico: No hay producción para {tope_pila} con entrada '{actual_entrada}'"
                    self.errores_sintacticos.append(error_msg)
                    print(f"❌ {error_msg}")
                    return False
            else:
                error_msg = f"Error sintáctico: Se esperaba '{tope_pila}' pero se encontró '{actual_entrada}'"
                self.errores_sintacticos.append(error_msg)
                print(f"❌ {error_msg}")
                return False
            
            paso += 1
        
        if len(self.pila) == 0 and len(self.entrada) == 0:
            print("\n✅ Análisis sintáctico COMPLETADO EXITOSAMENTE")
            return True
        else:
            error_msg = "Error: Análisis incompleto"
            self.errores_sintacticos.append(error_msg)
            print(f"❌ {error_msg}")
            return False
    
    def imprimir_tabla_sintactica(self):
        print("\n=== TABLA SINTÁCTICA ===")
        terminales = ['+', '-', '*', '/', '%', '(', ')', 'id', 'num', '$']
        
        # Encabezado
        print(f"{'NT':<4} | {' | '.join(f'{t:>8}' for t in terminales)}")
        print('-' * 90)
        
        for nt in ['E', "E'", 'T', "T'", 'F']:
            fila = f"{nt:<4} | "
            for t in terminales:
                produccion = self.tabla[nt].get(t)
                if produccion:
                    prod_str = f"{nt}→{''.join(produccion)}"
                    fila += f"{prod_str:>8} | "
                else:
                    fila += f"{'':>8} | "
            print(fila)