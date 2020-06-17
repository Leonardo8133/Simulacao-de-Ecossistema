import random
import numpy as np

# Classe Network
class Network(object):

    def __init__(self, sizes):
        """A lista `sizes` contém o número de neurônios nas
         respectivas camadas da rede. Por exemplo, se a lista
         for [2, 3, 1] então será uma rede de três camadas, com o
         primeira camada contendo 2 neurônios, a segunda camada 3 neurônios,
         e a terceira camada 1 neurônio. Os bias e pesos para a
         rede são inicializados aleatoriamente, usando uma distribuição Gaussiana com média 0 e variância 1. 
         Note que a primeira camada é assumida como uma camada de entrada, e por convenção nós
         não definimos nenhum bias para esses neurônios, pois os bias são usados
         na computação das saídas das camadas posteriores."""

        self.num_layers = len(sizes)
        self.sizes = sizes
        self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
        self.weights = [np.random.randn(y, x) for x, y in zip(sizes[:-1], sizes[1:])]

    def feedforward(self, a):
        """Retorna a saída da rede se `a` for input."""
        for b, w in zip(self.biases, self.weights):
            a = sigmoid(np.dot(w, a)+b)
        return a

    def SGD(self, training_data, epochs, mini_batch_size, eta, test_data=None):
        """Treinar a rede neural usando mini-batch stochastic
        gradient descent. O `training_data` é uma lista de tuplas
         `(x, y)` representando as entradas de treinamento e as
         saídas. Os outros parâmetros não opcionais são
         auto-explicativos. Se `test_data` for fornecido, então a
         rede será avaliada em relação aos dados do teste após cada
         época e progresso parcial impresso. Isso é útil para
         acompanhar o progresso, mas retarda as coisas substancialmente."""

        training_data = list(training_data)
        n = len(training_data)

        if test_data:
            test_data = list(test_data)
            n_test = len(test_data)

        for j in range(epochs):
            random.shuffle(training_data)
            mini_batches = [training_data[k:k+mini_batch_size] for k in range(0, n, mini_batch_size)]
            
            for mini_batch in mini_batches:
                self.update_mini_batch(mini_batch, eta)
            
            if test_data:
                print("Epoch {} : {} / {}".format(j,self.evaluate(test_data),n_test));
            else:
                print("Epoch {} finalizada".format(j))

    def update_mini_batch(self, mini_batch, eta):
        """Atualiza os pesos e bias da rede aplicando
         a descida do gradiente usando backpropagation para um único mini lote.
         O `mini_batch` é uma lista de tuplas `(x, y)`, e `eta` é a taxa de aprendizado."""

        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        
        for x, y in mini_batch:
            delta_nabla_b, delta_nabla_w = self.backprop(x, y)
            nabla_b = [nb+dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw+dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
        
        self.weights = [w-(eta/len(mini_batch))*nw for w, nw in zip(self.weights, nabla_w)]
        self.biases = [b-(eta/len(mini_batch))*nb for b, nb in zip(self.biases, nabla_b)]

    def backprop(self, x, y):
        """Retorna uma tupla `(nabla_b, nabla_w)` representando o
         gradiente para a função de custo C_x. `nabla_b` e
         `nabla_w` são listas de camadas de matrizes numpy, semelhantes
         a `self.biases` e `self.weights`."""

        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        
        # Feedforward
        activation = x

        # Lista para armazenar todas as ativações, camada por camada
        activations = [x] 

        # Lista para armazenar todos os vetores z, camada por camada
        zs = [] 

        for b, w in zip(self.biases, self.weights):
            z = np.dot(w, activation)+b
            zs.append(z)
            activation = sigmoid(z)
            activations.append(activation)
        
        # Backward pass
        delta = self.cost_derivative(activations[-1], y) * sigmoid_prime(zs[-1])
        nabla_b[-1] = delta
        nabla_w[-1] = np.dot(delta, activations[-2].transpose())
        
        # Aqui, l = 1 significa a última camada de neurônios, l = 2 é a
        # segunda e assim por diante. 
        for l in range(2, self.num_layers):
            z = zs[-l]
            sp = sigmoid_prime(z)
            delta = np.dot(self.weights[-l+1].transpose(), delta) * sp
            nabla_b[-l] = delta
            nabla_w[-l] = np.dot(delta, activations[-l-1].transpose())
        return (nabla_b, nabla_w)

    def evaluate(self, test_data):
        """Retorna o número de entradas de teste para as quais a rede neural 
         produz o resultado correto. Note que a saída da rede neural
         é considerada o índice de qualquer que seja
         neurônio na camada final que tenha a maior ativação."""

        test_results = [(np.argmax(self.feedforward(x)), y) for (x, y) in test_data]
        return sum(int(x == y) for (x, y) in test_results)

    def cost_derivative(self, output_activations, y):
        """Retorna o vetor das derivadas parciais."""
        return (output_activations-y)

# Função de Ativação Sigmóide
def sigmoid(z):
    return 1.0/(1.0+np.exp(-z))

# Função para retornar as derivadas da função Sigmóide
def sigmoid_prime(z):
    return sigmoid(z)*(1-sigmoid(z))