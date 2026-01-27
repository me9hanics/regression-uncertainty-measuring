#just testing

source("src/riskmeasures-R/load_all.R")

N <- 10000
B <- 1000
beta_0 <- 1
beta_1 <- 2
seed <- 17

data <- simulate_data(N = N, beta_0 = beta_0, beta_1 = beta_1,
                      seed = seed)
se <- bootstrap_beta(data, B = B, seed = seed)

print(paste("Standard error of slope:", se))