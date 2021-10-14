from random import randint

class Individual:
    """
    Classe que representa o individuo.
    """
    def __init__(self, number_as_decimal):
        """
        Construtor da classe que representa o individuo.

        Args:
            number_as_decimal (int): Valor x no sistema decimal.
        """
        self.number_as_decimal = number_as_decimal
        self.number_as_binary = bin(self.number_as_decimal).replace('0b', '' if self.number_as_decimal < 0 else '+')
        self.fitness_function_result = -float('inf')

    def __repr__(self):
        """
        Sobrescrita do metodo de representacao da classe.

        Returns:
            str: String que representa o individuo como o valor no sistema
                decimal e o resultado da funcao fitness desse valor.
        """
        return f'{self.number_as_decimal} | {self.fitness_function_result}'

class Population:
    """
    Classe que representa a populacao.
    """
    def __init__(self, initial_number_of_individuals, min_x=None, max_x=None):
        """
        Construtor da classe que representa a populacao. Quando a classe
        representa a populacao inicial, todos os individuos sao criados
        aleatoriamente.
        
        Args:
            initial_number_of_individuals (int): Numero inicial de individuos da
                populacao. A populacao eh iniciada vazia quando uma nova
                populacao eh criada no metodo 'run' da classe 'Algorithm'.
            min_x (int): Valor minimo de x.
            max_x (int): Valor maximo de x.
        """
        self.individuals = [] if initial_number_of_individuals == 0 else [Individual(randint(min_x, max_x)) for _ in range(initial_number_of_individuals)]

class Algorithm:
    """
    Classe que representa o algoritmo.
    """
    def __init__(self, initial_number_of_individuals=4, number_of_generations=5, crossover_rate=0.7, mutation_rate=0.01, max_population_size=30):
        """
        Construtor da classe que representa o algoritmo.

        Args:
            initial_number_of_individuals (int): Numero inicial de individuos,
                por padrao o numero inicial eh 4.
            number_of_generations (int): Numero de geracoes, por padrao eh 5.
            crossover_rate (float): Taxa de crossover, por padrao eh 0.7.
            mutation_rate (float): Taxa de mutacao, por padrao eh 0.01.
            max_population_size (int): Tamanho maximo da populacao, por padrao
                eh 30.
        """
        self.initial_number_of_individuals = initial_number_of_individuals
        self.min_x = -10
        self.max_x = 10
        self.population = Population(self.initial_number_of_individuals, self.min_x, self.max_x)
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.number_of_generations = number_of_generations
        min_x_bit_number = len(self.convert_decimal_to_binary(self.min_x))
        max_x_bit_number = len(self.convert_decimal_to_binary(self.max_x))
        self.number_of_bits = min_x_bit_number if min_x_bit_number > max_x_bit_number else max_x_bit_number
        self.max_population_size = max_population_size
    
    def best_individual(self):
        """
        Metodo que retorna o melhor individuo da populacao. O melhor individuo
        eh o individuo com menor resultado da funcao fitness.

        Returns:
            Individual: Individuo com menor valor resultante da funcao fitness.
        """
        return min(self.population.individuals, key=lambda individual: individual.fitness_function_result)
    
    def convert_binary_to_decimal(self, number_as_binary):
        """
        Metodo que converte um valor no sistem binario para o sistema decimal.

        Args:
            number_as_binary (str): Valor no sistema binario.
        
        Returns:
            int: Valor no sistema decimal.
        """
        return int(''.join(number_as_binary), 2)

    def convert_decimal_to_binary(self, number_as_decimal):
        """
        Metodo que converte um valor no sistema decimal para o sistema binario.

        Args:
            number_as_decimal (int): Valor no sistema decimal.

        Returns:
            str: Valor no sistema binario.
        """
        return bin(number_as_decimal).replace('0b', '' if number_as_decimal < 0 else '+')

    def evaluate(self):
        """
        Metodo que avalia todos os individuos da populacao a partir da funcao
        fitness.

        f(x) = x^2 - 3 * x + 4
        """
        for individual in self.population.individuals:
            fitness_function_result = individual.number_as_decimal ** 2 - 3 * individual.number_as_decimal + 4

            individual.fitness_function_result = fitness_function_result
    
    def select(self):
        """
        Metodo que seleciona um individuo aleatoriamente na populacao.
        Inicialmente, dois individuos sao selecionados aleatoriamente e, depois,
        o individuo com menor valor resultante da funcao fitness.

        Returns:
            Individual: Individuo aleatorio.
        """
        index_1 = randint(0, len(self.population.individuals) - 1)

        index_2 = randint(0, len(self.population.individuals) - 1)

        individual_1 = self.population.individuals[index_1]

        individual_2 = self.population.individuals[index_2]

        return individual_1 if individual_1.fitness_function_result <= individual_2.fitness_function_result else individual_2
    
    def crossover(self, parent_1, parent_2):
        """
        Metodo que realiza o crossover entre dois individuos e retorna dois
        filhos desses individuos. O ponto de corte eh gerado aleatoriamente e os
        filhos sao criados com uma parte de cada individuo pai.

        Args:
            parent_1 (Individual): Individuo pai.
            parent_2 (Individual): Individuo pai.
        
        Returns:
            (Individual, Individual): Tupla com dois individuos filhos.
        """
        if randint(0, 1) <= self.crossover_rate:
            cut = randint(1, self.number_of_bits)

            individual_1_as_binary = parent_1.number_as_binary[:cut] + parent_2.number_as_binary[cut:]

            individual_2_as_binary = parent_2.number_as_binary[:cut] + parent_1.number_as_binary[cut:]

            individual_1 = Individual(self.convert_binary_to_decimal(individual_1_as_binary))

            individual_2 = Individual(self.convert_binary_to_decimal(individual_2_as_binary))

            self.adjust(individual_1)

            self.adjust(individual_2)
        else:
            individual_1 = Individual(parent_1.number_as_decimal)

            individual_2 = Individual(parent_2.number_as_decimal)

        return (individual_1, individual_2)

    def adjust(self, individual):
        """
        Metodo para ajustar o individuo. Caso o individuo fique fora do
        intervalo durante o crossover e a mutacao, o individuo eh ajustado
        pegando o valor minimo, se o valor do individuo estiver menor que o
        valor minimo, ou pegando o valor maximo, se o valor do individuo estiver
        maior do que o valor maximo.

        Args:
            individual (Individual): Individuo a ser ajustado.
        """
        need_to_adjust = False

        if individual.number_as_decimal < self.min_x:
            new_decimal = self.min_x

            new_binary = self.convert_decimal_to_binary(new_decimal)

            need_to_adjust = True
        elif individual.number_as_decimal > self.max_x:
            new_decimal = self.max_x

            new_binary = self.convert_decimal_to_binary(new_decimal)
        
            need_to_adjust = True

        if need_to_adjust:
            individual.number_as_decimal = new_decimal

            individual.number_as_binary = new_binary

    def mutation(self, individual):
        """
        Metodo que realiza a mutacao de um individuo a uma taxa pre-determinada.

        Args:
            individual (Individual): Individuo a sofre mutacao.

        Returns:
            Individual: Individuo com a mutacao (se ele sofreu mutacao) ou o
                proprio individuo (se ele nao sofreu mutacao).
        """
        if randint(0, 1) <= self.mutation_rate:
            bit = randint(0, self.number_of_bits - 1)

            new_binary = ''

            for i in range(len(individual.number_as_binary)):
                if bit == 0 and i == 0:
                    new_binary += '+' if individual.number_as_binary[bit] == '-' else '-'
                elif bit == i:
                    new_binary += '1' if individual.number_as_binary[bit] == '0' else '0'
                else:
                    new_binary += individual.number_as_binary[i]

            new_decimal = self.convert_binary_to_decimal(new_binary)

            new_individual = Individual(new_decimal)

            self.adjust(new_individual)

            return new_individual
        
        return individual
    
    def run(self):
        """
        Metodo que executa o algoritmo. Inicialmente, a populacao inicial e
        avaliada. Depois, cada nova populacao eh criada a partir do crossover e
        da mutacao dos individuos da populacao anterior e depois a nova
        populacao eh avaliada.
        """
        self.evaluate()

        for i in range(self.number_of_generations):
            print(f'Resultado da geracao {i}: {self.best_individual()}')

            new_population = Population(0)

            while len(new_population.individuals) < self.max_population_size:
                parent_1 = self.select()

                parent_2 = self.select()

                individual_1, individual_2 = self.crossover(parent_1, parent_2)

                if individual_1:
                    individual_1 = self.mutation(individual_1)

                    new_population.individuals.append(individual_1)

                if individual_2:
                    individual_2 = self.mutation(individual_2)

                    new_population.individuals.append(individual_2)
            
            self.population = new_population

            self.evaluate()

        print(f'Resultado da geracao {i + 1}: {self.best_individual()}')

def main():
    """
    Funcao que le a entrada do usuario e executa o algoritmo.
    """
    option = input('Deseja customizar os dados? [S/N] ')

    if option == 'S':
        initial_number_of_individuals = int(input('Qual numero inicial de individuos? [Entre com um numero inteiro] '))

        number_of_generations = int(input('Qual numero de geracoes? [Entre com um numero inteiro] '))
        
        crossover_rate = float(input('Qual taxa de crossover? [Entre com um numero entre 0 e 1] '))
        
        mutation_rate = float(input('Qual taxa de mutacao? [Entre com um numero entre 0 e 1] '))
        
        max_population_size = int(input('Qual tamanho maximo da populacao? [Entre com um numero inteiro] '))

        algorithm = Algorithm(initial_number_of_individuals, number_of_generations, crossover_rate, mutation_rate, max_population_size)
    else:
        algorithm = Algorithm()

    algorithm.run()

if __name__ == '__main__':
    main()