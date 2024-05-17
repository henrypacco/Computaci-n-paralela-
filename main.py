
import multiprocessing
import numpy as np
import time

def worker(start_index, end_index, a, b, c):
    for i in range(start_index, end_index):
        c[i] = a[i] + b[i]

if __name__ == "__main__":
    size = 10**6  # Tamaño de los arrays
    a = np.random.randint(0, 200, size)
    b = np.random.randint(0, 200, size)
    c = multiprocessing.Array('i', size)  # Shared array

    # Suma ordinaria
    start_time = time.time()
    c_ordinary = a + b
    ordinary_time = time.time() - start_time

    # Suma paralela
    processes = []
    chunk_size = size // multiprocessing.cpu_count()

    start_time = time.time()
    for i in range(multiprocessing.cpu_count()):
        start_index = i * chunk_size
        end_index = size if i == multiprocessing.cpu_count() - 1 else (i + 1) * chunk_size
        process = multiprocessing.Process(target=worker, args=(start_index, end_index, a, b, c))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
    parallel_time = time.time() - start_time

    # Imprimir tiempos
    print(f"Tiempo de suma ordinaria: {ordinary_time:.4f} segundos")
    print(f"Tiempo de suma paralela: {parallel_time:.4f} segundos")

    # Verificación de resultados (opcional)
    if np.array_equal(c_ordinary, c[:]):
        print("La suma paralela es correcta")
    else:
        print("La suma paralela es incorrecta")

   

