import requests
import json

base_url = "https://petcqa.testrail.io/index.php?/api/v2/"
headers = {
  'Content-Type': 'application/json',
  'Authorization': '<provide auth key generated in postman>'
}

runids=[]
caseids=[]
comments=[]


def create_testcase(scenario,refs,exp_result,section_id):
    url = base_url + 'add_case/'+ str(section_id)
    req =  {
                "title": scenario,
                "type_id": 6,
                "priority_id": 2,
                "template_id": 2,
                "refs": refs,
                "custom_test_status": 2,
                "custom_autocandidate": 2,
                "custom_steps_separated":[
                    {
                        "content": scenario,
                        "expected": exp_result
                    }
                ]
            }

    request_body = json.dumps(req)   
    response = requests.request("POST", url, headers=headers, data = request_body)
    resp = response.json()
    caseids.append(resp["id"])



def create_run(runname,desc,project_id,suite_id,milestone_id):
    url = base_url+ 'add_run/'+ str(project_id)
    req =   {
                "suite_id": suite_id,
                "name": runname,
                "description": desc,
                "milestone_id": milestone_id,
                "include_all": False,
                "case_ids": caseids
            }

    request_body = json.dumps(req)
    response = requests.request("POST", url, headers=headers, data = request_body)
    resp = response.json()
    runids.append(resp['id'])


def update_run(t,comments,status):
    url = base_url + 'add_results_for_cases/' +str(runids[0])
    req =  {
                "results": [
                    {
                        "case_id": caseids[t],
                        "status_id": status,
                        "comment": comments[t]
                    }
                ]
            }
    request_body = json.dumps(req)
    requests.request("POST", url, headers=headers, data = request_body)
    
def send_report(reportid):
    url = base_url + 'run_report/' +str(reportid)
    payload = {}
    requests.request("GET", url, headers=headers, data = payload)


