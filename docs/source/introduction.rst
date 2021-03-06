====================
Introduction to SECOMO: A SEquence COntext MOdeler
====================

This package provides functionality to automatically
extract DNA sequence features from a provided set of sequences
using a **convolutional restricted Boltzmann machine**, which
was inspired by advances made in computer vision [1]_.
To that end, the cRBM learns redundant DNA sequnce features
in terms of a set of weight matrices.

For a downstream analysis of the features that have been learned
a number of utilities are provided:

1. Convert the cRBM features to **Position frequency matrices**,
   which are commonly used
   to represent transcription factor binding affinities [2]_.
2. Visualize the DNA features in terms of **Sequence logos** [2]_.
3. Visualize the **positional enrichment** of the features on a set of DNA sequences.
4. Visualize the **relative enrichment** of the features 
   across a number of different datasets (e.g. sequences of
   different ChIP-seq experiments; treatment-control).
5. Visualize sequence-based **clustering**.

The tutorial illustrates the main functionality of the package on a
toy example of *Oct4* ChIP-seq peak regions obtained from embryonic stem cells.

Finally, if this tool helps for your analysis, please cite the package::

    @Manual{,
        title = {SECOMO: A python package for automatically 
                extracting DNA sequence features},
        author = {Roman Schulte-Sasse, Wolfgang Kopp},
        year = {2017},
    }



References
----------
.. [1] Lee, Honglak (2009).
    Convolutional Deep Belief Networks for scalable
    unsupervised learning of hierarchical representations.
    Proceedings of the 26 th
    International Confefence on Machine Learning

.. [2] Stormo, Gary D. (2000). 
    DNA binding sites: representation and discovery.
    Bioinformatics.

