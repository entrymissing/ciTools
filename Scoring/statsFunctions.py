import numpy as np

#TODO docstrings and tests
def princomp(A):
	"""
	Performs principal components analysis (PCA) on the n-by-p data matrix A
	Rows of A correspond to observations, columns to variables.

	\param A the n by p data matrix
	\retval coeff A p-by-p matrix, each column containing coefficients for one principal component.
	\retval score The principal component scores; that is, the representation of A in the principal component space. Rows of SCORE correspond to observations, columns to components.
	\retval latent A vector containing the eigenvalues of the covariance matrix of A.
	"""
	# subtract the mean (along columns)
	M = (A-np.mean(A.T,axis=1)).T

	#compute the eigenvectors of the covariance matrix
	[latent,coeff] = np.linalg.eig(np.cov(M))

	# projection of the data in the new space
	score = np.dot(coeff.T,M)

	#return the stuff
	return coeff,score,latent

def zscore2(a,axis=0,ddof=0):
	"""
	Computes a stable version of the zscores not sure where it differs from zscore but was needed as a workaround at some point (might be obsolte)

	\param a The n by p data matrix
	\param axis The axis along which to compute the zscores (default is 0)
	\param ddof Number of degrees of freedom (check original implmentation in numpy for a description)
	\retval zscores The zscores for the matrix
	"""
	#make sure a is an array
	a = np.asanyarray(a)
	
	#compute mean and std
	mns = a.mean(axis=axis)
	sstd = a.std(axis=axis, ddof=ddof)
	
	#return the zscores
	if axis and mns.ndim < a.ndim:
		return ((a - np.expand_dims(mns, axis=axis)) / np.expand_dims(sstd,axis=axis))
	else:
		return (a - mns) / sstd