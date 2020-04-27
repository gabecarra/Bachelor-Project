import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from spektral.layers import GraphAttention, GlobalAttentionPool
from spektral.utils import conversion
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.regularizers import l2

from utils.category_filter import parse_category
from utils.networkx_converter import get_nx_graph


def get_graph_list(files):
    graph_list = []
    for file in files:
        graph_list.extend(get_nx_graph("../data/" + file))
    return graph_list


def generate_data():
    print('Retrieving categories...', end='')
    bicycling_files = parse_category("bicycling")
    running_files = parse_category("running")
    print('done')

    print('Generating networkx graphs...', end='')
    bicycling_graphs = get_graph_list(bicycling_files)
    running_graphs = get_graph_list(running_files)
    print('done')

    print('Converting to numpy matrix...', end='')
    bicycling_matrix = conversion.nx_to_numpy(bicycling_graphs, nf_keys=['x', 'y', 'confidence'])
    running_matrix = conversion.nx_to_numpy(running_graphs, nf_keys=['x', 'y', 'confidence'])
    A = np.append(bicycling_matrix[0], running_matrix[0], axis=0)
    X = np.append(bicycling_matrix[1], running_matrix[1], axis=0)
    y = np.append(np.repeat([[1.0, 0.0]], bicycling_matrix[0].shape[0], axis=0),
                  np.repeat([[0.0, 1.0]], running_matrix[0].shape[0], axis=0), axis=0)
    print('done')
    return A, X, y


A, X, y = generate_data()

# Parameters

n_nodes = X.shape[-2]
n_variables = X.shape[-1]
n_classes = y.shape[-1]
l2_reg = 5e-4            # Regularization rate for l2
learning_rate = 1e-3     # Learning rate for Adam
epochs = 20000           # Number of training epochs
batch_size = 32          # Batch size
es_patience = 200        # Patience fot early stopping

A_train, A_test, x_train, x_test, y_train, y_test = train_test_split(A, X, y, test_size=0.2)
X_in = Input(shape=(n_nodes, n_variables))
A_in = Input((n_nodes, n_nodes))

gc1 = GraphAttention(32, activation='relu', kernel_regularizer=l2(l2_reg))([X_in, A_in])
gc2 = GraphAttention(32, activation='relu', kernel_regularizer=l2(l2_reg))([gc1, A_in])
pool = GlobalAttentionPool(128)(gc2)
output = Dense(n_classes, activation='softmax')(pool)

model = Model(inputs=[X_in, A_in], outputs=output)
optimizer = Adam(lr=learning_rate)
model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['acc'])
# model.summary()

# Train model
print('Training the model...', end='')
history = model.fit([x_train, A_train], y_train, batch_size=batch_size, validation_split=0.1, epochs=epochs,
                    callbacks=[EarlyStopping(patience=es_patience, restore_best_weights=True)], verbose=0)
print('done')

# Plot training & validation accuracy values
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

# Plot training & validation loss values
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

# # Evaluate model
print('Evaluating model...', end='')
eval_results = model.evaluate([x_test, A_test], y_test, batch_size=batch_size, verbose=0)
print('done')
print('Test loss: {:.4f}. Test acc: {:.2f}'.format(*eval_results))
