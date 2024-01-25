from engine.models import TopThreeTip, ResultRace

def evaluate_tip(race):
    
    tips = TopThreeTip.objects.filter(race=race).all()
    result = ResultRace.objects.filter(race=race).all()
    
    for tip in tips:
        top_three = result.first(3)
        f = tip.first_place == top_three[1]
        s = tip.second_place == top_three[2]
        t = tip.third_place == top_three[3]
        points = sum([f, s, t] * 3)
        tip.points = points
        tip.evaluated = True


        

