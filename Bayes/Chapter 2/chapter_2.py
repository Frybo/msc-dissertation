import pymc as pm 

parameter = pm.Exponential("poisson_param", 1)
data_generator = pm.Poisson("data_generator", parameter)
data_plus_one = data_generator + 1

print "Children of `parameter`: "
print parameter.children
print "\nParents of `data_generator`: "
print data_generator.parents 
print "\nChildren of `data_generator`: "
print data_generator.children 

print "parameter.value =", parameter.value
print "data_generator.value =", data_generator.value
print "data_plus_one.value =", data_plus_one.value

