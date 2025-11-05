// Operaciones.java
public class Operaciones {
    public static void main(String[] args) {
        // Operaciones aritméticas básicas
        int a = 15;
        int b = 4;
        int c = 2;
        
        // Suma y resta
        int suma = a + b;
        int resta = a - b;
        
        // Multiplicación y división
        int multiplicacion = a * b;
        double division = a / b;
        
        // Módulo
        int modulo = a % b;
        
        // Expresiones complejas
        int expresion1 = (a + b) * c - a % c;
        double expresion2 = (a * b) / (c + 1) % 3;
        
        // Con variables diferentes
        int x = 10, y = 3, z = 7;
        int resultado = (x + y) * (z - x) / y % 2;
    }
}