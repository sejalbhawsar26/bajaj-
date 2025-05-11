#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests

# Your details
payload = {
    "name": "John Doe",
    "regNo": "REG12347",  # Make sure last digit determines correct question
    "email": "john@example.com"
}

# Step 1: Generate webhook and token
response = requests.post(
    "https://bfhldevapigw.healthrx.co.in/hiring/generateWebhook/PYTHON",
    json=payload
)

if response.status_code != 200:
    print("Failed to generate webhook:", response.text)
    exit()

data = response.json()
webhook_url = data["webhook"]
access_token = data["accessToken"]

print("Webhook URL:", webhook_url)
print("Access Token:", access_token)


final_sql_query = """
SELECT
    p.AMOUNT AS SALARY,
    CONCAT(e.FIRST_NAME, ' ', e.LAST_NAME) AS NAME,
    FLOOR(DATEDIFF('2025-05-01', e.DOB) / 365.25) AS AGE,
    d.DEPARTMENT_NAME
FROM PAYMENTS p
JOIN EMPLOYEE e ON p.EMP_ID = e.EMP_ID
JOIN DEPARTMENT d ON e.DEPARTMENT = d.DEPARTMENT_ID
WHERE DAY(p.PAYMENT_TIME) != 1
ORDER BY p.AMOUNT DESC
LIMIT 1;
"""

# Step 3: Submit the SQL query to webhook
headers = {
    "Authorization": access_token,
    "Content-Type": "application/json"
}

submission_payload = {
    "finalQuery": final_sql_query.strip()
}

submit_response = requests.post(webhook_url, json=submission_payload, headers=headers)

# Result
if submit_response.status_code == 200:
    print("Query submitted successfully!")
    print("Response:", submit_response.text)
else:
    print(" Submission failed!")
    print("Status Code:", submit_response.status_code)
    print("Response:", submit_response.text)


# In[ ]:




