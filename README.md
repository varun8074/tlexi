# **Setup instructions**:
•	Download and install python, preferred 3.10.0

•	Clone this repository as ```HTTPS``` or download the zip file and extract the files

•	Download requirements using command: ```pip install -r requirements.txt```
# **Test the API**:
### •	Localhost:
•	In the terminal run the localhost using command: ```uvicorn main:app --reload```

•	Open the localhost server

•	Example: ```INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)```

•	Then add this extension to the existing url: /docs 

•	Example:```http://127.0.0.1:8000/docs```

•	You will be redirected to swaggerUI where you can test the APIs

•	First execute ```/Q/load_data/``` then execute ```/Q/ask/```

•	You can find the example input value and it can be modified as per requirement

# **Example input/output**:
## Input:
```
{
  "query": "Is an insurance company liable to pay compensation if a transport vehicle involved in an accident was being used without a valid permit?"
}
```

## Output

```
{
  "answer": "How much is the compounding fee?",
  "citations": [
    {
      "text": "and are also liable to pay damages @ Rs.1,000/- per day from the \ndate of its disconnection till final realisation of the amount. \n1 of 15\n::: Downloaded on - 11-10-2017 19:11:13 :::...",
      "source": "Dakshin Haryana Bijli Vs. Sirohi Medical Center (Theft of Eletcricity Punjab).pdf"
    },
    {
      "text": "money' has been interpreted by judgments of this Court to \nPage 20 of 21Law Finder DocId # 2046163 Licensed to: Sh.Gurpreet Singh Mann,Advocate Bath...\n28-08-2023Law Finder...",
      "source": "Dashrath Vs Hitesh 138.pdf"
    },
    {
      "text": "tampered. A case of theft of energy by tampering meter seals was \nfound. Plaintiff was given memo for depositing compounding fee of \n2 of 15\n::: Downloaded on - 11-10-2017 19:11:14 :::...",
      "source": "Dakshin Haryana Bijli Vs. Sirohi Medical Center (Theft of Eletcricity Punjab).pdf"
    }
  ]
}
```
