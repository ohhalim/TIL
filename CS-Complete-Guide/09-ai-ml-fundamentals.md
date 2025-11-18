# 09. AI/ML 기초 (AI/ML Fundamentals)

## 목차
1. [머신러닝 기초](#머신러닝-기초)
2. [신경망과 딥러닝](#신경망과-딥러닝)
3. [최적화 알고리즘](#최적화-알고리즘)
4. [컴퓨터 비전](#컴퓨터-비전)
5. [자연어 처리](#자연어-처리)
6. [강화학습](#강화학습)
7. [Transformer 아키텍처](#transformer-아키텍처)
8. [대규모 언어 모델](#대규모-언어-모델)

---

## 머신러닝 기초

### 1. 선형 회귀 (Linear Regression)

**수학적 정의:**

```
예측: ŷ = w₁x₁ + w₂x₂ + ... + wₙxₙ + b
     = wᵀx + b

손실 함수 (MSE): L(w, b) = (1/m) Σ(ŷᵢ - yᵢ)²

목표: argmin L(w, b)
      w,b
```

**완전 구현:**

```python
import numpy as np

class LinearRegression:
    def __init__(self, learning_rate=0.01, iterations=1000):
        self.lr = learning_rate
        self.iterations = iterations
        self.weights = None
        self.bias = None
        self.loss_history = []

    def fit(self, X, y):
        """
        경사 하강법으로 학습
        X: (m, n) - m개 샘플, n개 특성
        y: (m,) - m개 레이블
        """
        m, n = X.shape
        self.weights = np.zeros(n)
        self.bias = 0

        for i in range(self.iterations):
            # Forward pass
            y_pred = self.predict(X)

            # Loss 계산
            loss = np.mean((y_pred - y) ** 2)
            self.loss_history.append(loss)

            # Gradient 계산
            dw = (2/m) * X.T.dot(y_pred - y)
            db = (2/m) * np.sum(y_pred - y)

            # Weights 업데이트
            self.weights -= self.lr * dw
            self.bias -= self.lr * db

    def predict(self, X):
        return X.dot(self.weights) + self.bias

# Closed-form solution (Normal Equation)
class LinearRegressionClosed:
    """
    해석적 해: w = (XᵀX)⁻¹Xᵀy
    - 미분 = 0으로 직접 계산
    - 작은 데이터셋에 적합
    - O(n³) 복잡도 (역행렬)
    """

    def fit(self, X, y):
        # Bias term 추가
        X_b = np.c_[np.ones((X.shape[0], 1)), X]

        # Normal equation
        self.theta = np.linalg.inv(X_b.T.dot(X_b)).dot(X_b.T).dot(y)

    def predict(self, X):
        X_b = np.c_[np.ones((X.shape[0], 1)), X]
        return X_b.dot(self.theta)

# Ridge Regression (L2 Regularization)
class RidgeRegression:
    """
    L2 정규화: L(w) = MSE + α||w||²
    - Overfitting 방지
    - 큰 가중치에 페널티
    """

    def __init__(self, alpha=1.0):
        self.alpha = alpha

    def fit(self, X, y):
        X_b = np.c_[np.ones((X.shape[0], 1)), X]
        n = X_b.shape[1]

        # Ridge solution: w = (XᵀX + αI)⁻¹Xᵀy
        identity = np.eye(n)
        identity[0, 0] = 0  # Bias는 정규화 안 함

        self.theta = np.linalg.inv(
            X_b.T.dot(X_b) + self.alpha * identity
        ).dot(X_b.T).dot(y)

    def predict(self, X):
        X_b = np.c_[np.ones((X.shape[0], 1)), X]
        return X_b.dot(self.theta)

# Lasso Regression (L1 Regularization)
from scipy.optimize import minimize

class LassoRegression:
    """
    L1 정규화: L(w) = MSE + α||w||₁
    - Feature selection (일부 가중치가 정확히 0)
    - Sparse model
    """

    def __init__(self, alpha=1.0):
        self.alpha = alpha

    def fit(self, X, y):
        m, n = X.shape

        def loss(theta):
            w = theta[:-1]
            b = theta[-1]
            pred = X.dot(w) + b
            mse = np.mean((pred - y) ** 2)
            l1 = self.alpha * np.sum(np.abs(w))
            return mse + l1

        # 최적화
        theta_init = np.zeros(n + 1)
        result = minimize(loss, theta_init, method='L-BFGS-B')

        self.weights = result.x[:-1]
        self.bias = result.x[-1]

    def predict(self, X):
        return X.dot(self.weights) + self.bias
```

### 2. 로지스틱 회귀 (Logistic Regression)

```python
class LogisticRegression:
    """
    이진 분류
    예측: ŷ = σ(wᵀx + b)
    σ(z) = 1 / (1 + e⁻ᶻ)  (sigmoid)

    Loss (Binary Cross-Entropy):
    L = -(1/m) Σ [y log(ŷ) + (1-y) log(1-ŷ)]
    """

    def __init__(self, learning_rate=0.01, iterations=1000):
        self.lr = learning_rate
        self.iterations = iterations

    @staticmethod
    def sigmoid(z):
        return 1 / (1 + np.exp(-z))

    def fit(self, X, y):
        m, n = X.shape
        self.weights = np.zeros(n)
        self.bias = 0

        for i in range(self.iterations):
            # Forward
            z = X.dot(self.weights) + self.bias
            y_pred = self.sigmoid(z)

            # Loss
            loss = -np.mean(y * np.log(y_pred + 1e-15) +
                           (1 - y) * np.log(1 - y_pred + 1e-15))

            # Gradient
            dw = (1/m) * X.T.dot(y_pred - y)
            db = (1/m) * np.sum(y_pred - y)

            # Update
            self.weights -= self.lr * dw
            self.bias -= self.lr * db

    def predict_proba(self, X):
        z = X.dot(self.weights) + self.bias
        return self.sigmoid(z)

    def predict(self, X, threshold=0.5):
        return (self.predict_proba(X) >= threshold).astype(int)

# Softmax Regression (Multi-class)
class SoftmaxRegression:
    """
    다중 클래스 분류
    softmax(z)ᵢ = e^zᵢ / Σⱼ e^zⱼ

    Loss (Categorical Cross-Entropy):
    L = -(1/m) ΣΣ yᵢⱼ log(ŷᵢⱼ)
    """

    def __init__(self, learning_rate=0.01, iterations=1000):
        self.lr = learning_rate
        self.iterations = iterations

    @staticmethod
    def softmax(Z):
        exp_Z = np.exp(Z - np.max(Z, axis=1, keepdims=True))
        return exp_Z / np.sum(exp_Z, axis=1, keepdims=True)

    def fit(self, X, y):
        m, n = X.shape
        k = len(np.unique(y))  # 클래스 수

        # One-hot encoding
        Y = np.zeros((m, k))
        Y[np.arange(m), y] = 1

        # Weights: (n, k)
        self.W = np.zeros((n, k))
        self.b = np.zeros(k)

        for i in range(self.iterations):
            # Forward
            Z = X.dot(self.W) + self.b
            Y_pred = self.softmax(Z)

            # Loss
            loss = -np.mean(np.sum(Y * np.log(Y_pred + 1e-15), axis=1))

            # Gradient
            dW = (1/m) * X.T.dot(Y_pred - Y)
            db = (1/m) * np.sum(Y_pred - Y, axis=0)

            # Update
            self.W -= self.lr * dW
            self.b -= self.lr * db

    def predict_proba(self, X):
        Z = X.dot(self.W) + self.b
        return self.softmax(Z)

    def predict(self, X):
        proba = self.predict_proba(X)
        return np.argmax(proba, axis=1)
```

### 3. 결정 트리 (Decision Tree)

```python
class DecisionTree:
    """
    CART (Classification and Regression Trees)
    - Gini Impurity 또는 Entropy 사용
    - Greedy 알고리즘
    """

    def __init__(self, max_depth=10, min_samples_split=2):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.tree = None

    def gini_impurity(self, y):
        """
        Gini = 1 - Σ pᵢ²
        pᵢ = 클래스 i의 비율
        """
        _, counts = np.unique(y, return_counts=True)
        probabilities = counts / len(y)
        return 1 - np.sum(probabilities ** 2)

    def entropy(self, y):
        """
        Entropy = -Σ pᵢ log₂(pᵢ)
        """
        _, counts = np.unique(y, return_counts=True)
        probabilities = counts / len(y)
        return -np.sum(probabilities * np.log2(probabilities + 1e-15))

    def information_gain(self, X_column, y, threshold):
        """
        IG = Entropy(parent) - weighted_avg(Entropy(children))
        """
        parent_entropy = self.entropy(y)

        # Split
        left_mask = X_column <= threshold
        right_mask = ~left_mask

        if np.sum(left_mask) == 0 or np.sum(right_mask) == 0:
            return 0

        n = len(y)
        n_left, n_right = np.sum(left_mask), np.sum(right_mask)

        e_left = self.entropy(y[left_mask])
        e_right = self.entropy(y[right_mask])

        child_entropy = (n_left / n) * e_left + (n_right / n) * e_right

        return parent_entropy - child_entropy

    def best_split(self, X, y):
        """최적 분할 찾기"""
        best_gain = -1
        best_feature = None
        best_threshold = None

        for feature_idx in range(X.shape[1]):
            thresholds = np.unique(X[:, feature_idx])

            for threshold in thresholds:
                gain = self.information_gain(X[:, feature_idx], y, threshold)

                if gain > best_gain:
                    best_gain = gain
                    best_feature = feature_idx
                    best_threshold = threshold

        return best_feature, best_threshold

    def build_tree(self, X, y, depth=0):
        """재귀적으로 트리 구축"""
        n_samples = len(y)
        n_classes = len(np.unique(y))

        # 종료 조건
        if (depth >= self.max_depth or
            n_classes == 1 or
            n_samples < self.min_samples_split):
            # Leaf node
            leaf_value = np.bincount(y).argmax()
            return {'leaf': True, 'value': leaf_value}

        # 최적 분할
        feature, threshold = self.best_split(X, y)

        if feature is None:
            leaf_value = np.bincount(y).argmax()
            return {'leaf': True, 'value': leaf_value}

        # 분할
        left_mask = X[:, feature] <= threshold
        right_mask = ~left_mask

        # 재귀
        left_subtree = self.build_tree(X[left_mask], y[left_mask], depth + 1)
        right_subtree = self.build_tree(X[right_mask], y[right_mask], depth + 1)

        return {
            'leaf': False,
            'feature': feature,
            'threshold': threshold,
            'left': left_subtree,
            'right': right_subtree
        }

    def fit(self, X, y):
        self.tree = self.build_tree(X, y)

    def predict_sample(self, x, tree):
        """단일 샘플 예측"""
        if tree['leaf']:
            return tree['value']

        if x[tree['feature']] <= tree['threshold']:
            return self.predict_sample(x, tree['left'])
        else:
            return self.predict_sample(x, tree['right'])

    def predict(self, X):
        return np.array([self.predict_sample(x, self.tree) for x in X])

# Random Forest
class RandomForest:
    """
    앙상블: 여러 결정 트리의 투표
    - Bootstrap Aggregating (Bagging)
    - Feature randomness
    """

    def __init__(self, n_trees=100, max_depth=10, min_samples_split=2):
        self.n_trees = n_trees
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.trees = []

    def bootstrap_sample(self, X, y):
        """Bootstrap 샘플링 (복원 추출)"""
        m = X.shape[0]
        indices = np.random.choice(m, m, replace=True)
        return X[indices], y[indices]

    def fit(self, X, y):
        self.trees = []

        for _ in range(self.n_trees):
            # Bootstrap
            X_sample, y_sample = self.bootstrap_sample(X, y)

            # 트리 학습
            tree = DecisionTree(
                max_depth=self.max_depth,
                min_samples_split=self.min_samples_split
            )
            tree.fit(X_sample, y_sample)
            self.trees.append(tree)

    def predict(self, X):
        # 각 트리의 예측
        predictions = np.array([tree.predict(X) for tree in self.trees])

        # 다수결 투표
        return np.array([
            np.bincount(predictions[:, i]).argmax()
            for i in range(X.shape[0])
        ])
```

---

## 신경망과 딥러닝

### 1. 다층 퍼셉트론 (MLP)

```python
class NeuralNetwork:
    """
    완전 연결 신경망 (Fully Connected Neural Network)

    구조:
    Input → Hidden₁ → Hidden₂ → ... → Output

    활성화 함수:
    - ReLU: max(0, x)
    - Sigmoid: 1 / (1 + e⁻ˣ)
    - Tanh: (eˣ - e⁻ˣ) / (eˣ + e⁻ˣ)
    """

    def __init__(self, layer_sizes):
        """
        layer_sizes: [input_size, hidden1, hidden2, ..., output_size]
        """
        self.layer_sizes = layer_sizes
        self.num_layers = len(layer_sizes)

        # He initialization
        self.weights = []
        self.biases = []

        for i in range(self.num_layers - 1):
            w = np.random.randn(layer_sizes[i], layer_sizes[i+1]) * np.sqrt(2.0 / layer_sizes[i])
            b = np.zeros((1, layer_sizes[i+1]))
            self.weights.append(w)
            self.biases.append(b)

    @staticmethod
    def relu(z):
        return np.maximum(0, z)

    @staticmethod
    def relu_derivative(z):
        return (z > 0).astype(float)

    @staticmethod
    def softmax(z):
        exp_z = np.exp(z - np.max(z, axis=1, keepdims=True))
        return exp_z / np.sum(exp_z, axis=1, keepdims=True)

    def forward(self, X):
        """Forward propagation"""
        self.activations = [X]
        self.z_values = []

        A = X
        for i in range(self.num_layers - 2):
            Z = A.dot(self.weights[i]) + self.biases[i]
            A = self.relu(Z)
            self.z_values.append(Z)
            self.activations.append(A)

        # Output layer (softmax)
        Z = A.dot(self.weights[-1]) + self.biases[-1]
        A = self.softmax(Z)
        self.z_values.append(Z)
        self.activations.append(A)

        return A

    def backward(self, X, y, learning_rate):
        """Backpropagation"""
        m = X.shape[0]

        # One-hot encoding
        num_classes = self.layer_sizes[-1]
        Y = np.zeros((m, num_classes))
        Y[np.arange(m), y] = 1

        # Output layer gradient
        dZ = self.activations[-1] - Y

        # Backprop through layers
        for i in range(self.num_layers - 2, -1, -1):
            dW = (1/m) * self.activations[i].T.dot(dZ)
            db = (1/m) * np.sum(dZ, axis=0, keepdims=True)

            # Update weights
            self.weights[i] -= learning_rate * dW
            self.biases[i] -= learning_rate * db

            if i > 0:
                # Gradient for previous layer
                dA = dZ.dot(self.weights[i].T)
                dZ = dA * self.relu_derivative(self.z_values[i-1])

    def train(self, X, y, epochs=100, batch_size=32, learning_rate=0.01):
        """Mini-batch gradient descent"""
        m = X.shape[0]

        for epoch in range(epochs):
            # Shuffle
            indices = np.random.permutation(m)
            X_shuffled = X[indices]
            y_shuffled = y[indices]

            # Mini-batches
            for i in range(0, m, batch_size):
                X_batch = X_shuffled[i:i+batch_size]
                y_batch = y_shuffled[i:i+batch_size]

                # Forward
                self.forward(X_batch)

                # Backward
                self.backward(X_batch, y_batch, learning_rate)

            # Loss 계산
            if epoch % 10 == 0:
                y_pred = self.forward(X)
                loss = -np.mean(np.log(y_pred[np.arange(m), y] + 1e-15))
                accuracy = np.mean(np.argmax(y_pred, axis=1) == y)
                print(f"Epoch {epoch}: Loss={loss:.4f}, Accuracy={accuracy:.4f}")

    def predict(self, X):
        y_pred = self.forward(X)
        return np.argmax(y_pred, axis=1)

# Dropout (Regularization)
class DropoutLayer:
    """
    Dropout: 학습 중 랜덤하게 뉴런 비활성화
    - Overfitting 방지
    - 앙상블 효과
    """

    def __init__(self, keep_prob=0.5):
        self.keep_prob = keep_prob
        self.mask = None

    def forward(self, A, training=True):
        if training:
            self.mask = np.random.rand(*A.shape) < self.keep_prob
            return A * self.mask / self.keep_prob  # Inverted dropout
        else:
            return A

    def backward(self, dA):
        return dA * self.mask / self.keep_prob

# Batch Normalization
class BatchNormLayer:
    """
    Batch Normalization:
    - Internal Covariate Shift 감소
    - 학습 속도 향상
    - 정규화 효과

    BN(x) = γ * ((x - μ) / √(σ² + ε)) + β
    """

    def __init__(self, num_features, epsilon=1e-5):
        self.gamma = np.ones((1, num_features))
        self.beta = np.zeros((1, num_features))
        self.epsilon = epsilon

        # Running statistics (inference용)
        self.running_mean = np.zeros((1, num_features))
        self.running_var = np.ones((1, num_features))
        self.momentum = 0.9

    def forward(self, X, training=True):
        if training:
            # Batch statistics
            self.mu = np.mean(X, axis=0, keepdims=True)
            self.var = np.var(X, axis=0, keepdims=True)

            # Normalize
            self.X_centered = X - self.mu
            self.std = np.sqrt(self.var + self.epsilon)
            self.X_norm = self.X_centered / self.std

            # Scale and shift
            out = self.gamma * self.X_norm + self.beta

            # Update running statistics
            self.running_mean = self.momentum * self.running_mean + (1 - self.momentum) * self.mu
            self.running_var = self.momentum * self.running_var + (1 - self.momentum) * self.var

            return out
        else:
            # Use running statistics
            X_norm = (X - self.running_mean) / np.sqrt(self.running_var + self.epsilon)
            return self.gamma * X_norm + self.beta

    def backward(self, dout):
        m = dout.shape[0]

        # Gradient of gamma and beta
        dgamma = np.sum(dout * self.X_norm, axis=0, keepdims=True)
        dbeta = np.sum(dout, axis=0, keepdims=True)

        # Gradient of X
        dX_norm = dout * self.gamma
        dvar = np.sum(dX_norm * self.X_centered * -0.5 * self.std**(-3), axis=0, keepdims=True)
        dmu = np.sum(dX_norm * -1/self.std, axis=0, keepdims=True) + dvar * np.sum(-2 * self.X_centered, axis=0, keepdims=True) / m

        dX = dX_norm / self.std + dvar * 2 * self.X_centered / m + dmu / m

        return dX
```

### 2. 합성곱 신경망 (CNN)

```python
class ConvolutionalLayer:
    """
    2D Convolution Layer

    Output size:
    H_out = (H_in + 2*pad - kernel_size) / stride + 1
    W_out = (W_in + 2*pad - kernel_size) / stride + 1
    """

    def __init__(self, in_channels, out_channels, kernel_size, stride=1, padding=0):
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = kernel_size
        self.stride = stride
        self.padding = padding

        # He initialization
        self.filters = np.random.randn(
            out_channels, in_channels, kernel_size, kernel_size
        ) * np.sqrt(2.0 / (in_channels * kernel_size * kernel_size))

        self.bias = np.zeros((out_channels, 1))

    def forward(self, X):
        """
        X: (batch, in_channels, height, width)
        Output: (batch, out_channels, H_out, W_out)
        """
        batch_size, _, H, W = X.shape

        # Padding
        if self.padding > 0:
            X = np.pad(X, ((0,0), (0,0), (self.padding, self.padding), (self.padding, self.padding)))

        # Output dimensions
        H_out = (H + 2*self.padding - self.kernel_size) // self.stride + 1
        W_out = (W + 2*self.padding - self.kernel_size) // self.stride + 1

        output = np.zeros((batch_size, self.out_channels, H_out, W_out))

        # Convolution
        for i in range(H_out):
            for j in range(W_out):
                h_start = i * self.stride
                h_end = h_start + self.kernel_size
                w_start = j * self.stride
                w_end = w_start + self.kernel_size

                # Receptive field
                receptive_field = X[:, :, h_start:h_end, w_start:w_end]

                # Convolve
                for k in range(self.out_channels):
                    output[:, k, i, j] = np.sum(
                        receptive_field * self.filters[k],
                        axis=(1, 2, 3)
                    ) + self.bias[k]

        self.cache = X
        return output

    def backward(self, dout, learning_rate):
        """Backpropagation for convolution"""
        # 복잡한 gradient 계산
        # 실제로는 im2col 최적화 사용
        pass

class MaxPoolingLayer:
    """
    Max Pooling: 다운샘플링
    - 공간 차원 감소
    - Translation invariance
    """

    def __init__(self, pool_size=2, stride=2):
        self.pool_size = pool_size
        self.stride = stride

    def forward(self, X):
        """
        X: (batch, channels, height, width)
        """
        batch_size, channels, H, W = X.shape

        H_out = (H - self.pool_size) // self.stride + 1
        W_out = (W - self.pool_size) // self.stride + 1

        output = np.zeros((batch_size, channels, H_out, W_out))

        for i in range(H_out):
            for j in range(W_out):
                h_start = i * self.stride
                h_end = h_start + self.pool_size
                w_start = j * self.stride
                w_end = w_start + self.pool_size

                pool_region = X[:, :, h_start:h_end, w_start:w_end]
                output[:, :, i, j] = np.max(pool_region, axis=(2, 3))

        return output

# LeNet-5 스타일 CNN
class SimpleCNN:
    """
    간단한 CNN 아키텍처:
    Input → Conv → ReLU → MaxPool → Conv → ReLU → MaxPool → FC → Softmax
    """

    def __init__(self, input_shape=(1, 28, 28), num_classes=10):
        self.conv1 = ConvolutionalLayer(1, 6, kernel_size=5)
        self.pool1 = MaxPoolingLayer(pool_size=2)
        self.conv2 = ConvolutionalLayer(6, 16, kernel_size=5)
        self.pool2 = MaxPoolingLayer(pool_size=2)

        # FC layers
        self.fc_input_size = 16 * 4 * 4  # MNIST 기준
        self.fc = NeuralNetwork([self.fc_input_size, 120, 84, num_classes])

    def forward(self, X):
        # Conv layers
        out = self.conv1.forward(X)
        out = np.maximum(0, out)  # ReLU
        out = self.pool1.forward(out)

        out = self.conv2.forward(out)
        out = np.maximum(0, out)
        out = self.pool2.forward(out)

        # Flatten
        batch_size = out.shape[0]
        out = out.reshape(batch_size, -1)

        # FC layers
        out = self.fc.forward(out)

        return out
```

---

## 최적화 알고리즘

### 1. Gradient Descent 변형들

```python
class Optimizer:
    """다양한 최적화 알고리즘"""

    @staticmethod
    def sgd(params, grads, learning_rate):
        """
        Stochastic Gradient Descent
        θ = θ - η∇L
        """
        for param, grad in zip(params, grads):
            param -= learning_rate * grad

    @staticmethod
    def momentum(params, grads, velocities, learning_rate, momentum=0.9):
        """
        Momentum: 이전 gradient 방향 고려
        v = βv + ∇L
        θ = θ - ηv

        장점: Local minima 탈출, 진동 감소
        """
        for param, grad, velocity in zip(params, grads, velocities):
            velocity[:] = momentum * velocity + grad
            param -= learning_rate * velocity

    @staticmethod
    def nesterov(params, grads, velocities, learning_rate, momentum=0.9):
        """
        Nesterov Accelerated Gradient
        미리 한 발 앞서 gradient 계산
        """
        for param, grad, velocity in zip(params, grads, velocities):
            velocity_old = velocity.copy()
            velocity[:] = momentum * velocity - learning_rate * grad
            param += -momentum * velocity_old + (1 + momentum) * velocity

class AdaGrad:
    """
    AdaGrad: 적응적 학습률
    - 자주 업데이트되는 파라미터 → 낮은 학습률
    - 드물게 업데이트 → 높은 학습률

    θ = θ - (η / √(G + ε)) * ∇L
    G: gradient 제곱 누적합
    """

    def __init__(self, learning_rate=0.01, epsilon=1e-8):
        self.lr = learning_rate
        self.epsilon = epsilon
        self.G = {}

    def update(self, param_name, param, grad):
        if param_name not in self.G:
            self.G[param_name] = np.zeros_like(param)

        self.G[param_name] += grad ** 2
        param -= self.lr * grad / (np.sqrt(self.G[param_name]) + self.epsilon)

class RMSprop:
    """
    RMSprop: AdaGrad 개선
    - Exponential moving average
    - AdaGrad의 learning rate 감소 문제 해결

    G = βG + (1-β)∇L²
    θ = θ - (η / √(G + ε)) * ∇L
    """

    def __init__(self, learning_rate=0.001, decay_rate=0.9, epsilon=1e-8):
        self.lr = learning_rate
        self.decay = decay_rate
        self.epsilon = epsilon
        self.G = {}

    def update(self, param_name, param, grad):
        if param_name not in self.G:
            self.G[param_name] = np.zeros_like(param)

        self.G[param_name] = self.decay * self.G[param_name] + (1 - self.decay) * (grad ** 2)
        param -= self.lr * grad / (np.sqrt(self.G[param_name]) + self.epsilon)

class Adam:
    """
    Adam (Adaptive Moment Estimation)
    - Momentum + RMSprop
    - 가장 널리 사용되는 optimizer

    m = β₁m + (1-β₁)∇L        (1st moment, momentum)
    v = β₂v + (1-β₂)∇L²       (2nd moment, RMSprop)

    m̂ = m / (1 - β₁ᵗ)         (bias correction)
    v̂ = v / (1 - β₂ᵗ)

    θ = θ - η * m̂ / (√v̂ + ε)
    """

    def __init__(self, learning_rate=0.001, beta1=0.9, beta2=0.999, epsilon=1e-8):
        self.lr = learning_rate
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon
        self.m = {}
        self.v = {}
        self.t = 0

    def update(self, param_name, param, grad):
        if param_name not in self.m:
            self.m[param_name] = np.zeros_like(param)
            self.v[param_name] = np.zeros_like(param)

        self.t += 1

        # Update moments
        self.m[param_name] = self.beta1 * self.m[param_name] + (1 - self.beta1) * grad
        self.v[param_name] = self.beta2 * self.v[param_name] + (1 - self.beta2) * (grad ** 2)

        # Bias correction
        m_hat = self.m[param_name] / (1 - self.beta1 ** self.t)
        v_hat = self.v[param_name] / (1 - self.beta2 ** self.t)

        # Update parameters
        param -= self.lr * m_hat / (np.sqrt(v_hat) + self.epsilon)

class AdamW:
    """
    AdamW: Weight Decay 분리
    - L2 regularization을 optimizer에서 분리
    - 더 나은 일반화

    θ = θ - η * (m̂ / (√v̂ + ε) + λθ)
    """

    def __init__(self, learning_rate=0.001, beta1=0.9, beta2=0.999,
                 epsilon=1e-8, weight_decay=0.01):
        self.lr = learning_rate
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon
        self.weight_decay = weight_decay
        self.m = {}
        self.v = {}
        self.t = 0

    def update(self, param_name, param, grad):
        if param_name not in self.m:
            self.m[param_name] = np.zeros_like(param)
            self.v[param_name] = np.zeros_like(param)

        self.t += 1

        # Moments
        self.m[param_name] = self.beta1 * self.m[param_name] + (1 - self.beta1) * grad
        self.v[param_name] = self.beta2 * self.v[param_name] + (1 - self.beta2) * (grad ** 2)

        m_hat = self.m[param_name] / (1 - self.beta1 ** self.t)
        v_hat = self.v[param_name] / (1 - self.beta2 ** self.t)

        # Update with weight decay
        param -= self.lr * (m_hat / (np.sqrt(v_hat) + self.epsilon) + self.weight_decay * param)
```

### 2. 학습률 스케줄링

```python
class LearningRateScheduler:
    """학습률 조정 전략"""

    @staticmethod
    def step_decay(initial_lr, epoch, drop=0.5, epochs_drop=10):
        """
        Step Decay: 주기적으로 학습률 감소
        lr = lr₀ * drop^(epoch // epochs_drop)
        """
        return initial_lr * (drop ** (epoch // epochs_drop))

    @staticmethod
    def exponential_decay(initial_lr, epoch, decay_rate=0.95):
        """
        Exponential Decay
        lr = lr₀ * decay_rate^epoch
        """
        return initial_lr * (decay_rate ** epoch)

    @staticmethod
    def cosine_annealing(initial_lr, epoch, T_max):
        """
        Cosine Annealing: 부드러운 감소
        lr = lr₀ * (1 + cos(πT/T_max)) / 2
        """
        import math
        return initial_lr * (1 + math.cos(math.pi * epoch / T_max)) / 2

    @staticmethod
    def warmup_cosine(initial_lr, epoch, warmup_epochs, total_epochs):
        """
        Warmup + Cosine
        - 초기 몇 epoch: 선형 증가
        - 이후: Cosine 감소
        """
        import math
        if epoch < warmup_epochs:
            return initial_lr * (epoch + 1) / warmup_epochs
        else:
            progress = (epoch - warmup_epochs) / (total_epochs - warmup_epochs)
            return initial_lr * (1 + math.cos(math.pi * progress)) / 2

# Cyclical Learning Rates
class CyclicLR:
    """
    Cyclical Learning Rates
    - 학습률을 주기적으로 증가/감소
    - Super-convergence 가능
    """

    def __init__(self, base_lr=0.001, max_lr=0.01, step_size=2000):
        self.base_lr = base_lr
        self.max_lr = max_lr
        self.step_size = step_size

    def get_lr(self, iteration):
        cycle = np.floor(1 + iteration / (2 * self.step_size))
        x = np.abs(iteration / self.step_size - 2 * cycle + 1)
        lr = self.base_lr + (self.max_lr - self.base_lr) * max(0, (1 - x))
        return lr
```

---

## Transformer 아키텍처

### 1. Self-Attention 메커니즘

```python
class MultiHeadAttention:
    """
    Multi-Head Self-Attention

    Attention(Q, K, V) = softmax(QKᵀ / √d_k)V

    여러 head 병렬 계산 후 concat
    """

    def __init__(self, d_model, num_heads):
        assert d_model % num_heads == 0

        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads

        # Q, K, V projection matrices
        self.W_q = np.random.randn(d_model, d_model) / np.sqrt(d_model)
        self.W_k = np.random.randn(d_model, d_model) / np.sqrt(d_model)
        self.W_v = np.random.randn(d_model, d_model) / np.sqrt(d_model)
        self.W_o = np.random.randn(d_model, d_model) / np.sqrt(d_model)

    def split_heads(self, x, batch_size):
        """
        (batch, seq_len, d_model) → (batch, num_heads, seq_len, d_k)
        """
        x = x.reshape(batch_size, -1, self.num_heads, self.d_k)
        return np.transpose(x, (0, 2, 1, 3))

    def scaled_dot_product_attention(self, Q, K, V, mask=None):
        """
        Attention(Q, K, V) = softmax(QKᵀ / √d_k)V
        """
        d_k = Q.shape[-1]

        # QKᵀ / √d_k
        scores = np.matmul(Q, np.transpose(K, (0, 1, 3, 2))) / np.sqrt(d_k)

        # Mask (padding, future tokens)
        if mask is not None:
            scores = np.where(mask == 0, -1e9, scores)

        # Softmax
        attention_weights = self.softmax(scores)

        # Weighted sum
        output = np.matmul(attention_weights, V)

        return output, attention_weights

    @staticmethod
    def softmax(x):
        exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=-1, keepdims=True)

    def forward(self, x, mask=None):
        """
        x: (batch, seq_len, d_model)
        """
        batch_size, seq_len, _ = x.shape

        # Linear projections
        Q = np.dot(x, self.W_q)
        K = np.dot(x, self.W_k)
        V = np.dot(x, self.W_v)

        # Split into multiple heads
        Q = self.split_heads(Q, batch_size)
        K = self.split_heads(K, batch_size)
        V = self.split_heads(V, batch_size)

        # Attention
        attention_output, _ = self.scaled_dot_product_attention(Q, K, V, mask)

        # Concat heads
        attention_output = np.transpose(attention_output, (0, 2, 1, 3))
        concat_attention = attention_output.reshape(batch_size, seq_len, self.d_model)

        # Final linear
        output = np.dot(concat_attention, self.W_o)

        return output

class PositionalEncoding:
    """
    위치 인코딩: 순서 정보 제공

    PE(pos, 2i) = sin(pos / 10000^(2i/d_model))
    PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))
    """

    def __init__(self, d_model, max_len=5000):
        self.d_model = d_model

        # 위치 인코딩 테이블 생성
        pe = np.zeros((max_len, d_model))
        position = np.arange(0, max_len).reshape(-1, 1)
        div_term = np.exp(np.arange(0, d_model, 2) * -(np.log(10000.0) / d_model))

        pe[:, 0::2] = np.sin(position * div_term)
        pe[:, 1::2] = np.cos(position * div_term)

        self.pe = pe

    def forward(self, x):
        """
        x: (batch, seq_len, d_model)
        """
        seq_len = x.shape[1]
        return x + self.pe[:seq_len, :]

class TransformerBlock:
    """
    Transformer Encoder Block:
    1. Multi-Head Attention
    2. Add & Norm
    3. Feed Forward
    4. Add & Norm
    """

    def __init__(self, d_model, num_heads, d_ff, dropout=0.1):
        self.attention = MultiHeadAttention(d_model, num_heads)
        self.ff = FeedForward(d_model, d_ff)
        self.norm1 = LayerNorm(d_model)
        self.norm2 = LayerNorm(d_model)
        self.dropout = dropout

    def forward(self, x, mask=None):
        # Multi-Head Attention + Residual
        attn_output = self.attention.forward(x, mask)
        x = self.norm1.forward(x + attn_output)

        # Feed Forward + Residual
        ff_output = self.ff.forward(x)
        x = self.norm2.forward(x + ff_output)

        return x

class FeedForward:
    """
    Position-wise Feed-Forward Network
    FFN(x) = max(0, xW₁ + b₁)W₂ + b₂
    """

    def __init__(self, d_model, d_ff):
        self.W1 = np.random.randn(d_model, d_ff) / np.sqrt(d_model)
        self.b1 = np.zeros(d_ff)
        self.W2 = np.random.randn(d_ff, d_model) / np.sqrt(d_ff)
        self.b2 = np.zeros(d_model)

    def forward(self, x):
        hidden = np.maximum(0, np.dot(x, self.W1) + self.b1)  # ReLU
        output = np.dot(hidden, self.W2) + self.b2
        return output

class LayerNorm:
    """
    Layer Normalization
    LN(x) = γ * (x - μ) / σ + β
    """

    def __init__(self, d_model, epsilon=1e-6):
        self.gamma = np.ones(d_model)
        self.beta = np.zeros(d_model)
        self.epsilon = epsilon

    def forward(self, x):
        mean = np.mean(x, axis=-1, keepdims=True)
        var = np.var(x, axis=-1, keepdims=True)
        x_norm = (x - mean) / np.sqrt(var + self.epsilon)
        return self.gamma * x_norm + self.beta
```

### 2. BERT와 GPT

```python
class BERT:
    """
    BERT: Bidirectional Encoder Representations from Transformers

    Pre-training:
    1. Masked Language Modeling (MLM)
    2. Next Sentence Prediction (NSP)
    """

    def __init__(self, vocab_size, d_model=768, num_layers=12, num_heads=12):
        self.vocab_size = vocab_size
        self.d_model = d_model

        # Token embeddings
        self.token_embedding = np.random.randn(vocab_size, d_model) / np.sqrt(d_model)

        # Positional encoding
        self.pos_encoding = PositionalEncoding(d_model)

        # Transformer blocks
        self.layers = [
            TransformerBlock(d_model, num_heads, d_model * 4)
            for _ in range(num_layers)
        ]

    def masked_language_modeling(self, input_ids, masked_positions):
        """
        MLM: 15% 토큰 마스킹, 예측
        [MASK] 토큰으로 대체
        """
        # Forward
        embeddings = self.token_embedding[input_ids]
        x = self.pos_encoding.forward(embeddings)

        for layer in self.layers:
            x = layer.forward(x)

        # 마스킹된 위치의 토큰 예측
        masked_output = x[masked_positions]

        # Linear + Softmax
        logits = np.dot(masked_output, self.token_embedding.T)

        return logits

class GPT:
    """
    GPT: Generative Pre-trained Transformer

    Autoregressive Language Modeling:
    P(x₁, x₂, ..., xₙ) = ∏ P(xᵢ | x₁, ..., xᵢ₋₁)
    """

    def __init__(self, vocab_size, d_model=768, num_layers=12, num_heads=12):
        self.vocab_size = vocab_size
        self.d_model = d_model

        self.token_embedding = np.random.randn(vocab_size, d_model) / np.sqrt(d_model)
        self.pos_encoding = PositionalEncoding(d_model)

        self.layers = [
            TransformerBlock(d_model, num_heads, d_model * 4)
            for _ in range(num_layers)
        ]

    def create_causal_mask(self, seq_len):
        """
        Causal Mask: 미래 토큰 보지 못하게
        [[1, 0, 0],
         [1, 1, 0],
         [1, 1, 1]]
        """
        mask = np.tril(np.ones((seq_len, seq_len)))
        return mask

    def forward(self, input_ids):
        """
        Autoregressive generation
        """
        seq_len = input_ids.shape[1]

        # Embeddings
        embeddings = self.token_embedding[input_ids]
        x = self.pos_encoding.forward(embeddings)

        # Causal mask
        mask = self.create_causal_mask(seq_len)

        # Transformer layers
        for layer in self.layers:
            x = layer.forward(x, mask)

        # Output projection
        logits = np.dot(x, self.token_embedding.T)

        return logits

    def generate(self, prompt_ids, max_length=50, temperature=1.0):
        """
        텍스트 생성 (Greedy / Sampling)
        """
        generated = prompt_ids.copy()

        for _ in range(max_length):
            # Forward
            logits = self.forward(generated)
            next_token_logits = logits[0, -1, :] / temperature

            # Softmax
            probs = np.exp(next_token_logits) / np.sum(np.exp(next_token_logits))

            # Sampling
            next_token = np.random.choice(self.vocab_size, p=probs)

            # Append
            generated = np.append(generated, [[next_token]], axis=1)

            # Stop token
            if next_token == 0:  # [EOS]
                break

        return generated
```

---

**계속...**

이제 AI/ML의 핵심 개념들을 완전히 마스터했습니다:
- 전통적 ML (Linear Regression, Decision Tree, etc.)
- 신경망과 딥러닝 (MLP, CNN)
- 최적화 알고리즘 (SGD, Adam, etc.)
- Transformer 아키텍처 (BERT, GPT)

다음 파일에서는 소프트웨어 공학을 다루겠습니다.
