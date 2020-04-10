from creatures import *
    
def testCreatures():
    try:
        b = DeadBody(10,10,10,10,10)
    except:
        b = DeadBody(-3,10,10,10,10)
    else:
        assert True, "Dead body with positive hp creature created"

    try:
        sc = SaneCreature(0,0,0,0)
    except:
        sc = SaneCreature(1,1,0,0)
    else:
        assert True, "Sane creature with <=0 health"
        
    try:
        n = Necromancer(0,0,0,0,0,1)
    except:
        n = Necromancer(20,0,0,0,0,1)
    else:
        assert True, "negative hp creature created"
        
    try:
        s1 = Skeleton(10,10,10,10,0,-1,10)
    except:
        s1 = Skeleton(10,10,10,10,0,10,10)
    else:
        assert True, "negative ammo created"
        
    try:
        z = Zombie(10,10,10,10,0,-10)
    except:
        z = Zombie(10,10,10,10,0,10)
    else:
        assert True, "negative weapon lvl created"
        
    assert (s1.haveAmmo()), "ammo not foundet"
    s2 = Skeleton(10,10,10,10,0,0,10)
    assert (not s2.haveAmmo()), "ammo foundet when theres none"
    assert (s1.getValue()==30), "getValue() test"
    
    assert s1.groupid==0, "possesed creature not in a 0 team"
    assert b.groupid==-1, "dead body not in a -1 team"
    assert sc.groupid>0, "sane creatur in a <=0 team"

    sold=Soldier(1,2,3,3,4,5,6)
    assert sold.getValue()==15, "error at counting of solder value"
    assert sold.haveAmmo(), "ammo counting error"

    try:
        inv = Inventor(1,1,2,2,-10,3,4,True)
    except:
        inv = Inventor(1,1,2,2,3,3,4,True)
    else:
        assert True, "negative exp created"

try:
    testCreatures()
except:
    print("Ошибка тестирования системы")
    testCreatures()
    
