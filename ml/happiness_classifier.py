from manimlib.imports import *
from sklearn import svm, metrics
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, ShuffleSplit, GridSearchCV

data = np.loadtxt(open("ARL/ml/SomervilleHappinessSurvey2015.csv", "rb"), dtype=np.int, delimiter=",", skiprows=1)

labels = data[:,0]
data = data[:,1:]

C_range = np.logspace(-10, 10, base=7)
gamma_range = np.logspace(-10, 10, base=5)
param_grid = {'C': C_range, 'gamma': gamma_range}
cv = ShuffleSplit(n_splits=3, test_size=0.2, train_size=0.2)
cv.split(data)
grid = GridSearchCV(svm.SVC(), param_grid=param_grid, cv=cv, verbose=1)
grid.fit(data, labels)
print("The best parameters are %s with a score of %0.2f"
      % (grid.best_params_, grid.best_score_))

classifier = svm.SVC(C=6.290005264075964, gamma=0.025275396791790108, random_state=42)  # find parameters using hyperparameter tuning
x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size = 0.6)

classifier.fit(x_train, y_train)

predicted = classifier.predict(x_test)

print("Classification report for classifier %s:\n%s\n"
      % (classifier, metrics.classification_report(y_test, predicted)))
disp = metrics.plot_confusion_matrix(classifier, x_test, y_test)
disp.figure_.suptitle("Confusion Matrix")
print("Confusion matrix:\n%s" % disp.confusion_matrix)