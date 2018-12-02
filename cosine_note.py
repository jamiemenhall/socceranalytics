But how to handle correlation between features? I prefer to use x'C^(-1) y -- that way it's equivalent to the familiar cosine similarity after applying any choice of spatial whitening filter to the data:

s1(x,y) = x' C^(-1) y/[sqrt(x'C^(-1)x)sqrt(y'C^(-1)y)] is equivalent to 
s2(x,y) = s3(w,v) = w'v/[||w||||v||] where w = Wx and v = Wy and W is any choice of whitening matrix, i.e. any matrix such that W'W = C^(-1)

(Here C is the covariance matrix and x and y are two column vectors of the observations of features.)

We get the inverse relationship between similarity and distance using whitening filters W and don't need to work with the uninverted covariance matrix.

We can think of Mahalanobis distance as just the squared L2 norm of the whitened difference between an observation vector and the mean vector. Treating this as a form of distance between any two vectors x and y, d(x,y) = ||W(x-y)||^2 = ||w-v||^2 , the same relationship between squared norm of difference and cosine similarity holds as in the unwhitened case. Thus increasing this "number of standard deviations" distance between x and y will decrease the cosine similarity if you hold the norms of the whitened vectors w and v constant.

Since with real data, ||w-v||^2 = ||w||^2 + ||v||^2 - 2w'v, we have that d(x,y) = ||w||^2 + ||v||^2 - 2||w||||v||s2(x,y), which is the sort of relationship between similarity and distance that we want.

