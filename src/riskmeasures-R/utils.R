#Utility functions (e.g. input validation)

validate_xy_data <- function(data, min_rows = 2) {
#' @param data Matrix or data.frame with (x, y) pairs
#' @param min_rows Minimum number of rows required (default 2)
#' @return Validated matrix
  if (is.data.frame(data)) {
    data <- as.matrix(data)
  }
  if (!is.matrix(data)) {
    stop("data must be a matrix or data.frame")
  }
  if (!is.numeric(data)) {
    stop("data must be numeric")
  }
  if (ncol(data) != 2) {
    stop(sprintf("data must have exactly 2 columns (x, y), got %d", ncol(data)))
  }
  if (nrow(data) < min_rows) {
    stop(sprintf("data must have at least %d rows, got %d", min_rows, nrow(data)))
  }
  if (any(!is.finite(data))) {
    stop("data contains NaN or infinite values")
  }
  data
}

validate_and_set_seed <- function(seed = NULL) {
#' @param seed Optional integer seed (NULL for random)
#' @return The seed that was set
  if (is.null(seed)) {
    seed <- sample.int(.Machine$integer.max, 1)
  }
  if (!is.numeric(seed) || length(seed) != 1 || is.na(seed) || seed %% 1 != 0) {
    stop("seed must be an integer")
  }
  if (seed < 0) {
    stop("seed must be non-negative")
  }
  set.seed(seed)
  invisible(seed)
}
