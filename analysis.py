import numpy as np

def aco_optimize_sharpe(mean_returns, cov_matrix, rf, n_ants=60, n_iter=200, rho=0.30, alpha0=60.0, top_frac=0.25, seed=None):
    """
    Ant Colony Optimization (continuous, Dirichlet-based) untuk memaksimalkan Sharpe Ratio.
    - mean_returns: pd.Series (annualized)
    - cov_matrix: pd.DataFrame (annualized)
    - rf: risk-free (annual)
    Constraints: w >= 0, sum(w) = 1
    """
    rng = np.random.default_rng(seed)
    n = len(mean_returns)
    mu = mean_returns.values
    Sigma = cov_matrix.values

    # Pheromone awal (preferensi aset) — mulai seragam
    tau = np.ones(n) / n

    def fitness(w):
        # Hindari bobot bermasalah
        if np.any(w < 0) or not np.isclose(w.sum(), 1.0, atol=1e-6):
            return -1e9
        vol = np.sqrt(np.dot(w, Sigma @ w))
        if vol <= 0:
            return -1e9
        ret = np.dot(w, mu)
        return (ret - rf) / vol  # Sharpe

    best_w = np.ones(n) / n
    best_f = fitness(best_w)

    top_k = max(1, int(n_ants * top_frac))

    for _ in range(n_iter):
        # Prob. sampling dari pheromone
        p = tau / (tau.sum() + 1e-16)

        # Kumpulan solusi per iterasi
        W = np.zeros((n_ants, n))
        F = np.full(n_ants, -1e9)

        # Bangun solusi oleh 'semut'
        alpha_vec = np.maximum(p * alpha0, 1e-6)  # konsentrasi Dirichlet
        for a in range(n_ants):
            w = rng.dirichlet(alpha_vec)
            W[a] = w
            F[a] = fitness(w)

        # Update best-so-far
        idx = np.argmax(F)
        if F[idx] > best_f:
            best_f = F[idx]
            best_w = W[idx].copy()

        # Evaporasi & deposit pheromone dari semut terbaik (elitist)
        elite_idx = np.argsort(-F)[:top_k]
        deposit = np.zeros(n)
        # Skala positif: gunakan Sharpe yang digeser agar non-negatif
        f_top = F[elite_idx]
        f_shift = f_top - f_top.min() + 1e-12
        for i, w in zip(elite_idx, W[elite_idx]):
            deposit += w * f_shift[list(elite_idx).index(i)]

        # Normalisasi deposit
        if deposit.sum() > 0:
            deposit = deposit / deposit.sum()

        tau = (1 - rho) * tau + rho * deposit
        # Stabilitas numerik
        tau = np.clip(tau, 1e-12, None)
        tau = tau / tau.sum()

    return best_w, best_f
