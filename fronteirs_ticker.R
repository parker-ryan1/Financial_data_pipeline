# Install and load necessary packages
install.packages("quantmod")
install.packages("PerformanceAnalytics")
install.packages("ggplot2")
library(quantmod)
library(PerformanceAnalytics)
library(ggplot2)

# Load historical price data for assets
getSymbols(c("AAPL", "MSFT", "GOOG", "AMZN"), src = "yahoo", from = "2015-01-01", to = "2020-12-31")
prices <- na.omit(merge(Cl(AAPL), Cl(MSFT), Cl(GOOG), Cl(AMZN)))

# Calculate daily returns
returns <- na.omit(Return.calculate(prices, method = "log"))

# Monte Carlo Simulation for Portfolio Diversification
set.seed(123)
num_portfolios <- 5000
results <- matrix(nrow = num_portfolios, ncol = 3)
colnames(results) <- c("Expected_Return", "Expected_Volatility", "Sharpe_Ratio")

for (i in 1:num_portfolios) {
  weights <- runif(ncol(returns))
  weights <- weights / sum(weights)
  
  port_return <- sum(weights * colMeans(returns)) * 252
  port_volatility <- sqrt(t(weights) %*% (cov(returns) * 252) %*% weights)
  sharpe_ratio <- port_return / port_volatility
  
  results[i,] <- c(port_return, port_volatility, sharpe_ratio)
}

# Convert results to a data frame
results_df <- as.data.frame(results)

# Plot the Efficient Frontier
ggplot(results_df, aes(x = Expected_Volatility, y = Expected_Return)) +
  geom_point(aes(color = Sharpe_Ratio)) +
  labs(title = "Efficient Frontier", x = "Expected Volatility", y = "Expected Return") +
  scale_color_gradient(low = "blue", high = "red")
