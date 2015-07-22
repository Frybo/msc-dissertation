import pymc as pm
import numpy as np
from matplotlib import pyplot as plt
from IPython.core.pylabtools import figsize
import scipy.stats as stats

count_data = np.loadtxt("txtdata.csv")
n_count_data = len(count_data)

alpha = 1.0 / count_data.mean()

lambda_1 = pm.Exponential("lambda_1", alpha)
lambda_2 = pm.Exponential("lambda_2", alpha)

tau = pm.DiscreteUniform("tau", lower = 0, upper = n_count_data)

print "Random output", tau.random(), tau.random(), tau.random()

@pm.deterministic
def lambda_(tau = tau, lambda_1 = lambda_1, lambda_2 = lambda_2):
	out = np.zeros(n_count_data)
	out[:tau] = lambda_1
	out[tau:] = lambda_2
	return out

observation = pm.Poisson("obs", lambda_, value = count_data, observed = True)

model = pm.Model([observation, lambda_1, lambda_2, tau])

mcmc = pm.MCMC(model)
mcmc.sample(40000, 10000, 1)

lambda_1_samples = mcmc.trace('lambda_1')[:]
lambda_2_samples = mcmc.trace('lambda_2')[:]
tau_samples = mcmc.trace('tau')[:]

figsize(12.5, 10)

ax = plt.subplot(311)
ax.set_autoscaley_on(False)

plt.hist(lambda_1_samples, histtype='stepfilled', bins=30, alpha=0.85, label="posterior of $\lambda_1$", color="#A60628", normed=True)
plt.legend(loc="upper left")
plt.title(r"""Posterior distributions of the variables $\lambda_1,\;\lambda_2,\;\tau$""")
plt.xlim([15, 30])
plt.xlabel("$\lambda_1$ value")

ax = plt.subplot(312)
ax.set_autoscaley_on(False)

plt.hist(lambda_2_samples, histtype='stepfilled', bins=30, alpha=0.85, label="posterior of $\lambda_2$", color="#7A68A6", normed=True)
plt.legend(loc="upper left")
plt.xlim([15, 30])
plt.xlabel("$\lambda_2$ value")

ax = plt.subplot(313)
w = 1.0 / tau_samples.shape[0] * np.ones_like(tau_samples)

plt.hist(tau_samples, bins=n_count_data, alpha=1, label=r"posterior of $\tau$", color="#467821", weights=w, rwidth=2.)
plt.xticks(np.arange(n_count_data))

plt.legend(loc="upper left")
plt.ylim([0, 0.75])
plt.xlim([35, len(count_data) - 20])
plt.ylabel("probability")
plt.xlabel(r"$\tau\$ (in days)")

plt.show()