"""Bot Mesh - Base Game | Abeer Aldosari © 2025"""
from abc import ABC,abstractmethod
from typing import Dict,Any,Optional,Set
from linebot.models import TextSendMessage
from dataclasses import dataclass
from datetime import datetime
import re

@dataclass
class PlayerScore:
    user_id:str;display_name:str;points:int=0;correct:int=0;wrong:int=0

class BaseGame(ABC):
    def __init__(self,line_bot_api,questions_count:int=10):
        self.line_bot_api=line_bot_api;self.questions_count=questions_count
        self.current_question=0;self.current_answer=None;self.game_active=True
        self.scores:Dict[str,PlayerScore]={};self.answered_users:Set[str]=set()
        self.created_at=self.last_activity=datetime.now()
    
    @abstractmethod
    def start_game(self)->TextSendMessage:pass
    
    @abstractmethod
    def get_question(self)->TextSendMessage:pass
    
    @abstractmethod
    def check_answer(self,user_answer:str,user_id:str,display_name:str)->Optional[Dict[str,Any]]:pass
    
    def normalize_text(self,text:str)->str:
        if not text:return""
        t=re.sub(r'[\u0617-\u061A\u064B-\u0652]','',text)
        t=re.sub(r'[إأآا]','ا',t);t=re.sub(r'[ة]','ه',t);t=re.sub(r'[ىئ]','ي',t)
        return' '.join(t.split()).strip()
    
    def add_score(self,user_id:str,display_name:str,points:int)->int:
        if user_id not in self.scores:
            self.scores[user_id]=PlayerScore(user_id=user_id,display_name=display_name)
        self.scores[user_id].points+=points;self.scores[user_id].correct+=1
        self.answered_users.add(user_id);self.last_activity=datetime.now();return points
    
    def get_hint(self)->str:
        if not self.current_answer:return"💡 لا يوجد تلميح"
        a=self.current_answer;h=max(1,len(a)//3)
        return f"💡 {a[:h]}{'_'*(len(a)-h)}"
    
    def reveal_answer(self)->str:return f"📝 الإجابة: {self.current_answer}"
    
    def next_question(self)->Any:
        self.current_question+=1;self.answered_users.clear();self.last_activity=datetime.now()
        return self.end_game()if self.current_question>=self.questions_count else self.get_question()
    
    def end_game(self)->Dict[str,Any]:
        self.game_active=False
        sp=sorted(self.scores.values(),key=lambda x:x.points,reverse=True)
        m="🏁 انتهت اللعبة!\n"+"═"*25+"\n\n"
        if sp:
            m+="🏆 النتائج:\n\n";medals=["🥇","🥈","🥉"]
            for i,p in enumerate(sp[:10]):
                medal=medals[i]if i<3 else f"{i+1}."
                m+=f"{medal} {p.display_name}: {p.points} نقطة\n"
            m+=f"\n🎉 مبروك {sp[0].display_name}!"
        else:m+="لم يشارك أحد"
        return{'game_over':True,'message':m,'response':TextSendMessage(text=m),'points':0,'won':bool(sp)}
    
    def is_expired(self,timeout_min:int=30)->bool:
        return(datetime.now()-self.last_activity).total_seconds()/60>timeout_min
