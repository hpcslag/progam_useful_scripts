import requests
import json
import datetime
import iso8601
import pytz
import time

slido_account = ""  # 請填上 sli.do account id
slido_authorization = "" # 請填上 sli.do Bearer Token Code (不用複製 `Bearer`，僅複製他後面的那串 token)
create_period = 3.5 #sec

sessions = json.load(open("./schedule.json", ))  # 須從 pretalx 上下載好 schedule.json

def parse_date(date_str, spec_hour=9):
  _date_obj = iso8601.parse_date(date_str)
  #_date_utc=_date_obj.astimezone(pytz.utc)
  #_date_utc_zformat=_date_utc.strftime('%Y-%m-%d %H:%M:%S')
  _date_obj = _date_obj.replace(hour=spec_hour, minute=0, second=0)
  _date_obj_format = _date_obj.strftime('%Y-%m-%d %H:%M:%S')
  return _date_obj_format

def create_slido_room_by_session_name(
    session_name = "COSCUP2021 TR403-1 S1", 
    event_join_code = "coscup21-TR403-1-S1",
    date_from = "2021-06-30 00:00:00",
    date_to = "2021-07-03 00:00:00"
  ):
  global slido_account
  url = "https://admin.sli.do/api/v0.5/events?account=%s" % slido_account

  payload = json.dumps({
    "code": event_join_code,
    "date_from": date_from,
    "date_to": date_to,
    "is_complete": True,
    "is_public": True,
    "location": "Taipei City, Taiwan",
    "name": session_name,
    "timezone": "Asia/Taipei",
    "collaboratorsEmails": []
  })
  headers = {
    'accept': 'application/json, text/plain, */*',
    'authorization': 'Bearer %s' % slido_authorization,
    'content-type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload)

  #print(response.text)
  slido_response = json.loads(response.text)
  return slido_response["url"]["app"]

if __name__ == '__main__':
  export_file = open("pretalx_session_slido.json", "w")
  export_data = []


  conference = sessions["schedule"]["conference"]
  conference_name = conference["title"]
  conference_acronym = conference['acronym']
  for day in conference["days"]:
    day_start = parse_date(day["day_start"], spec_hour=9)
    day_end = parse_date(day["day_end"], spec_hour=17)
    for room_name in day["rooms"].keys():
      print("-------- " + room_name + " ----------")
      for idx, room in enumerate(day["rooms"][room_name]):
        session_id = room["id"]
        session_title = room["title"]
        session_code = conference_acronym+"-"+str(session_id)
        print(str(idx+1) + ". " + session_title + "; session_code: "+ session_code + "; "+ day_start + " ~ " + day_end)
        slido_url = create_slido_room_by_session_name(
          session_name = session_title, 
          event_join_code = session_code,
          date_from = day_start,
          date_to = day_end
        )
        time.sleep(create_period)
        
        export_data.append({
          "session_id": session_id,
          "session_title": session_title,
          "slido_session_code": session_code,
          "slido_url": slido_url
        })

  json_dump = json.dumps(export_data)
  export_file.write(json_dump)
  export_file.close()

