from utils.category_filter import parse_category
from utils.networkx_converter import get_nx_graph
from sklearn.model_selection import train_test_split
import numpy as np
from spektral.utils import conversion


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
N = X.shape[-2]          # Number of nodes in the graphs
print(N)
F = X.shape[-1]          # Original feature dimensionality
n_classes = y.shape[-1]  # Number of classes
l2_reg = 5e-4            # Regularization rate for l2
learning_rate = 1e-3     # Learning rate for Adam
epochs = 20000           # Number of training epochs
batch_size = 32          # Batch size
es_patience = 200        # Patience fot early stopping

# A_train, A_test, x_train, x_test, y_train, y_test = train_test_split(A, X, y, test_size=0.2)

# X_in = Input(shape=(N, F))
# A_in = Input((N, N))
#
# gc1 = GraphAttention(32, activation='relu', kernel_regularizer=l2(l2_reg))([X_in, A_in])
# gc2 = GraphAttention(32, activation='relu', kernel_regularizer=l2(l2_reg))([gc1, A_in])
# pool = GlobalAttentionPool(128)(gc2)
#
# output = Dense(n_classes, activation='softmax')(pool)
#
# # Build model
# model = Model(inputs=[X_in, A_in], outputs=output)
# optimizer = Adam(lr=learning_rate)
# model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['acc'])
# model.summary()
#
# # Train model
# model.fit([x_train, A_train],
#           y_train,
#           batch_size=batch_size,
#           validation_split=0.1,
#           epochs=epochs,
#           callbacks=[
#               EarlyStopping(patience=es_patience, restore_best_weights=True)
#           ])
#
# # Evaluate model
# print('Evaluating model.')
# eval_results = model.evaluate([x_test, A_test],
#                               y_test,
#                               batch_size=batch_size)
# print('Done. Test loss: {:.4f}. Test acc: {:.2f}'.format(*eval_results))
