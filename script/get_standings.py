import sys,requests,time,csv,datetime
#コンテスト情報をロードする

def main():
  path=input("出力したjsonファイルのパスを入力してください")
  if path[0]=="\"":
    path=path[1:]
  if path[-1]=="\"":
    path=path[:-1]
  #path=
  f=open(path)
  try:
    S=eval(f.readline())
  except:
    sys.stderr.write("ファイルが壊れているか間違っています。\n")
    f.close()
    exit(1)
  f.close()
  contest_name=S["contest"]
  start_time=S["start_time"]//1000
  end_time=S["end_time"]//1000
  penalty=S["penalty_time"]
  problems=S["problems"]
  teams=S["teams"]

  prob_cnt=len(problems)

  #初期化
  team_score={}
  user_team={}#user:team
  users=[]
  problem_list=[]


  for i in problems:
    problem_list.append(problems[i]["problem_id"])

  for key in teams:
    team_score[key]={}
    for i in problems:
      team_score[key][problems[i]["problem_id"]]=[]
    for j in teams[key]:
      users.append(j)
      user_team[j]=key

  null=None
  for user_name in users:
    time.sleep(2)#APIを叩くのでsleepさせる
    site=requests.get(f"https://kenkoooo.com/atcoder/atcoder-api/results?user={user_name}")
    user_all_data=eval(site.text)
    for i in range(len(user_all_data)):
      if not (start_time<=user_all_data[i]["epoch_second"]<end_time):
        continue
      try:
        team_score[user_team[user_name]][user_all_data[i]["problem_id"]].append([user_all_data[i]["epoch_second"],user_all_data[i]["result"]])
      except:
        pass

  team_pena_dict={}

  for t in teams:
    u=team_score[t]
    team_pena_dict[t]=[];
    for p in range(len(problem_list)):
      team_p=u[problem_list[p]]
      team_p.sort()
      unbreak_flag=True
      ce_cnt=0
      for i in range(len(team_p)):
        if team_p[i][1]=="AC":
          team_pena_dict[t].append([problems[p+1]["score"],i,team_p[i][0]])#スコア,ペナ,時間
          unbreak_flag=False
          break
        if team_p[i][1]=="CE":
          ce_cnt+=1
      if unbreak_flag:
        team_pena_dict[t].append([0,len(team_p)-ce_cnt,-1])

  sum_list=[]
  for i in teams:
    ret=[i]
    sum_sc=0
    time_max=0
    pena=0
    #team_pena_dict[i]チームi
    for j in range(len(team_pena_dict[i])):
      sum_sc+=team_pena_dict[i][j][0]
      time_max=max(time_max,team_pena_dict[i][j][2])
      if team_pena_dict[i][j][2]!=-1:
        pena+=team_pena_dict[i][j][1]
    ret.append([sum_sc,pena,time_max+pena*penalty])
    ret+=team_pena_dict[i]
    sum_list.append(ret)
  
  sorted_sum=sorted(sum_list,key=lambda x:(x[1][0],x[1][2],x[1][1]))

  with open("result.csv",mode="w",newline="")as wf:
    wt=csv.writer(wf)
    header=["Team-Standings","Team","Score"]
    for i in range(prob_cnt):
      header.append(str(i+1))
    wt.writerow(header)
    for i in range(len(sorted_sum)):#チームごと
      u=sorted_sum[i]
      name=",".join(teams[u[0]])
      sc=[i+1,u[0]+f"({name})"]
      for j in range(prob_cnt+1):
        ret=str(u[j+1][0])
        if u[j+1][1]!=0:
          ret+=f" ({u[j+1][1]})"
        if u[j+1][2]!=-1:
          st=datetime.timedelta(seconds=u[j+1][2]-start_time)
          st_hour=st.seconds//3600
          st_minute=(st.seconds-st_hour*3600)//60
          st_sec=st.seconds-st_hour*3600-st_minute*60
          ret+=f" {st_hour+st.days*24}:{st_minute}:{st_sec}"
        sc.append(ret)
      wt.writerow(sc)
  return

main()
