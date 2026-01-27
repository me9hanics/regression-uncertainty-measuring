#Simulate data according to the linear regression model:
# y_i = beta_0 + beta_1 * x_i + epsilon_i
#where x_i ~ N(0, x_sigma^2) and epsilon_i ~ N(0, epsilon_sigma^2)

#source(file.path(dirname(sys.frame(1)$ofile), "utils.R"))

simulate_data <- function(N,
                          beta_0 = 1,
                          beta_1 = 2,
                          x_sigma = 1,
                          epsilon_sigma = 1,
                          seed = NULL) {
#' @param N Number of observations
#' @param beta_0 Intercept
#' @param beta_1 Slope
#' @param x_sigma Standard deviation of x values
#' @param epsilon_sigma Standard deviation of error terms
#' @param seed Optional random seed

  if (!is.numeric(N) || length(N) != 1 || is.na(N) || N %% 1 != 0) {
    stop("N must be an integer")
  }
  if (N < 2) {
    stop(sprintf("N must be >= 2, got %d", N))
  }
  if (!is.numeric(x_sigma) || length(x_sigma) != 1 || !is.finite(x_sigma) || x_sigma <= 0) {
    stop("x_sigma must be a positive finite number")
  }
  if (!is.numeric(epsilon_sigma) || length(epsilon_sigma) != 1 || !is.finite(epsilon_sigma) || epsilon_sigma <= 0) {
    stop("epsilon_sigma must be a positive finite number")
  }
  if (!is.null(seed)) {
    validate_and_set_seed(seed)
  }

  xs <- rnorm(N, mean = 0, sd = x_sigma)
  epsilons <- rnorm(N, mean = 0, sd = epsilon_sigma)
  ys <- beta_0 + beta_1 * xs + epsilons
  
  cbind(x = xs, y = ys)
}
