import numpy as np
import scipy as sp
import scipy.linalg as linalg

def my_LDA(X, Y):
    """
    Train a LDA classifier from the training set
    X: training data
    Y: class labels of training data

    """    
    
    classLabels = np.unique(Y) # different class labels on the dataset
    classNum = len(classLabels)
    datanum, dim = X.shape # dimensions of the dataset
    totalMean = np.mean(X,0) # total mean of the data

    # ====================== YOUR CODE HERE ======================
    # Instructions: Implement the LDA technique, following the
    # steps given in the pseudocode on the assignment.
    # The function should return the projection matrix W,
    # the centroid vector for each class projected to the new
    # space defined by W and the projected data X_lda.    
    # =============================================================

     # partition class labels per label - list of arrays per label
    partition = [np.where(Y==label)[0] for label in classLabels]

    # find mean value per class (per attribute) - list of arrays per label
    classMean = [(np.mean(X[idx],0),len(idx)) for idx in partition]

    # Compute the within-class scatter matrix
    Sw = np.zeros((dim,dim))
    for idx in partition:
        Sw += np.cov(X[idx],rowvar=0) * len(idx)# covariance matrix * fraction of instances per class

    # Compute the between-class scatter matrix
    Sb = np.zeros((dim,dim))
    for mu,class_size in classMean:
        mu=mu.reshape(dim,1) #make column vector
        Sb += class_size * np.dot((mu - totalMean), np.transpose((mu - totalMean)))

    # Solve the eigenvalue problem for discriminant directions to maximize class seperability while simultaneously minimizing
    # the variance within each class
    # The exception code can be ignored for the example dataset
    try:
        S = np.dot(linalg.inv(Sw), Sb)
        eigval, eigvec = linalg.eig(S)
    except: #SingularMatrix
        print "Singular matrix"
        eigval, eigvec = linalg.eig(Sb, Sw+Sb)

    idx = eigval.argsort()[::-1] # Sort eigenvalues
    eigvec = eigvec[:,idx] # Sort eigenvectors according to eigenvalues
    W = np.real(eigvec[:,:classNum-1]) # eigenvectors correspond to k-1 largest eigenvalues


    # Project data onto the new LDA space
    X_lda = np.real(np.dot(X, np.real(W)))

    # project the mean vectors of each class onto the LDA space
    projected_centroid = [np.dot(mu, np.real(W)) for mu,class_size in classMean]


    return W, projected_centroid, X_lda