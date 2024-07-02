import pandas as pd
import mplfinance as mpf
import time

def draw_price_graph(name, data):
    open = []
    close = []
    high = []
    low = []
    dates = []
    for i in data:
        dates.append(pd.to_datetime(i[0]))
        open += [i[1]]
        close += [i[2]]
        high += [i[3]]
        low += [i[4]]
    a = {}
    a["Open"] = open
    a["Close"] = open
    a["High"] = open
    a["Low"] = open
    price_series = pd.DataFrame(a, index=dates)
    mpf.plot(price_series, type="line")


draw_price_graph("GAZP", [['2024-01-03', 159.73, 161.44, 161.58, 159.73, 'SUR'], ['2024-01-04', 161.51, 161.25, 161.64, 161, 'SUR'], ['2024-01-05', 161.2, 161.94, 162.3, 161.07, 'SUR'], ['2024-01-08', 162.44, 163.05, 163.2, 162, 'SUR'], ['2024-01-09', 163.01, 162.41, 163.06, 161.77, 'SUR'], ['2024-01-10', 162.41, 162.87, 163.7, 162, 'SUR'], ['2024-01-11', 162.96, 162.5, 162.96, 161.93, 'SUR'], ['2024-01-12', 162.52, 163.37, 163.98, 162.2, 'SUR'], ['2024-01-15', 163.8, 163.34, 164.4, 163.26, 'SUR'], ['2024-01-16', 163.2, 163.22, 164.18, 162.37, 'SUR'], ['2024-01-17', 163.48, 164.04, 164.2, 163, 'SUR'], ['2024-01-18', 164.12, 166.52, 167.55, 164.12, 'SUR'], ['2024-01-19', 166.52, 165.9, 167.62, 165.2, 'SUR'], ['2024-01-22', 165.98, 166.06, 167, 165.26, 'SUR'], ['2024-01-23', 166.49, 168.31, 168.96, 165.6, 'SUR'], ['2024-01-24', 168.36, 166.36, 168.63, 166.2, 'SUR'], ['2024-01-25', 166.36, 165.42, 166.94, 165.36, 'SUR'], ['2024-01-26', 165.65, 163.99, 165.95, 163.65, 'SUR'], ['2024-01-29', 164, 163.5, 164.49, 162.85, 'SUR'], ['2024-01-30', 163.31, 163.22, 163.79, 162.71, 'SUR'], ['2024-01-31', 163.42, 166.33, 166.48, 162.9, 'SUR'], ['2024-02-01', 166.75, 165.25, 166.75, 164.8, 'SUR'], ['2024-02-02', 165.15, 164.4, 167.85, 164.4, 'SUR'], ['2024-02-05', 164.42, 164.87, 165.22, 163.55, 'SUR'], ['2024-02-06', 164.87, 164.56, 165.12, 164.04, 'SUR'], ['2024-02-07', 164.56, 164.62, 165.59, 164.34, 'SUR'], ['2024-02-08', 164.62, 163.21, 164.96, 163.1, 'SUR'], ['2024-02-09', 163.48, 163.23, 163.97, 163.2, 'SUR'], ['2024-02-12', 163.28, 162.49, 163.5, 162.21, 'SUR'], ['2024-02-13', 162.6, 162.29, 163.9, 162, 'SUR'], ['2024-02-14', 162.38, 161.92, 162.88, 161.07, 'SUR'], ['2024-02-15', 162.09, 161.59, 162.61, 161.31, 'SUR'], ['2024-02-16', 161.98, 161.19, 162, 161.1, 'SUR'], ['2024-02-19', 161.34, 161.24, 162.2, 160.84, 'SUR'], ['2024-02-20', 161.21, 159.5, 161.64, 159.16, 'SUR'], ['2024-02-21', 159.6, 158.64, 160.23, 158.3, 'SUR'], ['2024-02-22', 159, 158.12, 159.1, 158, 'SUR'], ['2024-02-26', 158.92, 160.09, 160.56, 158.85, 'SUR'], ['2024-02-27', 160.15, 159.04, 160.15, 158.81, 'SUR'], ['2024-02-28', 159.19, 160.65, 162.27, 159.05, 'SUR'], ['2024-02-29', 160.65, 161.82, 162.3, 160, 'SUR'], ['2024-03-01', 161.82, 161.34, 163.1, 161.18, 'SUR'], ['2024-03-04', 161.49, 161.24, 162, 160.86, 'SUR'], ['2024-03-05', 161.24, 160.98, 161.8, 160.23, 'SUR'], ['2024-03-06', 160.98, 161.65, 162, 160.5, 'SUR'], ['2024-03-07', 161.65, 160.91, 162.3, 160.75, 'SUR'], ['2024-03-11', 161.03, 160.56, 161.28, 160.51, 'SUR'], ['2024-03-12', 160.79, 162.99, 163.31, 160.56, 'SUR'], ['2024-03-13', 163.2, 161.77, 163.22, 161.1, 'SUR'], ['2024-03-14', 161.8, 161.1, 161.81, 160.53, 'SUR'], ['2024-03-15', 161.1, 160.86, 161.42, 160.04, 'SUR'], ['2024-03-18', 161.1, 160.58, 161.43, 160.31, 'SUR'], ['2024-03-19', 160.5, 158.55, 161.25, 158.04, 'SUR'], ['2024-03-20', 158.6, 158.42, 158.98, 157.75, 'SUR'], ['2024-03-21', 158.79, 158.28, 159.16, 157.87, 'SUR'], ['2024-03-22', 158.33, 156.44, 158.69, 156, 'SUR'], ['2024-03-25', 157.19, 158.84, 158.97, 155.75, 'SUR'], ['2024-03-26', 159.1, 157.94, 159.45, 156.9, 'SUR'], ['2024-03-27', 158, 157.79, 158.6, 157.2, 'SUR'], ['2024-03-28', 157.79, 157.05, 157.95, 157.04, 'SUR'], ['2024-03-29', 157.02, 157.22, 157.9, 156.51, 'SUR'], ['2024-04-01', 157.63, 158.06, 158.25, 157.43, 'SUR'], ['2024-04-02', 158.11, 164.18, 164.98, 157.51, 'SUR'], ['2024-04-03', 164.05, 162.63, 165.36, 162.12, 'SUR'], ['2024-04-04', 162.76, 162.69, 164.3, 161.52, 'SUR'], ['2024-04-05', 162.75, 163.59, 164.63, 162.1, 'SUR'], ['2024-04-08', 164, 163.89, 164.9, 163.57, 'SUR'], ['2024-04-09', 164, 164.08, 165.79, 163.49, 'SUR'], ['2024-04-10', 164.1, 164.74, 165.94, 163.59, 'SUR'], ['2024-04-11', 164.97, 166.24, 166.33, 164.15, 'SUR'], ['2024-04-12', 166.52, 164.83, 166.8, 164.69, 'SUR'], ['2024-04-15', 165, 163.33, 165.66, 163.27, 'SUR'], ['2024-04-16', 163.34, 164.38, 164.78, 162.65, 'SUR'], ['2024-04-17', 164.52, 164.62, 165.68, 163.78, 'SUR'], ['2024-04-18', 164.71, 165.4, 166.1, 163.85, 'SUR'], ['2024-04-19', 165.52, 167.03, 168.15, 165, 'SUR'], ['2024-04-22', 167.2, 166.77, 167.89, 165.55, 'SUR'], ['2024-04-23', 166.59, 163.7, 167.43, 162.62, 'SUR'], ['2024-04-24', 163.7, 162.86, 164.41, 162.62, 'SUR'], ['2024-04-25', 163, 163.35, 164.2, 162.67, 'SUR'], ['2024-04-26', 163.49, 162.46, 164.19, 162.11, 'SUR'], ['2024-04-27', 162.69, 164.06, 166.49, 161.7, 'SUR'], ['2024-04-29', 164.1, 164.03, 165.24, 163.83, 'SUR'], ['2024-04-30', 164.35, 163.22, 164.55, 163.22, 'SUR'], ['2024-05-02', 163.29, 157.75, 165.36, 156.38, 'SUR'], ['2024-05-03', 157.4, 155.2, 157.74, 154, 'SUR'], ['2024-05-06', 155.31, 153.64, 155.76, 153, 'SUR'], ['2024-05-07', 154, 154.16, 154.96, 153.5, 'SUR'], ['2024-05-08', 154.21, 154.22, 154.75, 154.16, 'SUR'], ['2024-05-10', 154.22, 154.58, 154.89, 154.22, 'SUR'], ['2024-05-13', 155.2, 157.9, 158.65, 154.91, 'SUR'], ['2024-05-14', 157.98, 156.16, 158.4, 155.82, 'SUR'], ['2024-05-15', 156.31, 156.97, 157.29, 154.91, 'SUR'], ['2024-05-16', 157, 157.88, 158.1, 156.67, 'SUR'], ['2024-05-17', 158.35, 155.17, 158.35, 154.75, 'SUR'], ['2024-05-20', 155.31, 145.03, 155.69, 145.01, 'SUR'], ['2024-05-21', 144.24, 139.54, 145.68, 137.35, 'SUR'], ['2024-05-22', 139.8, 139.25, 142.2, 138.67, 'SUR'], ['2024-05-23', 139.08, 134.69, 139.08, 133.17, 'SUR'], ['2024-05-24', 134.9, 133.34, 136.45, 133, 'SUR']])