# lexer.py
import re

class AnalizadorLexico:
    def __init__(self):
        self.tokens = []
        self.errores = []
        
        # Patrones para tokens
        self.patrones = [
            ('NUM', r'\b\d+(\.\d+)?\b'),        # Números
            ('ID', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'), # Identificadores
            ('OP', r'[+\-*/%]'),                # Operadores
            ('PAREN', r'[()]'),                 # Paréntesis
            ('ASIGN', r'='),                    # Asignación
            ('PUNTOCOMA', r';'),                # Punto y coma
            ('WS', r'\s+'),                     # Espacios en blanco
        ]
    
    def analizar(self, codigo):
        self.tokens = []
        self.errores = []
        linea = 1
        pos = 0
        
        while pos < len(codigo):
            match = None
            
            for token_type, pattern in self.patrones:
                regex = re.compile(pattern)
                match = regex.match(codigo, pos)
                
                if match:
                    valor = match.group(0)
                    
                    if token_type != 'WS':  # Ignorar espacios
                        self.tokens.append({
                            'tipo': token_type,
                            'valor': valor,
                            'linea': linea,
                            'posicion': pos
                        })
                    
                    # Actualizar posición y línea
                    pos = match.end()
                    
                    # Contar saltos de línea
                    if '\n' in valor:
                        linea += valor.count('\n')
                    
                    break
            
            if not match:
                # Carácter no reconocido
                self.errores.append({
                    'caracter': codigo[pos],
                    'linea': linea,
                    'posicion': pos
                })
                pos += 1
        
        # Agregar token de fin de archivo
        self.tokens.append({'tipo': 'EOF', 'valor': '$', 'linea': linea, 'posicion': pos})
        
        return self.tokens, self.errores
    
    def imprimir_tokens(self):
        print("\n=== TOKENS IDENTIFICADOS ===")
        for token in self.tokens:
            if token['tipo'] != 'EOF':
                print(f"Línea {token['linea']}: {token['tipo']} -> '{token['valor']}'")
    
    def imprimir_errores(self):
        if self.errores:
            print("\n=== ERRORES LÉXICOS ===")
            for error in self.errores:
                print(f"Línea {error['linea']}, Posición {error['posicion']}: Carácter no válido '{error['caracter']}'")