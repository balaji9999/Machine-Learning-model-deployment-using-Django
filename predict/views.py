from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
import pandas as pd
from .models import PredResults
import pickle
import joblib 
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from tensorflow.keras.models import Sequential
from keras.callbacks import TensorBoard



def predict(request):
    return render(request, 'predict.html')


def predict_chances(request):

    if request.POST.get('action') == 'post':

        #Bank loan
        firstname = str(request.POST.get('Firstname'))
        Lastname = str(request.POST.get('Lastname'))
        Dependents = int(request.POST.get('Dependents'))
        ApplicantIncome = int(request.POST.get('ApplicantIncome'))
        CoapplicantIncome = int(request.POST.get('CoapplicantIncome'))
        LoanAmount = int(request.POST.get('LoanAmount'))
        Loan_Amount_Term = int(request.POST.get('Loan_Amount_Term'))
        Credit_History = int(request.POST.get('Credit_History'))
        Gender = str(request.POST.get('Gender'))
        Married =str(request.POST.get('Married'))
        Education = str(request.POST.get('Education'))
        Self_Employed = str(request.POST.get('Self_Employed'))
        Property_Area= str(request.POST.get('Property_Property_AreaArea'))

        print(firstname)
        data=np.array([[Dependents,ApplicantIncome,CoapplicantIncome,LoanAmount,Loan_Amount_Term,Credit_History]])
  
        if Gender=='Male':
            data1=np.append(data,[1,0])
        else:
            data1=np.append(data,[0,1])

        if Married=='Yes':
            data2=np.append(data1,[1,0])
        else:
            data2=np.append(data1,[0,1])

        if Education=='Graduate':
            data3=np.append(data2,[1,0])
        else:
            data3=np.append(data2,[0,1])

        if Self_Employed=='Yes':
            data4=np.append(data3,[1,0])
        else:
            data4=np.append(data3,[0,1])

        if Property_Area=='Rural':
            data5=np.append(data4,[1,0,0])
        elif Property_Area=='Semiurban':
            data5=np.append(data4,[0,1,0])
        else:
            data5=np.append(data4,[0,0,1])
        print(data5)    
        total_data=np.array(data5)
        print(type(total_data))
        model = pd.read_pickle(r'C:\Users\mange\Desktop\Django-APP\django_app\new_model_logbank.pickle')  

        dat=np.array([[1,4583,1508,128000,360,1,0,1,0,1,1,0,1,0,1,0,0]])
        result = model.predict([total_data])
        print(result)
        print(firstname)
        if result==0:
            j="Loan Approved"
        else:
            j="Loan Rejected"
        classification = j
        #classification = result[0]
        print(classification)

        #firstname=firstname, Lastname=Lastname,
        PredResults.objects.create(firstname=firstname, Lastname=Lastname,Dependents=Dependents,
                                    ApplicantIncome=ApplicantIncome,CoapplicantIncome=CoapplicantIncome,
                                    LoanAmount=LoanAmount,Loan_Amount_Term=Loan_Amount_Term,Credit_History=Credit_History,
                                    Gender=Gender,Married=Married,Education=Education,Self_Employed=Self_Employed,Property_Area=Property_Area,
                                    classification=classification)

        return JsonResponse({'result': classification, 'firstname':firstname, 'Lastname':Lastname, 'Dependents':Dependents,
                                    'ApplicantIncome':ApplicantIncome,'CoapplicantIncome':CoapplicantIncome,
                                    'LoanAmount':LoanAmount,'Loan_Amount_Term':Loan_Amount_Term,'Credit_History':Credit_History,
                                    'Gender':Gender,'Married':Married,'Education':Education,'Self_Employed':Self_Employed,'Property_Area':Property_Area},
                            safe=False)


            


def view_results(request):
    # Submit prediction and show all
    data = {"dataset": PredResults.objects.all()}
    return render(request, "results.html", data)
