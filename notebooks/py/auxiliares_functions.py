import re

def amount(text):
    # Elimina caracteres no numéricos y divide en palabras
    words = str(text).split()
    
    # Filtra y limpia las palabras, convirtiéndolas en enteros
    numbers = [int(re.sub(r'\D', '', word)) for word in words if re.sub(r'\D', '', word).strip()]
    
    # Calcula la suma de los números
    total_sum = sum(numbers)
    
    # Obtiene el primer valor de la lista, o 0 si la lista está vacía
    first_value = numbers[0] if numbers else 0
    
    # Encuentra el primer valor diferente a 0
    first_non_zero = next((num for num in numbers if num != 0), 0)

    # Número de amounts
    len_number = len(numbers)
    
    # Retorna la suma, el primer valor y el primer valor diferente a 0
    return total_sum, first_value, first_non_zero, len_number
