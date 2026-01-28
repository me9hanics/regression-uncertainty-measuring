#' Entrypoint for CLI
#'
#' E.g.:
#'   Rscript src/riskmeasures-R/cli.R 
#'     --N 200 --B 1000 
#'     --beta0 1 --beta1 2 
#'     --x-sigma 1 --eps-sigma 1 
#'     --seed 17 --log

#' PACKAGES
tryCatch({
  if (!require("optparse", quietly = TRUE)) {
    install.packages("optparse")
    library(optparse)
  }
}, error = function(e) {
  stop("Failed to install 'optparse': ", e$message, call. = FALSE)
})

tryCatch({
  if (!require("jsonlite", quietly = TRUE)) {
    install.packages("jsonlite")
    library(jsonlite)
  }
}, error = function(e) {
  stop("Failed to install 'jsonlite': ", e$message, call. = FALSE)
})


source("src/riskmeasures-R/utils.R")
source("src/riskmeasures-R/simulation.R")
source("src/riskmeasures-R/methods.R")

ensure_parent_dir <- function(path) {
  parent <- dirname(path)
  if (parent != "" && !dir.exists(parent)) {
    dir.create(parent, recursive = TRUE)
  }
}

log_msg <- function(level, msg, log_level = "INFO") {
  levels <- c("INFO" = 1, "WARNING" = 2, "ERROR" = 3)
  if (levels[level] >= levels[log_level]) {
    cat(sprintf("[%s] %s: %s\n", format(Sys.time(), "%H:%M:%S"), level, msg))
  }
}

build_parser <- function() {
  option_list <- list(
    make_option(c("--N"), type = "integer", default = 10000, help = "Number of observations [required]"),
    make_option(c("--beta0"), type = "double", default = 1.0, help = "Intercept"),
    make_option(c("--beta1"), type = "double", default = 2.0, help = "Slope"),
    make_option(c("--x-sigma"), type = "double", default = 1.0, help = "SD of x"),
    make_option(c("--eps-sigma"), type = "double", default = 1.0, help = "SD of epsilon"),
    make_option(c("--seed"),type = "integer", default = 17, help = "Random seed"),
    make_option(c("--B"), type = "integer", default = 1000, help = "Bootstrap resamples [required]"),
    make_option(c("--out"), type = "character", help = "JSON output path"),
    make_option(c("--save-data"), type = "character", help = "CSV data path"),
    make_option(c("--log"), action = "store_true", default = FALSE, help = "Save to timestamped directory")
  )
  OptionParser(option_list = option_list, prog = "riskmeasures-R")
}


#MAIN (CLI call)
main <- function(argv = NULL) {
  parser <- build_parser()
  args <- parse_args(parser, args = argv)
  cat("DEBUG - args received:\n")
  print(names(args))
  print(args)
  if (is.null(args$N) || is.null(args$B)) {
    cat("Error: --N and --B are required\n\n")
    print_help(parser)
    return(2)
  }
  tryCatch({
    if (args$N < 2) stop("N must be >= 2")
    if (args$B < 2) stop("B must be >= 2")
    if (args$`x-sigma` <= 0) stop("x-sigma must be > 0")
    if (args$`eps-sigma` <= 0) stop("eps-sigma must be > 0")
  }, error = function(e) {
    log_msg("ERROR", paste("Validation error:", e$message))
    quit(status = 2)
  })
  
  t0 <- Sys.time() #for logging
  if (args$log) {
    timestamp_str <- format(Sys.time(), "%Y%m%d_%H%M%S")
    log_dir <- file.path("artifacts", timestamp_str)
    log_msg("INFO", paste("Logging to", log_dir))
  }
  
  log_msg("INFO", sprintf("Simulating: N=%d B=%d seed=%s", 
                          args$N, args$B, ifelse(is.null(args$seed), "random", args$seed)))
  
  data <- simulate_data(N = args$N, beta_0 = args$beta0, beta_1 = args$beta1,
                        x_sigma = args$`x-sigma`, epsilon_sigma = args$`eps-sigma`, 
                        seed = args$seed)
  
  beta_hat <- estimate_beta(data)
  log_msg("INFO", sprintf("OLS: beta0=%.6g beta1=%.6g", beta_hat[1], beta_hat[2]))
  
  se_boot <- bootstrap_beta(data, B = args$B, seed = args$seed)
  log_msg("INFO", sprintf("Bootstrap SE(beta1) = %.6g", se_boot))
  
  if (!is.null(args$`save-data`)) {
    ensure_parent_dir(args$`save-data`)
    write.csv(data, args$`save-data`, row.names = FALSE)
    log_msg("INFO", paste("Saved data to", args$`save-data`))
  }
  
  if (args$log) {
    ensure_parent_dir(file.path(log_dir, "data.csv"))
    write.csv(data, file.path(log_dir, "data.csv"), row.names = FALSE)
  }
  
  runtime_ms <- as.integer(difftime(Sys.time(), t0, units = "secs") * 1000)
  
  result <- list(
    inputs = list(N = args$N, B = args$B, beta0 = args$beta0, beta1 = args$beta1,
                  x_sigma = args$`x-sigma`, eps_sigma = args$`eps-sigma`, seed = args$seed),
    outputs = list(beta_hat = as.numeric(beta_hat), se_boot_beta1 = as.numeric(se_boot)),
    meta = list(timestamp_utc = format(Sys.time(), tz = "UTC"), runtime_ms = runtime_ms,
                r_version = paste(R.version$major, R.version$minor, sep = "."))
  )
  
  json_output <- toJSON(result, pretty = TRUE, auto_unbox = TRUE)
  
  if (!is.null(args$out)) {
    ensure_parent_dir(args$out)
    write(json_output, args$out)
    log_msg("INFO", paste("Wrote results to", args$out))
  }
  
  if (args$log) {
    write(json_output, file.path(log_dir, "result.json"))
  }
  
  if (is.null(args$out) && !args$log) {
    cat(json_output, "\n")
  }
  return(0)
}

#
if (!interactive()) {
  status <- main()
  quit(status = status)
}