import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-10, 10, 1000)

prior_mean = 0
prior_sigma = 3
prior = (1 / (np.sqrt(2 * np.pi) * prior_sigma)) * np.exp(-(x - prior_mean)**2 / (2 * prior_sigma**2))

obs_mean = 2
obs_sigma = 2  
likelihood = (1 / (np.sqrt(2 * np.pi) * obs_sigma)) * np.exp(-(x - obs_mean)**2 / (2 * obs_sigma**2))

posterior = prior * likelihood
posterior /= np.trapz(posterior, x) 

plt.figure(figsize=(12, 8))

plt.subplot(3, 1, 1)
plt.plot(x, prior, label="Prior (Smooth Dome)", color="blue")
plt.title("Prior: Initial Assumption")
plt.xlabel("Position")
plt.ylabel("Probability Density")
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(x, likelihood, label="Likelihood (Observation with Uncertainty)", color="orange")
plt.title("Likelihood: Measurement with Instrument Uncertainty")
plt.xlabel("Position")
plt.ylabel("Probability Density")
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(x, posterior, label="Posterior (Updated Belief)", color="green")
plt.title("Posterior: Combined Belief After Observation")
plt.xlabel("Position")
plt.ylabel("Probability Density")
plt.legend()

plt.tight_layout()
plt.show()
