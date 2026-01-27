$$E[Y^2] = E[(1+2X+\varepsilon)^2] = E[1 + 4X^2 + \varepsilon^2 + 4X + 2\varepsilon + 4X\varepsilon] = \\
= 1 + E[4X^2] + E[\varepsilon^2] + E[4X] + E[2\varepsilon] + E[4X]E[\varepsilon] = 1 + 4 + 1 = 6 \\
\text{ (since } X \text{ and } \varepsilon \text{ are independent)}$$

$$\text{Var}[Y] = 6 - 1 = 5$$


If we measure the standard error of the bootstrapped beta estimates, that is a "number" (e.g. 0.03) - but our estimate of that number has uncertainty itself.
So we can take the relative standard error of that estimate - which compares it to the standard deviation of the beta estimates themselves.
As it turns out, that is approximately:

$ \frac{SD(s_{\beta})}{\sigma_{\beta}} \approx  \frac{1}{\sqrt{2(B-1)}} $

so relative error decreases at rate of $O(\frac{1}{\sqrt{B}})$.

---