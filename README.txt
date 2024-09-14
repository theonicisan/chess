The main Jupyter Notebooks are:

1) create_dictionary_fastload.ipynb: This generates random replay buffers and writes them away to a Teradata database.
2) build_tree.ipynb: This builds a tree of n-level depth where the leaf nodes are the starting points of the subsequent plays through to a critical state.
3) train_tensorflow.ipynb: This notebook uses a training dataset of FEN's with associated aggregate rewards and builds a tensorflow model to predict the reward for a given target FEN.