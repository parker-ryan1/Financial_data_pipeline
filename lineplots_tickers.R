# Install and load necessary packages
install.packages("quantmod")
install.packages("tidyquant")
install.packages("dplyr")
install.packages("ggplot2")
install.packages("tidyverse")

library(quantmod)
library(tidyquant)
library(dplyr)
library(ggplot2)
library(tidyverse)

# Define NASDAQ 100 symbols manually (excluding FB for now)
nasdaq100_symbols <- c("AAPL", "MSFT", "AMZN", "GOOGL", "NVDA", "TSLA", "PYPL", "ADBE", "INTC")

# Function to safely get stock data
safe_tq_get <- safely(tq_get)

# Get historical stock prices for all NASDAQ 100 companies, with error handling
stock_data_list <- map(nasdaq100_symbols, ~ safe_tq_get(.x, from = "2015-01-01", to = "2023-01-01"))

# Filter out symbols that failed to fetch
valid_stock_data_list <- stock_data_list %>%
  keep(~ !inherits(.x$error, "error")) %>%
  map_dfr(~ if (!is.null(.x$result)) .x$result else data.frame())

# Filter the NASDAQ 100 list to include only valid symbols
valid_symbols <- stock_data_list %>%
  keep(~ !inherits(.x$error, "error")) %>%
  map_chr(~ .x$result$symbol[1])

nasdaq100 <- tibble(symbol = valid_symbols)

# Calculate daily returns
stock_returns <- valid_stock_data_list %>%
  group_by(symbol) %>%
  tq_transmute(select = adjusted,
               mutate_fun = periodReturn,
               period = "daily",
               col_rename = "daily_return")

# Merge stock returns with symbol information
stock_returns <- stock_returns %>%
  left_join(nasdaq100, by = c("symbol" = "symbol"))

# Calculate yearly profitability (average return) and risk (standard deviation of returns) by symbol
symbol_summary_yearly <- stock_returns %>%
  mutate(year = year(date)) %>%
  group_by(symbol, year) %>%
  summarise(profitability = mean(daily_return, na.rm = TRUE),
            risk = sd(daily_return, na.rm = TRUE)) %>%
  arrange(symbol, year)

# Plot profitability by symbol over the years
profitability_plot <- ggplot(symbol_summary_yearly, aes(x = year, y = profitability, color = symbol)) +
  geom_line() +
  labs(title = "Yearly Profitability by Symbol (NASDAQ 100)",
       x = "Year",
       y = "Average Daily Return") +
  theme_minimal() +
  theme(legend.position = "bottom")

# Plot risk by symbol over the years
risk_plot <- ggplot(symbol_summary_yearly, aes(x = year, y = risk, color = symbol)) +
  geom_line() +
  labs(title = "Yearly Risk by Symbol (NASDAQ 100)",
       x = "Year",
       y = "Standard Deviation of Daily Returns") +
  theme_minimal() +
  theme(legend.position = "bottom")

# Print the plots
print(profitability_plot)
print(risk_plot)
