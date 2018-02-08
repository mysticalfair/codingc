from pulp import *
#finds the number of people who like the food and drink choices

def solve:
    prob=LpProblem("party", LpMinimize)
    
    #just saves the prices in hashtable
    fid=open('food.txt', 'r')
    for line in fid:
        food, price=line.split(':', 2)[0], line.split(':', 2)[1]
        prices{food}=price
    fid.close()

    fidd=open('drinks.txt', 'r')

    for line in fidd:
        drink, price=line.split(':', 2)[0], line.split(':', 2)[1]
        prices{drink}=price
    fidd.close()
     
   #starts making variables and appending them into var  
    total=0
    var={}, prices={}, pof={}
    choice=open('people.txt', 'r')
    for i in range(0, len(choice), 3):
        name, drinks, food = choice[i], choice[i+1].split(';'), choice[i+2].split(';')
        drinkvar=[], foodvar=[]
        for drink in drinks:
            name_drink=name+str(drink)
            var[name_drink]= LpVariable(name_drink, 0, 1, cat='Binary')
            total+=prices[drink]*var[name_drink]
            drinkvar.append(var[name_drink])
        prob+= sum(drinkvar)==1 #constraint only one drink

        for food in food:
            name_food=name+str(food)
            var[name_food]= LpVariable (name_food, 0, 1, cat='Binary')
            total+=prices[food]*var[name_food]
            foodvar.append(var[name_food])
        prob+= sum(foodvar)==1 #constraint only one food

    prob += total<=budget
    # objective is arbitrary
    prob += 3
    GLPK().solve(prob)

# Solution
    for v in prob.variables():
        print v.name, "=", v.varValue
        print "objective=", value(prob.objective)
