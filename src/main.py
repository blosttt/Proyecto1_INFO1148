# main.py
from lexer import AnalizadorLexico
from parser import AnalizadorSintactico
from gramatica import GramaticaAritmetica
import os

def main():
    print("=" * 60)
    print("    ANALIZADOR DE OPERACIONES ARITMÉTICAS EN JAVA")
    print("    INFO1148 - Teoría de la Computación")
    print("=" * 60)
    
    # Ejemplo de código Java con operaciones aritméticas
    codigo_ejemplo = """
    public class Calculadora {
        public static void main(String[] args) {
            int a = 10;
            int b = 5;
            int resultado = (a + b) * 2 - 3 % 2;
            double division = a / b;
            int modulo = a % b;
        }
    }
    """
    
    # Mostrar gramáticas
    gramatica = GramaticaAritmetica()
    
    print("\n1. GRAMÁTICA ORIGINAL:")
    for nt, prods in gramatica.gramatica_original.items():
        print(f"   {nt} → {' | '.join([' '.join(p) for p in prods])}")
    
    print("\n2. GRAMÁTICA SIN RECURSIÓN IZQUIERDA:")
    for nt, prods in gramatica.gramatica_sin_recursion.items():
        print(f"   {nt} → {' | '.join([' '.join(p) for p in prods])}")
    
    # Calcular conjuntos First y Follow
    first = gramatica.calcular_first()
    follow = gramatica.calcular_follow(first)
    
    print("\n3. CONJUNTOS FIRST:")
    for nt, conj in first.items():
        print(f"   FIRST({nt}) = {conj}")
    
    print("\n4. CONJUNTOS FOLLOW:")
    for nt, conj in follow.items():
        print(f"   FOLLOW({nt}) = {conj}")
    
    # Análisis léxico
    print("\n" + "=" * 60)
    print("ANÁLISIS LÉXICO")
    print("=" * 60)
    
    lexer = AnalizadorLexico()
    tokens, errores_lexicos = lexer.analizar(codigo_ejemplo)
    
    lexer.imprimir_tokens()
    if errores_lexicos:
        lexer.imprimir_errores()
    else:
        print("✅ No se encontraron errores léxicos")
    
    # Análisis sintáctico
    print("\n" + "=" * 60)
    print("ANÁLISIS SINTÁCTICO")
    print("=" * 60)
    
    parser = AnalizadorSintactico()
    parser.imprimir_tabla_sintactica()
    
    resultado_sintactico = parser.analizar(tokens)
    
    if resultado_sintactico:
        print("\n✅ El código Java tiene una estructura sintáctica VÁLIDA")
    else:
        print("\n❌ El código Java tiene errores sintácticos:")
        for error in parser.errores_sintacticos:
            print(f"   - {error}")
    
    # Guardar resultados en archivos
    guardar_resultados(gramatica, first, follow, parser.tabla, tokens, errores_lexicos, parser.errores_sintacticos)

def guardar_resultados(gramatica, first, follow, tabla, tokens, errores_lexicos, errores_sintacticos):
    """Guardar todos los resultados en archivos"""
    
    # Gramáticas
    with open('gramatica_original.txt', 'w', encoding='utf-8') as f:
        f.write("GRAMÁTICA ORIGINAL\n")
        f.write("==================\n")
        for nt, prods in gramatica.gramatica_original.items():
            f.write(f"{nt} → {' | '.join([' '.join(p) for p in prods])}\n")
    
    with open('gramatica_sin_recursion.txt', 'w', encoding='utf-8') as f:
        f.write("GRAMÁTICA SIN RECURSIÓN IZQUIERDA\n")
        f.write("=================================\n")
        for nt, prods in gramatica.gramatica_sin_recursion.items():
            f.write(f"{nt} → {' | '.join([' '.join(p) for p in prods])}\n")
    
    # Conjuntos First y Follow
    with open('conjuntos_first_follow.txt', 'w', encoding='utf-8') as f:
        f.write("CONJUNTOS FIRST\n")
        f.write("===============\n")
        for nt, conj in first.items():
            f.write(f"FIRST({nt}) = {conj}\n")
        
        f.write("\nCONJUNTOS FOLLOW\n")
        f.write("================\n")
        for nt, conj in follow.items():
            f.write(f"FOLLOW({nt}) = {conj}\n")
    
    # Tabla sintáctica
    with open('tabla_sintactica.txt', 'w', encoding='utf-8') as f:
        f.write("TABLA SINTÁCTICA\n")
        f.write("================\n")
        terminales = ['+', '-', '*', '/', '%', '(', ')', 'id', 'num', '$']
        
        f.write(f"{'NT':<4} | {' | '.join(f'{t:>8}' for t in terminales)}\n")
        f.write('-' * 90 + '\n')
        
        for nt in ['E', "E'", 'T', "T'", 'F']:
            fila = f"{nt:<4} | "
            for t in terminales:
                produccion = tabla[nt].get(t)
                if produccion:
                    prod_str = f"{nt}→{''.join(produccion)}"
                    fila += f"{prod_str:>8} | "
                else:
                    fila += f"{'':>8} | "
            f.write(fila + '\n')
    
    # Tokens y errores
    with open('analisis_lexico.txt', 'w', encoding='utf-8') as f:
        f.write("ANÁLISIS LÉXICO\n")
        f.write("===============\n")
        f.write("TOKENS IDENTIFICADOS:\n")
        for token in tokens:
            if token['tipo'] != 'EOF':
                f.write(f"Línea {token['linea']}: {token['tipo']} -> '{token['valor']}'\n")
        
        if errores_lexicos:
            f.write("\nERRORES LÉXICOS:\n")
            for error in errores_lexicos:
                f.write(f"Línea {error['linea']}, Posición {error['posicion']}: Carácter no válido '{error['caracter']}'\n")
        else:
            f.write("\n✅ No se encontraron errores léxicos\n")
    
    print("\n📁 Archivos generados:")
    print("   - gramatica_original.txt")
    print("   - gramatica_sin_recursion.txt")
    print("   - conjuntos_first_follow.txt")
    print("   - tabla_sintactica.txt")
    print("   - analisis_lexico.txt")

if __name__ == "__main__":
    main()