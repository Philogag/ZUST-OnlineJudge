import requests
import json

def submit():
    values={
        "pid": 3,
        "ptitle": "Local - 2 | Spj test problem",
        "contestid" : -1,
        "user": "root",
        "lang": "c++",
        "code":"""
#include<iostream>
using namespace std;
int main()
{
    int a[int(1e8)];
    int a,b;
    while(1);
}
"""
    }
    response = requests.post(
        "http://localhost:8000/api/submition/new/",
        values
    )
    print(response.text)


submit()