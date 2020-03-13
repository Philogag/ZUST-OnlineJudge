import requests
import json

def submit():
    values={
        "pid": 1,
        "ptitle": "Local - 1 | Nomal problem",
        "contestid" : -1,
        "user": "root",
        "lang": "c++",
        "code":"""
#include<iostream>
using namespace std;
int main()
{
    int a,b; 
    cin >> a >> b;
    cout << a + b << endl;
}
"""
    }
    response = requests.post(
        "http://localhost:8000/api/submition/new/",
        values
    )
    print(response.text)


submit()
submit()
submit()
submit()
submit()
submit()
submit()
submit()
submit()
submit()