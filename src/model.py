#===================================================================================================================================================================
#                       PREDICTIVE ANALYSIS 
#===================================================================================================================================================================
           # Testing for
                     # Logistic Regression
                     # Support Vector Machine
                     # Decision Tree Classifier
                     # K-nearest Neighbour

#imports 
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

#Confusion matrix plot

def plot_confusion_matrix(y,y_predict):
    "this function plots the confusion matrix"
    from sklearn.metrics import confusion_matrix

    cm = confusion_matrix(y, y_predict)
    ax= plt.subplot()
    sns.heatmap(cm, annot=True, ax = ax); #annot=True to annotate cells
    ax.set_xlabel('Predicted labels')
    ax.set_ylabel('True labels')
    ax.set_title('Confusion Matrix');
    ax.xaxis.set_ticklabels(['did not land', 'land']); ax.yaxis.set_ticklabels(['did not land', 'landed'])
    plt.show()

URL1 = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv"
data1 = pd.read_csv(URL1)
data1.head()

URL2 = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_3.csv'
data2=pd.read_csv(URL2)
data2.head()

# data1=df1 and data2=df 

Class_Outcome=data1['Class'].to_numpy()
Class_Outcome

#StandardScaler()
scaler = preprocessing.StandardScaler()

# Train Test split (80-20) BEFORE scaling
x_train_raw, x_test_raw, y_train, y_test = train_test_split(data2, Class_Outcome, test_size=0.2, random_state=2, stratify=Class_Outcome)

# Scale the data using the scaler fitted on x_train_raw
x_train = scaler.fit_transform(x_train_raw)
x_test = scaler.transform(x_test_raw) # Only transform, do not fit again

print(x_train.shape,y_train.shape)
print(x_test.shape,y_test.shape)

#===============================================================================
#         LOGISTIC REGRESSION
#===============================================================================

parameters={'C':[0.01,0.1,1],'penalty':['l2'],'solver':['lbfgs']}
parameters={"C":[0.01,0.1,1],'penalty':['l2'], 'solver':['lbfgs']}

# Logistic Regression object - Increased max_iter for better convergence
lr=LogisticRegression(max_iter=1000) # Increased max_iter from default (100)

# GridSearchCV object
logreg_cv = GridSearchCV(lr, parameters, cv=10)

# Fit the GridSearchCV object to the training data
logreg_cv.fit(x_train, y_train)

print("tuned hpyerparameters :(best parameters) ",logreg_cv.best_params_)
print("accuracy :",logreg_cv.best_score_)
test_accuracy = logreg_cv.score(x_test, y_test)
print("Test set accuracy:", test_accuracy)

#calling confusion matrix
yhat=logreg_cv.predict(x_test)
plot_confusion_matrix(y_test,yhat)

#===============================================================================
#                          SVM
#===============================================================================

parameters = {'kernel':('linear', 'rbf','poly','rbf', 'sigmoid'),
              'C': np.logspace(-3, 3, 5),
              'gamma':np.logspace(-3, 3, 5)}

#SVM object
svm = SVC()

#GridSearchCV object
svm_cv=GridSearchCV(svm,parameters,cv=10)

#fit
svm_cv.fit(x_train,y_train)


print("tuned hyperparameters :(best parameters)", svm_cv.best_params_)
print("accuracy :", svm_cv.best_score_)

#Test accuracy
test_accuracy = svm_cv.score(x_test,y_test)
print("Test set accuracy:", test_accuracy)

# Plotting confusion matrix
yhat_svm=svm_cv.predict(x_test)
plot_confusion_matrix(y_test,yhat_svm)


#===============================================================================
#         DECISION TREE CLASSIFIER
#===============================================================================

parameters = {'criterion': ['gini', 'entropy'],
     'splitter': ['best', 'random'],
     'max_depth': [2*n for n in range(1,10)],
     'max_features': ['auto', 'sqrt'],
     'min_samples_leaf': [1, 2, 4],
     'min_samples_split': [2, 5, 10]}

# tree object
tree = DecisionTreeClassifier()

# gridsearch object
tree_cv = GridSearchCV(tree,parameters,cv=10)

# fit
tree_cv.fit(x_train,y_train)

print("tuned hpyerparameters :(best parameters) ",tree_cv.best_params_)
print("accuracy :",tree_cv.best_score_)

#Confusion matrix
yhat_tree=tree_cv.predict(x_test)
plot_confusion_matrix(y_test,yhat_tree)

 #==============================================================================
 #         K-Neighbors Classifier
 #==============================================================================

parameters = {'n_neighbors': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
              'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
              'p': [1,2]}

KNN=KNeighborsClassifier()

# gridsearch object
knn_cv=GridSearchCV(KNN, parameters, cv=10)

# fit
knn_cv.fit(x_train, y_train)

print("tuned hpyerparameters :(best parameters) ",knn_cv.best_params_)
print("accuracy :",knn_cv.best_score_)

#Test score
test_accuracy=knn_cv.score(x_test, y_test)
print("Test set accuracy:",test_accuracy)

#Confusion matrix

yhat_knn=knn_cv.predict(x_test)
plot_confusion_matrix(y_test,yhat_knn)

# collect test accuracies
acc_logreg=logreg_cv.score(x_test, y_test)
acc_svm=svm_cv.score(x_test, y_test)
acc_tree=tree_cv.score(x_test, y_test)
acc_knn=knn_cv.score(x_test, y_test)

print("Logistic Regression:", acc_logreg)
print("SVM:", acc_svm)
print("Decision Tree:", acc_tree)
print("KNN:", acc_knn)

methods = {
    "Logistic Regression": acc_logreg,
    "SVM": acc_svm,
    "Decision Tree": acc_tree,
    "KNN": acc_knn
}

best_score = max(methods.values())
best_methods = [m for m, s in methods.items() if s == best_score]

print("Best performing method(s):", best_methods)


