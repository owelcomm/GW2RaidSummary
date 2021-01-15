from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import numpy as np


def polyreg(x, y):
    """
    Polynomial regression

    Parameters
    ----------
    x : list[float]
        Ids of the fights
    y : list[float]
        data to "smooth" using regression

    Returns
    -------
    x : np.array[float]
        A column array version of the input x
    y_poly_pred :
        Prediction curve of the data, using the poly. regression, indexed by x
    """
    x = np.array(x)
    y = np.array(y)
    x = x[:, np.newaxis]  # We want a column array, not a line array
    polynomial_features = PolynomialFeatures(
        degree=5)  # feel free to increase de degree for a more accurate but less smooth curve
    x_poly = polynomial_features.fit_transform(x)
    model = LinearRegression()
    model.fit(x_poly, y)
    LinearRegression(copy_X=True, fit_intercept=True, n_jobs=None, normalize=False)
    y_poly_pred = model.predict(x_poly)
    return (x, y_poly_pred)
