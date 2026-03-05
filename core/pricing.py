import math

class PricingEngine:
    def __init__(self):
        pass

    def calculate_price(self, instrument_type: str, params: dict) -> float:
        if instrument_type.lower() == 'option':
            return self._black_scholes(
                params.get('S'), # Spot price
                params.get('K'), # Strike price
                params.get('T'), # Time to maturity (years)
                params.get('r'), # Risk-free rate
                params.get('sigma'), # Volatility
                params.get('type', 'call') # call or put
            )
        else:
            return params.get('price', 0.0)

    def calculate_greeks(self, instrument_type: str, params: dict) -> dict:
        if instrument_type.lower() == 'option':
            return self._black_scholes_greeks(
                params.get('S'),
                params.get('K'),
                params.get('T'),
                params.get('r'),
                params.get('sigma'),
                params.get('type', 'call')
            )
        return {}

    def _black_scholes(self, S, K, T, r, sigma, option_type='call'):
        if S is None or K is None:
            return 0.0

        T = float(T) if T is not None else 1.0
        r = float(r) if r is not None else 0.05
        sigma = float(sigma) if sigma is not None else 0.2
        S = float(S)
        K = float(K)

        if T <= 0:
            if option_type == 'call':
                return max(0, S - K)
            else:
                return max(0, K - S)

        d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
        d2 = d1 - sigma * math.sqrt(T)

        if option_type == 'call':
            price = S * self._norm_cdf(d1) - K * math.exp(-r * T) * self._norm_cdf(d2)
        else:
            price = K * math.exp(-r * T) * self._norm_cdf(-d2) - S * self._norm_cdf(-d1)

        return round(price, 4)

    def _black_scholes_greeks(self, S, K, T, r, sigma, option_type='call'):
        if S is None or K is None:
            return {}

        T = float(T) if T is not None else 1.0
        r = float(r) if r is not None else 0.05
        sigma = float(sigma) if sigma is not None else 0.2
        S = float(S)
        K = float(K)

        if T <= 0:
            return {'delta': 0.0, 'gamma': 0.0, 'theta': 0.0, 'vega': 0.0, 'rho': 0.0}

        d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
        d2 = d1 - sigma * math.sqrt(T)

        nd1 = self._norm_cdf(d1)
        nd2 = self._norm_cdf(d2)
        n_prime_d1 = self._norm_pdf(d1)

        gamma = n_prime_d1 / (S * sigma * math.sqrt(T))
        vega = S * math.sqrt(T) * n_prime_d1

        if option_type == 'call':
            delta = nd1
            theta = (- (S * n_prime_d1 * sigma) / (2 * math.sqrt(T))
                     - r * K * math.exp(-r * T) * nd2)
            rho = K * T * math.exp(-r * T) * nd2
        else:
            delta = nd1 - 1
            theta = (- (S * n_prime_d1 * sigma) / (2 * math.sqrt(T))
                     + r * K * math.exp(-r * T) * self._norm_cdf(-d2))
            rho = -K * T * math.exp(-r * T) * self._norm_cdf(-d2)

        return {
            'delta': round(delta, 4),
            'gamma': round(gamma, 4),
            'theta': round(theta / 365.0, 4), # Theta per day typically
            'vega': round(vega / 100.0, 4),   # Vega per 1% vol change typically
            'rho': round(rho / 100.0, 4)      # Rho per 1% rate change typically
        }

    def _norm_cdf(self, x):
        """Cumulative distribution function for the standard normal distribution."""
        return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0

    def _norm_pdf(self, x):
        """Probability density function for the standard normal distribution."""
        return (1.0 / math.sqrt(2.0 * math.pi)) * math.exp(-0.5 * x * x)
