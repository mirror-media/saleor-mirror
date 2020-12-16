import requests

api_ep = "http://104.155.209.114/graphql/"
query_string = """query user {
  user(id:1) {
    
    lastLogin
  }
}
"""
jwt = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MDc5MzUxMDYsImV4cCI6MTYxMDUyNzEwNiwidG9rZW4iOiJTNFd0aHc1VjJ5Qm4iLCJlbWFpbCI6ImFuZHlodWFuZ0BtaXJyb3JtZWRpYS5tZyIsInR5cGUiOiJyZWZyZXNoIiwidXNlcl9pZCI6IlZYTmxjam94IiwiaXNfc3RhZmYiOnRydWUsImNzcmZUb2tlbiI6IjJwcFFWZktnQzZNNVJNUmtIQXlBdTM1bWlMQkhyNHhyZ3FTRlJFWG9oaFVlcEFnejlvN0NmYXRyNkVSTk51MHcifQ.I_6cq19ftPGTU68aNToIhqhwcn_B-9kvWwzSNWb_bh8"
headers = {"AUTHORIZATION": f"JWT {jwt}", "Content-Type": "application/json"}
r = requests.post(api_ep, json={'query':query_string}, headers=headers)
# r = requests.post(gql, json=query_string) # error
print(r.json())
res = r.json()
# print(res['data']['Post'].keys())
# content = json.loads(res['data']['Post']['content']) # If the content column is text
# content = res['data']['Post']['content']
print('='*70)
# print(content['html'], type(content['html']))
