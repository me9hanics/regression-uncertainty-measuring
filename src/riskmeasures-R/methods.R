#Statistical methods

#source(file.path(dirname(sys.frame(1)$ofile), "utils.R"))

estimate_beta <- function(data) {
#' @param data Matrix with (x, y) pairs, shape (N, 2)
#' @return Numeric vector of length 2: c(intercept, slope)
  data <- validate_xy_data(data, min_rows = 2)
  x <- data[, 1]
  y <- data[, 2]
  design <- cbind(1, x)
  A_inv <- t(design)  %*% design
  B <- t(design)  %*% y
  beta <- solve(A_inv, B)
  as.numeric(beta)
}

bootstrap_samples <- function(data, B, seed = NULL) {
#' @param data Matrix with (x, y) pairs, shape (N, 2)
#' @param B Number of bootstrap samples to generate
#' @param seed Optional random seed for reproducibility
#' @return 3D array of shape (B, N, 2) containing bootstrap samples
  data <- validate_xy_data(data, min_rows = 2)
  
  if (!is.numeric(B) || length(B) != 1 || is.na(B) || B %% 1 != 0 || B < 1) {
    stop("B must be an integer >= 1")
  }
  if (!is.null(seed)) {
    validate_and_set_seed(seed)
  }
  n <- nrow(data)
  indices <- matrix(sample.int(n, size = B * n, replace = TRUE), nrow = B, ncol = n)
  samples <- array(dim = c(B, n, 2))
  for (b in seq_len(B)) {
    samples[b, , ] <- data[indices[b, ], ]
  }
  samples
}

sample_std <- function(values) {
#' @param values Numeric vector of values
#' @return Sample standard deviation
  values <- as.numeric(values)
  if (length(values) < 2) {
    stop(sprintf("values must have at least 2 elements, got %d", length(values)))
  }
  
  n <- length(values)
  mean_val <- mean(values)
  variance <- sum((values - mean_val)^2) / (n - 1)
  sqrt(variance)
}

bootstrap_beta <- function(data, B, seed = NULL) {
#' @param data Matrix with (x, y) pairs, shape (N, 2)
#' @param B Number of bootstrap samples (integer >= 2)
#' @param seed Optional random seed for reproducibility
#' @return Estimated standard error of the slope coefficient
  data <- validate_xy_data(data, min_rows = 2)
  if (!is.numeric(B) || length(B) != 1 || is.na(B) || B %% 1 != 0 || B < 2) {
    stop("B must be an integer >= 2")
  }
  if (!is.null(seed)) {
    validate_and_set_seed(seed)
  }
  samples <- bootstrap_samples(data, B = B, seed = NULL)
  
  betas <- vapply(seq_len(B), function(b) {
    estimate_beta(samples[b, , ])
  }, numeric(2))
  slopes <- betas[2, ]
  sample_std(slopes)
}
