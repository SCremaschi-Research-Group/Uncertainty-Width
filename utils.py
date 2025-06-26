import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import seaborn as sns

def area_between_curves(curve1, curve2):
    """
    curve 1 and curve 2 are two stage shape cdf. 
    they don't have the same x-coordinates
    curve1 and curve2 are 2D array. curve: [cdf, x]
    """
    curve1 = np.array(curve1)
    curve2 = np.array(curve2)

    # merge ad sort x-coordinates
    x_common = np.union1d(curve1[:, 1], curve2[:, 1])

    # Interpolate y-values for curve1 at the common x-coordinates
    interp_curve1 = interp1d(curve1[:, 1], curve1[:, 0], kind='nearest', 
                             bounds_error = False, fill_value= 'extrapolate')
    y_curve1_interpolated = interp_curve1(x_common)

    # Interpolate y-values for curve2 at the same common x-coordinates
    interp_curve2 = interp1d(curve2[:, 1], curve2[:, 0], kind='nearest',
                             bounds_error = False, fill_value= 'extrapolate')
    y_curve2_interpolated = interp_curve2(x_common)

    # Calculate the absolute difference between the interpolated y-values
    y_diff = np.abs(y_curve1_interpolated - y_curve2_interpolated)

    # Calculate the area between the curves using the trapezoidal rule
    area = np.trapz(y_diff, x_common)
    return area

def run_exp(sk_kt_1,
            sk_kt_2,
            data,
            difference
            ):
    """
    """
    c1 = data[(data['skewness'] == sk_kt_1[0]) & (data['kurtosis'] == sk_kt_1[1])][['cdf', 'x']].values
    c2 = data[(data['skewness'] == sk_kt_2[0]) & (data['kurtosis'] == sk_kt_2[1])][['cdf', 'x']].values
    if len(c1) > 0 and len(c2) > 0:
        c2[:,1] = c2[:,1] + difference
        am= area_between_curves(c1, c2)
    else:
        am = 'NA'
    return am

def generate_heatmap(results,difference):

    pivot_table = results.pivot(columns ='sk1', index ='kt1', values='percentage')

    # Create the heatmap using imshow from matplotlib
    plt.imshow(pivot_table, cmap='GnBu', interpolation='nearest', aspect='auto')
    plt.colorbar()  # Add a colorbar to show the scale

    # Set the ticks and labels for the X and Y axes
    plt.xticks(range(len(pivot_table.columns)), pivot_table.columns)
    plt.yticks(range(len(pivot_table.index)), pivot_table.index)

    plt.xlabel('skewness')
    plt.ylabel('kurtosis')
    plt.title(f'Difference = {difference}')


    plt.show()

def generate_binary_heatmap(data):
    # Create a pivot table
    pivot_table = data.pivot_table(values='percentage', index='kt1', columns='sk1', fill_value=0)

    # Plotting the heatmap
    plt.figure(figsize=(10, 8))
    ax = sns.heatmap(pivot_table, annot=True, cmap='GnBu')
    # ax.set_title('')
    ax.set_xlabel('Skewness')
    ax.set_ylabel('Kurtosis')

    # Customize tick labels to represent True/False instead of 1/0
    cbar = ax.collections[0].colorbar
    cbar.set_ticks([0, 1])
    cbar.set_ticklabels(['False', 'True'])

    plt.show()